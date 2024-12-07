from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Content-based recommendations using TF-IDF and cosine similarity
def content_based_recommendations(user_data, posts_df):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(posts_df['tags'])  # Assuming 'tags' is a column
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get similar posts based on user interaction
    similar_scores = cosine_sim[user_data.index]
    recommended_indices = similar_scores.argsort()[::-1][:10]  # Get top 10 recommendations
    return posts_df.iloc[recommended_indices]


# Collaborative filtering using Nearest Neighbors
def collaborative_filtering(user_data, posts_df):
    ratings_matrix = posts_df.pivot_table(index='user_id', columns='post_id', values='rating')
    ratings_matrix.fillna(0, inplace=True)

    model = NearestNeighbors(metric="cosine")
    model.fit(ratings_matrix)
    distances, indices = model.kneighbors(user_data, n_neighbors=10)

    recommended_posts = ratings_matrix.iloc[indices.flatten()]
    return recommended_posts
