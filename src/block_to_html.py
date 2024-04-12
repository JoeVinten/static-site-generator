import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from block_markdown import (
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
)


def text_to_leaf(content):
    inline_nodes = text_to_textnodes(content)
    return [text_node_to_html_node(node) for node in inline_nodes]


def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_leaf(paragraph)
    return ParentNode("p", children)


def heading_to_html(block):
    heading_number = len(re.match(r"^#{1,6}", block).group())
    leaf_nodes = text_to_leaf(block[heading_number + 1 :])
    return ParentNode(f"h{heading_number}", leaf_nodes)


def code_to_html(block):
    lines = block.strip("```").split("\n")
    leaf_node = ParentNode("code", text_to_leaf(" ".join(lines)))
    return ParentNode("pre", [leaf_node])


def quote_to_html(block):
    lines = block.split("\n")
    content = list(map(lambda x: x.lstrip("> "), lines))
    leaf_nodes = text_to_leaf(" ".join(content))
    return ParentNode("blockquote", leaf_nodes)


def unordered_list_to_html(block):
    lines = block.split("\n")
    content = map(lambda x: x[2:], lines)
    li_list = map(lambda x: ParentNode("li", text_to_leaf(x)), content)
    return ParentNode("ul", li_list)


def ordered_list_to_html(block):
    lines = block.split("\n")
    content = map(lambda x: re.sub(r"^\d+\.\s", "", x), lines)
    li_list = map(lambda x: ParentNode("li", text_to_leaf(x)), content)
    return ParentNode("ol", li_list)


def convert_block(block):
    block_type = block_to_block_type(block)
    convert_dic = {
        block_type_paragraph: paragraph_to_html,
        block_type_heading: heading_to_html,
        block_type_code: code_to_html,
        block_type_quote: quote_to_html,
        block_type_unordered_list: unordered_list_to_html,
        block_type_ordered_list: ordered_list_to_html,
    }
    convert_func = convert_dic[block_type]
    if convert_func is None:
        raise ValueError("Invalid block type")
    return convert_func(block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_html = []
    for block in blocks:
        html_node = convert_block(block)
        block_html.append(html_node)
    return ParentNode("div", block_html, None)
