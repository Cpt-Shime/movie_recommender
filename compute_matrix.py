import functions as recommender

#Calculate matrix
cosine_sim_genre, cosine_sim_desc = recommender.compute()

#Store it into MongoDB cloud - atlas... Does not work for bigger matrix
#recommender.store_matrices(matrix, matrix_desc, cosine_sim_genre, cosine_sim_desc)

# Store the matrix locally on the pc 
recommender.store_matrices_locally(cosine_sim_genre, cosine_sim_desc)