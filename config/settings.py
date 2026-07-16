
from dotenv import load_dotenv
import os

load_dotenv()

# =====================================================
# Authentication
# =====================================================

USERNAME = "admin"
PASSWORD = "admin123"

# =====================================================
# API
# =====================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =====================================================
# Models
# =====================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama-3.3-70b-versatile"

# =====================================================
# RAG
# =====================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5
SIMILARITY_THRESHOLD = 0.65

# =====================================================
# Paths
# =====================================================

PDF_FOLDER = "uploads"
VECTORSTORE_FOLDER = "vectorstore"