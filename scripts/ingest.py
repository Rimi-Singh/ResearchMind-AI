import os
import pickle

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from scripts.text_splitter import split_text
from config.settings import (
    VECTORSTORE_FOLDER,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
)
from scripts.logger import logger


# ==========================================================
# Load Embedding Model
# ==========================================================

logger.info(f"Loading Embedding Model: {EMBEDDING_MODEL}")

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# ==========================================================
# PDF Ingestion
# ==========================================================

def ingest_pdf(pdf_path: str):

    logger.info("=" * 80)
    logger.info("ResearchMind.ai Ingestion")
    logger.info("=" * 80)

    # ======================================================
    # Read PDF
    # ======================================================

    filename = os.path.basename(pdf_path)

    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:

        t = page.extract_text()

        if t:
            full_text += t + "\n"

    if not full_text.strip():
        raise Exception("No text extracted from PDF.")

    # ======================================================
    # Split Text into Chunks
    # ======================================================

    chunks = split_text(
        text=full_text,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # ======================================================
    # Generate Embeddings
    # ======================================================

    embeddings = np.asarray(
        embedding_model.encode(
            chunks,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True,
        ),
        dtype="float32",
    )

    # ======================================================
    # Create Vector Store Folder
    # ======================================================

    os.makedirs(VECTORSTORE_FOLDER, exist_ok=True)

    index_path = os.path.join(
        VECTORSTORE_FOLDER,
        "faiss_index.bin",
    )

    chunks_path = os.path.join(
        VECTORSTORE_FOLDER,
        "chunks.pkl",
    )

    metadata_path = os.path.join(
        VECTORSTORE_FOLDER,
        "metadata.pkl",
    )

    # ======================================================
    # Load Existing Database (if available)
    # ======================================================

    if os.path.exists(index_path):

        index = faiss.read_index(index_path)

        with open(chunks_path, "rb") as f:
            stored_chunks = pickle.load(f)

        with open(metadata_path, "rb") as f:
            stored_metadata = pickle.load(f)

    else:

        index = faiss.IndexFlatIP(embeddings.shape[1])

        stored_chunks = []

        stored_metadata = []

    # ======================================================
    # Add New Embeddings
    # ======================================================

    index.add(embeddings)

    stored_chunks.extend(chunks)

    # ======================================================
    # Store Metadata
    # ======================================================

    for i in range(len(chunks)):

        stored_metadata.append(
            {
                "source": filename,
                "page": "-",
                "chunk": i + 1,
                "path": os.path.join(
                    "data",
                    "pdfs",
                    filename,
                ),
            }
        )

    # ======================================================
    # Save Vector Database
    # ======================================================

    faiss.write_index(index, index_path)

    with open(chunks_path, "wb") as f:
        pickle.dump(stored_chunks, f)

    with open(metadata_path, "wb") as f:
        pickle.dump(stored_metadata, f)

    # ======================================================
    # Success
    # ======================================================

    return True