from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime

db=SQLAlchemy()

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    is_superuser = db.Column(db.Integer, default=0, nullable=False)
    mail=db.Column(db.String,unique=True,nullable=False)
    pwd=db.Column(db.String,nullable=False)
    f_name=db.Column(db.String,nullable=False)
    qual=db.Column(db.String)
    dob=db.Column(db.Date)

class Subject(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    description=db.Column(db.Text,nullable=True)

class Chapter(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    s_id=db.Column(db.Integer,db.ForeignKey('subject.id', ondelete="CASCADE"))

class Quiz(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date, nullable=False)
    time_duration=db.Column(db.Integer,nullable=False)
    remarks=db.Column(db.Text)
    c_id=db.Column(db.Integer,db.ForeignKey('chapter.id',ondelete="CASCADE"))

class Questions(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    q_id=db.Column(db.Integer,db.ForeignKey('quiz.id', ondelete="CASCADE"))
    question=db.Column(db.Text,nullable=False)
    op1=db.Column(db.Text,nullable=False)
    op2=db.Column(db.Text,nullable=False)
    op3=db.Column(db.Text,nullable=False)
    op4=db.Column(db.Text,nullable=False)
    cop=db.Column(db.Integer,nullable=False)

class Scores(db.Model):
    q_id=db.Column(db.Integer,db.ForeignKey('quiz.id', ondelete="CASCADE"),primary_key=True)
    u_id=db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"),primary_key=True)
    score=db.Column(db.Integer,nullable=False)
