import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        file_dirs = os.path.split(abs_file)[0]
        if not os.path.exists(file_dirs):
            os.makedirs(file_dirs)
        
        with open(abs_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'