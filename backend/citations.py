import os

def get_citations(docs):
  """
  Extract page numbers from the response context.
  Args:
    response (dict): The response dictionary containing 'context' with metadata about each source.
  Returns:
    list: A list of page numbers from the context documents.
  """
  # Extract page numbers from the context metadata in response
  page_numbers = [
    doc.metadata.get('page', 'Unknown page') + 1 for doc in docs
    if isinstance(doc.metadata.get('page'), int)
  ]
  return page_numbers

def format_citations(page_numbers):
    """
    Format a list of page numbers as HTML links, displaying index numbers but linking to actual pages.
    Args:
      page_numbers (list): A list of page numbers.
    Returns:
      str: A formatted string of HTML links, displaying citation indexes while linking to actual PDF pages.
    """
    pdf_path = f"{os.getenv('CORPUS_SOURCE')}/textbook.pdf"
    links = [
      f'<a href="/team3/?view=pdf&file={pdf_path}&page={page}" target="_blank">  Source {index + 1}</a>'
      for index, page in enumerate(page_numbers)
    ]
    return "\n\nSources: " + "  ".join(links)
