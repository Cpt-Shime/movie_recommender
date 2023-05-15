# movie_recommender
Simple movie recommender using TheMovieDB API to get the data. Store it in MongoDB atlas and find the similar movies using cosine similarity over genres and description!


## Step by step working

1. get_data.py gets data from the API request and stores it into MongoDB on Mongo Atlas platfrom. NUM of movies is around 20 * num of movies varijable as the api returns page of movies around 20.  Then we compute the similarity matrix and store it locally!

2. running the recommender.py will load all of our movies from the database and load the cosine_sim_matrix for genries and description. Ask the user to input and movie and then call the function print_recommanded movies  with more weight on 0.7 and 0.3 on movie description. 