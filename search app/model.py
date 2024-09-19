import os
import json
import requests
import ollama
# from transformers import pipeline


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
                "content": f" Include as much details as possible. Provide all relevant important content for the question: {user_ask[0]}, using the help doc content and answer from conversation history, if relevant: {prompt}."

            }
        ]
    })
    response1 = requests.request("POST", endpoint, headers=headers, data=summary_content)
    result1 = response1.json()
    generated_text = result1['choices'][0]['message']['content']
    return generated_text


def query_llama_3_1(user_ask: str, prompt: str):
    print("Local llama called")
    response = ollama.chat(
        model="llama3.1",  # Specify the model you want to use
        messages=[{
            'role': 'user',
            "content": f" Include as much details as possible. Provide all relevant important content for the question: {user_ask[0]}, using the help doc content and conversation history: {prompt}"
        }]
    )
    llama_output = response['message']['content']
    return llama_output


def query_distill_bert(user_ask: str, prompt: str):
    # Load a pre-trained DistilBERT model fine-tuned on SQuAD for QA
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    # Get the answer
    result = qa_pipeline(question=user_ask[0], context=prompt)
    response = result['answer']
    print(response)
    return response
