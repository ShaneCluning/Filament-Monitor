def getFileContents(fileName):
    file_contents = ""
    try:
        with open(fileName, "r") as f:
            file_contents = f.read()
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))
    return file_contents


def writeFileContents(fileName, data):
    try:
        with open(fileName, "w") as f:
            f.write(data)
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))
