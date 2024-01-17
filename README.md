# Movie Recommendation System
This script implements a simple movie recommendation system based on content filtering. It uses cosine similarity to recommend movies similar to the user-inputted movie title using cosine similarity over genres and description!

## Prerequisites
Python 3.x
Required Python libraries: functions

## Functionality
Loads movie data from a database.
Implements content-based filtering using cosine similarity.
Recommends movies based on the inputted movie title.
Allows the user to request more recommendations.
Customization
Modify the more variable to change the prompt for additional recommendations.
Adjust the start_index variable to control the starting index for displaying recommendations.

## Step by step working

1. get_data.py gets data from the API request and stores it into MongoDB on Mongo Atlas platfrom. NUM of movies is around 20 * num of movies varijable as the api returns page of movies around 20.  Then we compute the similarity matrix and store it locally!

2. running the recommender.py will load all of our movies from the database and load the cosine_sim_matrix for genries and description. Ask the user to input and movie and then call the function print_recommanded movies  with more weight on 0.7 and 0.3 on movie description.
