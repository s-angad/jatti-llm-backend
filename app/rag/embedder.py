from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self.model = None

    def _load(self):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text):
        self._load()
        return self.model.encode(text).tolist()

    def embed_batch(self, texts):
        self._load()
        return self.model.encode(texts).tolist()

embedder = Embedder()