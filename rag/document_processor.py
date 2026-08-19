from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            extracted_pages.append(
                f"[Page {page_number}]\n{page_text.strip()}"
            )

    return "\n\n".join(extracted_pages)


def create_text_chunks(text, chunk_size=200, overlap=40):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def process_pdf(pdf_file):
    extracted_text = extract_text_from_pdf(pdf_file)

    if not extracted_text.strip():
        raise ValueError(
            "No readable text was found in the uploaded PDF."
        )

    chunks = create_text_chunks(extracted_text)

    return {
        "text": extracted_text,
        "chunks": chunks,
        "chunk_count": len(chunks)
    }