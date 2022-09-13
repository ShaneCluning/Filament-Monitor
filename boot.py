import gc
import webrepl
import _WiFiManager

_WiFiManager.checkWiFi()
webrepl.start()
gc.enable()
gc.collect()
