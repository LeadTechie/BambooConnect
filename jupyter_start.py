import os

def get_py_files(root_dir):
    py_files = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(subdir, file))
    return py_files

def print_file_list(file_list):
    for i, file_path in enumerate(file_list):
        print(f"{i+1}. {file_path}")

if __name__ == '__main__':
    root_dir = input("Enter root directory to search for Python files: ")
    py_files = get_py_files(root_dir)
    print(f"Found {len(py_files)} Python files:")
    print_file_list(py_files)
    file_numbers = input("Enter numbers of files to edit (separated by spaces): ")
    selected_files = [py_files[int(num)-1] for num in file_numbers.split()]
    for file_path in selected_files:
        os.system(f"jupytext --to notebook {file_path}")
        os.system(f"jupytext --set-formats ipynb,py {os.path.splitext(file_path)[0]}.ipynb")
        os.system(f"jupytext --sync {os.path.splitext(file_path)[0]}.ipynb")
    os.system("jupyter notebook")
