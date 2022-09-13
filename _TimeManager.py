import ntptime
from time import ticks_ms, ticks_diff, ticks_add, gmtime

NTP_TIME_REFRESH_DELAY = 24 * 60 * 60 * 1000  # 24 hours


ntptime.host = "pool.ntp.org"
next_ntp_check_time = 0


def checkNTP():
    global next_ntp_check_time
    now = ticks_ms()
    try:
        if ticks_diff(next_ntp_check_time, now) <= 0:
            print("Updating NTP")
            next_ntp_check_time = ticks_add(now, NTP_TIME_REFRESH_DELAY)
            refreshNTP()
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))


def refreshNTP():
    ntptime.settime()


def getISO8601TimeString():
    raw_time = gmtime()

    iso_string = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        raw_time[0], raw_time[1], raw_time[2], raw_time[3], raw_time[4], raw_time[5]
    )

    return iso_string
