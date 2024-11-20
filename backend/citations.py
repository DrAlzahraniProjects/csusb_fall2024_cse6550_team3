import os

def get_citations(docs):
    """
    Extract page numbers and content from the response context.
    Args:
      docs (list): List of document objects, each with metadata.
    Returns:
      list: A list of dictionaries containing page numbers and text to highlight.
    """
    # Extract relevant information
    citations = [
        {
            'page': doc.metadata.get('page', 'Unknown page') + 1,
            'text': doc.page_content[:300]  # Add the first 300 characters of content
        }
        for doc in docs
        if isinstance(doc.metadata.get('page'), int)
    ][:2]
    return citations if citations else []

def format_citations(citations, response):
    """
    Format a list of page numbers and text to highlight as HTML links.
    Args:
      citations (list): A list of dictionaries with page numbers and text.
      response (str): The chatbot's response to the user's question.
    Returns:
      str: A formatted string of HTML links if relevant, otherwise an empty string.
    """
    pdf_path = f"{os.getenv('CORPUS_SOURCE')}/textbook.pdf"
    links = [
        f'<a href="/team3/?view=pdf&file={pdf_path}&page={citation["page"]}&highlight={citation["text"]}" target="_blank">[{index + 1}]</a>'
        for index, citation in enumerate(citations)
    ]
    return "\n\nSources: " + "".join(links)

