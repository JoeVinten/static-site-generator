import re

# does not handle nested delimiters
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise ValueError("invalid markdown, no closing delimiter")
        txt_node_list = []
        for index, item in enumerate(split_nodes):
            if item == "":
                continue
            if index % 2 == 0:
                txt_node_list.append(TextNode(item, TextType.TEXT))
            else:
                txt_node_list.append(TextNode(item, text_type))
        new_nodes.extend(txt_node_list)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_images = extract_markdown_images(node.text)

        if not extracted_images:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for image_alt, image_link in extracted_images:

            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for link_name, link_url in links:

            sections = remaining_text.split(f"[{link_name}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_name, TextType.LINK, link_url))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_and_bold_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    all_inline_text_nodes = split_nodes_delimiter(
        italic_and_bold_nodes, "`", TextType.CODE
    )
    return split_nodes_link(split_nodes_image(all_inline_text_nodes))
