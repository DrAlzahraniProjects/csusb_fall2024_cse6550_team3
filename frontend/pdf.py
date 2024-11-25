import os
import fitz  # PyMuPDF
import streamlit as st
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
        doc.close()
        return normalize_text(text) if text.strip() else ""
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return ""


def serve_pdf(pdf_path, page):
    """
    Serve a PDF page
    """
    if not os.path.exists(pdf_path):
        st.error(f"PDF file not found at {pdf_path}")
        return

    try:
        with st.spinner(f"Rendering page {page}..."):
            pdf_viewer(
                pdf_path,
                width=700,
                height=1000,
                pages_to_render=[page],
                scroll_to_page=page,
                render_text=True
            )
    except Exception as e:
        st.error(f"Error loading page {page}: {str(e)}")