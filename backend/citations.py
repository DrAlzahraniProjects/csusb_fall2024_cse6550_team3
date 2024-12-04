import os

def get_citations(docs):
    """
    # Purpose: Extract page numbers from document metadata
    # Input: List of document objects with metadata
    # Output: List of dictionaries containing page numbers without text content
    # Processing: Filters documents with valid page numbers and creates citation entries
    """
    citations = [
        {'page': doc.metadata.get('page', 'Unknown page') + 1, 'text': ''}  # No text
        for doc in docs
        if isinstance(doc.metadata.get('page'), int)
    ][:1]
    return citations if citations else []

def format_citations(citations):
    """
    # Purpose: Format citations as HTML links
    # Input: List of citation dictionaries containing page numbers
    # Output: HTML string with formatted citation links
    # Processing: Generates clickable PDF links for each citation
    """
    pdf_path = f"{os.getenv('CORPUS_SOURCE')}/textbook.pdf"
    links = [
        f'<a href="/team3/?view=pdf&file={pdf_path}&page={citation["page"]}" target="_blank">[{index + 1}]</a>'
        for index, citation in enumerate(citations)
    ]
    return "\n\nSource: " + "".join(links)

def handle_citations(relevant_docs):
    """
    # Purpose: Process and format citations from relevant documents
    # Input: List of relevant document objects
    # Output: Formatted citation string or None if no citations exist
    # Processing: Extracts citations and formats them as HTML links
    """
    page_numbers = get_citations(relevant_docs)
    if page_numbers:
        citations = format_citations(page_numbers)
        return citations
    return None
    