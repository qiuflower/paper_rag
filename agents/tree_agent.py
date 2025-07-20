# agents/tree_agent.py

from utils.markdown_tree import build_multi_level_tree

class TreeAgent:
    def __init__(self, documents):
        self.tree = {}
        for fname, md_text in documents.items():
            self.tree[fname] = build_multi_level_tree(md_text)

    def search_by_heading(self, query):
        query_lower = query.lower()
        results = []

        def dfs(node, path):
            if node.heading != "root":
                heading_text = node.heading.lstrip("# ").lower()
                if query_lower in heading_text:
                    results.append({
                        "heading": node.heading,
                        "content": node.content,
                        "path": " > ".join(path + [node.heading])
                    })
            for child in node.children:
                dfs(child, path + [node.heading])

        for fname, root in self.tree.items():
            dfs(root, [])
        return results


# 测试代码
if __name__ == "__main__":
    from utils.file_loader import load_markdown_files
    docs = load_markdown_files("data")
    tree_agent = TreeAgent(docs)
    res = tree_agent.search_by_heading("介绍")
    for r in res:
        print(f"{r['filename']} - {r['heading']}\n{r['content'][:200]}...\n")
