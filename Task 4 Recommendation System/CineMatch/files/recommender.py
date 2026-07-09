import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class CineMatchRecommender:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "data", "movies.csv")
        self.data_path = data_path
        self.df = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self._load_and_prepare_data()

    def _load_and_prepare_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
            
        self.df = pd.read_csv(self.data_path)
        
        # Fill NA
        for col in ['Genres', 'Overview', 'Keywords', 'Cast', 'Director']:
            self.df[col] = self.df[col].fillna('')
            
        # Create combined text feature for TF-IDF
        # Give more weight to Director and Genres by repeating them
        self.df['combined_features'] = (
            self.df['Genres'] + " " + self.df['Genres'] + " " +
            self.df['Director'] + " " + self.df['Director'] + " " +
            self.df['Keywords'] + " " +
            self.df['Cast'] + " " +
            self.df['Overview']
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        
    def get_movie_by_id(self, movie_id):
        movie = self.df[self.df['Movie ID'] == movie_id]
        if not movie.empty:
            return movie.iloc[0].to_dict()
        return None
        
    def get_movies_by_ids(self, movie_ids):
        # Preserve order of movie_ids
        # Since pandas is unordered, we map them back
        movies = self.df[self.df['Movie ID'].isin(movie_ids)]
        movies_dict = {row['Movie ID']: row.to_dict() for _, row in movies.iterrows()}
        
        return [movies_dict[m_id] for m_id in movie_ids if m_id in movies_dict]
        
    def get_trending(self, top_n=20):
        sorted_df = self.df.sort_values(by='Popularity', ascending=False).head(top_n)
        return [row.to_dict() for _, row in sorted_df.iterrows()]
        
    def get_top_rated(self, top_n=20, min_votes=500):
        filtered_df = self.df[self.df['Vote Count'] >= min_votes]
        if filtered_df.empty:
            filtered_df = self.df # Fallback if constraints are too tight
        sorted_df = filtered_df.sort_values(by='IMDb Rating', ascending=False).head(top_n)
        return [row.to_dict() for _, row in sorted_df.iterrows()]
        
    def get_by_genre(self, genre, top_n=20):
        filtered = self.df[self.df['Genres'].str.contains(genre, case=False, na=False)]
        sorted_df = filtered.sort_values(by='Popularity', ascending=False).head(top_n)
        return [row.to_dict() for _, row in sorted_df.iterrows()]
        
    def recommend(self, movie_id, top_n=10):
        """
        Recommends similar movies based on a given movie_id.
        """
        idx_series = self.df.index[self.df['Movie ID'] == movie_id]
        if len(idx_series) == 0:
            return []
            
        target_idx = idx_series[0]
        target_movie = self.df.iloc[target_idx]
        
        # Calculate cosine similarity with all movies
        cosine_sims = cosine_similarity(self.tfidf_matrix[target_idx], self.tfidf_matrix).flatten()
        
        # Get top indices (excluding the movie itself)
        # We sort by argsort and get the last top_n+1, then remove the target_idx
        similar_indices = cosine_sims.argsort()[-(top_n+2):][::-1]
        
        results = []
        for idx in similar_indices:
            if idx == target_idx:
                continue
                
            sim_score = cosine_sims[idx]
            row = self.df.iloc[idx]
            
            # Generate reasons
            reasons = []
            
            if row['Director'] and row['Director'] == target_movie['Director']:
                reasons.append(f"Same director ({row['Director']})")
                
            # Check genre overlap
            target_genres = set([g.strip() for g in target_movie['Genres'].split(',') if g.strip()])
            row_genres = set([g.strip() for g in row['Genres'].split(',') if g.strip()])
            common_genres = target_genres.intersection(row_genres)
            if len(common_genres) >= 2:
                reasons.append(f"Similar genres ({', '.join(list(common_genres)[:2])})")
            elif len(common_genres) == 1:
                reasons.append(f"Similar genre ({list(common_genres)[0]})")
                
            # Check cast overlap
            target_cast = set([c.strip() for c in target_movie['Cast'].split(',') if c.strip()])
            row_cast = set([c.strip() for c in row['Cast'].split(',') if c.strip()])
            common_cast = target_cast.intersection(row_cast)
            if common_cast:
                reasons.append(f"Features {list(common_cast)[0]}")
                
            if sim_score > 0.4:
                reasons.append("High content similarity score")
            else:
                reasons.append("Similar keywords/plot")
                
            final_score_pct = int(min(round(sim_score * 100), 99))
            # Just to make scores look appealing on the UI even if TF-IDF similarity is low textually
            # We map 0.05-1.0 to 50-99%
            if final_score_pct < 50:
                final_score_pct = min(50 + int(sim_score * 500), 99)
                
            product_dict = row.to_dict()
            product_dict['recommendation_score'] = final_score_pct
            product_dict['reasons'] = reasons
            
            results.append(product_dict)
            
            if len(results) >= top_n:
                break
                
        return results

    def get_all_genres(self):
        """Return a sorted list of unique genres across the dataset."""
        all_genres = set()
        for g in self.df['Genres'].dropna():
            for genre in g.split(','):
                genre = genre.strip()
                if genre:
                    all_genres.add(genre)
        return sorted(all_genres)

if __name__ == "__main__":
    recommender = CineMatchRecommender()
    print("Testing recommendations for 'Interstellar' (Movie ID 1)")
    recs = recommender.recommend(1, top_n=3)
    for r in recs:
        print(f"{r['Title']} | {r['recommendation_score']}% Match")
        for reason in r['reasons']:
            print(f"  - {reason}")
