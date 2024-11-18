from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT_WITH_CONTEXT = """
You are a chatbot that answers the question in the <question> tags.
- Answer based only on provided context in <context> tags only if relevant.
- Always identify yourself as a chatbot, not the textbook.
"""

SYSTEM_PROMPT_NO_CONTEXT = """
- To questions about your purpose, say: "I'm a chatbot designed to answer questions about the provided textbook."
- DO NOT answer the question.
- Inform the user that you cannot answer their question as no relevant information was found
- Suggest they rephrase or try a different question
"""

def get_prompt(has_context=True):
    """
    Get the appropriate prompt template based on context availability.
    Args:
        has_context (bool): Whether relevant context exists
    Returns:
        ChatPromptTemplate: Configured prompt template
    """
    system_prompt = SYSTEM_PROMPT_WITH_CONTEXT if has_context else SYSTEM_PROMPT_NO_CONTEXT
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "<question>{input}</question>\n\n<context>{context}<context>"),
    ])