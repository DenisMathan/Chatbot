import chromadb

chroma_client = chromadb.PersistentClient(path="./")

def getEmbedding(input):
    #topics = getTopics()
    topics = ["Impfstoff"]
    results = []
    for topic in topics:
        collection = chroma_client.get_collection(topic)
        result = collection.query(
        query_texts=[input],
        n_results=3)
        print(result["distances"][0])
        for num, distance in enumerate(result["distances"][0]):
            print(num, distance)
            results.append({"distance":distance, "document": result["documents"][0][num],"source": result["metadatas"][0][num]["source"] })
    
    results.sort(key=lambda x:x['distance'])
    print(checkDistance(results, 0.9))
    return 

def getTopics():
    result = []
    return result

def checkDistance(results, maxDistance):
    i=0
    documents = []
    sources = []
    for result in results:
        if (result['distance'] <= maxDistance):
            documents.append(result['document'])
            sources.append(result['source'])
    return documents, list(set(sources))

getEmbedding("Corona-Impfung verursacht heftige langzeitnebenwirkungen!")