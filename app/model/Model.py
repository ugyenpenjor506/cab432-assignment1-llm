from app import db
from sqlalchemy import PrimaryKeyConstraint, DateTime, Text, Table, Column, Integer, String, ForeignKey, engine
from sqlalchemy import create_engine
from app import engine

class User(db.Model):
    __tablename__ = 'tbl_user'
    UserID = db.Column(Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(String(255), nullable=False)
    UserEmail = db.Column(String(255), nullable=True)
    Password = db.Column(String(255), nullable=False)
    CreatedAt = db.Column(DateTime, server_default=db.func.now())

class Conversation(db.Model):
    __tablename__ = 'tbl_conversation'
    ConversationID = db.Column(Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(Integer, db.ForeignKey('tbl_user.UserID'), nullable=False)
    StartTime = db.Column(DateTime, server_default=db.func.now())
    EndTime = db.Column(DateTime, nullable=True)

class UserQuery(db.Model):
    __tablename__ = 'tbl_user_query'
    QueryID = db.Column(Integer, primary_key=True, autoincrement=True)
    ConversationID = db.Column(Integer, db.ForeignKey('tbl_conversation.ConversationID'), nullable=False)
    QueryText = db.Column(Text, nullable=False)
    CreatedAt = db.Column(DateTime, server_default=db.func.now())

class BotResponse(db.Model):
    __tablename__ = 'tbl_bot_response'
    ResponseID = db.Column(Integer, primary_key=True, autoincrement=True)
    ConversationID = db.Column(Integer, db.ForeignKey('tbl_conversation.ConversationID'), nullable=False)
    QueryID = db.Column(Integer, db.ForeignKey('tbl_user_query.QueryID'), nullable=True)
    ResponseText = db.Column(Text, nullable=False)
    CreatedAt = db.Column(DateTime, server_default=db.func.now())

