import os
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download data pendukung NLTK (Hanya jalan satu kali)
nltk.download('stopwords')
nltk.download('punkt')

# Inisialisasi Porter Stemmer dan Stopwords Bahasa Inggris
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    """
    Fitur Wajib 1: Text Preprocessing
    Melakukan Case Folding, Cleaning, Stopword Removal, dan Stemming (Bahasa Inggris).
    """
    # 1. Case Folding (Kecilkan huruf)
    text = str(text).lower()
    # 2. Cleaning (Hapus karakter non-huruf/angka)
    text = re.sub(r'[^a-z\s]', '', text)
    # 3. Tokenization & Stopword Removal & Stemming
    words = text.split()
    cleaned = [stemmer.stem(w) for w in words if w not in stop_words]
    
    return " ".join(cleaned)

def load_documents(folder_path):
    """Membaca 30 file .txt yang sudah dibuat dari dataset Enron."""
    docs = []
    if not os.path.exists(folder_path):
        return pd.DataFrame()
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # Metadata sederhana: pisahkan Perihal dan Isi
                lines = content.split('\n\n', 1)
                subject = lines[0].replace("PERIHAL: ", "")
                body = lines[1] if len(lines) > 1 else ""
                
                docs.append({
                    'filename': filename,
                    'subject': subject,
                    'content': body,
                    'processed_content': preprocess(subject + " " + body)
                })
    return pd.DataFrame(docs)

def search_engine(query, df):
    """
    Fitur Wajib 3 & 4: Model IR & Ranking
    Menggunakan TF-IDF dan Cosine Similarity.
    """
    if df.empty: return df
    
    q_cleaned = preprocess(query)
    vectorizer = TfidfVectorizer()
    
    # Menghitung TF-IDF Matrix
    tfidf_matrix = vectorizer.fit_transform(df['processed_content'])
    query_vec = vectorizer.transform([q_cleaned])
    
    # Menghitung Cosine Similarity (Ranking)
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    df['score'] = scores
    
    return df[df['score'] > 0].sort_values(by='score', ascending=False)

def get_summary(text, limit=2):
    """
    Fitur Wajib 6: Extractive Summarization
    Mengambil 2 kalimat awal sebagai ringkasan.
    """
    sentences = nltk.sent_tokenize(text)
    summary = " ".join(sentences[:limit]).strip()
    return summary + "..." if summary else "No summary available."