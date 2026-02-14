import os 
import os.path
from google.genai import types
MAXCHARS = 10000


def get_file_content(working_directory,file_path ):
    try:

        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        allowed = os.path.commonpath([abs_path, target_file]) == abs_path
        if not allowed:
            return  f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, 'r') as file:
            content = file.read(MAXCHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAXCHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content= types.FunctionDeclaration(
    name="get_file_content",
    description="Get the text content of a specified file",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read",
            ),
        },
    ),
)