# Filament-Monitor

Setup to use a PiicoDev Oled Monitor and a PiicoDev BME280 (on address 0x76)

Runs a nonblocking Webserver on port 80 and by default has 2 API end points:

/Update -> which takes in a parameter 'location' and sets the location to the requested value

/GetData -> which returns a json object including:
'averageTemp' the current average temp over the last 5 minutes (measured every 5 seconds)
'averageHumidity' the current average humidity over the last 5 minutes (measured every 5 seconds)
'location' the currently set location
'time' the current UTC time in the ISO8601 format (yyyy-mm-dd HH:MM:SS)
