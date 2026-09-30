import os

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()


def get_mistral_client() -> Mistral:
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not configured")

    return Mistral(api_key=api_key)