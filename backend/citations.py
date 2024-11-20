import os

def get_citations(docs):
    """
    Extract page numbers from the response context.
    Args:
      docs (list): List of document objects, each with metadata.
    Returns:
      list: A list of page numbers from the context documents.
    """
    # Extract max of 2 page numbers from the context metadata in response
    page_numbers = [
        doc.metadata.get('page', 'Unknown page') + 1 for doc in docs
        if isinstance(doc.metadata.get('page'), int)
    ][:1]
    return page_numbers if page_numbers else []

def format_citations(page_numbers, response):
    """
    Format a list of page numbers as HTML links, displaying index numbers but linking to actual pages.
    Args:
      page_numbers (list): A list of page numbers.
      response (str): The chatbot's response to the user's question.
    Returns:
      str: A formatted string of HTML links if relevant, otherwise an empty string.
    """
    pdf_path = f"{os.getenv('CORPUS_SOURCE')}/textbook.pdf"
    links = [
        f'<a href="/team3/?view=pdf&file={pdf_path}&page={page}" target="_blank">[{index + 1}]</a>'
        for index, page in enumerate(page_numbers)
    ]
    return "\n\nSources: " + "".join(links)
