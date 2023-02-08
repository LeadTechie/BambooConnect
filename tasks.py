import os
import subprocess

def lint_project():
    # Get a list of all .py files in the project
    py_files = [f for f in os.listdir() if f.endswith('.py')]

    # Lint each file using flake8
    for file in py_files:
        result = subprocess.run(["flake8", file], capture_output=True, text=True)

        # Print the linting results
        print(f"Linting results for {file}:")
        print(result.stdout)

if __name__ == "__main__":
    lint_project()
