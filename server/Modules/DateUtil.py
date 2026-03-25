from datetime import date

def isLeapYear(year):
    if year % 4 != 0:
        return False
    if year % 100 != 0:
        return True
    if year % 400 != 0:
        return False
    
    return True
    

def monthNumberOfDays(year, month):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (month == 2):
        return 28 if not isLeapYear(year) else 29
    
    return days[month-1] # subtract one because months range from 1 to 12, not 0 to 11

def firstOfMonth(d: date):
    year = d.year
    month = d.month
    return date(year, month, 1)

def lastOfMonth(d: date):
    year = d.year
    month = d.month
    day = monthNumberOfDays(year, month)
    return date(year, month, day)

def addMonth(d: date):
    year = d.year
    month = d.month + 1
    day = d.day
    if month > 12:
        month = 1
        year += 1
    maxDay = monthNumberOfDays(year, month)

    return date(year, month, min(day, maxDay))

def subtractMonth(d: date):
    year = d.year
    month = d.month - 1
    day = d.day
    if month < 1:
        month = 12
        year -= 1
    maxDay = monthNumberOfDays(year, month)

    return date(year, month, min(day, maxDay))