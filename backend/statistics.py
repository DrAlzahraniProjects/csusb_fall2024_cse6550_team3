import time
from datetime import datetime, timedelta
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

from collections import Counter

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
