import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(md_block):
    if re.match(r"^#{1,6}\s", md_block):
        return block_type_heading
    if md_block.startswith("```") and md_block.endswith("```"):
        return block_type_code
    lines = md_block.split("\n")
    if md_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if md_block.startswith(("* ", "- ")):
        for line in lines:
            if not line.startswith(("* ", "- ")):
                return block_type_paragraph
        return block_type_unordered_list
    if md_block.startswith("1. "):
        prev_number = 1
        for line in lines:
            if not line.startswith(f"{prev_number}. "):
                return block_type_paragraph
            prev_number += 1
        return block_type_ordered_list

    return block_type_paragraph
