import time
from typing import List, Dict
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    Text, 
    DateTime, 
    Boolean, 
    ForeignKey, 
    func,
    and_
)

Base = declarative_base()
engine = create_engine('sqlite:///team3.db', echo=False) # Set echo=True for debuggin
Session = sessionmaker(bind=engine)

###################
# DATABASE SCHEMA #
###################
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    time_logged_in = Column(DateTime(timezone=True), default=datetime.utcnow)
    session_length = Column(Integer)

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    response = Column(Text)
    citations = Column(Text)
    model_name = Column(String(255))
    source = Column(String(255))
    response_time = Column(Integer)
    correct = Column(Boolean, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    answerable = Column(Boolean, nullable=True)
    common_topics = Column(Text)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

##################################
# DATABASE INIT, INSERT, UPDATE #
##################################

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(engine)

def init_user_session():
    print("Initializing user session...")
    with Session() as session:
        new_user = User(session_length=0)
        session.add(new_user)
        session.commit()
        return new_user.id

def update_user_session(user_id):
    print("Updating user session...")
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user and user.time_logged_in:
            current_time = time.time()
            user.session_length = current_time - int(user.time_logged_in.timestamp())
            session.commit()

def insert_conversation(
    question, 
    response, 
    citations,
    model_name,
    source,
    response_time,
    user_id,
    answerable=None, 
    correct=None,  
    common_topics=""
):
    print("Inserting new conversation...")
    with Session() as session:
        new_conversation = Conversation(
            question=question,
            response=response,
            citations=citations,
            model_name=model_name,
            source=source,
            response_time=response_time,
            correct=correct,
            user_id=user_id,
            answerable=answerable,
            common_topics=common_topics
        )
        session.add(new_conversation)
        session.commit()
        return new_conversation.id

def toggle_correctness(conversation_id, value):
    """Toggle the correctness status of a conversation."""
    print(f"Toggling correctness for chat#{conversation_id}, Value = {value}")
    with Session() as session:
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()
        if conversation:
            conversation.correct = value
            session.commit()

def reset_confusion_matrix():
    """Reset the correctness and answerability fields in the conversations table"""
    with Session() as session:
        session.query(Conversation).filter(
            Conversation.answerable.isnot(None)
        ).update({
            Conversation.correct: None
        })
        session.commit()

####################
# DATABASE QUERIES #
####################

def query_common_topics(session, top_k, date_filter):
    """Query common topics from the database."""
    query = session.query(Conversation).filter(date_filter)

    all_topics = []
    for conv in query.all():
        if conv.common_topics:
            all_topics.extend(conv.common_topics.split(", "))  # Assuming comma-separated topics

    if not all_topics:
        return "No common topics found."
    
    common_topic_counts = Counter(all_topics)
    most_common_topics = common_topic_counts.most_common(top_k)
    return ", ".join([topic for topic, _ in most_common_topics])
        
def get_statistics(period="Daily"):
    """Retrieve various statistics from the database."""
    with Session() as session:
        stats = {}
        date_filter = True # if period == "overall"
        if period == "Daily":
            today = datetime.utcnow().date() # This is in UTC time not PST
            start_of_day = datetime(today.year, today.month, today.day)
            end_of_day = start_of_day + timedelta(days=1)
            date_filter = and_(Conversation.date >= start_of_day, Conversation.date < end_of_day)

        # Retrieve base metrics
        base_query = session.query(Conversation).filter(date_filter)
        stats = {
            'num_questions': base_query.count(),
            'num_correct': base_query.filter(Conversation.correct == True).count(),
            'num_incorrect': base_query.filter(Conversation.correct == False).count(),
            'avg_response_time': (base_query.with_entities(
                func.avg(Conversation.response_time)).scalar() or 0)
        }

        # Calculate user engagement
        user_query = session.query(func.avg(User.session_length))
        if period == 'Daily':
            user_query = user_query.filter(User.time_logged_in >= start_of_day)
        stats['user_engagement'] = user_query.scalar() or 0

        # Calculate Remaining metrics
        total_feedback = stats['num_correct'] + stats['num_incorrect']
        feedback_rate = (stats['num_correct'] / total_feedback * 100) if total_feedback > 0 else 0
        stats.update({
            'accuracy_rate': feedback_rate,
            'satisfaction_rate': feedback_rate,
            'common_topics': query_common_topics(session, 5, date_filter)
        })
        return stats

def calculate_confusion_matrix(conversations: List[Conversation]) -> Dict[str, int]:
    """Calculate confusion matrix values from conversations."""
    # True Positives (TP): The chatbot correctly answers an answerable question.
    tp = sum(1 for c in conversations if c.correct and c.answerable)
    # False Negatives (FN): The chatbot fails to provide a correct answer for an answerable question.
    fn = sum(1 for c in conversations if not c.correct and c.answerable)
    # False Positives (FP): The chatbot provides an answer for an unanswerable question.
    fp = sum(1 for c in conversations if not c.correct and not c.answerable)
    tn = sum(1 for c in conversations if c.correct and not c.answerable)
    # True Negatives (TN): The chatbot correctly identifies an unanswerable question.
    return {'tp': tp, 'fn': fn, 'fp': fp, 'tn': tn}

def calculate_confusion_matrix_elements(confusion_matrix: Dict[str, int]) -> tuple:
    """
    Extracts elements from confusion matrix for easier use in metrics calculation.
    """
    tp = confusion_matrix.get('tp', 0)
    fn = confusion_matrix.get('fn', 0)
    fp = confusion_matrix.get('fp', 0)
    tn = confusion_matrix.get('tn', 0)
    return tp, fn, fp, tn

def calculate_accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
    """Accuracy: Measures the proportion of correctly classified questions (both answerable and unanswerable)"""
    total = tp + tn + fp + fn
    return (tp + tn) / total if total > 0 else None

def calculate_precision(tp: int, fp: int) -> float:
    """Precision (or Positive Predictive Value): Measures the proportion of questions classified as answerable that were actually answerable"""
    return tp / (tp + fp) if (tp + fp) > 0 else None

def calculate_recall(tp: int, fn: int) -> float:
    """Recall (Sensitivity): Measures the proportion of answerable questions that were correctly answered"""
    return tp / (tp + fn) if (tp + fn) > 0 else None

def calculate_specificity(tn: int, fp: int) -> float:
    """Specificity: Measures the proportion of unanswerable questions that were correctly identified as unanswerable"""
    return tn / (tn + fp) if (tn + fp) > 0 else None

def calculate_f1(precision: float, recall: float) -> float:
    """F1 Score: The harmonic mean of precision and recall, providing a balance between the two, especially when the dataset is imbalanced"""
    return (2 * precision * recall) / (precision + recall) if precision and recall and (precision + recall) > 0 else None

def calculate_metrics(confusion_matrix: Dict[str, int]) -> Dict[str, float]:
    tp, fn, fp, tn = calculate_confusion_matrix_elements(confusion_matrix)
    accuracy = calculate_accuracy(tp, tn, fp, fn)
    precision = calculate_precision(tp, fp)
    recall = calculate_recall(tp, fn)
    specificity = calculate_specificity(tn, fp)
    f1 = calculate_f1(precision, recall)
    return {
        'Specificity': specificity,
        'Sensitivity': recall,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }

def get_metrics() -> Dict[str, Dict]:
    """
    Retrieve confusion matrix and evaluation metrics from the database.

    This function queries the database for conversations where the correctness 
    and answerability are determined. It calculates the confusion matrix from 
    these conversations and computes various performance metrics based on it 
    (e.g., accuracy, precision, recall).

    Returns:
        dict: A dictionary containing the confusion matrix and the computed metrics.
    """
    with Session() as session:
        conversations = session.query(Conversation).filter(
            Conversation.correct.isnot(None),
            Conversation.answerable.isnot(None)
        ).all()
        matrix = calculate_confusion_matrix(conversations)
        metrics = calculate_metrics(matrix)
        return {'matrix': matrix, 'metrics': metrics}