from dotenv import load_dotenv
import os
from mistralai import Mistral
from knowledge.Knowledge import Knowledge

root_path = os.getenv('ROOT_PATH', ".")
load_dotenv()

class Chatbot:
  def __init__(self, settings):
    self.api_key = os.getenv("LE_CHAT_TOKEN")
    print("key: ", self.api_key)
    self.model = "mistral-large-latest"
    self.client = Mistral(api_key= self.api_key)
    self.knowledge = Knowledge(root_path + '/chroma/chromaDB')
  
  def getEmbeddings(self, query):
      #  find embeddings 
     embeddings, sources = self.knowledge.query(query, 1.1)
     return embeddings, sources
  
  def insertknowledge(self, embeddings):
    sysprompt = "You're an ironic and dark humored student!"
    for index, input in enumerate(embeddings):
      if (index == 0):
        sysprompt += "\nYou know the following Facts:"
      sysprompt += "\n\t - " + input
    return sysprompt
  
  def answer(self, input):
    embeddings, sources = self.getEmbeddings(input[len(input)-1]["content"])
    print('embeddings: ')
    print(embeddings)
    # return 'hui'
    messages = [
      {
          "role": "system",
          "content": self.insertknowledge(embeddings)
      }
    ]
    if(len(input)>10):
      input = input[len(input)-10:]
    messages += input
    chat_response = self.client.chat.complete(
    model= self.model,
    messages = messages
    )
    return chat_response.choices[0].message.content