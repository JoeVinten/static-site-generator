import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_unequal(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_unequal_url(self):
        node = TextNode("This is a text node", "bold", "www.joevinten.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_equal_url(self):
        node = TextNode("This is a text node", "bold", "www.joevinten.com")
        node2 = TextNode("This is a text node", "bold", "www.joevinten.com")
        self.assertEqual(node, node2)

    def test_unequal_text(self):
        node = TextNode("This is a paragraph", "bold", "www.joevinten.com")
        node2 = TextNode("This is a text node", "bold", "www.joevinten.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
