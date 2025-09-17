from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import db

class Loan(db.Model):
    __tablename__ = 'loan'
    
    loan_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    type_of_loan = Column(String(150))
    loan_amount = Column(DECIMAL(12, 2))
    payment_term = Column(Integer)  # Payment term in months or as specified
    interest_rate = Column(DECIMAL(5, 2))  # Interest rate as percentage (e.g., 5.25 for 5.25%)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship to Client
    client = relationship("Client", back_populates="loans")

    # Relationship to Applicantion linking table
    applicantions = relationship("Applicantion", back_populates="loan", cascade="all, delete-orphan")
