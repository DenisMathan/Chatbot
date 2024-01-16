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


bgb1 = """§ 27 Bestellung und Geschäftsführung des Vorstands
(1) Die Bestellung des Vorstands erfolgt durch Beschluss der Mitgliederversammlung.
(2) Die Bestellung ist jederzeit widerruflich, unbeschadet des Anspruchs auf die vertragsmäßige Vergütung. Die Widerruflichkeit kann durch die Satzung auf den Fall beschränkt werden, dass ein wichtiger Grund
für den Widerruf vorliegt; ein solcher Grund ist insbesondere grobe Pflichtverletzung oder Unfähigkeit zur ordnungsmäßigen Geschäftsführung.
(3) Auf die Geschäftsführung des Vorstands finden die für den Auftrag geltenden Vorschriften der §§ 664 bis 670 entsprechende Anwendung. Die Mitglieder des Vorstands sind unentgeltlich tätig."""

hunde1 = """Es gibt 100 verschiedene Hundearten, wobei es von jeder art zwischen 2- und 3-hundert individuen gibt. Insgesamt gibt es 25000 Hunde!
Seehunde werden nicht mit einbezogen.
"""

hunde2 = """Im jahr 1990 sind 2 Hundearten ausgestorben"""

hunde3 = """bis zum Jahr 2027 soll es nur 50 hundearten geben"""

documents = [bgb1, hunde1, hunde2, hunde3]
metadatas = [{"source": "bgb"}, {"source":"hunde"},{"source":"hunde"},{"source":"hunde"}]
ids = ["bgb1", "hunde1", "hunde2", "hunde3"]

#files = [file for file in os.listdir('./data/') if file.endswith(('.txt', '.pdf'))]
#for file_name in files:
#    file_path = os.path.join('./data/', file_name)
#    file_format = os.path.splitext(file_name)[-1].lower()
#    file_name = os.path.basename(file_path)
#    title = os.path.splitext(file_name)[0]
#    file_info = {
#        'format': file_format,
#        'title': title,
#        'path': file_path
#    }
#    documents.append(title)
#    metadatas.append({"source": file_path})
#    ids.append(file_path)
#    print(file_info)
#
print(collection)
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
query='Wie viele Hundearten gibt es?'
results = collection.query(
    query_texts=[query],
    n_results=2,
)
print(collection.count())
print(results)
print(results['distances'][0][0], results['ids'][0][0])
print(results['distances'][0][1], results['ids'][0][1])
#print(results.distances[1], results.ids[1])