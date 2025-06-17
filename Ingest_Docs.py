#.\venv\Scripts\pip.exe install python-dotenv tqdm langchain langchain-community cassio astrapy sentence-transformers pypdf

import os
from dotenv import load_dotenv
from tqdm import tqdm

from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Cassandra
from langchain_huggingface import HuggingFaceEmbeddings
import cassio

# Load environment variables
load_dotenv()

ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION")

# Step 1: Set up CassIO connection
cassio.init(
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    database_id=os.getenv("ASTRA_DB_ID"),
    keyspace=os.getenv("ASTRA_DB_KEYSPACE"),
    #database_region=os.getenv("ASTRA_DB_REGION"), #Invalid argument now, it picks region based on DB ID
)

# Step 2: Set up embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 3: Function to ingest documents from folder
def ingest_documents_from_folder(folder_path: str):
    docs = []

    for file_name in tqdm(os.listdir(folder_path), desc="Loading documents"):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_name.endswith(".txt"):
            try:
                loader = TextLoader(file_path, encoding="utf-8")  # 🔧 CHANGED: added encoding
            except Exception as e:
                print(f"❌ Error initializing TextLoader for {file_name}: {e}")
                continue
        elif file_path.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            print(f"Skipping unsupported file: {file_name}")
            continue

        try:
            docs.extend(loader.load())
        except Exception as e:
            print(f"Failed to load {file_name}: {e}")

    print(f"Total loaded documents: {len(docs)}")

    # Step 4: Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100) #make it 1500,200 in future 
    chunks = splitter.split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")

    # Step 5: Upload to Astra
    vectorstore = Cassandra(
        embedding=embedding_model,
        table_name=ASTRA_DB_COLLECTION,
    )
    vectorstore.add_documents(chunks)
    print(f"✅ Successfully ingested {len(chunks)} chunks into AstraDB!")

# Step 6: Run ingestion
if __name__ == "__main__":
    folder_path = 'C:/Users/hp/OneDrive/Desktop/Python/Langchain x Astra DB/Docs_For_Ingestion/'  # Change if needed
    ingest_documents_from_folder(folder_path)
    #with open("Docs_For_Ingestion/txt/Actuarial_Doc.txt", encoding="utf-8") as f:
    #    print(f.read())


#CQL
#use actuarial_documents; # use keyspace name
#select * from actuarial_documents LIMIT 5; #To print metada and its embeddings