import os

# os.path.abspath(): Get an absolute path from a relative path
# os.path.join(): Join two paths together safely (handles slashes)
# .startswith(): Check if a string starts with a substring
# os.path.isdir(): Check if a path is a directory
# os.listdir(): List the contents of a directory
# os.path.getsize(): Get the size of a file
# os.path.isfile(): Check if a path is a file
# .join(): Join a list of strings together with a separator

# The directory parameter should be treated as a relative path within the working_directory. Use os.path.join(working_directory, directory) 
# to create the full path, then validate it stays within the working directory boundaries.
def get_files_info(working_directory, directory="."):
    if not os.path.isdir(working_directory):
        return f'Error: "{working_directory}" is not a directory'
    
    path = os.path.join(working_directory, directory)
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    
    retString = ""
    if directory not in os.listdir(working_directory) and \
        directory != ".":
        retString = f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    else:
        directory_content = os.listdir(path)
        for element in directory_content:
            path = os.path.join(working_directory, directory, element)
            retString += f" - {element}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n"
    
    directory = "current" if directory == "." else f"'{directory}'"
    return f"""Result for {directory} directory:
{retString}"""