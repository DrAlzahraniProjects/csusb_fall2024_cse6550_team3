# citations.py
import os

def get_citations(docs):
    """
    Extract page numbers from the response context.
    Args:
        docs (list): The list of document objects that may contain relevant answers.
    Returns:
        list: A list of page numbers from the context documents.
    """
    # Assuming each doc is an object or dictionary that includes metadata about the page number
    return [doc['metadata']['page'] for doc in docs if 'page' in doc['metadata']]

def format_citations(page_numbers):
    """
    Format a list of page numbers as HTML links.
    Args:
        page_numbers (list): A list of page numbers.
    Returns:
        str: A formatted string of HTML links.
    """
    pdf_path = os.getenv('CORPUS_SOURCE') + '/textbook.pdf'  # Ensure this path is correct
    links = [f'<a href="/team3/?view=pdf&file={pdf_path}&page={page}" target="_blank">[Source {index + 1}]</a>' for index, page in enumerate(page_numbers)]
    return "\n\nSources: " + " ".join(links)
