import os
import os.path
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        allowed = os.path.commonpath([abs_path, target_file]) == abs_path

        if not allowed:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        if not os.path.isdir(os.path.dirname(target_file)):
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"



schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file",
    parameters=types.Schema(
        required=["file_path","content"],
        type=types.Type.OBJECT,
        properties={

            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file.",
            ),
        },
    ),
)