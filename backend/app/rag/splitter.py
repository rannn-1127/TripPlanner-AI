# 文档切分
import re
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def split_documents(
    documents: list[Document]
) -> list[Document]:
    """
    按页面进行结构化切分。
    页面内优先按照景点/章节切分，
    超过 500 字的内容再使用递归字符切分。
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=[
            "\n\n",
            "\n",
            "。",
            "，",
            " "
        ]
    )
    chunks = []

    for document in documents:
        text = document.page_content.strip()

        if not text:
            continue

        # 当前页面的基础 metadata
        base_metadata = document.metadata.copy()

        # 按“数字 + . / 、”形式的章节标题切分
        sections = re.split(
            r"(?=\n?\d+[、.．]\s*)",
            text
        )

        for section in sections:
            section = section.strip()

            if not section:
                continue
            # 提取章节/景点名称
            match = re.match(
                r"(\d+)[、.．]\s*(.+?)(?:\n|$)",
                section
            )

            metadata = base_metadata.copy()

            if match:
                metadata["title"] = match.group(2).strip()

            # 不超过 500 字，直接作为一个 Chunk
            if len(section) <= 500:
                chunks.append(
                    Document(
                        page_content=section,
                        metadata=metadata
                    )
                )
                continue

            # 超过 500 字，再递归切分
            sub_chunks = splitter.split_text(section)

            for index, sub_chunk in enumerate(sub_chunks):
                sub_metadata = metadata.copy()
                sub_metadata["chunk_index"] = index

                chunks.append(
                    Document(
                        page_content=sub_chunk,
                        metadata=sub_metadata
                    )
                )

    return chunks
