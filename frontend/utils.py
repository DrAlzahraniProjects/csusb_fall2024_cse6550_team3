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

baseline_questions = {
    # 10 Answerable questions
    "Who is Hironori Washizaki?": True,
    "What is software quality?": True,
    "What is agile approach?": True,
    "How does the Agile approach impact software quality?": True,
    "What is software testing process?": True,
    "What is ROI?": True,
    "What is a Quality Management System (QMS) in software?": True,
    "What are some key challenges to ensuring software quality?": True,
    "How do risk management and SQA interact in projects?": True,
    "How does testability affect software testing processes?": True,

    # 10 Unanswerable Questions
    "How many defects will occur in a specific software project?": False,
    "What is the cost of nonconformance for a project?": False,
    "How will a new process affect software defect rates?": False,
    "What is the probability of a defect reoccurring in software?": False,
    "How long will it take to resolve defects from an audit?": False,
    "What level of software quality is `good enough` for stakeholders?": False,
    "What is the future impact of AI on software quality standards?": False,
    "What ROI will be achieved through additional SQA measures?": False,
    "What specific changes improve software quality across all projects?": False,
    "How many resources are needed to achieve a quality level?": False
}

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
    st.sidebar.markdown("<h3>Confusion Matrix</h3>", unsafe_allow_html=True)
    cm_tooltip = {
        "fp": "False positive: The chatbot incorrectly answers an unanswerable question",
        "Tn": "True negative: The chatbot correctly answers an unanswerable question",
        "Tp": "True positive: The chatbot correctly answers an answerable question",
        "fn": "False negative: The chatbot incorrectly answers an answerable question"
    }
    st.sidebar.markdown(
        """
        <table class="confusion-matrix-table">
            <tr>
                <th></th>
                <th>Predicted +</th>
                <th>Predicted -</th>
            </tr>
            <tr>
                <th>Actual +</th>
                <td>{tp} (TP)</td>
                <td>{fn} (FN)</td>
            </tr>
            <tr>
                <th>Actual -</th>
                <td>{fp} (FP)</td>
                <td>{tn} (TN)</td>
            </tr>
        </table>
        """.format(
            tp=matrix['tp'],
            fn=matrix['fn'],
            fp=matrix['fp'],
            tn=matrix['tn']
        ),
        unsafe_allow_html=True
    )

    # PERFORMANCE METRICS
    st.sidebar.markdown("<h3>Performance Metrics</h3>", unsafe_allow_html=True)
    pm_tooltip = {
        'Sensitivity': 'Proportion of actual positives correctly identified',
        'Specificity': 'Proportion of actual negatives correctly identified',
        'Accuracy': 'Overall proportion of correct predictions',
        'Precision': 'Proportion of positive identifications that were actually correct',
        'Recall': 'Proportion of actual positives correctly identified (Sensitivity)',
        'F1 Score': 'Harmonic mean of precision and recall'
    }
    st.sidebar.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-main'>
                <span class='metric-label'>Sensitivity:</span>
                <span class='metric-value'>{f"{metrics['Sensitivity']:.2f}" if metrics['Sensitivity'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-main'>
                <span class='metric-label'>Specificity:</span>
                <span class='metric-value'>{f"{metrics['Specificity']:.2f}" if metrics['Specificity'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item'>
                <span class='metric-label'>Accuracy:</span>
                <span class='metric-value'>{f"{metrics['Accuracy']:.2f}" if metrics['Accuracy'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item'>
                <span class='metric-label'>Precision:</span>
                <span class='metric-value'>{f"{metrics['Precision']:.2f}" if metrics['Precision'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item'>
                <span class='metric-label'>Recall:</span>
                <span class='metric-value'>{f"{metrics['Recall']:.2f}" if metrics['Recall'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-item'>
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