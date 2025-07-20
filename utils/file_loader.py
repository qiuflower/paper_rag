import os

def load_markdown_files(data_dir):
    """
    读取目录下所有 .md 文件，返回 dict {filename: content}
    """
    md_files = [f for f in os.listdir(data_dir) if f.endswith('.md')]
    documents = {}
    for fname in md_files:
        path = os.path.join(data_dir, fname)
        with open(path, encoding='utf-8') as f:
            documents[fname] = f.read()
    return documents
