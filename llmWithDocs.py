import sys

from langchain import PromptTemplate, LLMChain, LlamaCpp

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader

from langchain.vectorstores import Chroma
from langchain.embeddings import LlamaCppEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler,
) # for streaming resposne


text_loader = TextLoader('./data/data.txt')
documents = text_loader.load()
print(documents)



#######################################
## chat-code

model_path = "./llama-2-13b-chat.Q4_K_S.gguf" # <-------- enter your model path here 

template = """Question: {question}

Answer: """

prompt = PromptTemplate(template=template, input_variables=["question"])

print(prompt)
# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    callback_manager=callback_manager,
    verbose=False,
    return_final_only=True,
    # temperature=1
)

# Uncomment the code below if you want to run inference on CPU
# llm = LlamaCpp(
#     model_path="/Users/sauravsharma/privateGPT/models/GPT4All-13B-snoozy.ggmlv3.q4_0.bin", callback_manager=callback_manager, verbose=True
# )

llm_chain = LLMChain(prompt, llm=llm)

question = "Tell me a random joke "

query = None


while True:
  if not query:
    query = input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
#   result = chain({"question": query, "chat_history": chat_history})
  print(llm_chain.run(query))
  query = None
  #chat_history.append((query, result['answer']))
  
##############################################