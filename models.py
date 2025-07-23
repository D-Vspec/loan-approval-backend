from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import relationship
from db import db
from enum import Enum as PyEnum

class SalutationEnum(PyEnum):
    Mr = 'Mr'
    Ms = 'Ms'
    Others = 'Others'
class GenderEnum(PyEnum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'
class MaritalStatusEnum(PyEnum):
    Single = 'Single'
    Married = 'Married'
    Divorced = 'Divorced'
    Widowed = 'Widowed'
    Separated = 'Separated'
    Other = 'Other'
class IncomeExpenseTypeEnum(PyEnum):
    Business = 'business'
    Sales = 'sales'
    Household = 'household'
class FrequencyEnum(PyEnum):
    Daily = 'daily'
    Weekly = 'weekly'
    SemiMonthly = 'semi_monthly'
    Monthly = 'monthly'
class PrimaryRepaymentSourceEnum(PyEnum):
    Agriculture = 'agriculture'
    InformalBusiness = 'informal_business'
    StableOccupation = 'stable_occupation'
    PermanentStall = 'permanent_stall'
    RegisteredBusiness = 'registered_business'
    Other = 'other'
class OtherRepaymentSourceEnum(PyEnum):
    PensionSubsidy = 'pension_subsidy'
    SidelineHustle = 'sideline_hustle'
    LandFarming = 'land_farming'
    SpouseChildIncome = 'spouse_child_income'
    Remittances = 'remittances'
    Other = 'other'
class CashFlowCategoryEnum(PyEnum):
    Below180 = 'below_180'
    Exactly180 = 'exactly_180'
    Above180 = 'above_180'
    SufficientMatches = 'sufficient_matches'
    ExceedsInstallment = 'exceeds_installment'
class LengthOfStayEnum(PyEnum):
    OneToTwoYears = '1_to_2_years'
    ThreeToFiveYears = '3_to_5_years'
    MoreThanFiveYears = 'more_than_5_years'
    SpouseSinceChildhood = 'spouse_since_childhood'
    ApplicantSinceChildhood = 'applicant_since_childhood'
    Other = 'other'
class OwnershipTypeEnum(PyEnum):
    Renting = 'renting'
    Squatter = 'squatter'
    Tenant = 'tenant'
    LivingWithParents = 'living_with_parents'
    OwnsHouseAndLot = 'owns_house_and_lot'
    Other = 'other'
class FamilyStatusEnum(PyEnum):
    SeparatedNewPartner = 'separated_new_partner'
    WidowedSeparatedAlone = 'widowed_separated_alone'
    Single = 'single'
    LivingWithPartner = 'living_with_partner'
    LegallyMarried = 'legally_married'
    Other = 'other'
class ToiletStatusEnum(PyEnum):
    NoPersonalToilet = 'no_personal_toilet'
    ToiletOutsideHome = 'toilet_outside_home'
    ToiletInsideNoWater = 'toilet_inside_no_water'
    ToiletInsideWithWater = 'toilet_inside_with_water'
    ToiletInsideWaterTiled = 'toilet_inside_water_tiled'
    Other = 'other'
class TimeInProgramEnum(PyEnum):
    SecondCycleOrEarlier = '2nd_cycle_or_earlier'
    ThirdToFourthCycle = '3rd_to_4th_cycle'
    FifthToSixthCycle = '5th_to_6th_cycle'
    SeventhToEighthCycle = '7th_to_8th_cycle'
    NinthCycleAndBeyond = '9th_cycle_and_beyond'
class CollectionRecordEnum(PyEnum):
    WeeklyPaymentsNotCompleted = 'weekly_payments_not_completed'
    PaymentsIncompleteDueDateCompletedWithinWeek = 'payments_incomplete_due_date_completed_within_week'
    PaymentsCompletedMoreThan2hrsLateAfterADFollowup = 'payments_completed_more_than_2hrs_late_after_ad_followup'
    PaymentsCompletedOnTime = 'payments_completed_on_time'
    PaymentsCompletedWithinSchedulePromptly = 'payments_completed_within_schedule_promptly'
class PaymentHistoryEnum(PyEnum):
    NoWeeklyPaymentsNotCoveredByOthers = 'no_weekly_payments_not_covered_by_others'
    OneToTwoRedMarksInPassbook = '1_to_2_red_marks_in_passbook'
    CoveredByCenterWithinTime = 'covered_by_center_within_time'
    WeeklyContributionsUpToDate = 'weekly_contributions_up_to_date'
    PersonallyPaysOnTime = 'personally_pays_on_time'
class LendingGroupsEnum(PyEnum):
    MemberOfMoreThan4Groups = 'member_of_more_than_4_groups'
    NoExperienceWithLoanGroup = 'no_experience_with_loan_group'
    MemberOf3To4Groups = 'member_of_3_to_4_groups'
    SpouseMemberOfAnotherGroup = 'spouse_member_of_another_group'
    MemberOf1To2Groups = 'member_of_1_to_2_groups'
class CenterMembersEnum(PyEnum):
    FiveToTenMembers = '5_to_10_members'
    ElevenToFifteenMembers = '11_to_15_members'
    TwentySixOrMoreMembers = '26_or_more_members'
    SixteenToTwentyMembers = '16_to_20_members'
    TwentyOneToTwentyFiveMembers = '21_to_25_members'
class MeetingAttendanceEnum(PyEnum):
    AttendedOnceIn6Months = 'attended_once_in_6_months'
    AttendedTwiceIn6Months = 'attended_twice_in_6_months'
    Attended3TimesIn6Months = 'attended_3_times_in_6_months'
    Attended4TimesIn6Months = 'attended_4_times_in_6_months'
    Attended5OrMoreTimesIn6Months = 'attended_5_or_more_times_in_6_months'
class ProgramBenefitsEnum(PyEnum):
    NoBenefitsReceived = 'no_benefits_received'
    ReceivedOnlyOneBenefit = 'received_only_one_benefit'
    ReceivedTwoOrMoreBenefits = 'received_two_or_more_benefits'
class YearsInProgramEnum(PyEnum):
    TwoYearsOrLess = '2_years_or_less'
    ThreeToFourYears = '3_to_4_years'
    FiveToSixYears = '5_to_6_years'
    SixToSevenYears = '6_to_7_years'
    EightYearsOrMore = '8_years_or_more'
class PastdueRatioEnum(PyEnum):
    FourPercentOrHigher = '4_percent_or_higher'
    ThreePercent = '3_percent'
    TwoPercent = '2_percent'
    OnePercent = '1_percent'
    ZeroPercentNoPastDue = '0_percent_no_past_due'

class Client(db.Model):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)  # SERIAL
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
    verified = Column(db.Boolean, default=False)
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
    benefits_received = Column(Enum(ProgramBenefitsEnum), nullable=False)
    custom_description = Column(String(255))
    score = Column(Integer, default=0)
    
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
