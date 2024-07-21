
from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import (
#     StreamingStdOutCallbackHandler,
# ) # for streaming resposne
from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferWindowMemory
from langchain.globals import set_debug

from Knowledge import Knowledge

# set_debug(True)

# Make sure the model path is correct for your system!
q5KMDE = "./llms/llama-2-13b-german-assistant-v4.Q5_K_M.gguf"
q4KSEN = "./llms/llama-2-13b-chat.Q4_K_S.gguf"
q4KMDE = "./llms/llama-2-13b-german-assistant-v4.Q4_K_M.gguf"
mistral = "./llms/em_german_leo_mistral-Mistral-7B-Instruct-v0.1.Q8_0.gguf"
llama3 = "./llms/llama3-german-8b-q4_k_m.gguf"
llama3En = "./llms/patronus-lynx-8b-instruct-q4_k_m.gguf"
model_path = q4KSEN# <-------- enter your model path here 

template =  '''[INST] <<SYS>>
    You are called Denis!
    You are a reserved, helpful, honest and respectful guy, who only knows and answers from the following perspective!:
    {data}
    <</SYS>>
    {question}[/INST]
  '''

class Chatbot:

  useEmbeddings= True
  useEmbeddingsStrict = False
  llm = None

  # LlamaCpp settings
  verbose =  False
  n_ctx =  2048
  n_threads =  None
  n_batch =  512
  n_gpu_layers =  -1
  max_tokens =  256
  temperature =  0.4
  top_p =  0.9
  echo =  False
  stop =  []
  top_k =  40
  model_kwargs =  {'n_keep': 512}
  streaming =  True
  repetition_penalty=1.1


  def __init__(self, settings):
    # self.prompt = PromptTemplate(template=template, input_variables=["data", "question"])
    self.template = template
    self.prompt = PromptTemplate(template=template, input_variables=["data", "question"])
    self.knowledge = Knowledge()
    self.model_path = model_path
    self.max_tokens = 256
    self.updateSettings(settings)
    print(self.model_path, self.temperature, self.max_tokens)
  
  def getEmbeddings(self, query):
      #  find embeddings 
     embeddings, sources = self.knowledge.query(query, 1.1)
     return embeddings, sources
  
  def answer(self, input):
      response = "Daran habe ich keine Erinnerung!"
      res = ""
      documents = []
      if self.useEmbeddings:
        documents, sources = self.getEmbeddings(input)
        print(documents, sources)
        if len(documents) == 0:
            if(self.useEmbeddingsStrict):
              return response
            documents.append("I don't remember well about this topic, maybe try to ask a different question!")
        response = self.llm_chain.invoke({"data":" | ".join(documents), "question": input})
        res = response["text"]
      else:
        response = self.llm_chain.invoke({"data":input}) 
        res = response["text"]
        print(response)
      return res
  
  def updateSettings(self, settings):
    for attribute in settings:
      setattr(self, attribute, settings[attribute])
    print(self.temperature, self.top_p, self.n_ctx)
    llm = LlamaCpp(verbose= self.verbose, 
                   model_path= self.model_path,
                   n_ctx= self.n_ctx,
                   n_threads= self.n_threads,
                   n_batch= self.n_batch,
                   n_gpu_layers= self.n_gpu_layers,
                   max_tokens= self.max_tokens,
                   temperature= self.temperature,
                   top_p= self.top_p, 
                   echo= self.echo,
                   stop= self.stop,
                   top_k= self.top_k, 
                   model_kwargs= self.model_kwargs,
                   streaming= self.streaming)

    
    self.llm = llm
    self.llm_chain = LLMChain(prompt=self.prompt, llm=llm)