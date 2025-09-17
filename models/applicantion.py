# filepath: /home/dv/Documents/Programming/Opsycon/loan-approval-backend/models/applicantion.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import db


class Applicantion(db.Model):
    __tablename__ = 'applicantion'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    loan_id = Column(Integer, ForeignKey('loan.loan_id', ondelete='CASCADE'), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="applicantions")
    loan = relationship("Loan", back_populates="applicantions")
