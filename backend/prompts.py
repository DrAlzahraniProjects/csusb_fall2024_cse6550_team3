import re
from .abb import abbreviations
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a chatbot that answers the question inside the <question_start><question_end> tags.
Use the context provided to answer the question.
If the context is not relavent answer the question if it's related to software engineering.
The context is present within the <context_start> and <context_end> tags.
"""
REWRITE_PROMPT = """Rewrite this text to be more descriptive. Be focused."""

def get_prompt():
    """Get the appropriate prompt template based on context availability. """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "<question_start>{input}<question_end>\n\n<context_start>{context}<context_end>"),
    ])

def rewrite_prompt():
    """Return a ChatPromptTemplate for prompt rewriting."""
    return ChatPromptTemplate.from_messages([
        ("system", REWRITE_PROMPT),
        ("human", "<start_of_text>{text}<end_of_text>"),
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
    pattern = r'(?:what\s+is\s+)?[A-Z]{2,4}\s\d{3,4}'
    if re.match(pattern, question):
        return False
    # Remove incomplete questions
    ignore_list = [
        "what", "whatis", "what's", "explain",
        "how", "howdoes", "howis", "when", "whenis", "why", "whyis", "who", "whois"
    ]
    cleaned_question = remove_spaces(question.lower().strip())
    sanitized_question = remove_spaces(sanitize_question(question)).lower()
    if cleaned_question in ignore_list or sanitized_question in ignore_list:
        return False
    return len(sanitized_question) > 0 and len(sanitized_question) <= 200
    
def replace_text(question: str) -> str:
    """
    # Purpose: Replace abbreviations with their full forms
    # Input: Question string containing potential abbreviations
    # Output: Question string with expanded abbreviations
    # Processing: Identifies and replaces known abbreviations with full forms
    """
    if not question.lower().startswith(("how", "when", "why", "who")):
        if question.lower().startswith("what is"):
            question = question.replace(question[:7], "Explain")
        elif question.lower().startswith("what's"):
            question = question.replace(question[:6], "Explain")
        elif question.lower().startswith("explain"):
            question = question.replace(question[:7], "What is")
        else:
            question = "What is " + question

    words = question.split()
    result = []
    for word in words:
        replaced_word = word
        for abbrev, full_form in abbreviations.items():
            if abbrev in word:
                replaced_word = word.replace(abbrev, full_form)
        result.append(replaced_word)
    return ' '.join(result)