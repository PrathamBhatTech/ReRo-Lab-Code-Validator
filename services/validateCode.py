import ast
import yaml

with open('../config/config.yaml', 'r') as yaml_file:
    config_data = yaml.safe_load(yaml_file)

allowed_libraries = config_data['allowed_libraries']


def extract_imports(node):
    imports = set()
    for item in node.body:
        if isinstance(item, ast.Import):
            for alias in item.names:
                imports.add(alias.name)
        elif isinstance(item, ast.ImportFrom):
            if item.module:
                imports.add(item.module)
    return imports


def check_allowed_libraries(code):
    try:
        parsed = ast.parse(code)
        imported_libraries = extract_imports(parsed)

        for lib in imported_libraries:
            if lib not in allowed_libraries:
                return False, lib
        return True, None
    except SyntaxError:
        return False, "SyntaxError"


def validate_code(file_path):
    # Read the Python code from a file
    with open(file_path, "r") as file:
        code_content = file.read()

    # Check if the code uses only allowed libraries
    is_allowed, disallowed_lib = check_allowed_libraries(code_content)

    if is_allowed:
        print("The code uses only allowed libraries.")
    else:
        print(f"The code uses a disallowed library: {disallowed_lib}")
