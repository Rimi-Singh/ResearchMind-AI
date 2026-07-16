# 🧠 ResearchMind.ai

An AI-powered **Research Paper Question Answering System** built using **FastAPI**, **Retrieval-Augmented Generation (RAG)**, **FAISS**, **Sentence Transformers**, and the **Groq Large Language Model (LLM)**.

ResearchMind.ai enables administrators to ingest research papers into a semantic knowledge base. Users can then ask natural language questions about the indexed research papers and receive accurate, context-aware, citation-backed answers generated through a Retrieval-Augmented Generation (RAG) pipeline.

The system combines semantic search with a Large Language Model to retrieve relevant document sections, generate grounded answers, and provide downloadable source references.

---

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![RAG](https://img.shields.io/badge/Retrieval-Augmented%20Generation-red)
![FAISS](https://img.shields.io/badge/Vector%20Database-FAISS-orange)
![Groq](https://img.shields.io/badge/LLM-Groq-purple)
![Version](https://img.shields.io/badge/Version-v2.0-success)

---

# Table of Contents

- Overview
- Key Highlights
- Features
- Technology Stack
- System Architecture
- Project Structure
- Installation
- Environment Variables
- Running the Application
- API Endpoints
- RAG Workflow
- Guardrails
- Future Enhancements
- License
- Acknowledgements
- Author

---

# Overview

ResearchMind.ai simplifies research paper exploration by allowing users to ask natural language questions instead of manually reading lengthy academic papers.

Administrators upload research papers through the ingestion module, where documents are processed into semantic embeddings and stored in a FAISS vector database.

When a user asks a question, the system retrieves the most relevant document chunks using semantic search and uses the Groq LLM to generate an answer that is grounded only in the retrieved research context.

---

# Key Highlights

- Retrieval-Augmented Generation (RAG)
- Semantic search using FAISS
- Context-aware responses using Groq LLM
- Downloadable PDF citations
- Prompt Injection Guardrails
- FastAPI REST APIs
- Chat history support
- Modular service-based architecture

---

# Features

## 📄 Research Paper Processing

- Upload research papers in PDF format
- Automatic PDF text extraction
- Intelligent semantic text chunking
- Sentence Transformer embedding generation
- Efficient FAISS vector indexing

---

## 🤖 AI-Powered Question Answering

- Retrieval-Augmented Generation (RAG)
- Semantic similarity search
- Context-aware responses
- Grounded answers using retrieved document context
- Source citations for every generated response
- Download original cited PDF documents directly from the chatbot

---

## 🛡️ Guardrails

- Prompt injection detection
- Empty question validation
- Context-only answer generation
- Hallucination reduction
- System prompt protection
- Invalid query filtering

---

## 💬 User Experience

- User authentication
- Interactive chatbot interface
- Chat history management
- Research paper ingestion page
- Responsive dashboard
- Downloadable research paper citations

---

# Technology Stack

## Backend

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2

## AI & Machine Learning

- Groq API
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- NumPy

## Document Processing

- PyPDF

## Configuration

- python-dotenv

---

# System Architecture

                         +----------------------+
                         |     User Browser     |
                         +----------+-----------+
                                    |
                                    v
                         FastAPI Application
                                    |
              +---------------------+----------------------+
              |                                            |
              |                                            |
              v                                            v
      Authentication                              Chat Dashboard
              |                                            |
              +---------------------+----------------------+
                                    |
                                    v
                          Question Validation
                             (Guardrails)
                                    |
                                    v
                     Is it a general conversation?
                          /                    \
                       Yes                      No
                        |                       |
                        v                       v
                 Groq General Chat      FAISS Vector Search
                                                |
                                                v
                                  Retrieve Relevant Chunks
                                                |
                                                v
                                     Prompt Construction
                                                |
                                                v
                                          Groq LLM
                                                |
                                                v
                         AI Response + Source Citations
                                    + Downloadable PDFs
                                    
## 1. Research Paper Ingestion Pipeline

```text
Administrator
      │
      ▼
 Upload PDF
      │
      ▼
 Extract PDF Text
      │
      ▼
 Chunk Text
      │
      ▼
 Generate Embeddings
      │
      ▼
 Store in FAISS Vector Database
```

---

## 2. Question Answering Pipeline

```text
User
   │
   ▼
FastAPI Web Application
   │
   ▼
Input Validation & Guardrails
   │
   ▼
General Conversation?
 ┌───────────────┐
 │ Yes           │
 ▼               ▼
Groq Chat     FAISS Retrieval
                  │
                  ▼
        Retrieve Relevant Chunks
                  │
                  ▼
          Prompt Construction
                  │
                  ▼
             Groq LLM
                  │
                  ▼
 AI Response + Source Citations
        + PDF Download Links
```

---

# RAG Workflow

```text
Upload PDF
     │
     ▼
Extract Text
     │
     ▼
Chunk Documents
     │
     ▼
Generate Embeddings
     │
     ▼
Store in FAISS
     │
     ▼
User Question
     │
     ▼
Guardrails
     │
     ▼
Semantic Retrieval
     │
     ▼
Prompt Builder
     │
     ▼
Groq LLM
     │
     ▼
Grounded Answer
     │
     ▼
Download Source PDF
```

---

# Project Structure

```text
ResearchMind-AI/

├── api/
│   ├── auth.py
│   ├── chat.py
│   ├── files.py
│   ├── history.py
│   └── upload.py
│
├── config/
│   └── settings.py
│
├── data/
│   ├── pdfs/
│   └── vectorstore/
│
├── scripts/
│   ├── ingest.py
│   ├── logger.py
│   ├── query.py
│   └── text_splitter.py
│
├── services/
│   ├── guardrails.py
│   ├── history_service.py
│   ├── pdf_service.py
│   └── rag_service.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── dashboard.html
│   ├── ingestion.html
│   └── login.html
│
├── uploads/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/ResearchMind-AI.git

cd ResearchMind-AI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_api_key

USERNAME=admin
PASSWORD=admin123

EMBEDDING_MODEL=all-MiniLM-L6-v2

LLM_MODEL=llama-3.3-70b-versatile

TOP_K=5

SIMILARITY_THRESHOLD=0.65
```

---

# Running the Application

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Login page |
| POST | `/login` | Authenticate user |
| GET | `/dashboard` | Chat dashboard |
| GET | `/ingestion` | PDF ingestion page |
| POST | `/upload` | Upload PDF |
| POST | `/chat` | Ask questions |
| GET | `/history/` | Retrieve chat history |
| POST | `/history/new` | Create chat |
| GET | `/history/{chat_id}` | Retrieve chat |
| PUT | `/history/{chat_id}/rename` | Rename chat |
| DELETE | `/history/{chat_id}` | Delete chat |
| GET | `/files/pdfs` | List uploaded PDFs |
| GET | `/download-source` | Download cited PDF |
| GET | `/health` | Health check |

---

# Example

### Question

> Compare GPT and BERT.

### Answer

> BERT is a bidirectional Transformer encoder trained using Masked Language Modeling and Next Sentence Prediction, whereas GPT is an autoregressive Transformer model trained using next-token prediction. Based on the indexed research papers, BERT demonstrates stronger performance on several NLP benchmark tasks due to its bidirectional pre-training strategy.

### Sources

- BERT.pdf
- GPT.pdf

---

# Guardrails

ResearchMind.ai implements lightweight guardrails to improve reliability and prevent unintended responses.

### Implemented Guardrails

- Prompt injection detection
- Empty input validation
- Context-only answer generation
- Hallucination reduction
- System prompt protection
- Invalid query filtering

---

# Future Enhancements

- Hybrid Retrieval (Semantic + Keyword Search)
- Metadata-aware Retrieval
- OCR support for scanned PDFs
- DOCX and TXT document support
- Multi-user authentication
- Streaming AI responses
- Conversation memory
- Docker deployment
- Cloud storage integration
- Citation highlighting within PDFs

---

# License

This project was developed for educational and research purposes.

---

# Acknowledgements

- FastAPI
- Groq
- Sentence Transformers
- FAISS
- PyPDF
- NumPy
- Jinja2

---

# Author

**Rimi Singh**

**ResearchMind.ai — AI-Powered Research Paper Question Answering System**
