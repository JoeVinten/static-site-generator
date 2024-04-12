import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_invalid_delim(self):
        node = TextNode("This is text with a **bolded* word", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", text_type_bold)

    def test_bold_textnode(self):
        node = TextNode("This is a paragraph", text_type_bold)
        self.assertListEqual([node], [node])

    def test_handles_multiple(self):
        node = TextNode(
            "This is text with a **bolded** word **multiple**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word ", text_type_text),
                TextNode("multiple", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with `code`", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        self.assertListEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("code", text_type_code),
            ],
            new_nodes,
        )

    def test_delims(self):
        test_cases = [
            ("*italic*", "*", text_type_italic, TextNode("italic", text_type_italic)),
            ("**bold**", "**", text_type_bold, TextNode("bold", text_type_bold)),
            ("`code`", "`", text_type_code, TextNode("code", text_type_code)),
        ]

        for text, delim, text_type, expected in test_cases:
            with self.subTest(
                text=text, delim=delim, text_type=text_type, expected=expected
            ):
                node = TextNode(f"This is text with {text}", text_type_text)
                new_nodes = split_nodes_delimiter([node], delim, text_type)
                self.assertListEqual(
                    [
                        TextNode("This is text with ", text_type_text),
                        TextNode(text.replace(delim, ""), text_type),
                    ],
                    new_nodes,
                )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertListEqual(
            extract_markdown_images(text),
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_split_nodes_image_no_image(self):
        node = TextNode("This is a Text Node with no Image", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def split_nodes_link_no_link(self):
        node = TextNode("This is a Text Node with no Link", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](www.google.com) and a [second link](netflix.com)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "www.google.com"),
                TextNode(" and a ", text_type_text),
                TextNode("second link", text_type_link, "netflix.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )
