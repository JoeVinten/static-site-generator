import os
from block_to_html import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"⚙️ Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown_contents = file.read()
    with open(template_path, "r") as file:
        template_contents = file.read()

    title = extract_title(markdown_contents)
    content = markdown_to_html_node(markdown_contents).to_html()

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", content)

    dest_dir_path = os.path.dirname(dest_path)

    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as html:
        html.write(template_contents)
