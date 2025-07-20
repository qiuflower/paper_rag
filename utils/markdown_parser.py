import re

def split_markdown_by_heading(text, level=2):
    """
    按Markdown标题分块，默认按二级标题 ##。
    返回 [{"heading": "## 标题", "content": "正文"}]
    如果没有对应标题，则返回 [{"heading": "全文", "content": 全文}]
    """
    # 精确匹配指定级别标题，如 level=2 -> ##
    pattern = re.compile(rf"(^{'#' * level}\s+.+$)", re.MULTILINE)
    matches = list(pattern.finditer(text))

    if not matches:
        # 尝试用任意标题分割
        any_heading = re.compile(r"(^#+\s+.+$)", re.MULTILINE)
        matches = list(any_heading.finditer(text))
        if not matches:
            return [{"heading": "全文", "content": text.strip()}]

    chunks = []
    for i, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        chunks.append({"heading": heading, "content": content})

    return chunks
