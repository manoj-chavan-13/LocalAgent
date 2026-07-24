from typing import List, Dict

class TextChunker:
    """Splits source code into semantic chunks."""

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, filepath: str) -> List[Dict[str, str]]:
        """
        Splits text into chunks by newlines, trying to stay within chunk_size.
        Returns a list of dicts with 'content' and metadata.
        """
        lines = text.splitlines()
        chunks = []
        current_chunk = []
        current_length = 0
        start_line = 1

        for idx, line in enumerate(lines, 1):
            line_len = len(line) + 1  # +1 for newline
            
            if current_length + line_len > self.chunk_size and current_chunk:
                # Store the current chunk
                content = "\n".join(current_chunk)
                chunks.append({
                    "content": content,
                    "filepath": filepath,
                    "start_line": start_line,
                    "end_line": idx - 1
                })
                
                # Backtrack for overlap
                overlap_length = 0
                overlap_chunk = []
                for prev_line in reversed(current_chunk):
                    if overlap_length + len(prev_line) > self.chunk_overlap:
                        break
                    overlap_chunk.insert(0, prev_line)
                    overlap_length += len(prev_line) + 1

                current_chunk = overlap_chunk
                current_length = overlap_length
                start_line = idx - len(overlap_chunk)

            current_chunk.append(line)
            current_length += line_len

        # Add the final chunk
        if current_chunk:
            content = "\n".join(current_chunk)
            chunks.append({
                "content": content,
                "filepath": filepath,
                "start_line": start_line,
                "end_line": len(lines)
            })

        return chunks
