import os
import shutil
import sys
from copy_static import copy_static
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"

markdown_dir_path = "./content/index.md"
template_path = "./template.html"
output_path = "./docs/index.html"


def main():
    print("Deleting public directory...")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_static(dir_path_static, dir_path_public)

    generate_pages_recursive("./content", template_path, dir_path_public, basepath)


main()
