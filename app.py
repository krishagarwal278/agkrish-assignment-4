from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')

app = Flask(__name__)

# Fetch the dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data

# Initialize the vectorizer and fit on the dataset
vectorizer = TfidfVectorizer(max_df=0.5, max_features=1000, stop_words=stop_words)
term_doc_matrix = vectorizer.fit_transform(documents)

# Apply SVD to reduce dimensionality
svd_model = TruncatedSVD(n_components=100)
lsa_matrix = svd_model.fit_transform(term_doc_matrix)

# Cosine similarity calculation
def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # Transform the query into the TF-IDF space
    query_vec = vectorizer.transform([query])
    
    # Project the query vector into the LSA space
    query_lsa = svd_model.transform(query_vec)
    
    # Compute cosine similarities between the query and all documents
    similarities = cosine_similarity(query_lsa, lsa_matrix).flatten()
    
    # Get top 5 similar documents
    top_indices = similarities.argsort()[-5:][::-1]
    top_similarities = similarities[top_indices]
    top_documents = [documents[i] for i in top_indices]
    
    return top_documents, top_similarities, top_indices

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    # Return the documents, similarities, and indices for chart
    return jsonify({'documents': documents, 'similarities': similarities.tolist(), 'indices': indices.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
