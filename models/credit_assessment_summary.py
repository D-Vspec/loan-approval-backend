from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import db


class CreditAssessmentSummary(db.Model):
    __tablename__ = 'credit_assessment_summary'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)

    capacity_score = Column(DECIMAL(6, 2))
    capacity_credit_score = Column(DECIMAL(6, 2))
    residency_score = Column(DECIMAL(6, 2))
    residency_credit_score = Column(DECIMAL(6, 2))
    record_score = Column(DECIMAL(6, 2))
    record_credit_score = Column(DECIMAL(6, 2))
    center_score = Column(DECIMAL(6, 2))
    center_credit_score = Column(DECIMAL(6,  2))

    credit_score = Column(DECIMAL(6, 2))
    risk_grade = Column(String(10))

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    client = relationship("Client", back_populates="credit_assessment_summaries")

    def __repr__(self) -> str:
        return f"<CreditAssessmentSummary client_id={self.client_id} credit_score={self.credit_score} risk_grade={self.risk_grade}>"
