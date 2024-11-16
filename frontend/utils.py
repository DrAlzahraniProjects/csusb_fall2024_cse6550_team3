import os
import yake
import streamlit as st
from backend.statistics import (
    update_user_session,
    toggle_correctness,
    reset_confusion_matrix,
    get_statistics,
    get_metrics,
)


def load_css():
    """Load custom CSS for the Streamlit app."""
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "style.css")
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found. Please check the file path.")


def search_questions(search_term: str, questions: dict):
    """Filter questions based on a search term."""
    if not search_term:
        return list(questions.keys())
    return [q for q in questions.keys() if search_term.lower() in q.lower()]


def handle_feedback(conversation_id):
    """Handle feedback submission for a conversation."""
    feedback_value = st.session_state.get(f"feedback_{conversation_id}", None)
    if feedback_value is not None:
        toggle_correctness(conversation_id, feedback_value == 1)
        update_user_session(st.session_state.user_id)


def extract_keywords(texts, max_keywords=10):
    """
    Extract keywords from a list of texts using YAKE.

    Args:
        texts (list): List of strings to extract keywords from.
        max_keywords (int): Maximum number of keywords to extract.

    Returns:
        str: Comma-separated keywords.
    """
    extractor = yake.KeywordExtractor(lan="en", n=1, features=None)
    ignore_words = {
        "pdf", "education", "engineering", "software", "practitioner", "file", 
        "textbook.pdf", "swebok", "app", "view", "details", "level", "target", 
        "blank", "page", "href", "pressman", "detail", "system", "systems"
    }
    keywords = set()
    for text in texts:
        extracted = dict(extractor.extract_keywords(text)).keys()
        filtered_keywords = {kw.lower() for kw in extracted if kw.lower() not in ignore_words}
        keywords.update(filtered_keywords)
    return ", ".join(list(keywords)[:max_keywords])


def update_and_display_statistics():
    """Display and update statistics in the sidebar."""
    st.sidebar.markdown("<h1 class='title-stat'>Statistics Reports</h1>", unsafe_allow_html=True)
    stat_period = st.sidebar.radio(
        "Statistics period (Daily or Overall)",
        ("Daily", "Overall"),
        key="stats_period",
        label_visibility="hidden",
        horizontal=True,
    )
    stats = get_statistics(stat_period)
    st.session_state.statistics = stats

    for key, value in stats.items():
        st.sidebar.markdown(
            f"""
            <div class='btn-stat-container'>
                <span class="btn-stat">{key.replace('_', ' ').capitalize()}: {value}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_confusion_matrix():
    """Display confusion matrix and associated metrics in the sidebar."""
    st.sidebar.markdown("<h2>Evaluation Report</h2>", unsafe_allow_html=True)

    # Fetch confusion matrix and metrics
    results = get_metrics()
    matrix, metrics = results["matrix"], results["metrics"]

    # Tooltips
    cm_tooltip = {
        "tp": "True positive (TP): Correctly answered answerable questions.",
        "fp": "False positive (FP): Incorrectly answered unanswerable questions.",
        "tn": "True negative (TN): Correctly identified unanswerable questions.",
        "fn": "False negative (FN): Failed to answer answerable questions."
    }
    metrics_tooltip = {
        "Sensitivity": "Proportion of actual positives correctly identified.",
        "Specificity": "Proportion of actual negatives correctly identified.",
        "Accuracy": "Overall proportion of correct predictions.",
        "Precision": "Proportion of positive identifications that were correct.",
        "Recall": "Proportion of actual positives correctly identified.",
        "F1 Score": "Harmonic mean of precision and recall."
    }

    def format_metric(value):
        """Format a metric for display, returning 'N/A' if None."""
        return f"{value:.2f}" if value is not None else "N/A"

    # Key Metrics
    st.sidebar.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-main' title="{metrics_tooltip['Sensitivity']}">
                <span class='metric-label'>Sensitivity:</span>
                <span class='metric-value'>{format_metric(metrics.get("Sensitivity"))}</span>
            </div>
            <div class='metric-main' title="{metrics_tooltip['Specificity']}">
                <span class='metric-label'>Specificity:</span>
                <span class='metric-value'>{format_metric(metrics.get("Specificity"))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Confusion Matrix
    st.sidebar.markdown("<h3>Confusion Matrix</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <table class="confusion-matrix-table">
            <tr>
                <th></th><th>Predicted +</th><th>Predicted -</th>
            </tr>
            <tr>
                <th>Actual +</th>
                <td title="{cm_tooltip['tp']}">{matrix['tp']} (TP)</td>
                <td title="{cm_tooltip['fn']}">{matrix['fn']} (FN)</td>
            </tr>
            <tr>
                <th>Actual -</th>
                <td title="{cm_tooltip['fp']}">{matrix['fp']} (FP)</td>
                <td title="{cm_tooltip['tn']}">{matrix['tn']} (TN)</td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True,
    )

    # Additional Metrics
    st.sidebar.markdown("<h3>Additional Metrics</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-item' title="{metrics_tooltip['Accuracy']}">
                <span class='metric-label'>Accuracy:</span>
                <span class='metric-value'>{format_metric(metrics.get("Accuracy"))}</span>
            </div>
            <div class='metric-item' title="{metrics_tooltip['Precision']}">
                <span class='metric-label'>Precision:</span>
                <span class='metric-value'>{format_metric(metrics.get("Precision"))}</span>
            </div>
            <div class='metric-item' title="{metrics_tooltip['Recall']}">
                <span class='metric-label'>Recall:</span>
                <span class='metric-value'>{format_metric(metrics.get("Recall"))}</span>
            </div>
            <div class='metric-item' title="{metrics_tooltip['F1 Score']}">
                <span class='metric-label'>F1 Score:</span>
                <span class='metric-value'>{format_metric(metrics.get("F1 Score"))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Reset Confusion Matrix Button
    if st.sidebar.button("Reset Confusion Matrix"):
        reset_confusion_matrix()
        st.rerun()
