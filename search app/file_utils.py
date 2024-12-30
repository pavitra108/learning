from bs4 import BeautifulSoup
import os
import string
import nltk
from sentence_transformers import SentenceTransformer, util
import re


# Download the Punkt tokenizer models and list of stopwords.
nltk.download('punkt')
nltk.download('stopwords')

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

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
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'<.*?>', ' ', text)
    return text


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

# Preprocess text and get Sentence-Bert embeddings
def encode_docs(html_dir: str):
    all_texts = extract_texts_from_directory(html_dir)

    if not all_texts:
        print("No texts were extracted.")
        return None, None
    else:
        print("Extracted texts from HTML files.")

def remove_repeated_content(text):
    # Define regex patterns to match the repetitive content
    patterns = [
        r"Skip To Main Content",
        r"Account\nSettings\nLogout",
        r"Filter:\n.*?\nSubmit Search",
        r"All Files"
        r"You are here:.*?\n",
        r"placeholder",

    ]

    # Iterate through patterns and remove each one from the text
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)

    # Optionally, remove multiple blank lines that may be left behind
    text = re.sub(r'\n\s*\n', '\n', text)  # Replace multiple newlines with a single newline

    return text.strip()  # Return cleaned text without leading/trailing whitespace

    # Preprocess and get embeddings for each document
    document_embeddings = {}
    for filename, text in all_texts.items():
        preprocessed_text = preprocess_text(text)
        document_embedding = model.encode(preprocessed_text, convert_to_tensor=True)
        print(f"Document embedding shape: {document_embedding.shape}")
        document_embeddings[filename] = document_embedding
    return document_embeddings, all_texts

def get_most_similar_docs_for_user_input(user_query, document_embeddings, top_n=3):
    user_embedding = user_query
    print(f"User query embedding shape: {user_embedding.shape}")
    similarities = {}
    for filename, doc_embedding in document_embeddings.items():
        print(f"Document embedding shape for {filename}: {doc_embedding.shape}")
        similarity = util.pytorch_cos_sim(user_embedding, doc_embedding).item()
        similarities[filename] = similarity

    # Sort documents by similarity score (in descending order)
    sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

    # Get the top N most similar documents
    most_similar_files = [filename for filename, similarity in sorted_similarities[:top_n]]
    return most_similar_files

def extract_top_n_file_content(most_similar_files: list, top_n=3):
    extracted_texts = []
    for file in most_similar_files[:top_n]:
        file_path = os.path.join(HTML_DIR, file)
        file_text = extract_text_from_html(file_path)
        extracted_texts.append(file_text)
    return extracted_texts


HTML_DIR = "C:\\Users\\mvisw\\Downloads\\help docs for testing"

#Extract and encode the HTML documents
document_embeddings, _ = encode_docs(HTML_DIR)


