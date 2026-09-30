import json

from src.configs.groq_client import get_groq_client
from src.configs.prompts import TEXT_PROCESSING_SYSTEM_PROMPT


client = get_groq_client()


def process_text(
    raw_title: str,
    raw_description: str
):
    user_prompt = f"""
Raw Title:
{raw_title}

Raw Description:
{raw_description}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": TEXT_PROCESSING_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    result = json.loads(
        response.choices[0].message.content
    )

    # need_clarification must always be boolean
    result["need_clarification"] = bool(
        result.get("need_clarification", False)
    )

    return result