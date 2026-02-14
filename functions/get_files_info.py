import os.path
import os
from google.genai import types
def get_files_info(working_directory, directory='.'):
	try:
		abs_path = os.path.abspath(working_directory)
		target_dir = os.path.normpath(os.path.join(abs_path, directory))
		allowed_target = os.path.commonpath([abs_path, target_dir]) == abs_path 
		if not allowed_target:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(target_dir):
			return f'Error: "{directory}" is not a directory'

		dir_list = os.listdir(target_dir)
		full_data = []
		for item in dir_list:
			name = item
			file_size = os.path.getsize(os.path.join(target_dir, item))
			is_dir = True
			if not os.path.isdir(os.path.join(target_dir, item)):
				is_dir = False
			data = f"- {name}: file_size={file_size} bytes, is_dir={"True" if is_dir else "False"}"
			full_data.append(data)
		info = "\n".join(full_data)
		return info
	except Exception as e:
		return f"Error: {e}"


print(get_files_info("../../", "ai-agent"))


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)