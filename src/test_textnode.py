import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_types_unequal(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_text_unequal(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a boldest node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a image node", TextType.IMAGE, 'www.google.com')
        node2 = TextNode("This is a image node", TextType.IMAGE, 'www.google.com')
        self.assertEqual(node, node2)
        
    def test_url_do_not_match(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is a code node", TextType.CODE, 'www.google.com')
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node =TextNode("This is a text node", TextType.TEXT, 'www.google.com')
        self.assertEqual(
			"TextNode(This is a text node, text, www.google.com)", repr(node)
		)

if __name__ == '__main__':
    unittest.main()
