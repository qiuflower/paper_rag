# utils/markdown_tree.py

class TreeNode:
    def __init__(self, heading):
        self.heading = heading
        self.content = ""
        self.children = []

    def __repr__(self, level=0):
        indent = "  " * level
        repr_str = f"{indent}{self.heading}\n"
        if self.content.strip():
            repr_str += f"{indent}  Content: {self.content.strip()[:40]}...\n"
        for child in self.children:
            repr_str += child.__repr__(level + 1)
        return repr_str

def get_heading_level(line):
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return 0
    count = 0
    for ch in stripped:
        if ch == "#":
            count += 1
        else:
            break
    return count

def build_multi_level_tree(markdown_text):
    lines = markdown_text.splitlines()
    root = TreeNode("root")
    stack = [(0, root)]

    for line in lines:
        level = get_heading_level(line)
        if level > 0:
            node = TreeNode(line.strip())
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack[-1][1].children.append(node)
            stack.append((level, node))
        else:
            stack[-1][1].content += line + "\n"

    return root
