import sys
import os
sys.path.insert(1, os.path.dirname(sys.path[0]))
import chromadb
import time
from jsonReader import readFile, writeFile
from webscraper import scrapeURL
# chroma_client = chromadb.Client()
#collection = chroma_client.get_or_create_collection(name="my_collection")
chroma_client = chromadb.PersistentClient(path="./chroma/chromaDB")

file_info_list = []
collection = None

# Use glob to get a list of files in the specified directory
# files = glob.glob(os.path.join('./data/', '*'))

def setup():
    settings = readFile('./data.json')

    for topic in settings:
        print(topic["title"])
        if not topic["update"]:
            print("noUpdate")
            continue
        topic["update"] = False
        collection = chroma_client.get_or_create_collection(name = topic["title"])
        print(collection)
        continue
        documents = []
        metadatas = []
        ids = []
        for source in topic["sources"]:
            url = source["URL"]
            setting = {
                "minLength": source["minLength"],
                "start": source["start"], 
                "end": source["end"]
            }
            stringArr = scrapeURL(url, setting)
            i = 0
            for string in stringArr:
                ids.append(url + '||' + str(i))
                metadatas.append({"source": url})
                documents.append(string)
                i = i+1
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    print(settings)
    writeFile(settings, "data.json")
    collection = chroma_client.get_or_create_collection(name = "Impfstoff")

def checkDistance(results, maxDistance):
    i=0
    documents = []
    sources = []
    print(results["distances"])
    for distance in results["distances"][0]:
        print(distance)
        if distance <= maxDistance:
            documents.append(results["documents"][0][i])
            sources.append(results["metadatas"][0][i]["source"])
            i = i + 1
        else:
            break
    return documents, list(set(sources))

def getDocuments(query, maxDistance):
    print(collection)
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    documents, sources = checkDistance(results, maxDistance)
    return documents, sources

def getCollection():
    return collection

setup()