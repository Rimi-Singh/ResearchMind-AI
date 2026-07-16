"""
Simple sliding-window text splitter.

This replaces LangChain's RecursiveCharacterTextSplitter
for this project.
"""


def split_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
):
    """
    Split text into overlapping chunks.

    Parameters
    ----------
    text : str
        Input text.

    chunk_size : int
        Maximum characters per chunk.

    chunk_overlap : int
        Number of overlapping characters.

    Returns
    -------
    list[str]
    """

    if not text:
        return []

    text = " ".join(text.split())

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[start:end]

        # Try not to cut words in half
        if end < text_length:

            last_space = chunk.rfind(" ")

            if last_space > chunk_size // 2:
                end = start + last_space
                chunk = text[start:end]

        chunks.append(chunk.strip())

        if end >= text_length:
            break

        start = max(
            0,
            end - chunk_overlap
        )

    return chunks