import os 
import os.path
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