
from webscraper import scrapeURL

import chromadb
import json
import os

class Perception:

    def __init__(self, path = './data.json', chroma_path="./chroma/chromaDB"):
        self.path = path
        self.chroma_path = chroma_path
        self.chroma_client = chromadb.PersistentClient(chroma_path)
        self.readJson()
        self.setup()
        self.writeJson()

    def readJson(self):
        f = open(self.path)
        data = json.load(f)
        return data
    
    def setup(self):
        print(self.settings)
        for collection in self.settings:
            if collection.get('update'):
                # collection['update'] = False #UNCOMMENT
                self.collection = self.chroma_client.get_or_create_collection(name = collection.get('title'))
                print("collection: ", self.collection)
                for source in collection.get('sources'):
                    print(source.get("update"))
                    if source.get("update") != False:
                        self.updateCollection(source)

    # def deleteCollection(self, id):
    #     print(self.chroma_client.get_collection(id))
    #     print(self.chroma_client.get_settings())
    #     directoryFolderPath = self.chroma_path + '/' + str(self.chroma_client.get_collection(id).id)
    #     print(directoryFolderPath)
    #     self.chroma_client.delete_collection(id)
    #     os.remove(directoryFolderPath)
    #     print("test2")
    
    def createCollection(self, id):
        self.chroma_client.create_collection(id)

    def updateCollection(self, source):
        update = False
        create = False
        existingIds = {}
        _exisitingIds = self.collection.get()["ids"]
        for id in _exisitingIds:
            existingIds[id] = True
        updateItems = {
            'documents': [],
            'metadatas': [],
            'ids': []
        }
        createItems = {
            'documents': [],
            'metadatas': [],
            'ids': []
        }

    
        url = source.get('URL')
        setting = {
            "minLength": source.get("minLength"),
            "start": source.get("start"), 
            "end": source.get("end")
        }

        stringArr = scrapeURL(url, setting)


        for i, string in enumerate(stringArr):
            itemId = url + '||' + str(i)
            if existingIds.get(itemId) == None:
                createItems['ids'].append(url + '||' + str(i))
                createItems['metadatas'].append({"source": url})
                createItems['documents'].append(string)
                create = True
            else:
                updateItems['ids'].append(url + '||' + str(i))
                updateItems['metadatas'].append({"source": url})
                updateItems['documents'].append(string)
                existingIds.pop(itemId)
                update = True

        # TODO: Delete embeddinges
        print(len(existingIds), 'can be deleted')
        print(existingIds)

        if update:
            print('updates: ',len(updateItems['ids']))
            self.collection.update(
                documents=updateItems['documents'],
                metadatas=updateItems['metadatas'],
                ids=updateItems['ids']
            )
        
        if create:
            print('creates: ', len(createItems['ids']))
            self.collection.add(
                documents=createItems['documents'],
                metadatas=createItems['metadatas'],
                ids=createItems['ids']
            )

        # source["update"] = False #UNCOMMENT

    def writeJson(self):
        with open(self.path, "w") as outfile:
            json.dump(self.settings, outfile)
        # Serializing json
        json_object = json.dumps(self.settings, indent=4)

        # Writing to sample.json
        with open(self.path, "w") as outfile:
            outfile.write(json_object)

Vision = Perception()
