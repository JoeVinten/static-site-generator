from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code,
)
import re


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        sections = []
        split_nodes = old_node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            print(split_nodes)
            raise ValueError(f"Cannot find closing delimiter for {delimiter}")
        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            if i % 2 == 0:
                sections.append(TextNode(split_nodes[i], text_type_text))
            else:
                sections.append(TextNode(split_nodes[i], text_type))
        new_nodes.extend(sections)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        md_images = extract_markdown_images(original_text)
        if len(md_images) == 0:
            new_nodes.append(old_node)
            continue
        for md_image in md_images:
            sections = original_text.split(f"![{md_image[0]}]({md_image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Image brackets were not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(md_image[0], text_type_image, md_image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        md_links = extract_markdown_links(original_text)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue
        for md_link in md_links:
            sections = original_text.split(f"[{md_link[0]}]({md_link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Link brackets were not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(md_link[0], text_type_link, md_link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes
