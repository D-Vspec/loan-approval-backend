# Utility functions for client routes
from datetime import datetime

def map_salutation(salutation):
    mapping = {
        'mr': 'Mr',
        'mr.': 'Mr',
        'ms': 'Ms',
        'ms.': 'Ms',
        'others': 'Others',
        'other': 'Others'
    }
    return mapping.get(salutation.strip().lower(), 'Others')

def map_gender(gender):
    mapping = {
        'male': 'Male',
        'female': 'Female',
        'other': 'Other'
    }
    return mapping.get(gender.lower(), 'Other')

def map_marital_status(status):
    mapping = {
        'single': 'Single',
        'married': 'Married',
        'divorced': 'Divorced',
        'widowed': 'Widowed',
        'separated': 'Separated',
        'other': 'Other'
    }
    return mapping.get(status.lower(), 'Other')

def parse_date(date_string):
    if not date_string:
        return None
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.date()
    except:
        return None

def parse_decimal(value):
    if not value:
        return None
    try:
        return float(value)
    except:
        return None

def parse_int(value):
    if not value:
        return None
    try:
        return int(value)
    except:
        return None

def reverse_map_salutation(salutation):
    mapping = {
        'Mr.': 'mr',
        'Ms.': 'ms',
        'Others': 'others'
    }
    return mapping.get(salutation, 'others')

def reverse_map_gender(gender):
    mapping = {
        'Male': 'male',
        'Female': 'female',
        'Other': 'other'
    }
    return mapping.get(gender, 'other')

def reverse_map_marital_status(status):
    mapping = {
        'Single': 'single',
        'Married': 'married',
        'Divorced': 'divorced',
        'Widowed': 'widowed',
        'Separated': 'separated',
        'Other': 'other'
    }
    return mapping.get(status, 'other')

def format_date_to_iso(date_obj):
    if not date_obj:
        return ""
    try:
        dt = datetime.combine(date_obj, datetime.min.time())
        return dt.isoformat() + ".000Z"
    except:
        return ""

def map_other_repayment_source(source):
    mapping = {
        'pension_subsidy': 'PensionSubsidy',
        'sideline_hustle': 'SidelineHustle',
        'land_farming': 'LandFarming',
        'land_income': 'LandFarming',  # alias for land_farming
        'spouse_child_income': 'SpouseChildIncome',
        'remittances': 'Remittances',
        'other': 'Other'
    }
    return mapping.get(source.strip().lower(), 'Other')
