import os
import json
import faiss
import numpy as np
import pickle
import sys

# Ensure the app module can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.embedder import embedder
from app.rag.chunker import chunk_text

def build_index():
    data_dir = "data"
    docs = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".md"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()
                chunks = chunk_text(content)
                docs.extend(chunks)
        elif filename.endswith(".jsonl"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if "prompt" in data and "completion" in data:
                            docs.append(f"Prompt: {data['prompt']}\nCode: {data['completion']}")
                    except:
                        pass

    if not docs:
        print("No documents found.")
        return

    print(f"Embedding {len(docs)} chunks...")
    embeddings = embedder.embed_batch(docs)
    emb_array = np.array(embeddings).astype("float32")
    
    print("Building FAISS index...")
    index = faiss.IndexFlatL2(384)
    index.add(emb_array)
    
    faiss.write_index(index, "data/faiss_index.bin")
    with open("data/docs.pkl", "wb") as f:
        pickle.dump(docs, f)
        
    print("Done! Index saved to data/faiss_index.bin and docs to data/docs.pkl")

if __name__ == "__main__":
    build_index()
