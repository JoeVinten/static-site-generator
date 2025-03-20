import unittest

from blocks_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestInlineMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
	"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_lines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
	"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = """
        This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line      

- This is a list
- with items
	"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        md_heading = "## This is a heading"

        self.assertEqual(BlockType.HEADING, block_to_block_type(md_heading))

    def test_block_to_block_type_invalid_heading(self):
        md_not_heading = "this is ## not a heading"

        self.assertNotEqual(BlockType.HEADING, block_to_block_type(md_not_heading))

    def test_block_to_block_type_code(self):
        md_code = "```<code></code>```"

        self.assertEqual(BlockType.CODE, block_to_block_type(md_code))

    def test_block_to_block_type_quote(self):
        md = ">this is a quote\n>this is another line of said quote"

        self.assertEqual(BlockType.QUOTE, block_to_block_type(md))

    def test_block_to_block_type_not_quote(self):
        md = ">this is a quote\n- this is another line of said quote"

        self.assertNotEqual(BlockType.QUOTE, block_to_block_type(md))

    def test_block_to_block_type_unordered_list(self):
        md = "- this is a unordered list\n- this is another line of said unordered list"

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(md))

    def test_block_to_block_type_unordered_not_list(self):
        md = "- this is a not unordered list\nthis is another line of said not unordered list"

        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_block_type(md))

    def test_block_to_block_type_ordered_list(self):
        md = "1. this is a ordered list\n2. this is another line of said ordered list"

        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(md))

    def test_block_to_block_type_not_incremental_ordered_list(self):
        md = "1. this is a not ordered list\n3. this is another line of said not ordered list"

        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(md))

    def test_block_to_block_type_not_ordered_list(self):
        md = "1. this is a not ordered list\n- this is another line of said not ordered list"

        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(md))

    def test_block_to_block_type_paragraph(self):
        md = "A normal paragraph block"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
