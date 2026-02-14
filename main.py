import os 
import sys
from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from argparse import ArgumentParser
from prompts import system_prompt
#initialize argument parser class
arg_parser = ArgumentParser()
arg_parser.add_argument('user_prompt', help="Request string")
arg_parser.add_argument('-v', '--verbose', help="Show more content!", action="store_true")
arguments = arg_parser.parse_args()

load_dotenv()

if os.environ.get("GEMINI_API_KEY"):
    api_key = os.environ.get("GEMINI_API_KEY")
else:
    raise RuntimeError("Api key not found!")

client = genai.Client(api_key=api_key)

messages = [types.Content(role="user", parts=[types.Part(text=arguments.user_prompt)])]
function_call_results = []
while True:
    for num in range(20):
        print("About to call Gemini...")
        content = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
        
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0,),
        )

        

        print("Got response, about to print results...")
        if not content.usage_metadata:
            raise RuntimeError("Oops! API call failed!")
        if content.candidates:
            for prop in content.candidates:
                messages.append(prop.content)
        if arguments.verbose:
            print(f"User prompt: {arguments.user_prompt}")
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")

        if not content.function_calls:
            print(f"Response: {content.text}")
            sys.exit(0)
        else:
            if num == 19:
                print(f"Something went wrong, unable to complete task.")
                sys.exit(1)
            for function_call in content.function_calls:
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception("Oops! Function contnets not found!")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Oops! Function result not found.")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Oops! Function result not found.")
                function_call_results.append(function_call_result.parts[0])
                messages.append(types.Content(role="tool", parts=[function_call_result.parts[0]]))
                
                if arguments.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")




