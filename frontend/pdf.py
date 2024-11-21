import os
import io
import fitz  # PyMuPDF
import streamlit as st
from rapidfuzz import fuzz
from PIL import Image
import pytesseract
from streamlit_pdf_viewer import pdf_viewer

def normalize_text(text):
    """Normalize text for consistent matching."""
    return " ".join(text.lower().strip().split())

def extract_text_with_fallback(pdf_path, page_number):
    """
    Extract text from a PDF using PyMuPDF. If text is not found, fallback to OCR.
    """
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]  # Pages are zero-indexed
        text = page.get_text("text")
        if not text.strip():
            # Fallback to OCR if text is empty
            pix = page.get_pixmap(dpi=150)
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image)
        doc.close()
        return normalize_text(text)
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return ""

def fuzzy_highlight(pdf_path, search_string, page_number):
    """
    Highlight text in a PDF using fuzzy matching.
    """
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]
        extracted_text = page.get_text("text")
        extracted_lines = extracted_text.splitlines()
        normalized_search = normalize_text(search_string)

        # Find the best fuzzy matches
        matches = []
        for line in extracted_lines:
            score = fuzz.partial_ratio(normalized_search, normalize_text(line))
            if score > 80:  # Threshold for a good match
                matches.append(line)

        # Highlight all matches
        for match in matches:
            rects = page.search_for(match)
            for rect in rects:
                highlight = page.add_highlight_annot(rect)
                highlight.update()

        # Save changes to a temporary file
        temp_pdf_path = f"{pdf_path}.temp"
        doc.save(temp_pdf_path, garbage=4, deflate=True)  # Save optimized temporary file
        doc.close()
        return temp_pdf_path, matches
    except Exception as e:
        st.error(f"Error during highlighting: {str(e)}")
        return None, []

def serve_pdf_with_highlight(text_to_highlight, pdf_path, page):
    """
    Serve a PDF with highlighted text.
    """
    if not os.path.exists(pdf_path):
        st.error(f"PDF file not found at {pdf_path}")
        return

    try:
        # Highlight text and save to a temporary file
        temp_pdf_path, matches = fuzzy_highlight(pdf_path, text_to_highlight, page)

        # Render the PDF page with highlights
        if temp_pdf_path:
            with st.spinner(f"Rendering page {page} with highlights..."):
                pdf_viewer(
                    temp_pdf_path,
                    width=700,
                    height=1000,
                    pages_to_render=[page],
                    scroll_to_page=page,
                    
                )
    except Exception as e:
        st.error(f"An error occurred while rendering the PDF: {str(e)}")

def serve_pdf():
    """
    Fallback function to serve a PDF page without highlighting.
    """
    pdf_path = st.query_params.get("file")
    page = max(int(st.query_params.get("page", 1)), 1)

    if pdf_path and os.path.exists(pdf_path):
        try:
            with st.spinner(f"Rendering page {page}..."):
                pdf_viewer(
                    pdf_path,
                    width=700,
                    height=1000,
                    pages_to_render=[page],
                    scroll_to_page=page,
                )
        except Exception as e:
            st.error(f"Error loading page {page}: {str(e)}")
    else:
        st.error("No PDF file specified or file not found.")
