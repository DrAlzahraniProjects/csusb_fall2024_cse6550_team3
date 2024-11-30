import os

def get_citations(docs):
    """
    Extract page numbers without text content.
    """
    # print(docs)
    citations = [
        {'page': doc.metadata.get('page', 'Unknown page') + 1, 'text': ''}  # No text
        for doc in docs
        if isinstance(doc.metadata.get('page'), int)
    ][:1]
    return citations if citations else []


def format_citations(citations, response):
    pdf_path = f"{os.getenv('CORPUS_SOURCE')}/textbook.pdf"
    links = [
        f'<a href="/team3/?view=pdf&file={pdf_path}&page={citation["page"]}" target="_blank">[{index + 1}]</a>'
        for index, citation in enumerate(citations)
    ]
    return "\n\nSource: " + "".join(links)