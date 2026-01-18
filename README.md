# chatbot-dsba
1. Project Context
1.1 Business Problem

Applicants to the DSBA program regularly ask repetitive questions related to admission requirements, deadlines, required documents, and program details.
A common issue among applicants to our DSBA program is the multiple questions they ask concerning the details of the program, the deadline, maybe the documents needed to apply, and the some difficult steps to gain admission to the program.

While official details exist on public websites, sometimes the information is not relevant to the questions asked and tends to exist on more than one webpage or document, this creating a hassle to find answers to each question.

Using a chatbot with a Retrieval-Augmented Generation (also called RAG) system would streamline the process by answering questions, possibly increasing the accessibility of official documents, and maybe decreasing the strain on the admissions committee.

1.2 Target Audience and Users

They will mostly be used: bachelor’s and master’s applicants to the DSBA program. Also they parents.

Interaction channel: text-based chatbot deployed in Telegram.

Expected load: moderate user activity with most users active(maybe) during the deadline of the admission .

1.3 Constraints and Assumptions

The chatbot won't be able to anticipate outcomes, such as chances of admission, or the score of a random student.

Also the chatbot is not official, and it does not make any promises. It is not a substitute for the admissions committee.

The chatbot operates solely within the DSBA domain and relies exclusively on official documents for its responses.

2. Solution Architecture
2.1 High-Level Overview

User → Telegram chat → Chatbot → RAG module → Vector knowledge base → LLM → Response to user.

Main components: user interface, retrieval module, generative model, and knowledge base.

2.2 Knowledge Base and Document Management

Sources of knowledge: official DSBA admission pages, admission rules, FAQs, and stats.

For all knowledge sources: PDF and HTML documents parsing, text cleaning and semantic chunking.

Information is updated manually or semi-automatically based on the official changed information.

2.3 Retrieval + Generation

For retrieval - vector-based semantic search (FAISS and embedding models).

For generation: LLM that answers based on the fragments of documents that were retrieved.

Answer control: tight grounding to the retrieved context and fallback answers if the relevant information is not present.

2.4 Integrations and Interfaces

Integration of Telegram Bot.

Handling of requests through REST.

Quality control through the logging of users’ requests and the system’s responses.

2.5 Infrastructure and Deployment

Using Docker for Containerization.

Development and production environments.

Computing requirements involve CPU-based inference.

Basic security measures in place, without the processing of sensitive personal data.

3. Data and Knowledge Quality
3.1 Data Collection and Preprocessing

Two format - PDF and HTML documents.

Text preprocessing - cleaning, normalization, and chunking.

Metadata: source, document type, and publication date.

3.2 Vectorization and Indexing

Embedding model: general purpose multilingual embedding model.

Similarity metric: cosine similarity.

Indexing: new document additions.

3.3 Knowledge Quality Metrics

Coverage of applicant questions.

Timeliness of updates regarding official changes.

Consistency: no duplicated or contradictory information.
4. Model and Generation
4.1 LLM Selection and Prompting

A general purpose LLM is used no fine-tuning is applied.

A system prompt is used to keep responses confined to the knowledge base and the DSBA admissions domain.

Responses should be brief and in a formal, neutral tone.

4.2 Answer Quality Control

Metrics of evaluation include the correctness, completeness, and usefulness of the responses.

Sufficient information is needed to answer a question, and if there is not enough information, the system will not answer.

If the answer is not in the base of knowledges , the system will direct the user to the official DSBA documents for information.

4.3 Training / Fine-Tuning

No plans have been made for fine-tuning.

The updates to the knowledge base and modifications to the prompt will enhance the quality of the responses.

5. UX / User Experience
5.1 Interaction Scenarios

Greeting the user and stating the purpose of the chatbot.

Providing answers related to the admissions question .

Informing the user if there is no information available regarding to the topic.

5.2 Dialogue Logic

It can handle short chats and a few back-and-forths.

It remembers what you said earlier in the same chat.

It talks in a formal and polite way.

5.3 UX Metrics

Response time.

Percentage of successfully answered questions.

Optional user feedback collection.

6. Security, Compliance, and Ethics

Users are informed that they are talking with an automated system.

There is no collection or processing of users personal data .

It blocks questions that are inappropriate

7. Deployment and Maintenance Plan
7.1 Project Stages

Problem analysis and data collection.

Develop a minimum viable chatbot

Test it and make it better over time.

7.2 Maintenance and Operations

Watching for errors and logging.

Regular updates of the knowledges base.

Analys of users requests to identify gaps.

8. Risks and Assumptions

Insufficient coverage of the knowledge base.

Admission rules or dates could change.

Risk mitigation through updates and fallback mechanisms.

9. Budget and Resources

Human resources: one or a few ML/NLP engineer.

Technical resources: host server. Also LLM access.

Cost: minimal.

ROI: less work for the admissions team and faster info for students.

10. Appendices

Glossary of terms such as RAG, LLM, embeddings.

Links to official DSBA admission resources.
