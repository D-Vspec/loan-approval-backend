from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import db
from .enums import SalutationEnum, GenderEnum, MaritalStatusEnum, ClientStatusEnum

class Client(db.Model):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)  
    salutation = Column(Enum(SalutationEnum))
    last_name = Column(String(100))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    gender = Column(Enum(GenderEnum))
    birthdate = Column(Date)
    place_of_birth = Column(String(150))
    height = Column(DECIMAL(5, 2))
    contact_number = Column(String(20))
    no_of_dependents = Column(Integer)
    marital_status = Column(Enum(MaritalStatusEnum))
    nationality = Column(String(100))
    weight = Column(DECIMAL(5, 2))
    education = Column(String(150))
    spouse_name = Column(String(150))
    spouse_birthdate = Column(Date)
    work = Column(String(150))
    monthly_income = Column(DECIMAL(12, 2))
    type_of_loan = Column(String(150))
    loan_amount = Column(DECIMAL(12, 2))
    existing = Column(db.Boolean, default=False)
    CIF_number = Column(String(100), nullable=True)
    submission_date = Column(DateTime, default=func.now(), nullable=True)  # Track when form was submitted

    verified = Column(db.Boolean, default=False)  # Keep for backward compatibility
    status = Column(Enum(ClientStatusEnum), default=ClientStatusEnum.PENDING)
    rejection_reason = Column(String(500), nullable=True)  # Store rejection reason when client is rejected

    addresses = relationship("AddressInformation", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiaries", cascade="all, delete-orphan")
    co_insured = relationship("CoInsured", cascade="all, delete-orphan")
    incomes = relationship("Income", cascade="all, delete-orphan")
    expenses = relationship("Expense", cascade="all, delete-orphan")
    primary_repayment_sources = relationship("PrimaryRepaymentSource", cascade="all, delete-orphan")
    other_repayment_sources = relationship("OtherRepaymentSource", cascade="all, delete-orphan")
    cash_flow_analyses = relationship("CashFlowAnalysis", cascade="all, delete-orphan")
    residencies = relationship("Residency", cascade="all, delete-orphan")
    family_and_toilet_statuses = relationship("FamilyAndToiletStatus", cascade="all, delete-orphan")
    time_in_programs = relationship("TimeInProgram", cascade="all, delete-orphan")
    center_collection_records = relationship("CenterCollectionRecord", cascade="all, delete-orphan")
    payment_histories = relationship("PaymentHistory", cascade="all, delete-orphan")
    lending_groups = relationship("LendingGroups", cascade="all, delete-orphan")
    center_status_members = relationship("CenterStatusMembers", cascade="all, delete-orphan")
    meeting_attendances = relationship("MeetingAttendance", cascade="all, delete-orphan")
    program_benefits_received = relationship("ProgramBenefitsReceived", cascade="all, delete-orphan")
    years_in_program = relationship("YearsInProgram", cascade="all, delete-orphan")
    pastdue_ratios = relationship("PastdueRatio", cascade="all, delete-orphan")
    barangay_records = relationship("BarangayRecord", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="client", cascade="all, delete-orphan")
    credit_assessment_summaries = relationship("CreditAssessmentSummary", back_populates="client", cascade="all, delete-orphan")


class AddressInformation(db.Model):
    __tablename__ = 'address_information'
    id = Column(Integer, primary_key=True)  # SERIAL
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    street = Column(String(255))
    barangay = Column(String(100))
    city_municipality = Column(String(150))
    province = Column(String(150))
    region = Column(String(150))

class Beneficiaries(db.Model):
    __tablename__ = 'beneficiaries'
    id = Column(Integer, primary_key=True)  # SERIAL
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    name = Column(String(150))
    birthdate = Column(Date)
    age = Column(Integer)
    relationship = Column(String(100))

class CoInsured(db.Model):
    __tablename__ = 'co_insured'
    id = Column(Integer, primary_key=True)  # SERIAL
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    name = Column(String(150))
    birthdate = Column(Date)
    age = Column(Integer)
    relationship = Column(String(100))
