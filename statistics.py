from sqlalchemy import (
	create_engine, 
	Column, 
	Integer, 
	String, 
	Text, 
	DateTime, 
	Boolean, 
	ForeignKey, 
	func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///team3.db', echo=True)
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
	correct = Column(Boolean)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
	common_topics = Column(Text)
	date = Column(DateTime(timezone=True), default=datetime.utcnow)

def init_db():
	print("Intializing database...")
	Base.metadata.create_all(engine)

def init_user_session():
	with Session() as session:
		new_user = User(session_length=0)
		session.add(new_user)
		session.commit()
		return new_user.id

def update_user_session(user_id, session_length=0):
	with Session() as session:
		user = session.query(User).filter_by(id=user_id).first()
		if user:
			user.session_length += session_length
			user.time_logged_in = datetime.utcnow()
			session.commit()

def insert_conversation(
	question, 
	response, 
	citations,
	model_name,
	response_time, 
	user_id,
	correct=True,
	common_topics=""
):
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

def get_statistics(
	type="daily"
):
	with Session() as session:
		stats = {}
		# Number of questions
		stats['num_questions'] = session.query(Conversation).count()
		# Number of correct answers
		stats['num_correct'] = session.query(Conversation).filter(Conversation.correct == True).count()
		# Number of incorrect answers
		stats['num_incorrect'] = session.query(Conversation).filter(Conversation.correct == False).count()
		# User engagement metrics
		stats['user_engagement'] = session.query(func.avg(User.session_length)).scalar() or 0
		# Average response time
		stats['avg_response_time'] = session.query(func.avg(Conversation.response_time)).scalar() or 0
		# Accuracy rate
		total_answers = stats['num_correct'] + stats['num_incorrect']
		stats['accuracy_rate'] = (stats['num_correct'] / total_answers * 100) if total_answers > 0 else 0
		
		""" 
		Todo:
		- Common topics
		- User satifaction ratings
		- Improvement over time
		- Feedback summary
		"""
		return stats

def toggle_correctness(
	conversation_id,
	value
):
	with Session() as session:
		conversation = session.query(Conversation).filter_by(id=conversation_id).first()
		if conversation:
			conversation.correct = value
			session.commit()