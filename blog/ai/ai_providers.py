import os
import requests
from dotenv import load_dotenv

import os
import requests
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Resolve absolute paths for .env.local and .env
env_local_path = os.path.join(BASE_DIR, '.env.local')
env_path = os.path.join(BASE_DIR, '.env')

# Debug: Print the resolved paths
print(f"Resolved .env.local path: {env_local_path}")
print(f"Resolved .env path: {env_path}")

# Clear cached environment variables
os.environ.pop('AI_OPENAI_API_TOKEN', None)
os.environ.pop('AI_DEEPSEEK_API_TOKEN', None)

# Load environment variables
if os.path.exists(env_local_path):
    load_dotenv(dotenv_path=env_local_path, override=True)
    print("✅ Loaded environment variables from .env.local")
else:
    load_dotenv(dotenv_path=env_path, override=True)
    print("✅ Loaded environment variables from .env")

# Debugging: Check if the variables are loaded correctly
print(f"OPENAI TOKEN: {os.getenv('AI_OPENAI_API_TOKEN')}")
print(f"DEEPSEEK TOKEN: {os.getenv('AI_DEEPSEEK_API_TOKEN')}")


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
            return None  # Invalid provider

    def generate_with_openai(self, prompt):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.openai_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-3.5-turbo',  # Using GPT-3.5 Turbo
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 150
        }

        response = requests.post(url, headers=headers, json=data)

        print(f"API Response Status: {response.status_code}")
        if response.status_code == 200:
            print(f"API Response: {response.json()}")
            result = response.json()
            print(f"Generated Content: {result['choices'][0]['message']['content'].strip()}")
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"OpenAI API error {response.status_code}: {response.text}")
            return None

    def generate_with_deepseek(self, prompt):
        url = 'https://api.deepseek.com/generate'
        headers = {'Authorization': f'Bearer {self.deepseek_token}'}
        data = {'prompt': prompt}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            generated_content = response.json().get('generated_content', '')
            print(f"Generated Content: {generated_content}")
            return generated_content
        else:
            print(f"DeepSeek API error {response.status_code}: {response.text}")
            return None
