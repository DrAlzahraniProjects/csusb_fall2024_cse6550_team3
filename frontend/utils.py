import os
import yake
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
    results = get_confusion_matrix()
    matrix = results['matrix']
    metrics = results['metrics']

    # Plotly configurations
    plotly_config={
        'scrollZoom': False,'doubleClick': False,
        'showTips': False,
        'displayModeBar': False,
        'draggable': False
    }
    bg_color = '#0D0D0D'

    """
    Confusion Matrix
    """
    z = [
        [matrix['fp'], matrix['tn']],
        [matrix['tp'], matrix['fn']],
    ]
    text = [
        ["FP: " + str(matrix['fp']), "TN: " + str(matrix['tn'])],
        ["TP: " + str(matrix['tp']), "FN: " + str(matrix['fn'])]
    ]
    is_null = all(val == 0 for row in z for val in row) # check if values in matrix are all 0
    tooltips = [
        [
            "False Positive:<br>The chatbot answers an unanswerable question.",
            "True Negative:<br>The chatbot does not answer an unanswerable question."
        ],
        [
            "True Positive:<br>The chatbot correctly answers an answerable question.",
            "False Negative:<br>The chatbot incorrectly answers an answerable question."
        ]
    ]
    colorscale = 'Whites' if is_null else 'Purples'
    fig = go.Figure(data=go.Heatmap(
        z=z, x=['True', 'False'], y=['False', 'True'],
        text=text, texttemplate="%{text}", textfont={"size": 16},
        showscale=False, colorscale=[[0, '#CFCFCF'], [1, '#CFCFCF']] if is_null else 'Purples',
        hoverongaps=False, hoverinfo='text', hovertext=tooltips
    ))
    fig.update_layout(
        xaxis_title='Feedback', yaxis_title='Answerable', paper_bgcolor=bg_color,
        width=300, height=250, margin=dict(l=50, r=30, t=50, b=50)
    )
    st.sidebar.markdown("<h3>Confusion Matrix</h3>", unsafe_allow_html=True)
    st.sidebar.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    """
    Performance Metrics
    """
    st.sidebar.markdown("<h3>Performance Metrics</h3>", unsafe_allow_html=True)

    def create_metric_bars(metrics_list):
        tooltips = {
            'Sensitivity': 'Proportion of actual positives correctly identified',
            'Specificity': 'Proportion of actual negatives correctly identified',
            'Accuracy': 'Overall proportion of correct predictions',
            'Precision': 'Proportion of positive identifications that were actually correct',
            'Recall': 'Proportion of actual positives correctly identified (Sensitivity)',
            'F1 Score': 'Harmonic mean of precision and recall'
        }
        
        traces = []
        for metric in metrics_list:
            value = metrics.get(metric)
            text = "N/A" if value is None else f"{value:.2f}"
            hover_text = f"{tooltips[metric]}"
            color = '#1D1D1D' if value is None else (
                '#62A834' if value >= 0.8 else # Good values get green
                '#D7AA21' if value >= 0.5 else # Mid values get yellow
                '#A83434'# Low values get red
            )
            traces.append(go.Bar(
                name=f"{metric}_bg", y=[metric], x=[1], orientation='h', marker_color='#1D1D1D', hoverinfo='text', hovertext=hover_text, showlegend=False,
            ))
            traces.append(go.Bar(
                name=metric, y=[metric], x=[value if value is not None else 0], orientation='h', hoverinfo='skip', marker_color=color, showlegend=False, text=text, textposition='outside', textfont=dict(color='#D6D6D6', size=14), texttemplate='%{text}'
            ))
        return traces

    traces = []
    metrics_order = ['Sensitivity', 'Specificity', 'Accuracy', 'Precision', 'Recall', 'F1 Score']
    for metric in metrics_order:
        traces.extend(create_metric_bars([metric]))
    fig = go.Figure(data=traces)
    fig.update_layout(
        barmode='overlay', plot_bgcolor=bg_color, paper_bgcolor=bg_color, height=250, margin=dict(l=100, r=20, t=10, b=10),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange="reversed"),
        xaxis=dict(range=[0, 1.2], showgrid=False, zeroline=False, showticklabels=False, showline=False)
    )
    # Add custom annotations for each metric
    for i, metric in enumerate(metrics_order):
        color = '#FFDF40' if metric in ['Sensitivity', 'Specificity'] else '#FFFFFF'
        fig.add_annotation(x=-0.1, y=i,text=metric, showarrow=False, font=dict(color=color, size=14), xref='paper', yref='y',xanchor='right')
    st.sidebar.plotly_chart(fig, use_container_width=False, config=plotly_config)

    """
    Reset Button
    """
    if st.sidebar.button("Reset"):
        reset_confusion_matrix()
        st.rerun()