import os
import yake
import streamlit as st
import pandas as pd
from backend.statistics import (
    update_user_session,
    toggle_correctness,
    reset_confusion_matrix,
    get_statistics,
    get_confusion_matrix_data
)

def search_questions(search_term: str):
    """Search function for the searchbox"""
    if not search_term:
        return list(baseline_questions.keys())
    return [question for question in baseline_questions.keys() if search_term.lower() in question.lower()]

def load_css():
    """Load CSS styles"""
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "style.css")
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def handle_feedback(conversation_id):
    """Handle feedback button click"""
    feedback_value = st.session_state.get(f"feedback_{conversation_id}", None)
    if feedback_value is not None:
        toggle_correctness(conversation_id, feedback_value == 1)
        update_user_session(st.session_state.user_id)

def extract_keywords(texts):
    """Extract top N keywords from text using YAKE"""
    extractor = yake.KeywordExtractor(lan="en", n=1, features=None)
    ignore_words = {
        'pdf', 'education', 'engineering', 'software', 'practitioner', 'file', 'textbook.pdf', 'swebok', 'app', 'view',
        'details', 'level', 'target', 'blank', 'page', 'href', 'pressman', 'detail', 'system', 'systems'
    }
    keywords = set()
    for text in texts:
        extracted = dict(extractor.extract_keywords(text)).keys()
        filtered_keywords = {word.lower() for word in extracted if word.lower() not in ignore_words}
        keywords.update(filtered_keywords)
    return ", ".join(list(keywords))

def update_and_display_statistics():
    """Updates statistics report in the left sidebar based on selected period (Daily/Overall)"""
    st.sidebar.markdown("<h1 class='title-stat'>Statistics Reports</h1>", unsafe_allow_html=True)
    stat_period = st.sidebar.radio(
        "Statistics period (Daily or Overall)",
        ('Daily', 'Overall'),
        key="stats_period",
        label_visibility="hidden",
        horizontal=True
    )
    stats = get_statistics(stat_period)
    st.session_state.statistics = stats
    statistics = [
        f"Number of questions: {stats['num_questions']}",
        f"Number of correct answers: {stats['num_correct']}",
        f"Number of incorrect answers: {stats['num_incorrect']}",
        f"User engagement metrics: {stats['user_engagement']:.2f} seconds",
        f"Response time analysis: {stats['avg_response_time']:.2f} seconds",
        f"Accuracy rate: {stats['accuracy_rate']:.2f}%",
        f"Satisfaction rate: {stats['satisfaction_rate']:.2f}%",
        f"Common topics or keywords: {stats['common_topics']}",
        f"Improvement over time",
        f"Feedback summary"
    ]
    for stat in statistics:
        st.sidebar.markdown(f"""
            <div class='btn-stat-container'>
                <span class="btn-stat">{stat}</span>
            </div>
        """, unsafe_allow_html=True)

def display_confusion_matrix():
    """Display confusion matrix and evaluation metrics"""
    st.sidebar.header("Evaluation Report")

    # Get confusion matrix and metrics
    results = get_confusion_matrix_data()
    matrix = results['matrix']
    metrics = results['metrics']
    
    # CONFUSION MATRIX
    st.sidebar.markdown("<h3><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Confusion Matrix</a></h3>", unsafe_allow_html=True)
    cm_tooltip = {
        "fp": "False positive: The chatbot incorrectly answers an unanswerable question",
        "tn": "True negative: The chatbot correctly answers an unanswerable question",
        "tp": "True positive: The chatbot correctly answers an answerable question",
        "fn": "False negative: The chatbot incorrectly answers an answerable question"
    }
    st.sidebar.markdown(
        f"""
        <table class="confusion-matrix-table">
            <tr>
                <th></th>
                <th>Predicted +</th>
                <th>Predicted -</th>
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
        unsafe_allow_html=True
    )

    # PERFORMANCE METRICS
    st.sidebar.markdown("<h3><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Performance Metrics</a></h3>", unsafe_allow_html=True)
    pm_tooltip = {
        'Sensitivity': 'Sensitivity: Proportion of actual positives correctly identified',
        'Specificity': 'Specificity: Proportion of actual negatives correctly identified',
        'Accuracy': 'Accuracy: Overall proportion of correct predictions',
        'Precision': 'Precision: Proportion of positive identifications that were actually correct',
        'Recall': 'Recall: Proportion of actual positives correctly identified',
        'F1 Score': 'F1 Score: Harmonic mean of precision and recall'
    }
    st.sidebar.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-main' title="{pm_tooltip['Sensitivity']}">
                <span class='metric-label'>Sensitivity:</span>
                <span class='metric-value'>{f"{metrics['Sensitivity']:.2f}" if metrics['Sensitivity'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-main' title="{pm_tooltip['Specificity']}">
                <span class='metric-label'>Specificity:</span>
                <span class='metric-value'>{f"{metrics['Specificity']:.2f}" if metrics['Specificity'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item' title="{pm_tooltip['Accuracy']}">
                <span class='metric-label'>Accuracy:</span>
                <span class='metric-value'>{f"{metrics['Accuracy']:.2f}" if metrics['Accuracy'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item' title="{pm_tooltip['Precision']}">
                <span class='metric-label'>Precision:</span>
                <span class='metric-value'>{f"{metrics['Precision']:.2f}" if metrics['Precision'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item' title="{pm_tooltip['Recall']}">
                <span class='metric-label'>Recall:</span>
                <span class='metric-value'>{f"{metrics['Recall']:.2f}" if metrics['Recall'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item' title="{pm_tooltip['F1 Score']}">
                <span class='metric-label'>F1 Score:</span>
                <span class='metric-value'>{f"{metrics['F1 Score']:.2f}" if metrics['F1 Score'] is not None else 'N/A'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # RESET BUTTON
    if st.sidebar.button("Reset"):
        reset_confusion_matrix()
        st.rerun()