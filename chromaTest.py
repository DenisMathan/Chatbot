import os
import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="my_collection")
client = chromadb.PersistentClient(path="./")

file_info_list = []

# Use glob to get a list of files in the specified directory
# files = glob.glob(os.path.join('./data/', '*'))
documents = []
metadatas = []
ids = []

files = [file for file in os.listdir('./data/') if file.endswith(('.txt', '.pdf'))]
for file_name in files:
    file_path = os.path.join('./data/', file_name)
    file_format = os.path.splitext(file_name)[-1].lower()
    file_name = os.path.basename(file_path)
    title = os.path.splitext(file_name)[0]
    file_info = {
        'format': file_format,
        'title': title,
        'path': file_path
    }
    documents.append(title)
    metadatas.append({"source": file_path})
    ids.append(file_path)
    print(file_info)

print(collection)
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
query='Corona-Impfung verursacht heftige langzeitnebenwirkungen!'
results = collection.query(
    query_texts=[query],
    n_results=5
)
print(results)
print(results['distances'][0][0], results['ids'][0][0])
print(results['distances'][0][1], results['ids'][0][1])
#print(results.distances[1], results.ids[1])