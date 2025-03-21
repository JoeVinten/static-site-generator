import os
import pathlib
from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as open_from_path:
        md_file = open_from_path.read()
        converted_html = markdown_to_html_node(md_file).to_html()
        title = extract_title(md_file)

    with open(template_path) as open_template:
        read_template = open_template.read()

    processed_template = (
        read_template.replace("{{ Title }}", title)
        .replace("{{ Content }}", converted_html)
        .replace('href="/', 'href="' + basepath)
        .replace('src="/', 'src="' + basepath)
    )

    if not os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as output_file:
        output_file.write(processed_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    os.makedirs(dest_dir_path, exist_ok=True)

    for item in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, item)

        if os.path.isfile(current_path):
            new_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(current_path, template_path, new_path, basepath)
        else:
            new_path = os.path.join(dest_dir_path, item)

            generate_pages_recursive(
                current_path, template_path, pathlib.Path(new_path), basepath
            )
