
import chromadb

class Knowledge:
    #Initialisiert die Knowledge-Klasse mit einem PersistentClient von ChromaDB.
    #:param chroma_path: Pfad zur ChromaDB-Datenbank.
    def __init__(self, chroma_path="./chroma/chromaDB"):
        print(chroma_path)
        self.chroma_client = chromadb.PersistentClient(chroma_path)
        pass


    def query(self, query, maxDistance, collectionId="MyInfos"):
        """
        Führt eine Abfrage auf der angegebenen Sammlung durch und gibt die Dokumente zurück,
        deren Distanz kleiner als maxDistance ist.
        :param query: Die Abfrage als Text.
        :param maxDistance: Maximale erlaubte Distanz.
        :param collectionId: ID der Sammlung, in der gesucht werden soll.
        :return: Tuple aus Dokumenten und Quellen.
        """
        collection = self.chroma_client.get_collection(collectionId)
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        return self.checkDistance(results, maxDistance)
    
    def checkDistance(self, results, maxDistance):
        documents = []
        sources = []
        print(results["distances"])
        for i, distance in enumerate(results["distances"][0]):
            if distance <= maxDistance:
                documents.append(results["documents"][0][i])
                sources.append(results["metadatas"][0][i]["source"])
            else:
                break
        return documents, list(set(sources))

