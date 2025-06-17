# QnA-Chatbot-using-AstraDB-and-Ollama
A local AI-powered Q&amp;A bot that ingests documents into Astra DB and answers user questions using Ollama (Mistral) with LangChain.

**📚 LangChain x AstraDB Q&A Bot**
A lightweight, local Q&A assistant that lets you query your own .txt, .pdf, or .docx documents using LangChain, AstraDB, and Ollama (e.g., Mistral). Documents are embedded and stored in AstraDB's vector database for fast, intelligent retrieval — enabling follow-up questions and persistent context-aware conversation.

**✨ Features**
✅ Ingest .txt, .pdf, and .docx files into AstraDB

✅ Generate semantic embeddings using HuggingFace

✅ Store and retrieve chunks via AstraDB vector store

✅ Chatbot powered by Ollama (e.g., Mistral)

✅ Supports follow-up or new questions via LangChain memory

✅ Fully offline LLM with interactive CLI


🚀** **Project Workflow****

**1. Document Ingestion**

-Place your documents in Docs_For_Ingestion/

-Run Ingest_Docs.py:
  
  Loads and splits documents
  
  Generates embeddings using sentence-transformers/all-MiniLM-L6-v2
  
  Uploads chunks + embeddings to AstraDB

**2. Chatbot Setup**

-Run QA_Bot.py:
  
  Initializes Ollama model (e.g., Mistral)
  
  Connects to AstraDB vector store
  
  Enables chat history memory

**3. Interactive Q&A**

-Ask anything about your documents:
  
  Specific facts: What is the total loss in 2023?
  
  Follow-up queries: And what about 2024?
  
  Summaries: Give a loss breakdown by profile


**🧠 Tech Stack**
Tool	Role
LangChain	Framework for chaining LLM and retrieval

Astra DB	Vector DB for document storage & retrieval

CassIO	Python SDK for Astra

Ollama	Local LLM runtime (e.g., Mistral)

HuggingFace Transformers	Embedding model

Python-dotenv	Secure .env management

**.env file**
ASTRA_DB_APPLICATION_TOKEN="AstraCS:*********"

ASTRA_DB_ID="*******"

ASTRA_DB_KEYSPACE="actuarial_keyspace" #Container

ASTRA_DB_REGION="us-east-2"

ASTRA_DB_COLLECTION="actuarial_documents" #Table Name
