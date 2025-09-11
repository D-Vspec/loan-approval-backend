from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from db import db
from .enums import (
    LengthOfStayEnum, OwnershipTypeEnum, FamilyStatusEnum, ToiletStatusEnum,
    TimeInProgramEnum, CollectionRecordEnum, PaymentHistoryEnum, LendingGroupsEnum,
    CenterMembersEnum, MeetingAttendanceEnum, ProgramBenefitsEnum, 
    YearsInProgramEnum, PastdueRatioEnum, BarangayRecordEnum
)

class Residency(db.Model):
    __tablename__ = 'residency'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    length_of_stay = Column(Enum(LengthOfStayEnum), nullable=False)
    length_of_stay_custom = Column(String(255))
    ownership_type = Column(Enum(OwnershipTypeEnum), nullable=False)
    ownership_type_custom = Column(String(255))
    score = Column(Integer, default=0)

class FamilyAndToiletStatus(db.Model):
    __tablename__ = 'family_and_toilet_status'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    family_status = Column(Enum(FamilyStatusEnum), nullable=False)
    family_status_custom = Column(String(255))
    toilet_status = Column(Enum(ToiletStatusEnum), nullable=False)
    toilet_status_custom = Column(String(255))
    score = Column(Integer, default=0)
    
class TimeInProgram(db.Model):
    __tablename__ = 'time_in_program'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    program_cycle = Column(Enum(TimeInProgramEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class CenterCollectionRecord(db.Model):
    __tablename__ = 'center_collection_record'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    collection_status = Column(Enum(CollectionRecordEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class PaymentHistory(db.Model):
    __tablename__ = 'payment_history'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    payment_status = Column(Enum(PaymentHistoryEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class LendingGroups(db.Model):
    __tablename__ = 'lending_groups'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    group_participation = Column(Enum(LendingGroupsEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class CenterStatusMembers(db.Model):
    __tablename__ = 'center_status_members'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    member_count = Column(Enum(CenterMembersEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class MeetingAttendance(db.Model):
    __tablename__ = 'meeting_attendance'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    attendance_frequency = Column(Enum(MeetingAttendanceEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class ProgramBenefitsReceived(db.Model):
    __tablename__ = 'program_benefits_received'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    benefits_name = Column(Enum(ProgramBenefitsEnum), nullable=False)
    
class YearsInProgram(db.Model):
    __tablename__ = 'years_in_program'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    program_duration = Column(Enum(YearsInProgramEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
class PastdueRatio(db.Model):
    __tablename__ = 'pastdue_ratio'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    ratio_category = Column(Enum(PastdueRatioEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)

class BarangayRecord(db.Model):
    __tablename__ = 'barangay_record'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    record_status = Column(Enum(BarangayRecordEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
