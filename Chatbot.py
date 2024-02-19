# from langchain.llms import LlamaCpp
# from langchain import PromptTemplate, LLMChain
import sys
import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler,
) # for streaming resposne
from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.globals import set_debug
#from langchain.document_loaders import TextLoader, PyPDFLoader

from Knowledge import Knowledge
#PyPDFLoader = PyPDFLoader('./data/BGB.pdf')
#text_loader = TextLoader('./data/data.txt')
#documents = text_loader.load()

# set_debug(True)

# Make sure the model path is correct for your system!
q5KMDE = "./llms/llama-2-13b-german-assistant-v4.Q5_K_M.gguf"
q4KSEN = "./llms/llama-2-13b-chat.Q4_K_S.gguf"
q4KMDE = "./llms/llama-2-13b-german-assistant-v4.Q4_K_M.gguf"
model_path = q4KSEN # <-------- enter your model path here 

# template = """
# Du bist Psychiater sagst dies aber nicht!
# Antworte auf deutsch!
# Fasse folgende Daten
# [[{data}]]
# in zwei bis drei Sätzen auf Deutsch zusammen und gib eine Antwort auf folgende Aussage:
# [[{question}]]
# """
template = """Answer the following question:
  {data}
"""

class Chatbot:

  useEmbeddings= True
  useEmbeddingsStrict = True

  # LlamaCpp settings
  name =  None
  cache =  None
  verbose =  False
  callbacks =  None
  tags =  None
  metadata =  None
  callback_manager =  None
  model_path =  "./llms/llama-2-13b-chat.Q4_K_S.gguf"
  lora_base =  None
  lora_path =  None
  n_ctx =  2048
  n_parts =  -1
  seed =  -1
  f16_kv =  True
  logits_all =  False
  vocab_only =  False
  use_mlock =  False
  n_threads =  None
  n_batch =  512
  n_gpu_layers =  -1
  suffix =  None
  max_tokens =  256
  temperature =  0.5
  top_p =  0.95
  logprobs =  None
  echo =  False
  stop =  []
  repeat_penalty =  1.1
  top_k =  40
  last_n_tokens_size =  64
  use_mmap =  True
  rope_freq_scale =  1.0
  rope_freq_base =  10000.0
  model_kwargs =  {'n_keep': 512}
  streaming =  True

  def __init__(self, settings = {}, template = template):
    # self.prompt = PromptTemplate(template=template, input_variables=["data", "question"])
    self.template = template
    self.prompt = PromptTemplate(template=self.template, input_variables=["data", "question"])
    self.knowledge = Knowledge()
    self.updateSettings(settings)

  def getResponse(self, documents, query):
      # response = self.llm_chain.ainvoke({"data":documents[0], "question":query}) 
      response = self.llm_chain.invoke({"data":query}) 
      res = response["text"]
      return res
  
  def getEmbeddings(self, query):
        #  find embeddings TODO
     embeddings, sources = self.knowledge.query(query, 1)
     return embeddings, sources
  
  def answer(self, input):
      response = "Darüber habe ich keine Daten gespeichert"
      res = ""
      documents = []
      # 
      if self.useEmbeddings:
        documents, sources = self.getEmbeddings(input)
        print(documents, sources)
        if self.useEmbeddingsStrict and len(documents) == 0:
            return response
        response = self.llm_chain.invoke({"data":" | ".join(documents), "question":input})
        res = response["text"] + "\n\nQuellen: " + ', '.join(sources)
      else:
        response = self.llm_chain.invoke({"data":input}) 
        res = response["text"]
      return res
  
  def updateSettings(self, settings):
    for attribute in settings:
      print(attribute, ": ", settings[attribute])
      setattr(self, attribute, settings[attribute])
    llm = LlamaCpp(name= self.name,cache= self.cache,verbose= self.verbose,callbacks= self.callbacks,tags= self.tags,metadata= self.metadata,callback_manager= self.callback_manager,model_path= self.model_path,lora_base= self.lora_base,lora_path= self.lora_path,n_ctx= self.n_ctx,n_parts= self.n_parts,seed= self.seed,f16_kv= self.f16_kv,logits_all= self.logits_all,vocab_only= self.vocab_only,use_mlock= self.use_mlock,n_threads= self.n_threads,n_batch= self.n_batch,n_gpu_layers= self.n_gpu_layers,suffix= self.suffix,max_tokens= self.max_tokens,temperature= self.temperature,top_p= self.top_p,logprobs= self.logprobs,echo= self.echo,stop= self.stop,repeat_penalty= self.repeat_penalty,top_k= self.top_k,last_n_tokens_size= self.last_n_tokens_size,use_mmap= self.use_mmap,rope_freq_scale= self.rope_freq_scale,rope_freq_base= self.rope_freq_base,model_kwargs= self.model_kwargs,streaming= self.streaming)
    self.llm_chain = LLMChain(prompt=self.prompt, llm=llm)