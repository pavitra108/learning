import ollama

# Query the model
response = ollama.chat(
    model="llama3.1",  # Specify the model you want to use
    messages=[{
        'role': 'user',
        'content': 'why is sky blue'
    }]
)

# Print the response
print("Response from Ollama:")
print(response['message']['content'])
