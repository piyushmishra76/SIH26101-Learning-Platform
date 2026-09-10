def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        start = end - overlap

    return chunks
if __name__ == "__main__":

    text = "This is a sample text. " * 300

    chunks = chunk_text(text)

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}:")
        print(chunk[:100])