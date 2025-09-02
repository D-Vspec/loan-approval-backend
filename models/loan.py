from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from db import db

class Loan(db.Model):
    __tablename__ = 'loan'
    
    loan_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    payment_term = Column(Integer)  # Payment term in months or as specified
    interest_rate = Column(DECIMAL(5, 2))  # Interest rate as percentage (e.g., 5.25 for 5.25%)
    
    # Relationship to Client
    client = relationship("Client", back_populates="loans")
