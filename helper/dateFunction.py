from datetime import date

def getDateToday():
    dateToday = (str(date.today()).split('-'))
    formatedDate = '/'.join(dateToday[::-1])
    return formatedDate

