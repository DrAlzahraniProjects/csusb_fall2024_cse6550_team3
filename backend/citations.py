import os
from roman import toRoman

# Custom citations for Software Engineering: A PRACTITIONER’S APPROACH
def default_textbook(page, pdf_path):
  # The documents are zero indexed. So page 1 of the pdf is page 0 in docs
  # Chapter 1 starts at doc 33 (page 34 of the PDF)
  adjusted_page = page - 33 
  if adjusted_page >= 0: # For pages starting from Chapter 1
    link = f'<a href="/team3/?view=pdf&file={pdf_path}&page={page + 1}" target="_blank">[{adjusted_page + 1}]</a>'
  else: # For pages before Chapter 1
    adjusted_page = "Cover" if page == 0 else toRoman(page)
    link = f'<a href="/team3/?view=pdf&file={pdf_path}&page={page + 1}" target="_blank">[{adjusted_page}]</a>'
  return link


def get_answer_with_source(response):
  """
  Extract the answer and relevant source information from the response.
  This function processes the response from the RAG chain, extracting the answer
  and up to 5 source references (page numbers) from the context documents.

  Args:
    response (dict): The response dictionary from the RAG chain, containing 'answer' and 'context' keys.
  Returns:
    str: A formatted string containing the answer followed by source information.
  """
  pdf_path = f"{os.getenv('CORPUS_SOURCE')}/textbook.pdf"
  answer = response.get('answer', 'No answer found.') # Extract the answer
  sources = [] # Handle multiple contexts in the response (assuming response['context'] is a list)

  # Iterate over context documents and get top 5 sources
  for doc in response['context'][:5]:
    page = doc.metadata.get('page', 'Unknown page')
    # PDF's are zero indexed but the sources will start from 1
    link = f'<a href="/team3/?view=pdf&file={pdf_path}&page={page + 1}" target="_blank">[{page + 1}]</a>'
    if pdf_path.split("/")[-2] == "default": # "Software Engineering: A PRACTITIONER’S APPROACH"
      link = default_textbook(page, pdf_path)
    sources.append(link)

  # Join the top 5 sources with newlines
  sources_info = "\nSources: " + "".join(sources)
  final_answer = f"{answer}\n\n{sources_info}"
  return final_answer

