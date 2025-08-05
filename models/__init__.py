# Import all models to make them available when importing from models package
from .enums import *
from .client import Client, AddressInformation, Beneficiaries, CoInsured
from .financial import Income, Expense, PrimaryRepaymentSource, OtherRepaymentSource, CashFlowAnalysis
from .assessment import (
    Residency, FamilyAndToiletStatus, TimeInProgram, CenterCollectionRecord,
    PaymentHistory, LendingGroups, CenterStatusMembers, MeetingAttendance,
    ProgramBenefitsReceived, YearsInProgram, PastdueRatio
)

# Make all models available at package level
__all__ = [
    # Enums
    'SalutationEnum', 'GenderEnum', 'MaritalStatusEnum', 'IncomeExpenseTypeEnum',
    'FrequencyEnum', 'PrimaryRepaymentSourceEnum', 'OtherRepaymentSourceEnum',
    'CashFlowCategoryEnum', 'LengthOfStayEnum', 'OwnershipTypeEnum', 'FamilyStatusEnum',
    'ToiletStatusEnum', 'TimeInProgramEnum', 'CollectionRecordEnum', 'PaymentHistoryEnum',
    'LendingGroupsEnum', 'CenterMembersEnum', 'MeetingAttendanceEnum', 'ProgramBenefitsEnum',
    'YearsInProgramEnum', 'PastdueRatioEnum',
    
    # Client models
    'Client', 'AddressInformation', 'Beneficiaries', 'CoInsured',
    
    # Financial models
    'Income', 'Expense', 'PrimaryRepaymentSource', 'OtherRepaymentSource', 'CashFlowAnalysis',
    
    # Assessment models
    'Residency', 'FamilyAndToiletStatus', 'TimeInProgram', 'CenterCollectionRecord',
    'PaymentHistory', 'LendingGroups', 'CenterStatusMembers', 'MeetingAttendance',
    'ProgramBenefitsReceived', 'YearsInProgram', 'PastdueRatio'
]
