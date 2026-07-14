import faiss
import numpy as np
import pickle
import os
from app.rag.embedder import embedder
from app.core.logger import get_logger

logger = get_logger(__name__)

class Retriever:
    def __init__(self, index_path: str = "data/faiss_index.bin", docs_path: str = "data/docs.pkl"):
        self.index_path = index_path
        self.docs_path = docs_path
        self.index = None
        self.docs = []
        
        self.load()

    def load(self):
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.docs_path, 'rb') as f:
                    self.docs = pickle.load(f)
                logger.info(f"Loaded FAISS index with {len(self.docs)} chunks.")
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")
        else:
            logger.warning("FAISS index not found. Please run the indexing script.")
            # We initialize an empty one for now, dim=384 for all-MiniLM-L6-v2
            self.index = faiss.IndexFlatL2(384)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        if not self.docs or self.index.ntotal == 0:
            return []
            
        query_emb = np.array([embedder.embed_text(query)]).astype("float32")
        distances, indices = self.index.search(query_emb, top_k)
        
        results = []
        for idx in indices[0]:
            if idx >= 0 and idx < len(self.docs):
                results.append(self.docs[idx])
        return results

retriever = Retriever()
