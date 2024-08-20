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


def get_flattened_html_docs(html_dir: str):
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

    # Convert dic values into list
    documents = list(tokenized_texts.values())

    # Create TfidfVectorizer object and flatten (convert to single string)
    flattened_documents = [' '.join(tokens) for tokens in documents]

    return flattened_documents, all_texts


def get_vectorized_output(input_str: str) -> str:
    vectorizer_output = vectorizer.transform([input_str])
    return vectorizer_output


def get_most_similar_docs_for_user_input(user_y, top_n=3):
    similarities = cosine_similarity(user_y, document_x)
    similarity_scores = similarities.flatten()
    non_zero_indices = np.nonzero(similarity_scores)[0]
    print(similarity_scores)
    # Convert similarity scores to percentages
    similarity_percentages = similarity_scores * 100
    num_non_zero = len(non_zero_indices)
    top_n = min(top_n, num_non_zero)

    # Create a list of tuples (document index, similarity percentage)

    doc_similarity_list = [(idx, percent) for idx, percent in
                           zip(non_zero_indices, similarity_percentages[non_zero_indices])]

    # Sort the list by similarity percentage in descending order
    doc_similarity_list = sorted(doc_similarity_list, key=lambda x: x[1], reverse=True)
    top_docs = doc_similarity_list[:top_n]
    for idx, percent in top_docs:
        print(f"Document {idx} has a similarity score of {percent:.2f}%")

    most_similar_indices = np.argsort(similarity_scores[non_zero_indices])[::-1][:top_n]
    most_similar_indices = non_zero_indices[most_similar_indices]

    # Get the filenames of the most similar documents
    most_similar_files = [list(all_texts.keys())[i] for i in most_similar_indices]

    return most_similar_files


def extract_top_n_file_content(most_similar_files: list, top_n=3):
    extracted_texts = []
    for file in most_similar_files[:top_n]:
        file_path = os.path.join(HTML_DIR, file)
        file_text = extract_text_from_html(file_path)
        extracted_texts.append(file_text)
    return extracted_texts


HTML_DIR = "C:\\Users\\mvisw\\Documents\\workspace\\airline guide"

# Create TfidfVectorizer object and flatten (convert to single string)
flattened_documents, all_texts = get_flattened_html_docs(HTML_DIR)
vectorizer = TfidfVectorizer()

# Fit and transform the documents
document_x = vectorizer.fit_transform(flattened_documents)

# Get the feature names (words)
feature_names = vectorizer.get_feature_names_out()
