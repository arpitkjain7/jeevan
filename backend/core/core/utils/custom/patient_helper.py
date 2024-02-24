from datetime import datetime


def calculate_age(dob):
    current_date = datetime.now()
    age = current_date - dob
    age_years = age.days // 365
    remaining_days = age.days % 365
    age_months = remaining_days // 30
    return age_years, age_months
