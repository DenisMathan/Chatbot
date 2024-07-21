import sys
from Chatbot import Chatbot

# Make sure the model path is correct for your system!
q5KMDE = "./llms/llama-2-13b-german-assistant-v4.Q5_K_M.gguf"
q4KSEN = "./llms/llama-2-13b-chat.Q4_K_S.gguf"
q4KMDE = "./llms/llama-2-13b-german-assistant-v4.Q4_K_M.gguf"
mistral = "./llms/em_german_leo_mistral-Mistral-7B-Instruct-v0.1.Q8_0.gguf"
llama3 = "./llms/llama3-german-8b-q4_k_m.gguf"
llama3En = "./llms/patronus-lynx-8b-instruct-q4_k_m.gguf"
model_path = q4KSEN# <-------- enter your model path here 

# template = """
# Du bist Psychiater sagst dies aber nicht!
# Antworte auf deutsch!
# Fasse folgende Daten
# [[{data}]]
# in zwei bis drei Sätzen auf Deutsch zusammen und gib eine Antwort auf folgende Aussage:
# [[{question}]]
# """
template =  '''[INST] <<SYS>>
    You are called Denis!
    You are a reserved, helpful, honest and respectful guy, who only knows and answers from the following perspective!:
    {data}
    <</SYS>>
    {question}[/INST]
  '''
#mistral
templateI = '''
  <|im_start|>system
    Du bist ein netter chatbot, der nur folgende Dinge weiß und Antwortet!:
    {data}
  <|im_end|>
  <|im_start|>user
    {question}<|im_end|>
  <|im_start|>assistant
'''
# template = '''
#   Du Antwortest immer auf Deutsch!
#   Du bist ein netter chatbot, der nur folgende Dinge weiß und Antwortet!:
#   {data}
#   USER: {question} ASSISTANT:
# '''
# <s>
# <<SYS>> Du bist ein Webentwickler der Denis Mathan heißt.
# Beantworte folgende Aussage: <</SYS>

# [INST]{question}[/INST]
# <<sys>>Mit ausschließlich diesen Informationen:
#   {data}
# <</sys>>

def getBot():
  alfred = Chatbot({"max_tokens": 512})
  return alfred

alfred = Chatbot({"max_tokens": 512})
query = None
while True:
  if not query:
    query = input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
  print("Alfred: " + alfred.answer(query))
  query = None
