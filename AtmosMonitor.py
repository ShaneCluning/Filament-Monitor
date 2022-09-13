from time import ticks_ms, ticks_diff, ticks_add
from PiicoDev_BME280 import PiicoDev_BME280


MAX_TEMP_READINGS = 60
READ_DELAY = 5000
sensor = PiicoDev_BME280(address=0x76)

location = "Not Set"
Temp_Readings = []
Humidity_Readings = []
next_read_time = 0


def checkSensorReads():
    global next_read_time
    now = ticks_ms()
    try:
        if ticks_diff(next_read_time, now) <= 0:

            next_read_time = ticks_add(now, READ_DELAY)
            readTemp()
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))


def readTemp():
    global Temp_Readings
    tempC, presPa, humRH = sensor.values()
    print(
        "checking Sensor: Current Temp: %s, current Pressure: %s, current Humidity: %s"
        % (str(tempC), str(presPa), str(humRH))
    )
    if len(Temp_Readings) == MAX_TEMP_READINGS:
        del Temp_Readings[0]
    if len(Humidity_Readings) == MAX_TEMP_READINGS:
        del Humidity_Readings[0]
    Temp_Readings.append(tempC)
    Humidity_Readings.append(humRH)


def calculateAverageTemp():
    global Temp_Readings
    return calculateAverage(Temp_Readings)


def calculateAverageHumidity():
    global Humidity_Readings
    return calculateAverage(Humidity_Readings)


def calculateAverage(array):
    _sum = sum(array)
    _count = len(array)
    if _count < 1:
        return 0
    return _sum / _count
