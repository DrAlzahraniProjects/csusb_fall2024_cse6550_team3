from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a chatbot that answers the question in the <question> tags.
- Answer based only on provided context in <context> tags only if relevant.
- Always identify yourself as a chatbot, not the textbook.
"""

def get_prompt():
    """
    Get the appropriate prompt template based on context availability.

    Returns:
        ChatPromptTemplate: Configured prompt template
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "<question>{input}</question>\n\n<context>{context}<context>"),
    ])