import os
import requests
from dotenv import load_dotenv
from langchain_core.language_models import BaseLLM

# Load environment variables
load_dotenv()

class ApiLLM(BaseLLM):
    api_url: str
    api_key: str

    def __init__(self, api_url: str, api_key: str):
        """Initialize the ApiLLM class with the API URL and API key."""
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key

    def _call(self, prompt: str, stop=None, run_manager=None, **kwargs):
        """Make an API call to get the LLM's response for a given prompt."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "max_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.4,
        }
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['text']
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM used."""
        return "custom_api"

# Define the system prompt (you can customize this)
system_prompt = "You are an AI assistant that provides concise and accurate answers."

def chat_completion(question: str, llm: ApiLLM):
    """Get a completion from the LLM based on a user's question."""
    try:
        prompt = f"{system_prompt}\nQuestion: {question}"
        response = llm(prompt)
        return response.strip()
    except Exception as e:
        return f"An error occurred while processing the request: {e}"
