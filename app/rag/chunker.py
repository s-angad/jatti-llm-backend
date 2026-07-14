def chunk_text(text: str, chunk_size: int = 250, overlap: int = 50) -> list[str]:
    """A basic sliding window chunker for text."""
    words = text.split()
    chunks = []
    
    if not words:
        return chunks
        
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
            
    return chunks
