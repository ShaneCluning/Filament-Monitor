import network
from time import ticks_ms, ticks_diff, ticks_add

WIFI_CHECK_DELAY = 30 * 1000
WLAN = network.WLAN(network.STA_IF)
WLAN.active(True)

next_wifi_check_time = 0


def checkWiFi():
    global next_wifi_check_time
    now = ticks_ms()
    try:
        if ticks_diff(next_wifi_check_time, now) <= 0:
            print("checking WiFi")
            next_wifi_check_time = ticks_add(now, WIFI_CHECK_DELAY)
            if not WLAN.isconnected():
                print("connecting to network...")
                WLAN.connect("The3Clues", "BenQ2684")
                while not WLAN.isconnected():
                    pass
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))
