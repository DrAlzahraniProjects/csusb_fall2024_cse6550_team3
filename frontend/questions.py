BASELINE_QUESTIONS = {
    # 10 Answerable questions
    "Who is Hironori Washizaki?": True,
    "How does software testing impact the overall software development lifecycle?": True,
    "What is the agile methodology?": True,
    "What are the different types of software models, and when should each be used?": True,
    "How does software configuration management ensure project success?": True,
    "What role do user requirements play in software design and architecture?": True,
    "What is software dependability?": True,
    "How does project management in software engineering differ from traditional project management?": True,
    "What is chapter 11 about?": True,
    "What is the purpose of static analysis in software testing?": True,

    # 10 Unanswerable Questions
    "What class does Dr. Alzahrani teach?": False,
    "How will AI evolve in the next 100 years?": False,
    "What GPA do you have?": False,
    "What is the smallest possible Turing machine?": False,
    "What is the most efficient way to handle an infinite stream of data?": False,
    "Is there a way to build a fully self-sustaining human colony on Mars?": False,
    "What is chapter 200 about?": False,
    "How could we fully eliminate all types of noise in wireless communications?": False,
    "How can we create a material that is completely indestructible?": False,
    "Microsoft stock price?": False
}

def normalize_text(text: str) -> str:
    """Normalize text by converting to lowercase and stripping whitespace."""
    return text.strip().lower()

def check_baseline_answerable(prompt: str) -> bool | None:
    """
    Check if prompt is a baseline question and return its answerable status.
    Returns None if prompt is not a baseline question.
    """
    normalized_prompt = normalize_text(prompt)
    normalized_baseline = {normalize_text(q): a for q, a in BASELINE_QUESTIONS.items()}
    return normalized_baseline.get(normalized_prompt)