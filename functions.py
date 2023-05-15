
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymongo
import sys
import numpy as np
import json

client = pymongo.MongoClient("mongodb+srv://Vrsa:h9CDGt9WhLQOTIHs@moviecluster0.xwgrydc.mongodb.net/?retryWrites=true&w=majority")
db = client["movies_database"]
collection = db["movies"] 


def load_movies_from_database():
    movies = []
    for movie in collection.find():
        movies.append(movie)
    movies = pd.DataFrame(movies)
    
    #  Make missing values an empty string
    movies['Genre'] = movies['genre'].fillna('')
    movies['Description'] = movies['description'].fillna('')
    
    # Genre columns from list to string
    movies['Genre'] = movies['Genre'].apply(lambda x: ' '.join(x))
    
    return movies

def compute():
    movies = load_movies_from_database()

    # tf vektorizacija koja izbacuje engleske rijeci i gleda parove rijeci
    tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), use_idf=True, smooth_idf=True, norm=None, binary=False, sublinear_tf=False, max_features=5000)


    # Compute TF-IDF scores for genres and descriptions
    # Stvori vrijednosti za znarove i opise
    tfidf_matrix_genre = tfidf.fit_transform(movies['Genre'].values)
    tfidf_matrix_desc = tfidf.transform(movies['Description'].values)

    #Spajanje dvije matrice s različitim težinama jer je zanr bitniji od opisa
 
    #tfidf_matrix = 0.8 * tfidf_matrix_genre + 0.2 * tfidf_matrix_desc

    # iz racun cosine similartya za oba
    cosine_sim_genre = cosine_similarity(tfidf_matrix_genre, tfidf_matrix_genre)
    cosine_sim_desc = cosine_similarity(tfidf_matrix_desc, tfidf_matrix_desc)

    return  cosine_sim_genre, cosine_sim_desc



def store_matrices( cosine_sim_genre, cosine_sim_desc):

    collection = db["matrices"] 
    collection.delete_many({})


   # matrix_document = {"name": "tfidf_matrix", "matrix": matrix.toarray().tolist()}
    #matrix_desc_document = {"name": "tfidf_matrix_description", "matrix": matrix_desc.toarray().tolist()}
    cosine_sim_genre_document = {"name": "cosine_similarity_genre", "matrix": cosine_sim_genre.tolist()}
    cosine_sim_desc_document = {"name": "cosine_similarity_description", "matrix": cosine_sim_desc.tolist()}

    #collection.insert_one(matrix_document)
   # collection.insert_one(matrix_desc_document)
    collection.insert_one(cosine_sim_genre_document)
    collection.insert_one(cosine_sim_desc_document)




def store_matrices_locally(cosine_sim_genre, cosine_sim_desc):
    # Store the matrices in local files
    """ with open('matrix.json', 'w') as f:
        json.dump(matrix.toarray().tolist(), f)
    with open('matrix_desc.json', 'w') as f:
        json.dump(matrix_desc.toarray().tolist(), f)
        """
    with open('cosine_similarity_genre.json', 'w') as f:
        json.dump(cosine_sim_genre.tolist(), f)
    with open('cosine_sim_desc.json', 'w') as f:
        json.dump(cosine_sim_desc.tolist(), f)




def load_matrices_from_database():
    client = pymongo.MongoClient("mongodb+srv://Vrsa:h9CDGt9WhLQOTIHs@moviecluster0.xwgrydc.mongodb.net/?retryWrites=true&w=majority")
    db = client["movies_database"]
    collection = db["matrices"]

   # matrix = collection.find_one({"name": "tfidf_matrix"})["matrix"]
   # matrix_desc = collection.find_one({"name": "tfidf_matrix_description"})["matrix"]
    cosine_sim_genre = collection.find_one({"name": "cosine_similarity_genre"})["matrix"]
    cosine_sim_desc = collection.find_one({"name": "cosine_similarity_description"})["matrix"]

    return cosine_sim_genre, cosine_sim_desc



def load_matrices_from_local():
    try:
        with open('cosine_similarity_genre.json', 'r') as f:
            cosine_sim_genre = np.array(json.load(f))
        with open('cosine_sim_desc.json', 'r') as f:
            cosine_sim_desc = np.array(json.load(f))
        return cosine_sim_genre, cosine_sim_desc
    except FileNotFoundError:
        print("Missing cosine sim matrix!")
        print("To fix run compute_matrix.py!")
        sys.exit()


    """
    with open('matrix.json', 'r') as f:
        tfidf_matrix = np.array(json.load(f))
    with open('matrix_desc.json', 'r') as f:
        tfidf_matrix_desc = np.array(json.load(f))
    """
    




def get_recommendations(movies, cosine_sim_genre, cosine_sim_desc, title, start_index):
    #Ponadi index trazengo filma 
    idx = movies[movies['title'] == title].index[0]
    # Pronaci similarty rating sa tim filmom naspram ostalih
    sim_scores_genre = list(enumerate(cosine_sim_genre[idx]))
    sim_scores_desc = list(enumerate(cosine_sim_desc[idx]))
    
    sim_scores = [(i, 0.7 * sim_scores_genre[i][1] + 0.3 * sim_scores_desc[i][1]) for i in range(len(sim_scores_genre))]
    sim_scores = sorted(sim_scores, key=lambda x: (x[1], x[1] * movies.loc[x[0], 'rating']), reverse=True)

    sim_scores = [(i, score) for (i, score) in sim_scores if i != idx]
    movie_indices = [i[0] for i in sim_scores[start_index:start_index+5]]


    return movies[['title', 'genre', 'rating']].iloc[movie_indices]
 

def print_recommended_movies(title, start_index, movies, cosine_sim_genre, cosine_sim_desc):
    if title in movies['title'].values:
        recommendations = get_recommendations(movies, cosine_sim_genre, cosine_sim_desc, title, start_index)
        print("Recommended movies:")
        for i, movie in enumerate(recommendations.iterrows(), start_index):
            print(f"{i+1}. {movie[1]['title']} - {movie[1]['genre']} - {movie[1]['rating']}")
    else:
        print("Movie not found in dataset")
        sys.exit()



