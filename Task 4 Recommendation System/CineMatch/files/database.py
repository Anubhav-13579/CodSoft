import json
import os

class DatabaseManager:
    def __init__(self, data_file=None):
        if data_file is None:
            data_file = os.path.join(os.path.dirname(__file__), "data", "userdata.json")
        self.data_file = data_file
        self.data = {"favorites": [], "recently_viewed": []}
        self._load()
        
    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except Exception:
                pass
        
    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
            
    # --- Favorites ---
    
    def add_favorite(self, movie_id):
        if movie_id not in self.data["favorites"]:
            self.data["favorites"].append(movie_id)
            self._save()
            return True
        return False
        
    def remove_favorite(self, movie_id):
        if movie_id in self.data["favorites"]:
            self.data["favorites"].remove(movie_id)
            self._save()
            return True
        return False
        
    def is_favorite(self, movie_id):
        return movie_id in self.data["favorites"]
        
    def get_favorites(self):
        return self.data["favorites"]
        
    # --- Recently Viewed ---
    
    def add_recently_viewed(self, movie_id):
        # Remove if it already exists to put it at the front
        if movie_id in self.data["recently_viewed"]:
            self.data["recently_viewed"].remove(movie_id)
            
        # Insert at front
        self.data["recently_viewed"].insert(0, movie_id)
        
        # Keep only last 20
        if len(self.data["recently_viewed"]) > 20:
            self.data["recently_viewed"] = self.data["recently_viewed"][:20]
            
        self._save()
        
    def get_recently_viewed(self):
        return self.data["recently_viewed"]
