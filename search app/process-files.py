from bs4 import BeautifulSoup
import os
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

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
X = vectorizer.fit_transform(flattened_documents)

# Get the feature names (words)
feature_names = vectorizer.get_feature_names_out()

# Print the matrix of token counts
print("Matrix of token counts:")
print(X.toarray())

# Print the feature names
print("Feature names (words):")
print(feature_names)

# Process and tokenize the user query
user_ask = "what are page layouts in zoho crm and how to create"
process_ask = preprocess_text(user_ask)
print(process_ask)
token_ask = tokenize_text(process_ask)
print(token_ask)

# Vectorize the tokenized output
vectorizer_two = TfidfVectorizer()

# Fit and transform the query
Y = vectorizer_two.fit_transform(token_ask)
names = vectorizer_two.get_feature_names_out()

# Print the matrix of token counts
print("Matrix of user query token counts:")
print(Y.toarray())

# Print the feature names
print("User query feature names (words):")
print(names)