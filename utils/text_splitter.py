


def split_text_to_chunks(text, chunk_size=512, chunk_overlap=50):
    """
    根据 token 数（简单以空格拆分词）切分文本成多个chunk。
    chunk_overlap 表示重叠token数量，便于上下文衔接。
    
    返回 List[str]，每个字符串为一个chunk。
    """
    words = text.split()
    chunks = []
    start = 0
    length = len(words)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        if end == length:
            break
        start = end - chunk_overlap  # 重叠
    return chunks
