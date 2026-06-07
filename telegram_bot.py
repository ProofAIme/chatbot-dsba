import os
import re
import chromadb

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key
)

with open("About-program.txt", "r", encoding="utf-8") as f:
    text = f.read()

teacher_start = text.find("Учительский состав")
teacher_end = text.find("Скидки на обучение для поступивших")
teacher_text = text[teacher_start:teacher_end]

contact_start = text.find("Если есть вопросы по поступлению")
contact_end = text.find("Часто задаваемые вопросы")
contact_text = text[contact_start:contact_end]

def split_into_chunks(text, chunk_size=80, overlap=10):
    sections = re.split(r"-{5,}", text)
    chunks = []

    for section in sections:
        section = section.strip()
        words = section.split()
        step = chunk_size - overlap

        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])

            if len(chunk) > 50:
                chunks.append(chunk)

    return chunks

chunks = split_into_chunks(text)

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

client = chromadb.Client()

try:
    client.delete_collection(name="telegram_bot_collection")
except:
    pass

collection = client.create_collection(name="telegram_bot_collection")

embeddings = model.encode(chunks).tolist()

ids = []

for i in range(len(chunks)):
    ids.append("chunk_" + str(i))

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids
)

async def start(update, context):
    await update.message.reply_text(
        "Привет! Я бот для вопросов про DSBA / ПАД. "
        "Можешь спросить про поступление, стоимость, скидки, учебный план или карьеру.\n\n"
        "Полезные ссылки:\n"
        "Сайт программы: https://www.hse.ru/ba/pad/\n"
        "Поступление в бакалавриат: https://ba.hse.ru/\n"
        "Приёмная комиссия: https://ba.hse.ru/admission/"
    )

async def answer_question(update, context):
    question = update.message.text
    question_lower = question.lower()

    people_question = False

    if "преподав" in question_lower or "учител" in question_lower or "состав" in question_lower:
        people_question = True

    if "глав" in question_lower or "руковод" in question_lower or "фио" in question_lower:
        people_question = True

    if "офис" in question_lower or "менедж" in question_lower:
        people_question = True

    if people_question:
        context_text = teacher_text + "\n\n" + contact_text

    else:
        search_question = question
        number_of_results = 5

        if "стоим" in question_lower or "цен" in question_lower or "стоит" in question_lower:
            search_question = search_question + " стоимость обучение цена 1 млн рублей в год"

        if "балл" in question_lower or "егэ" in question_lower or "поступ" in question_lower:
            search_question = search_question + " ЕГЭ минимальные баллы математика русский информатика физика поступление"

        if "бюджет" in question_lower or "мест" in question_lower:
            search_question = search_question + " бюджетные места платные места количество мест"
            number_of_results = 7

        if "скид" in question_lower:
            search_question = search_question + " скидки на обучение олимпиады достижения баллы ЕГЭ"

        if "партнер" in question_lower or "партнёр" in question_lower or "сотруднич" in question_lower:
            search_question = search_question + " партнеры партнёры сотрудничество Сбер Т-Банк Московская биржа Яндекс 1С"
            number_of_results = 7

        question_embedding = model.encode(search_question).tolist()

        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=number_of_results
        )

        docs = results["documents"][0]

        context_text = ""

        for doc in docs:
            context_text = context_text + doc + "\n\n"

    prompt = (
        "Ты отвечаешь на вопросы абитуриентов про программу DSBA / ПАД. "
        "Используй только контекст ниже. "
        "Вопрос может быть коротким, разговорным или с ошибками. "
        "Если в контексте есть похожая информация, ответь по ней. "
        "Если спрашивают про преподавателей, учитывай, что в учебном плане указаны преподаватели по дисциплинам, а не должности. "
        "Если спрашивают должности, не придумывай их. "
        "Если спрашивают руководителя или главу программы, отвечай только если это прямо указано в контексте. "
        "Если информации нет, напиши, что информации недостаточно. "
        "Отвечай кратко и понятно на русском языке.\n\n"
        "Контекст:\n"
        + context_text
        + "\nВопрос:\n"
        + question
    )

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

    except:
        answer = "Не получилось получить ответ от LLM."

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(telegram_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question))

print("Bot is running...")
app.run_polling()