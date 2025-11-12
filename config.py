from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

# MAX_CHARS = 10000

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Create a new function that will handle the abstract task of calling one of our four functions. This is my definition:
# def call_function(function_call_part, verbose=False):

# function_call_part is a types.FunctionCall that most importantly has:

# A .name property (the name of the function, a string)
# A .args property (a dictionary of named arguments to the function)
# If verbose is specified, print the function name and args:

# print(f"Calling function: {function_call_part.name}({function_call_part.args})")

# Otherwise, just print the name:

# print(f" - Calling function: {function_call_part.name}")

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    functions = {}
    functions["get_file_content"] = get_file_content
    functions["get_files_info"] = get_files_info
    functions["run_python_file"] = run_python_file
    functions["write_file"] = write_file

    try:
        function_result = functions[function_name](**{**args, "working_directory": "./calculator"})
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
