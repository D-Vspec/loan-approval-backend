from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from db import db

class LoanApprover(db.Model):
    __tablename__ = 'loan_approver'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<LoanApprover {self.username}>'
