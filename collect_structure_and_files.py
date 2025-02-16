import os
import json
from gitignore_parser import parse_gitignore

def collect_directory_structure_and_files(base_path='.'):
    file_structure = {}
    
    # Parse .gitignore file if it exists
    gitignore_file = os.path.join(base_path, '.gitignore')
    if os.path.exists(gitignore_file):
        is_ignored = parse_gitignore(gitignore_file)
    else:
        is_ignored = lambda path: False  # No gitignore file, don't ignore anything

    # Walk through all directories and files starting from base_path
    for root, dirs, files in os.walk(base_path):
        # Skip files that match .gitignore
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d))]
        files = [f for f in files if not is_ignored(os.path.join(root, f))]
        
        # Get the relative path
        relative_root = os.path.relpath(root, base_path)
        
        if relative_root == '.':
            relative_root = ''
        
        # Store the directory and file structure
        file_structure[relative_root] = {
            'directories': dirs,
            'files': {}
        }
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip non-code files or files that can't be read
            if file.endswith(('.py', '.txt', '.md', '.json', '.yml', '.yaml')):  # Add more extensions as needed
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_structure[relative_root]['files'][file] = f.read()
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    
    return file_structure

def save_directory_structure_and_files(file_structure, output_filename="directory_structure_with_files.json"):
    # Save the directory structure and file contents to a JSON file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(file_structure, f, ensure_ascii=False, indent=4)
    print(f"Directory structure and file contents saved to {output_filename}")

if __name__ == "__main__":
    base_path = '.'  # Current directory
    structure_with_files = collect_directory_structure_and_files(base_path)
    save_directory_structure_and_files(structure_with_files)