import os
import requests
from dotenv import load_dotenv
import json

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Resolve absolute paths for .env.local and .env
env_local_path = os.path.join(BASE_DIR, '.env.local')
env_path = os.path.join(BASE_DIR, '.env')

# Load environment variables
if os.path.exists(env_local_path):
    load_dotenv(dotenv_path=env_local_path, override=True)
    print("✅ Loaded environment variables from .env.local")
else:
    load_dotenv(dotenv_path=env_path, override=True)
    print("✅ Loaded environment variables from .env")

class AIProvider:
    def __init__(self):
        self.openai_token = os.getenv("AI_OPENAI_API_TOKEN")
        self.deepseek_token = os.getenv("AI_DEEPSEEK_API_TOKEN")

    def generate_content(self, prompt, provider):
        print(f"Generating content using provider: {provider}")
        if provider == 'openai':
            return self.generate_with_openai(prompt)
        elif provider == 'deepseek':
            return self.generate_with_deepseek(prompt)
        else:
            return {'title': 'Untitled', 'content': ''}

    def generate_with_openai(self, prompt):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.openai_token}',
            'Content-Type': 'application/json'
        }
        
        # Function schema for structured output
        function_schema = {
            "name": "generate_blog_post",
            "description": "Generate a structured blog post with a title and content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the blog post"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content of the blog post"
                    }
                },
                "required": ["title", "content"]
            }
        }

        # Request body using function calling
        data = {
            'model': 'gpt-3.5-turbo',  
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that generates structured blog posts with titles and content.'
                },
                {
                    'role': 'user',
                    'content': f"Generate a concise blog post based on this prompt: '{prompt}'. Keep the response within 1000 tokens."

                }
            ],
            'tools': [
                {
                    "type": "function",
                    "function": function_schema
                }
            ],
            'tool_choice': {
                "type": "function",
                "function": {"name": "generate_blog_post"}
            },
            'max_tokens': 1000
        }

        response = requests.post(url, headers=headers, json=data)
        print(f"API Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"API Response: {json.dumps(result, indent=2)}")

            try:
                # Extracting function call arguments
                function_args = result['choices'][0]['message']['tool_calls'][0]['function']['arguments']
                structured_data = json.loads(function_args)
                return structured_data

            except (KeyError, json.JSONDecodeError) as e:
                print(f"⚠️ Failed to parse AI response: {e}")
                return {'title': prompt, 'content': ''}

        else:
            print(f"OpenAI API error {response.status_code}: {response.text}")
            return {'title': 'Untitled', 'content': ''}

    def generate_with_deepseek(self, prompt):
        url = 'https://api.deepseek.com/generate'
        headers = {'Authorization': f'Bearer {self.deepseek_token}'}
        data = {'prompt': f"Generate a blog post with a title and content based on: '{prompt}'. Format it as JSON."}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            ai_response = response.json().get('generated_content', '')
            try:
                structured_data = json.loads(ai_response)
                return structured_data
            except json.JSONDecodeError:
                return {'title': prompt, 'content': ai_response}
        else:
            print(f"DeepSeek API error {response.status_code}: {response.text}")
            return {'title': 'Untitled', 'content': ''}
