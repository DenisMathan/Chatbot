
from helper.webscraper import scrapeURL

import chromadb
import json

# Here are the ways defined of how the chatbot percepts his knowledge and stores it in his brain (ChromaDB as embeddings)
class Perception:
    def __init__(self, root_path='./', data_path = 'data.json', chroma_path="chroma/chromaDB"):
        self.root_path = root_path
        self.path = root_path+data_path
        self.chroma_path = root_path+chroma_path
        self.chroma_client = chromadb.PersistentClient(chroma_path)
        self.settings = self.readJson(data_path)
        # self.setup()
        # print(self.chroma_client.get_collection('MyInfos').get()['documents'])
        # self.writeJson()

    def readJson(self, path):
        file = open(path)
        return json.load(file)
    
    def setup(self):
        print(self.settings)
        for collection in self.settings:
            if collection.get('update'):
                # collection['update'] = False
                self.collection = self.chroma_client.get_or_create_collection(name = collection.get('title'))
                print("collection: ", self.collection)
                for source in collection.get('sources'):
                    print(source.get("update"))
                    if source.get("update") != False:
                        self.updateCollection(source)
    
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

        stringArr = []
        url = source.get('URL')
        file = self.root_path + source.get('file')
        if url != None:
            setting = {
                "minLength": source.get("minLength"),
                "start": source.get("start"), 
                "end": source.get("end")
            }
            stringArr = scrapeURL(url, setting)
        elif(file != None):
            print(file)
            stringArr = self.readJson(file)
            pathArr = file.split('/')
            url = pathArr[len(pathArr)-1]
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
                # existingIds.pop(itemId)
                update = True
                del existingIds[itemId]

        # Delete embeddinges which are not used to be updated or created
        print(len(existingIds), 'can be deleted')
        delArr = []
        for id in existingIds.keys():
            print(id)
            delArr.append(id)

        if len(delArr) > 0:
            self.collection.delete(ids=delArr)

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

        # source["update"] = False

    def writeJson(self):
        with open(self.path, "w") as outfile:
            json.dump(self.settings, outfile)
        # Serializing json
        json_object = json.dumps(self.settings, indent=4)

        # Writing to sample.json
        with open(self.path, "w") as outfile:
            outfile.write(json_object)


