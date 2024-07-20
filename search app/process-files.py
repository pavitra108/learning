import requests
import json
from bs4 import BeautifulSoup
import os
import re
import string
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st



# Download the Punkt tokenizer models and list of stopwords.
nltk.download('punkt')
nltk.download('stopwords')

# Extract text from HTML pages
def extract_text_from_html(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator=' ')
            if text.strip() == '':
                print(f"Warning: No text found in {html_file}")
            return text
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return None

# Preprocess text - remove HTMl tags and punctuation and convert to lower case.
def preprocess_text(text):
        text = re.sub(r'<.*?>', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.lower()
        return text

# Tokenize text (into words) that is cleaned up using Punkt tokenizer. Additionally, remove stopwords.
def tokenize_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return tokens

# Read through files individually from a folder of HTML files
def extract_texts_from_directory(directory):
    all_texts = {}
    file_count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".html") or filename.endswith(".htm"):  # Check if the file is an HTML file
            file_path = os.path.join(directory, filename)
            text = extract_text_from_html(file_path)
            if text is not None:
                all_texts[filename] = text
            file_count += 1
            if file_count % 10 == 0:  # Print progress every 10 files
                print(f"Processed {file_count} files")
    return all_texts

# Tokenize the text
def preprocess_and_tokenize_all_files(all_texts):
    tokenized_texts = {}
    for filename, text in all_texts.items():
        preprocessed_text = preprocess_text(text)
        tokens = tokenize_text(preprocessed_text)
        tokenized_texts[filename] = tokens
    return tokenized_texts

html_dir = "C:\\Users\\mvisw\\Documents\\workspace\\zoho help"
all_texts = extract_texts_from_directory(html_dir)
tokenized_texts = preprocess_and_tokenize_all_files(all_texts)
if not all_texts:
    print("No texts were extracted.")
else:
    print("Extracted texts from HTML files.")

print(f"Processed and tokenized {len(tokenized_texts)} HTML documents.")
for filename, tokens in tokenized_texts.items():
    print(f"File: {filename}")
    print(f"First 10 tokens: {tokens[:10]}")

#Convert dic values into list
documents = list(tokenized_texts.values())

# Create TfidfVectorizer object and flatten (convert to single string)
flattened_documents = [' '.join(tokens) for tokens in documents]
vectorizer = TfidfVectorizer()

# Fit and transform the documents
document_x = vectorizer.fit_transform(flattened_documents)

# Get the feature names (words)
feature_names = vectorizer.get_feature_names_out()

# Print the feature names
print("Feature names (words):")
print(feature_names)

st.title("Content Search App")
# Process and tokenize the user query
user_ask = [st.text_input("Enter your query:")]
if st.button("Search and Summarize"):
    if user_ask:
        # Fit and transform the query
        user_y = vectorizer.transform(user_ask)
        names = vectorizer.get_feature_names_out()

        # Print the matrix of token counts
        print("Matrix of user query token counts:")
        print(user_y.toarray())

        # Print the feature names
        print("User query feature names (words):")
        print(names)

        similarities = cosine_similarity(user_y, document_x)
        similarity_scores = similarities.flatten()
        non_zero_indices = np.nonzero(similarity_scores)[0]

        # Get the indices of the top N most similar documents
        top_n = 3

        num_non_zero = len(non_zero_indices)
        top_n = min(top_n, num_non_zero)

        most_similar_indices = np.argsort(similarity_scores[non_zero_indices])[::-1][:top_n]
        most_similar_indices = non_zero_indices[most_similar_indices]

        # Debugging print statements
        print("non_zero_indices:", non_zero_indices)
        print("most_similar_indices:", most_similar_indices)
        print("Number of documents in all_texts:", len(all_texts))

        # Get the filenames of the most similar documents
        most_similar_files = [list(all_texts.keys())[i] for i in most_similar_indices]

        print("Most similar documents:")
        for filename in most_similar_files:
            print(filename)

        extracted_texts = []
        for file in most_similar_files[:3]:
            file_path = os.path.join(html_dir, file)
            file_text = extract_text_from_html(file_path)
            extracted_texts.append(file_text)

        final_text = "\n\n".join(extracted_texts)

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
                    "content": f"Provide relevant important content for the question: {user_ask[0]}, based on the help doc content here: {final_text}. Include as much details as possible."

                }
            ]
        })
        response1 = requests.request("POST", endpoint, headers=headers, data=summary_content)
        result1 = response1.json()
        generated_text1 = result1['choices'][0]['message']['content']
        print(generated_text1)
        # Display the results
        st.write(f"Most relevant document: {most_similar_files}")
        st.write("Summary:")
        st.write(generated_text1)
    else:
        st.write("Please enter a query.")