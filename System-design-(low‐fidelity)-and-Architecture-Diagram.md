## Table of Contents

### 1. [Low-fidelity diagram](#Low-fidelity-diagram)
### 2. [Architecture diagram](#Architecture-diagram)

## Low fidelity diagram:

[Figma Link](https://www.figma.com/design/SDFYx5iBWYe1grbq6ZMfBZ/Textbook-Chatbot---Team3?node-id=0-1&t=33tVXRm7VDwR5YyQ-1)

![image](https://github.com/user-attachments/assets/3edf5359-99b6-4550-9800-6fe35c52d25c)


## Architecture diagram:

![Screenshot (164)](https://github.com/user-attachments/assets/5274a3b5-3a25-49ca-bb5a-5e94de36dc83)

**Description of architecture diagram:**

This diagram illustrates the architecture of a chatbot system designed to leverage the Software Engineering Body of Knowledge (SWEBOK) as a knowledge base. The system is divided into two main components: the Frontend (Streamlit interface) and the Backend (core logic and AI processing).

**User Interaction (Frontend):**

- The user inputs a query through the Streamlit-based User Interface.
- The prompt is sent to the backend for processing.

**Backend Components:**

- Orchestrator (LangChain): Enhances the prompt, retrieving relevant information from the SWEBOK corpus and enhancing the context using the FAISS vector database and the LLM (Mistral 7B). LangChain manages the integration and communication between these components to improve accuracy and context.

- FAISS Vector Database: Stores embeddings of the SWEBOK content and retrieves relevant chunks of knowledge to generate precise, context-aware responses.

- LLM (Mistral 7B): Generates the response based on the user prompt and the enriched context from the SWEBOK database.

- Safeguard (NeMo Guardrails): Ensures that the generated response adheres to safety, relevance, and appropriateness guidelines, adding a layer of filtering before sending the response back to the user.

