from json import loads, dumps
import _ServerManager
from ServerBinding import ServerBinding
import _TimeManager
import _WiFiManager
import AtmosMonitor
from gc import enable, collect
from _DataManager import getFileContents, writeFileContents
from PiicoDev_SSD1306_slim import *
from time import ticks_ms, ticks_diff, ticks_add

NTP_Controller = _TimeManager
Server = _ServerManager
WiFi_Manager = _WiFiManager
Atmos_Monitor = AtmosMonitor

Screen_Update_Delay = 2000
Next_Screen_Update = 0


display = create_PiicoDev_SSD1306()


def mainLoop():
    global Screen_Update_Delay
    global Next_Screen_Update
    while True:
        try:
            now = ticks_ms()
            Server.checkConnection()
            Atmos_Monitor.checkSensorReads()
            WiFi_Manager.checkWiFi()
            NTP_Controller.checkNTP()
            if ticks_diff(Next_Screen_Update, now) <= 0:
                Next_Screen_Update = ticks_add(now, Screen_Update_Delay)
                updateScreen()
        except Exception as err:
            print("error: %s, %s" % (str(err), str(type(err).__name__)))


def startUp():
    global Next_Screen_Update
    NTP_Controller.checkNTP()
    WiFi_Manager.checkWiFi()
    loadConfig()
    Server.SERVER_BINDINGS = setupServerBindings()
    Server.start()
    enable()
    collect()
    Next_Screen_Update = ticks_add(ticks_ms(), Screen_Update_Delay)
    mainLoop()


def updateScreen():
    display.fill(0)
    display.text("Filament Monitor!", 0, 0, 1)  # literal string
    display.text("Temp: ", 0, 15, 1)  # string variable
    display.text(
        "{:.2f}C".format(Atmos_Monitor.calculateAverageTemp()), 40, 15, 1
    )  # use formatted-print
    display.text("Humid: ", 0, 30, 1)  # string variable
    display.text(
        "{:.2f}%".format(Atmos_Monitor.calculateAverageHumidity()), 46, 30, 1
    )  # use formatted-print
    display.show()


def setupServerBindings():
    bindings = []

    newBinding = ServerBinding("Update", updateHandler)
    bindings.append(newBinding)

    newBinding = ServerBinding("GetData", getDataHandler)
    bindings.append(newBinding)

    return bindings


def loadConfig():
    config = loads(getFileContents("config.txt"))
    print("Loaded values: %s from config file: %s" % (str(config), "config.txt"))
    if "location" in config:
        Atmos_Monitor.location = config["location"]


def saveConfig():
    config_object = {
        "location": Atmos_Monitor.location,
    }
    json_string = dumps(config_object)
    # print("Writing config file with values: %s" % json_string)
    writeFileContents("config.txt", json_string)


def updateHandler(conn, url, params):
    updateConfig = False
    response_string = "OK"
    print("Got Update url: %s and params: %s" % (str(url), str(params)))
    for param in params:
        if "location" in param:
            Atmos_Monitor.location = param["location"]
            updateConfig = True
    if updateConfig:
        saveConfig()
    Server.stdResponse(conn, "text/plain", response_string)


def jsonResponseHandler(conn, object):
    Server.stdResponse(conn, "application/json", dumps(object))
    # json_string = json.dumps(object)
    # print("Responding with: %s" % json_string)


def getDataHandler(conn, url, params):
    print("Got Data url: %s and params: %s" % (str(url), str(params)))
    averageTemp = Atmos_Monitor.calculateAverageTemp()
    averageHumid = Atmos_Monitor.calculateAverageHumidity()
    current_data_object = {
        "averageTemp": averageTemp,
        "averageHumidity": averageHumid,
        "location": Atmos_Monitor.location,
        "time": NTP_Controller.getISO8601TimeString(),
    }
    jsonResponseHandler(conn, current_data_object)


startUp()
