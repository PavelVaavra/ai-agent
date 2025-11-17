import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from call_function import available_functions, call_function

def main():
    if len(sys.argv) < 2:
        sys.exit("You have to provide a prompt.")
    
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
    
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

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        if not response.function_calls and response.text != "":
            print(f"Final response:\n{response.text}")
            break

        for candidate in response.candidates:
            messages.append(candidate.content)
 
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            messages.append(types.Content(role="user", parts=[types.Part(function_response=function_call_result.parts[0].function_response)]))
            if verbose:
                try:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                except:
                    raise("No function_call_result.parts[0].function_response.response available")

    if verbose: 
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
