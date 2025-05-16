from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(String(10), primary_key=True)
    language = Column(String(20))
    code = Column(Text)
