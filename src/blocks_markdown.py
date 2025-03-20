from enum import Enum
import re


def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    blocks = []
    for block in split_md:
        if block != "":
            blocks.append(block.strip())

    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def is_heading(block: str) -> bool:
    heading_pattern = re.compile(r"^(#{1,6})\s")
    return bool(heading_pattern.match(block))


def is_code_block(block: str) -> bool:
    return block.startswith("```") and block.endswith("```")


def is_unordered_list_block(block: str) -> bool:
    lines = block.splitlines()
    return all(line.startswith("- ") for line in lines)


def is_quote_block(block: str) -> bool:
    lines = block.splitlines()
    return all(line.startswith(">") for line in lines)


def is_ordered_list_block(block: str) -> bool:
    lines = block.splitlines()
    ordered_list_pattern = re.compile(r"^(\d+)\.\s")
    for idx, line in enumerate(lines, start=1):
        match = ordered_list_pattern.match(line)
        if not match:
            return False
        current_num = int(match.group(1))
        if current_num != idx:
            return False
    return True


def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    if is_code_block(block):
        return BlockType.CODE
    if is_quote_block(block):
        return BlockType.QUOTE
    if is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
