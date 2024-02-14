import sys

import chromadb
#query = None
#while True:
#    if not query: 
#        query = input("Denis: ")
#    if query in ['quit', 'q']:
#        sys.exit()
#    print("Alfred: " + query)
#    query = None

chroma_client = chromadb.PersistentClient(path="./chroma/chromaDB")

collection = chroma_client.get_or_create_collection("Impfstoff")

print(collection.count())
#chroma_client = chromadb.Client()
##collection = chroma_client.get_or_create_collection(name="my_collection")
#client = chromadb.PersistentClient(path="./")
#
#collection = chroma_client.get_or_create_collection(name = "Impfstoff")
# collection = getCollection()
# print(collection.count())