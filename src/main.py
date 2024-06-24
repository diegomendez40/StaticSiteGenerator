import os
import shutil
from textnode import TextNode
from mdblock import generate_pages_recursive

def copy_dir(source_dir, target_dir):
    if os.path.exists(source_dir) and os.path.exists(target_dir):
        for entry in os.listdir(source_dir):
            new_source = os.path.join(source_dir, entry)
            if os.path.isfile(new_source):
                new_target = target_dir
                shutil.copy(new_source, new_target)
            else:
                new_target = os.path.join(target_dir, entry)
                os.mkdir(new_target)
                copy_dir(new_source, new_target)       
                print(f"Copying file: {new_source}")
    else:
        raise Exception('Directory does not exist')

def main():
    source_dir = "static"
    target_dir = "public"
    # TODO: Añadir: si existe
    # We clean up the directory so test can make sense
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    print(f"Created folder: {target_dir}")
    copy_dir(source_dir, target_dir)
    # Recursive generation of html pages
    generate_pages_recursive("content", "template.html", "public")

main()
