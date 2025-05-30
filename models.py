from sqlalchemy import Column, String, Text, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(String(10), primary_key=True)
    language = Column(String(20))
    code = Column(Text)

class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(String(36), primary_key=True)  # UUID
    code_id = Column(String(10))
    language = Column(String(20))
    output = Column(Text)
    output_type = Column(String(10))
    image_path = Column(String(255), nullable=True)
    exit_code = Column(Integer)
    error_type = Column(String(50), nullable=True)
    execution_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
