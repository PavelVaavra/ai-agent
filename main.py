import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt, available_functions, call_function

def main():
    if len(sys.argv) < 2:
        sys.exit("You have to provide a prompt.")
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    user_prompt = " ".join(args)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    
    if not response.function_calls:
        print(response.text)

    # Back where you handle the response from the model generate_content, instead of simply printing the name of the function the LLM decides to call, 
    # use call_function.
    # The types.Content that we return from call_function should have a .parts[0].function_response.response within.
    # If it doesn't, raise a fatal exception of some sort.
    # If it does, and verbose was set, print the result of the function call like this:
    # print(f"-> {function_call_result.parts[0].function_response.response}")    
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, True)
        if "--verbose" in sys.argv:
            try:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            except:
                raise("No function_call_result.parts[0].function_response.response available")

    if "--verbose" in sys.argv: 
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
