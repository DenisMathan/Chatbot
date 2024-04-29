import sys
from Chatbot import Chatbot

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

alfred = Chatbot({"model_path": model_path, "max_tokens": 512}, template)
query = None
while True:
  if not query:
    query = input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
  print("Alfred: " + alfred.answer(query))
  query = None