class SearchEngine:
    def __init__(self, recommender):
        self.recommender = recommender
        
    def search(self, query):
        if not query or not query.strip():
            return []
            
        q = query.lower().strip()
        df = self.recommender.df
        
        # Netflix style search: Title, Cast, Genre, Keywords
        mask = (
            df['Title'].str.lower().str.contains(q, na=False) |
            df['Cast'].str.lower().str.contains(q, na=False) |
            df['Genres'].str.lower().str.contains(q, na=False) |
            df['Keywords'].str.lower().str.contains(q, na=False)
        )
        
        matches = df[mask]
        
        if matches.empty:
            return []
            
        results = []
        for _, row in matches.iterrows():
            product_dict = row.to_dict()
            product_dict['recommendation_score'] = 0
            product_dict['reasons'] = ["Matched your search query"]
            results.append(product_dict)
            
        # Sort by popularity or rating
        results.sort(key=lambda x: (x['IMDb Rating'], x['Popularity']), reverse=True)
        return results
