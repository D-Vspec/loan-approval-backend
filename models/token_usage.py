from sqlalchemy import Column, Integer, Date, DateTime, String
from sqlalchemy.sql import func
from db import db

class TokenUsage(db.Model):
    __tablename__ = 'token_usage'
    
    id = Column(Integer, primary_key=True)
    usage_date = Column(Date, nullable=False, index=True)
    tokens_used = Column(Integer, nullable=False)
    api_endpoint = Column(String(255), nullable=True)  # Track which endpoint used the tokens
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f'<TokenUsage {self.usage_date}: {self.tokens_used} tokens>'