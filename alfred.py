# from langchain.llms import LlamaCpp
# from langchain import PromptTemplate, LLMChain
import sys
import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler,
) # for streaming resposne
from langchain.llms import LlamaCpp
from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.globals import set_debug
#from langchain.document_loaders import TextLoader, PyPDFLoader

from chroma import getDocuments
#PyPDFLoader = PyPDFLoader('./data/BGB.pdf')
#text_loader = TextLoader('./data/data.txt')
#documents = text_loader.load()

# set_debug(True)

# Make sure the model path is correct for your system!
q5KMDE = "./llms/llama-2-13b-german-assistant-v4.Q5_K_M.gguf"
q4KSEN = "./llms/llama-2-13b-chat.Q4_K_S.gguf"
q4KMDE = "./llms/llama-2-13b-german-assistant-v4.Q4_K_M.gguf"
model_path = q4KSEN # <-------- enter your model path here 

template = """
Du bist Psychiater sagst dies aber nicht!
Antworte auf deutsch!
Fasse folgende Daten
[[{data}]]
in zwei bis drei Sätzen auf Deutsch zusammen und gib eine Antwort auf folgende Aussage:
[[{question}]]
"""

prompt = PromptTemplate(template=template, input_variables=["data", "question"])

# Callbacks support token-wise streaming
#callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = -1  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512 # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx = 2048,
    model_kwargs = {
      "n_keep": 512
    },
    #callback_manager=callback_manager,
    verbose=False,
    #return_final_only=False,
    temperature=0.5
)
# Uncomment the code below if you want to run inference on CPU
# llm = LlamaCpp(
#     model_path="/Users/sauravsharma/privateGPT/models/GPT4All-13B-snoozy.ggmlv3.q4_0.bin", callback_manager=callback_manager, verbose=True
# )

llm_chain = LLMChain(prompt=prompt, llm=llm)
query = None

async def getResponse(documents, query):
    response = llm_chain.ainvoke({"data":documents[0], "question":query}) 
    res = await response
    return res

while True:
  if not query:
    query = input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
  documents, sources = getDocuments(query, 1)
  print(len(documents))
  response = ""
  if len(documents) == 0:
    response = """Darüber habe ich keine Daten gespeichert!"""
  else:
    response = llm_chain.invoke({"data":" | ".join(documents), "question":query})
    response = response["text"] + "\n\nQuellen: " + ', '.join(sources)
  print("Alfred: " + response)
  query = None
#query='Corona-Impfung verursacht heftige langzeitnebenwirkungen!'