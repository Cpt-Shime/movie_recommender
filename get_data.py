import requests
import pymongo
import functions as recommender


# API ključ
API_KEY = "0a6734c048020b4e5c718fdfbb23fd21"


# Broj stranica filmova
NUM_MOVIES = 200

# URL za API
GENRE_URL = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
MOVIE_URL = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="

# Get Data
genres_response = requests.get(GENRE_URL)
genres_data = genres_response.json()

# Znarove spajamo u jedan rijecnik
genre_dict = {genre.get("id"): genre.get("name") for genre in genres_data.get("genres", [])}

# Connect mongo
client = pymongo.MongoClient("mongodb+srv://Vrsa:h9CDGt9WhLQOTIHs@moviecluster0.xwgrydc.mongodb.net/?retryWrites=true&w=majority")
db = client["movies_database"]
collection = db["movies"]

# API odgovoroj spremi u MONGO
for i in range(1, NUM_MOVIES):
    response = requests.get(MOVIE_URL + str(i))
    data = response.json()

    
    for movie in data.get("results", []):
        # Provjera duplica
        if collection.find_one({"id": movie.get("id")}) is None:
            # Ako ih nema duplica onda ubacujemo film
            movie_data = {
                "id": movie.get("id"),
                "title": movie.get("title"),
                "rating": movie.get("vote_average"),
                "genre": [genre_dict.get(genre_id) for genre_id in movie.get("genre_ids", [])],
                "original_language": movie.get("original_language"),
                "popularity": movie.get("popularity"),
                "release_date": movie.get("release_date"),
                "description": movie.get("overview")
            }
            collection.insert_one(movie_data)
        else:
            # Ako je duplic onad preskoci
            print(f"Skipping movie {movie.get('id')} ... already exists!")



#Calculate matrix
cosine_sim_genre, cosine_sim_desc = recommender.compute()
recommender.store_matrices_locally(cosine_sim_genre, cosine_sim_desc)
