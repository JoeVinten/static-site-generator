import unittest

from block_to_html import (
    markdown_to_html_node,
)


class TestBlockToHtml(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_heading(self):
        md = """
## Heading *Node*

The above should be a heading node with italics
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading <i>Node</i></h2><p>The above should be a heading node with italics</p></div>",
        )

    def test_blocks(self):
        md = """
> This is a quote
> This is another part of the same block

```
def __init__(self, tag, children, props=None):
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote This is another part of the same block</blockquote><pre><code> def __init__(self, tag, children, props=None): </code></pre></div>",
        )

    def test_ol(self):
        md = """
* **This** is a bullet
* *This* is another bullet
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>This</b> is a bullet</li><li><i>This</i> is another bullet</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
