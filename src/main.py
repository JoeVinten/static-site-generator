import os
import shutil
from copy_static import copy_static
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"

markdown_dir_path = "./content/index.md"
template_path = "./template.html"
output_path = "./public/index.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_static(dir_path_static, dir_path_public)

    generate_pages_recursive("./content", template_path, dir_path_public)


main()
