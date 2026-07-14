from __future__ import annotations

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from typing import List, Tuple
from .context_store import ContextBundle

class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def embed(self, texts: List[str]) -> torch.Tensor:
        if not texts:
            return torch.empty((0, self.model.config.hidden_size), device=self.device)
            
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(self.device)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        
        # Mean Pooling
        attention_mask = encoded_input['attention_mask']
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        # Normalize
        return F.normalize(embeddings, p=2, dim=1)


class SemanticRAG:
    def __init__(self, context: ContextBundle):
        self.embedder = EmbeddingService()
        self.chunks: List[str] = []
        self.chunk_embeddings: torch.Tensor | None = None
        self._build_index(context)

    def _split_markdown(self, markdown: str) -> List[str]:
        sections = []
        current_title = ""
        current_lines = []

        for line in markdown.splitlines():
            if line.startswith("## "):
                if current_title or current_lines:
                    sections.append(f"## {current_title}\n" + "\n".join(current_lines).strip())
                current_title = line[3:].strip()
                current_lines = []
            else:
                current_lines.append(line)

        if current_title or current_lines:
            sections.append(f"## {current_title}\n" + "\n".join(current_lines).strip())

        return [s for s in sections if s.strip()]

    def _split_blocks(self, text: str) -> List[str]:
        blocks = []
        current = []

        for line in text.splitlines():
            if line.strip():
                current.append(line)
            elif current:
                blocks.append("\n".join(current).strip())
                current = []

        if current:
            blocks.append("\n".join(current).strip())

        return [b for b in blocks if b.strip()]

    def _build_index(self, context: ContextBundle):
        self.chunks = []
        self.chunks.extend(self._split_markdown(context.syntax_docs))
        self.chunks.extend(self._split_blocks(context.examples))
        self.chunks.extend(self._split_blocks(context.test_cases))
        
        if self.chunks:
            # Batch embedding to avoid OOM on large datasets, though this dataset is small
            batch_size = 16
            all_embeddings = []
            for i in range(0, len(self.chunks), batch_size):
                batch = self.chunks[i:i + batch_size]
                emb = self.embedder.embed(batch)
                all_embeddings.append(emb)
            self.chunk_embeddings = torch.cat(all_embeddings, dim=0)

    def retrieve(self, query: str, top_k: int = 4) -> str:
        if not self.chunks or self.chunk_embeddings is None:
            return ""

        query_embedding = self.embedder.embed([query])
        
        # Cosine similarity (tensors are already normalized)
        similarities = torch.matmul(query_embedding, self.chunk_embeddings.T).squeeze(0)
        
        top_k = min(top_k, len(self.chunks))
        top_indices = torch.topk(similarities, top_k).indices.tolist()
        
        retrieved_chunks = [self.chunks[i] for i in top_indices]
        return "\n\n".join(retrieved_chunks)

rag_instance: SemanticRAG | None = None

def init_rag(context: ContextBundle):
    global rag_instance
    rag_instance = SemanticRAG(context)

def get_rag() -> SemanticRAG | None:
    return rag_instance
