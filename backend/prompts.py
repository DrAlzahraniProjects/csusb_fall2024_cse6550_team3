import re
from .abb import abbreviations
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a chatbot that answers the question in the <question> tags.
- Answer based only on provided context in <context> tags only if relevant.
- Always identify yourself as a chatbot, not the textbook.
- Keep your answer short and to the point.
"""

REWRITE_PROMPT = """
- Rewrite the text to be more descriptive
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

def sanitize_question(question: str) -> str:
    return ''.join(char for char in question if char.isalpha() or char.isspace())

def remove_spaces(question: str) -> str:
    return question.replace(" ", "")

def validate_question(question: str) -> bool:
    return len(remove_spaces(sanitize_question(question))) > 0

def replace_text(question: str) -> str:
    """Replace abbreviations in the question with their full forms"""
    words = question.split()
    result = []
    for word in words:
        replaced_word = word
        for abbrev, full_form in abbreviations.items():
            if abbrev in word:
                replaced_word = word.replace(abbrev, full_form)
        result.append(replaced_word)
    return ' '.join(result)