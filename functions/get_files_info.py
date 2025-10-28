import os

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    
    try:
        retString = ""
        for element in os.listdir(abs_directory):
            path = os.path.join(abs_directory, element)
            retString += f" - {element}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n"
        return retString
    except Exception as e:
        return f'Error: {e}'