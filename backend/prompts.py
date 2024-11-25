from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a chatbot that answers the question in the <question> tags.
- Answer based only on provided context in <context> tags only if relevant.
- Always identify yourself as a chatbot, not the textbook.
- Keep your answer short and to the point.
"""

REWRITE_PROMPT = """
- If the text is unrelated to software engineering only return "NONE"
- If the text is related to the software engineering rewrite the text
- Keep the rewritten text concise
"""

def get_prompt():
    """
    Get the appropriate prompt template based on context availability.
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "<question>{input}</question>\n\n<context>{context}<context>"),
    ])

def rewrite_prompt():
    """Return a ChatPromptTemplate for prompt rewriting."""
    return ChatPromptTemplate.from_messages([
        ("system", REWRITE_PROMPT),
        ("human", "{text}"),
    ])