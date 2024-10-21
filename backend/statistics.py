import time
import yake
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

Base = declarative_base()
engine = create_engine('sqlite:///team3.db', echo=False)
Session = sessionmaker(bind=engine)

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
    response_time = Column(Integer)
    correct = Column(Boolean, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    common_topics = Column(Text)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

def init_db():
    """Initialize the database and create all tables."""
    print("Initializing database...")
    Base.metadata.create_all(engine)

def init_user_session():
    """Initialize a new user session and return the user ID."""
    print("Initializing user session...")
    with Session() as session:
        new_user = User(session_length=0)
        session.add(new_user)
        session.commit()
        return new_user.id

def update_user_session(user_id):
    """Update the session length for a user."""
    print("Updating user session...")
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user and user.time_logged_in:
            current_time = time.time()
            user.session_length = current_time - int(user.time_logged_in.timestamp())
            session.commit()

def insert_conversation(question, response, citations, model_name, response_time, user_id, correct=None, common_topics=""):
    """Insert a new conversation record into the database."""
    print("Inserting new conversation...")
    with Session() as session:
        new_conversation = Conversation(
            question=question,
            response=response,
            citations=citations,
            model_name=model_name,
            response_time=response_time,
            correct=correct,
            user_id=user_id,
            common_topics=common_topics
        )
        session.add(new_conversation)
        session.commit()
        return new_conversation.id

def get_statistics():
    """Retrieve various statistics from the database."""
    with Session() as session:
        stats = {}
        stats['num_questions'] = session.query(Conversation).count()
        stats['num_correct'] = session.query(Conversation).filter(Conversation.correct == True).count()
        stats['num_incorrect'] = session.query(Conversation).filter(Conversation.correct == False).count()
        stats['user_engagement'] = session.query(func.avg(User.session_length)).scalar() or 0
        stats['avg_response_time'] = session.query(func.avg(Conversation.response_time)).scalar() or 0
        
        total_feedback = stats['num_correct'] + stats['num_incorrect']
        stats['accuracy_rate'] = (stats['num_correct'] / total_feedback * 100) if total_feedback > 0 else 0
        stats['satisfaction_rate'] = (stats['num_correct'] / total_feedback * 100) if total_feedback > 0 else 0
        conversation_texts = [conv.question + " " + conv.response for conv in session.query(Conversation).all()]

        # Combine common topics and keywords extraction
        stats['common_topics'] = extract_keywords_yake(conversation_texts)
        #stats['extracted_keywords'] = extract_keywords_tfidf(session)  # Pass session for context

        print(f"Statistics: {stats}")
        return stats

def extract_keywords_yake(texts, max_keywords=5):
    """Extract top N keywords using YAKE."""
    # Create a YAKE extractor
    extractor = yake.KeywordExtractor(lan="en", n=1, top=max_keywords, features=None)
    
    # Extract keywords for each text
    keywords = set()  # Use a set to avoid duplicates
    for text in texts:
        keywords.update(dict(extractor.extract_keywords(text)).keys())
    
    return ", ".join(list(keywords))  # Return the top N keywords as a string


def extract_common_topics(session=None):
    """Extract common topics from the conversation data in the database."""
    all_topics = []
    
    if session is None:
        session = Session()  # Create a new session if none is passed

    for conv in session.query(Conversation).all():
        if conv.common_topics:
            all_topics.extend(conv.common_topics.split(", "))  # Assuming comma-separated topics

    if all_topics:
        common_topic_counts = Counter(all_topics)
        most_common_topics = common_topic_counts.most_common(5)  # Get top 5 common topics
        return ", ".join([topic for topic, _ in most_common_topics])
    else:
        return "No common topics found."

def toggle_correctness(conversation_id, value):
    """Toggle the correctness status of a conversation."""
    print(f"Toggling correctness for chat#{conversation_id}, Value = {value}")
    with Session() as session:
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()
        if conversation:
            conversation.correct = value
            session.commit()