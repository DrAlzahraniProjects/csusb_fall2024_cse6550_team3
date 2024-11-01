import os
import yake
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from backend.statistics import (
    update_user_session,
    toggle_correctness,
    reset_confusion_matrix,
    get_statistics,
    get_confusion_matrix
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
    st.sidebar.markdown("<h1 class='title-stat'>Evaluation Report</h1>", unsafe_allow_html=True)

    # Get confusion matrix and metrics
    results = get_confusion_matrix()
    matrix = results['matrix']
    metrics = results['metrics']
    
    # If no data
    if all(v == 0 for v in matrix.values()):
        st.sidebar.markdown(
            "<div style='text-align: center; padding: 10px;'>"
            "No evaluation data available yet."
            "</div>", 
            unsafe_allow_html=True
        )
        return
    
    # Confusion Matrix
    z = [
        [matrix['tp'], matrix['fn']], 
        [matrix['fp'], matrix['tn']]
    ]
    annotations = [
        [str(matrix['tp']), str(matrix['fn'])],
        [str(matrix['fp']), str(matrix['tn'])]
    ]
    fig_matrix = go.Figure(data=go.Heatmap(
        z=z,
        x=['Predicted Answerable', 'Predicted Unanswerable'],
        y=['Actual Answerable', 'Actual Unanswerable'],
        text=annotations,
        texttemplate="%{text}",
        textfont={"size": 16},
        hoverongaps=False,
        colorscale='Blues'
    ))
    fig_matrix.update_layout(
        title='Confusion Matrix',
        width=300,
        height=300,
        margin=dict(l=10, r=10, t=60, b=20)
    )
    st.sidebar.plotly_chart(fig_matrix, use_container_width=True)
    
    # Performance Metrics
    valid_metrics = {k: v for k, v in metrics.items() if v is not None}
    if valid_metrics:
        st.sidebar.markdown("#### Performance Metrics")
        for metric, value in valid_metrics.items():
            # Display metric using the existing btn-stat style
            st.sidebar.markdown(f"""
                <div class='btn-stat-container'>
                    <span class="btn-stat">{metric}: {value:.2f}</span>
                </div>
            """, unsafe_allow_html=True)

    # Reset button
    if st.sidebar.button("Reset"):
        reset_confusion_matrix()
        st.rerun()

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