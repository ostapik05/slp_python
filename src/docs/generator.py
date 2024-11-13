"""
Module for generating documentation for Python files in a given directory.
The documentation is generated using pydoc.
"""

import os
import subprocess

from config.settings_paths import current_dir


def generate_docs(directory):
    """
    :param directory: The base directory from which to gather .py files and generate documentation.
    :return: None. Generates documentation files.
    """
    # Get the absolute path of the directory containing your codebase
    directory = os.path.abspath(os.path.join(directory, ".."))

    for root, dirs, files in os.walk(directory):
        # Ignore directories starting with a dot (e.g., .git, .vscode)
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.endswith(".py"):
                # Get the relative path from the base directory
                relative_path = os.path.relpath(os.path.join(root, file), directory)

                # Replace OS-specific path separators with dots and remove the .py extension
                module_name = os.path.splitext(relative_path)[0].replace(os.sep, ".")

                # Exclude __init__ files if you don't want docs for them
                if module_name.endswith(".__init__"):
                    continue

                print(f"Generating docs for: {module_name}")

                # Call pydoc to generate documentation
                subprocess.run(["python", "-m", "pydoc", "-w", module_name], check=True)


if __name__ == "__main__":
    generate_docs(current_dir)
