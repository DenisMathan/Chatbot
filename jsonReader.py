import json

def readFile(source):
    f = open(source)
    data = json.load(f)
    return data