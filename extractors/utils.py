from typing import List


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def split_into_chunks(text: str, max_lines=10_000) -> List[str]:
    """
    Splits a large text into chunks of a specified maximum number of lines.
    Assumptions:
    - Paragraphs are separated by blank lines.
    - We won't be splitting across pieces of text relevant to the extraction. (less likely to split a needle)
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = []
    line_count = 0

    for line in lines:
        current_chunk.append(line)
        line_count += 1

        # Check if we have reached the desired chunk size
        if line_count >= max_lines:
            # Assumption: paragraph is separated by blank lines
            if line.strip() == "":
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                line_count = 0

    # Append any remaining lines
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks
