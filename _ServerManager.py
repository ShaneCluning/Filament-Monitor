import socket
import uselect
from gc import collect
from micropython import mem_info
from machine import lightsleep, reset
from _DataManager import getFileContents

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

poller = uselect.poll()
mimeTypes = {
    ".css": "text/css",
    ".jpg": "image/jpg",
    ".png": "image/png",
    ".html": "text/html",
    ".js": "text/javascript",
    ".txt": "text/plain",
}
SERVER_BINDINGS = []


def stdResponse(conn, contentType, data=None):
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: %s\n" % contentType)
    conn.send("Access-Control-Allow-Origin: *\n")
    conn.send("Connection: close\n\n")
    if data != None:
        conn.sendall(data)
    conn.close()
    collect()


def returnFile(conn, filename):
    contentType = "text/plain"
    for ext in mimeTypes:
        if filename.endswith(ext):
            contentType = mimeTypes[ext]
    stdResponse(conn, contentType, getFileContents(filename))


def getParams(url):
    path = url[1:]
    params = []
    if url.find("?") != -1:
        path = url[1 : url.find("?")]
        params_string = url[url.find("?") + 1 :]
        params_list = params_string.split("&")
        params = []
        for para in params_list:
            key = para[0 : para.find("=")].replace("%20", " ")
            value = para[para.find("=") + 1 :].replace("%20", " ")
            params.append({key: value})
    if path == "":
        path = "main.html"
    return path, params


def interpretRequest(conn):
    request = conn.recv(1024)
    request = request.decode("utf-8")
    if request[0:3] == "GET":
        request_url_full = request[4 : request.find(" ", 5)]
        request_path, request_params = getParams(request_url_full)
        print(
            "Got request, path: %s, params: %s"
            % (str(request_path), str(request_params))
        )
        served = False
        if request_path == "RamStatus":
            mem_info(1)
            stdResponse(conn, "text/plain", "OK")
            served = True
        elif request_path == "Reboot":
            stdResponse(conn, "text/plain", "OK")
            served = True
            lightsleep(1000)
            reset()
        else:
            for binding in SERVER_BINDINGS:
                if binding.url == request_path:
                    served = True
                    binding.handler(conn, request_path, request_params)
        if not served:
            returnFile(conn, request_path)

    collect()


def start():
    server.settimeout(1)
    server.bind(("", 80))
    server.listen(5)
    poller.register(server, uselect.POLLIN)


def checkConnection():
    try:
        req = poller.poll(1)
        if req:
            conn, addr = server.accept()
            conn.settimeout(1)
            interpretRequest(conn)
            collect()
    except Exception as err:
        if type(err).__name__ != "OSError":
            print(
                "error in checking connection, error: %s, %s"
                % (str(err), str(type(err).__name__))
            )
