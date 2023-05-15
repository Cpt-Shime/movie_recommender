import functions as recommender

movies = recommender.load_movies_from_database()

#Load the matrix from the cloud
#matrix, matrix_desc, cosine_sim_genre, cosine_sim_desc = recommender.load_matrices_from_database()


#Load local matrix

cosine_sim_genre, cosine_sim_desc = recommender.load_matrices_from_local()


# Ask the user to input a movie title
title = input("Enter a movie title: ")
start_index = 0
recommender.print_recommended_movies(title, start_index, movies, cosine_sim_genre, cosine_sim_desc)

more = 'yes'
while (more == 'yes' or more == "y"):
    more = input("Do you want more recommended movies, write yes! ")
    if more == "yes" or more == "y":
        start_index += 5
        recommender.print_recommended_movies(title, start_index, movies, cosine_sim_genre, cosine_sim_desc)
    else:
        print("Thank you for using our movie recommendation system!")
        break
