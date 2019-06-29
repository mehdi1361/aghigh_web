import jdatetime


def to_julian(persian_date):
    result_date = persian_date.split('/')
    result_date = jdatetime.JalaliToGregorian(int(result_date[0]), int(result_date[1]), int(result_date[2]))
    result_date = str(result_date.gyear) + "-" + str(result_date.gmonth) + "-" + str(result_date.gday)
    return result_date


def to_jorjean(miladi_date):
    date_time = miladi_date.split('T')
    result_date = date_time[0].split('-')
    result_date = jdatetime.GregorianToJalali(int(result_date[0]), int(result_date[1]), int(result_date[2]))
    result_date = str(result_date.jyear) + "/" + add_zero(str(result_date.jmonth)) + "/" + add_zero(
        str(result_date.jday))
    return result_date + " " + date_time[1][0:5]


def add_zero(value):
    if len(value) == 1:
        return "0" + value
    return value
