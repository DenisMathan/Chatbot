
import chromadb

class Knowledge:

    def __init__(self, chroma_path="./chroma/chromaDB"):
        self.chroma_client = chromadb.PersistentClient(chroma_path)
        pass

    def query(self, query, maxDistance, collectionId="Impfstoff"):
        collection = self.chroma_client.get_collection("Impfstoff")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        return self.checkDistance(results, maxDistance)
    
    def checkDistance(self, results, maxDistance):
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

