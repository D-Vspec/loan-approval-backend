from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Enum
from db import db
from .enums import (
    IncomeExpenseTypeEnum, FrequencyEnum, PrimaryRepaymentSourceEnum, 
    OtherRepaymentSourceEnum, CashFlowCategoryEnum
)

class Income(db.Model):
    __tablename__ = 'income'
    id = Column(Integer, primary_key=True)  # SERIAL
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    type = Column(Enum(IncomeExpenseTypeEnum))
    frequency = Column(Enum(FrequencyEnum))
    amount = Column(DECIMAL(12, 2))
    description = Column(String(255))

class Expense(db.Model):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True)  # SERIAL
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    type = Column(Enum(IncomeExpenseTypeEnum))
    frequency = Column(Enum(FrequencyEnum))
    amount = Column(DECIMAL(12, 2))
    description = Column(String(255))

class PrimaryRepaymentSource(db.Model):
    __tablename__ = 'primary_repayment_source'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    source_type = Column(Enum(PrimaryRepaymentSourceEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)

class OtherRepaymentSource(db.Model):
    __tablename__ = 'other_repayment_source'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    source_type = Column(Enum(OtherRepaymentSourceEnum), nullable=False)
    custom_description = Column(String(255))
    points = Column(Integer, default=0)

class CashFlowAnalysis(db.Model):
    __tablename__ = 'cash_flow_analysis'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    weekly_cash_flow = Column(DECIMAL(12, 2), nullable=False)
    cash_flow_category = Column(Enum(CashFlowCategoryEnum), nullable=False)
    desired_weekly_installment = Column(DECIMAL(12, 2))
    score = Column(Integer, default=0)
