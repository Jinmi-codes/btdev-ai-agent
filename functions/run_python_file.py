import os
import os.path
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:

        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        allowed = os.path.commonpath([abs_path, target_file]) == abs_path

        if not allowed:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ['python', target_file]
        if args:
            command.extend(args)

        process = subprocess.run(command, text=True, capture_output=True, timeout=30)
        output = ''
        if process.returncode != 0:
            output += "Process exited with code X"
        if not (process.stderr or process.stdout):
            output += "No output produced"

        output += f"STDOUT: {process.stdout} \nSTDERR: {process.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file= types.FunctionDeclaration(
    name="run_python_file",
    description="Run specified python file.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={

            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of optional arguments",
                items=types.Schema(
                    type=types.Type.STRING,
    ),
),
        },
    ),
)