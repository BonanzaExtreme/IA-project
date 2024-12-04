

The dataset: https://www.kaggle.com/datasets/niharika41298/gym-exercise-data

The dataset was cleaned and reprocessed. The exercises data is loaded from a CSV file (megaGymDataset.csv) using the pandas library. An additional column (ID) was added
which served as a unique identifier for each exercises. 

The textual data from the dataset (exercise titles, descriptions, etc.) is used to create a profile for both the user and the exercises.

The dataset was used in our homepage which displayed all exercises from the dataset.

The type of recommendation algorithm used was "content-based filtering". Content-based filtering recommends items to users based on the attributes or characteristics of the items and the preferences or profiles of the users. 
unlike collaborative filtering, content-based filtering does not rely on other user's profile to make recommendations. This method relies solely on the content (e.g., descriptions, features)
of the items to make recommendations

The user is described by their fitness profile, including characteristics like level, goal, body_part, and equipment. 
The profile is essentially a description of the user’s preferences or needs,

The system compares the user profile's textual description with the exercises' descriptions using TF-IDF (Term Frequency-Inverse Document Frequency) and Cosine Similarity.

Based on the similarity between the user's profile and the exercises' content, the system selects and recommends the most similar exercises.

The exercises are then sorted based on the cosine similarity scores, and the top exercises with the highest similarity are selected as recommendations for the user.
