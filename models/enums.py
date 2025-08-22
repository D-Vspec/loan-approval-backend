from enum import Enum as PyEnum

class ClientStatusEnum(PyEnum):
    PENDING = 'pending'
    VERIFIED = 'verified'
    REJECTED = 'rejected'

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
