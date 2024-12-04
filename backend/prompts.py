import re
from .abb import abbreviations
from langchain_core.prompts import ChatPromptTemplate

REWRITE_PROMPT = """Rewrite this text to be more descriptive. Be focused."""

def rewrite_prompt():
    """Return a ChatPromptTemplate for prompt rewriting."""
    return ChatPromptTemplate.from_messages([
        ("system", REWRITE_PROMPT),
        ("human", "{text}"),
    ])

def sanitize_question(question: str) -> str:
    """
    # Purpose: Clean user input by removing non-alphabetic characters
    # Input: Raw question string
    # Output: Sanitized question string
    # Processing: Filters out all characters except letters and spaces
    """
    return ''.join(char for char in question if char.isalpha() or char.isspace())

def remove_spaces(question: str) -> str:
    """
    # Purpose: Remove all spaces from input text
    # Input: Question string
    # Output: String without spaces
    # Processing: Removes all whitespace characters from the input
    """
    return question.replace(" ", "")

def validate_question(question: str) -> bool:
    """
    # Purpose: Verify if a question is valid for processing
    # Input: Question string
    # Output: Boolean indicating validity
    # Processing: Checks if sanitized question contains non-empty content
    """
    return len(remove_spaces(sanitize_question(question))) > 0

def replace_text(question: str) -> str:
    """
    # Purpose: Replace abbreviations with their full forms
    # Input: Question string containing potential abbreviations
    # Output: Question string with expanded abbreviations
    # Processing: Identifies and replaces known abbreviations with full forms
    """
    words = question.split()
    result = []
    for word in words:
        replaced_word = word
        for abbrev, full_form in abbreviations.items():
            if abbrev in word:
                replaced_word = word.replace(abbrev, full_form)
        result.append(replaced_word)
    return ' '.join(result)