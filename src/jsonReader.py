import json

def readFile(source):
    f = open(source)
    data = json.load(f)
    return data

def writeFile(file, store):
    with open(store, "w") as outfile:
        json.dump(file, outfile)

    # Serializing json
    json_object = json.dumps(file, indent=4)
    
    # Writing to sample.json
    with open(store, "w") as outfile:
        outfile.write(json_object)