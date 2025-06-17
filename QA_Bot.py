import os
from dotenv import load_dotenv
import cassio

from langchain_community.vectorstores import Cassandra
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load .env variables
load_dotenv()

# Setup Cassandra connection
cassio.init(
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    database_id=os.getenv("ASTRA_DB_ID"),
    keyspace=os.getenv("ASTRA_DB_KEYSPACE"),
)

# Set up embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Set up vectorstore
vectorstore = Cassandra(
    embedding=embedding_model,
    table_name=os.getenv("ASTRA_DB_COLLECTION"),
)

# Ollama LLM (e.g., mistral, llama3, etc.)
llm = OllamaLLM(model="mistral")  # or "llama3", "phi3", etc.

# Add memory for follow-up questions
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Combine everything into a QA chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory,
)

# Chat loop
print("🤖 Ask me anything from the documents (type 'exit' to quit):")
while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit"]:
        break

    result = qa_chain({"question": query})
    print("\nAI:", result["answer"])