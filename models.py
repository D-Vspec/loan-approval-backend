from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import relationship
from db import db

class Client(db.Model):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    salutation = Column(Enum('Mr.', 'Ms.', 'Others'))
    last_name = Column(String(100))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    gender = Column(Enum('Male', 'Female', 'Other'))
    birthdate = Column(Date)
    place_of_birth = Column(String(150))
    height = Column(DECIMAL(5, 2))
    contact_number = Column(String(20))
    no_of_dependents = Column(Integer)
    marital_status = Column(Enum('Single', 'Married', 'Divorced', 'Widowed', 'Separated', 'Other'))
    nationality = Column(String(100))
    weight = Column(DECIMAL(5, 2))
    education = Column(String(150))
    spouse_name = Column(String(150))
    spouse_birthdate = Column(Date)
    work = Column(String(150))
    monthly_income = Column(DECIMAL(12, 2))

    addresses = relationship("AddressInformation", cascade="all, delete")
    beneficiaries = relationship("Beneficiaries", cascade="all, delete")
    co_insured = relationship("CoInsured", cascade="all, delete")
    incomes = relationship("Income", cascade="all, delete")
    expenses = relationship("Expense", cascade="all, delete")

class AddressInformation(db.Model):
    __tablename__ = 'address_information'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    street = Column(String(255))
    barangay = Column(String(100))
    city_municipality = Column(String(150))
    province = Column(String(150))
    region = Column(String(150))

class Beneficiaries(db.Model):
    __tablename__ = 'beneficiaries'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    name = Column(String(150))
    birthdate = Column(Date)
    age = Column(Integer)
    relationship = Column(String(100))

class CoInsured(db.Model):
    __tablename__ = 'co_insured'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    name = Column(String(150))
    birthdate = Column(Date)
    age = Column(Integer)
    relationship = Column(String(100))

class Income(db.Model):
    __tablename__ = 'income'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    type = Column(Enum('business', 'sales', 'household'))
    frequency = Column(Enum('daily', 'weekly', 'semi_monthly', 'monthly'))
    amount = Column(DECIMAL(12, 2))
    description = Column(String(255))

class Expense(db.Model):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    type = Column(Enum('business', 'sales', 'household'))
    frequency = Column(Enum('daily', 'weekly', 'semi_monthly', 'monthly'))
    amount = Column(DECIMAL(12, 2))
    description = Column(String(255))
