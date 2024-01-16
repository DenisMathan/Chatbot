import os
import chromadb
from jsonReader import readFile
from webscraper import scrapeURL
chroma_client = chromadb.Client()
#collection = chroma_client.get_or_create_collection(name="my_collection")
client = chromadb.PersistentClient(path="./")

file_info_list = []

# Use glob to get a list of files in the specified directory
# files = glob.glob(os.path.join('./data/', '*'))

settings = readFile('./data.json')

for topic in settings:
    print(topic["title"])
    collection = chroma_client.get_or_create_collection(name = topic["title"])
    documents = []
    metadatas = []
    ids = []
    for source in topic["sources"]:
        url = source["URL"]
        stringArr = scrapeURL(url, source["minLength"])
        i = 0
        for string in stringArr:
            ids.append(url + str(i))
            metadatas.append({"source": url})
            documents.append(string)
            i = i+1
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
collection = chroma_client.get_or_create_collection(name = "Impfstoff")
#query='Corona-Impfung verursacht heftige langzeitnebenwirkungen!'
#results = collection.query(
#    query_texts=[query],
#    n_results=5
#)

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
    results = collection.query(
    query_texts=[query],
    n_results=3
    )
    documents, sources = checkDistance(results, maxDistance)
    return documents, sources