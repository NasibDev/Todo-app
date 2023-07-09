from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

app = Flask(__name__)

# Load the trained model
model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    vectorizer = pickle.load(file)

movies_data = pd.read_csv('movies.csv')

selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

featured_vectors = vectorizer.transform(combined_features)
similar_feature = cosine_similarity(featured_vectors)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    movie_name_list = movies_data['title'].tolist()
    similar_movie_name = difflib.get_close_matches(movie_name, movie_name_list)
    exact_movie_name = similar_movie_name[0]
    movie_index = movies_data[movies_data.title == exact_movie_name]['index'].values[0]
    similarity_score = list(enumerate(similar_feature[movie_index]))
    similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:20]

    suggested_movies = []
    for movie in similar_movies:
        index = movie[0]
        title_of_the_movie = movies_data[movies_data.index == index]['title'].values[0]
        suggested_movies.append(title_of_the_movie)

    return render_template('result.html', movie=movie_name, suggestions=suggested_movies)

if __name__ == '__main__':
    app.run(debug=True)
