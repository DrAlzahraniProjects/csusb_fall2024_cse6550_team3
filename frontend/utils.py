import os
import streamlit as st
from .questions import check_baseline_answerable
from backend.statistics import (
    update_user_session,
    toggle_correctness,
    reset_confusion_matrix,
    get_statistics,
    get_metrics,
)

#######
# CSS #
#######
def load_css():
    """Load custom CSS for the Streamlit app."""
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "style.css")
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found. Please check the file path.")


############
# Feedback #
############
def handle_feedback(conversation_id: int):
    """Handle feedback submission for a conversation."""
    feedback_value = st.session_state.get(f"feedback_{conversation_id}", None)
    if feedback_value is not None:
        toggle_correctness(conversation_id, feedback_value == 1)
        update_user_session(st.session_state.user_id)

def get_feedback_question(answerable: bool) -> str:
    """Return feedback question based on baseline questions."""
    if answerable is not None:
        return (
            "Did the chatbot correctly answer this answerable question?" if answerable
            else "Did the chatbot correctly answer this unanswerable question?"
        )
    return "Was this response helpful?"

def reset_feedback():
    """Reset all feedback values to None in the session state."""
    for key in st.session_state:
        if key.startswith('feedback_'):
            st.session_state[key] = None

###########
# METRICS #
###########
def format_metric(value):
    """Format a metric for display, returning 'N/A' if None."""
    return f"{value:.2f}" if value is not None else "N/A"

def display_confusion_matrix():
    """Display confusion matrix and associated metrics in the sidebar."""
    st.sidebar.markdown("<h2><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Evaluation Report</a></h2>", unsafe_allow_html=True)

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

    # KEY METRICS
    st.sidebar.markdown("<h3><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Key Metrics</a></h3>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-main' title="{metrics_tooltip['Sensitivity']}">
                <span class='metric-label'>Sensitivity (true positive rate):</span>
                <span class='metric-value'>{format_metric(metrics.get("Sensitivity"))}</span>
            </div>
            <div class='metric-main' title="{metrics_tooltip['Specificity']}">
                <span class='metric-label'>Specificity (true negative rate):</span>
                <span class='metric-value'>{format_metric(metrics.get("Specificity"))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CONFUSION MATRIX
    st.sidebar.markdown("<h3><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Confusion Matrix</a></h3>", unsafe_allow_html=True)
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

    # Other Metrics
    st.sidebar.markdown("<h3><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Other Metrics</a></h3>", unsafe_allow_html=True)
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
    if st.sidebar.button("Reset"):
        reset_feedback()
        reset_confusion_matrix()
        st.rerun()
