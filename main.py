import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from argparse import ArgumentParser

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

print("About to call Gemini...")
content = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)
print("Got response, about to print text...")
if not content.usage_metadata:
    raise RuntimeError("Oops! API call failed!")

if arguments.verbose:
    print(f"User prompt: {arguments.user_prompt}")
    print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
print(f"Response: {content.text}")



