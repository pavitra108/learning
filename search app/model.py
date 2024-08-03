import os
import json
import requests


def query_chat_gpt(user_ask: str, prompt: str) -> str:
    api_key = os.getenv('API_KEY')
    endpoint = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }

    summary_content = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f" Include as much details as possible. Provide all relevant important content for the question: {user_ask[0]}, using the help doc content and conversation history: {prompt}"

            }
        ]
    })
    response1 = requests.request("POST", endpoint, headers=headers, data=summary_content)
    result1 = response1.json()
    generated_text = result1['choices'][0]['message']['content']
    return generated_text
