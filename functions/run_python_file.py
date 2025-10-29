import os
from subprocess import run

# Use the subprocess.run function to execute the Python file and get back a "completed_process" object. Make sure to:
# - Set a timeout of 30 seconds to prevent infinite execution
# - Capture both stdout and stderr
# - Set the working directory properly
# - Pass along the additional args if provided
def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'

    if os.path.split(abs_file)[-1].split(".")[-1] != "py":
        return f'Error: "{file_path}" is not a Python file.'
    
    # Return a string with the output formatted to include:
    # - The stdout prefixed with STDOUT:, and stderr prefixed with STDERR:. The "completed_process" object has a stdout and stderr attribute.
    # - If the process exits with a non-zero code, include "Process exited with code X"
    # - If no output is produced, return "No output produced."
    try:
        completed_process = run(["uv", "run", abs_file, *args], capture_output=True, timeout=30, text=True, cwd=abs_working_directory)
        
        ret_s = ""
        if completed_process.stdout:
            ret_s += f"STDOUT: {completed_process.stdout}\n"
        if completed_process.stderr:
            ret_s += f"STDERR: {completed_process.stderr}\n"
        if completed_process.returncode != 0:
            ret_s += f"Process exited with code {completed_process.returncode}\n"
        if ret_s == "":
            ret_s += "No output produced."
    
        return ret_s
    except Exception as e:
        return f"Error: executing Python file: {e}"