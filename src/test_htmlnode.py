import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_node(self):
        node = HTMLNode("a", "A Link", None, {"href": "www.google.com", "target": "_blank"})
        props_to_html_return = node.props_to_html()
        expected_output = ' href="www.google.com" target="_blank"'
        self.assertEqual(props_to_html_return, expected_output)
    
    def test_to_html_renders(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node.to_html(), '<p>This is a paragraph of text.</p>')
        leaf_node_2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node_2.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_to_html(self):
         node = LeafNode(None, 'Just a String')
         self.assertEqual(node.to_html(), 'Just a String')
    
    def test_to_html_children(self):
        child_node = LeafNode("p", "child node")
        node = ParentNode("div", [child_node])
        self.assertEqual(node.to_html(), "<div><p>child node</p></div>")

    def test_to_html_grandchildren(self):
        grandchild_node = LeafNode("b", "bold node")
        child_node = ParentNode("p", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><p><b>bold node</b></p></div>")

    def test_to_html_many_children(self):
        children = ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode("a", "link", {"href": "https://www.google.com"}),
            LeafNode(None, "no tag")
        ])
        self.assertEqual(
            children.to_html(), 
                '<p><b>bold</b><a href="https://www.google.com">link</a>no tag</p>'
            )

        


if __name__ == '__main__':
    unittest.main()
