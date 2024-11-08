# citations.py
import os

def get_citations(docs):
    """
    Extract page numbers from the document objects which contain metadata about each source.
    """
    return [doc.metadata.get('page', 'Unknown page') for doc in docs if 'page' in doc.metadata]

def format_citations(page_numbers):
    """
    Format a list of page numbers as HTML links to display in the chatbot response.
    """
    pdf_path = os.getenv('CORPUS_SOURCE') + '/textbook.pdf'  # Ensure this path is correct
    links = [f'<a href="/team3/?view=pdf&file={pdf_path}&page={page}" target="_blank">[Source {index + 1}]</a>' for index, page in enumerate(page_numbers)]
    return "Sources: " + ", ".join(links)
