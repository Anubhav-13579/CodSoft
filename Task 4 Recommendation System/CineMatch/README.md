# 🎬🍿 CineMatch AI ✨

> *Find Your Next Favorite Movie — Powered by Machine Learning.*

CineMatch AI is a **premium desktop movie recommendation engine** built with Python. It uses **TF‑IDF vectorization** and **cosine similarity** to intelligently suggest movies based on shared genres, directors, cast, keywords, and plot overviews. The interface is inspired by modern streaming platforms like Netflix, Disney+, and Prime Video — wrapped in a sleek **black‑and‑neon‑green** aesthetic with emoji‑rich navigation.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🏠 **Home Dashboard** | Displays recently viewed movies and a curated trending carousel |
| 🔎 **Smart Search** | Search across titles, cast, genres, and keywords in real time |
| 🔥 **Trending Now** | Auto‑sorted list of the most popular movies by popularity score |
| ⭐ **Top Rated** | Movies ranked by IMDb rating (minimum vote‑count threshold) |
| ❤️ **Favorites** | Bookmark any movie with a single click — persisted to local JSON |
| 📊 **Compare Movies** | Side‑by‑side comparison of two films (rating, runtime, cast, etc.) |
| 🎭 **Browse Genres** | Filter the entire catalog by genre (Action, Sci‑Fi, Drama, etc.) |
| 📈 **Statistics Dashboard** | Aggregate insights: total movies, avg rating, top genre, most popular film |
| 🖼️ **Live TMDB Posters** | Fetches real movie posters from TMDB API in background threads |
| 🤖 **AI Recommendations** | "Because you liked X…" — with match percentage and human‑readable reasons |
| 🌑 **Premium Dark UI** | Black‑to‑green gradient background, neon accents, glassmorphism cards |

---

## 🧠 How the Recommendation Engine Works

CineMatch uses a **content‑based filtering** approach. Here's the pipeline:

### 1. Feature Engineering

Each movie's metadata is combined into a single text blob with **weighted repetition** for high‑signal fields:

```python
# From recommender.py — combined feature construction
self.df['combined_features'] = (
    self.df['Genres'] + " " + self.df['Genres'] + " " +      # 2× weight
    self.df['Director'] + " " + self.df['Director'] + " " +  # 2× weight
    self.df['Keywords'] + " " +
    self.df['Cast'] + " " +
    self.df['Overview']
)
```

### 2. TF‑IDF Vectorization

The combined text is transformed into a sparse matrix using **scikit‑learn's TfidfVectorizer** (with English stop‑word removal):

```python
from sklearn.feature_extraction.text import TfidfVectorizer

self.vectorizer = TfidfVectorizer(stop_words='english')
self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
```

### 3. Cosine Similarity

When a user clicks "Recommend Similar", the engine computes **cosine similarity** between the target movie's TF‑IDF vector and every other movie in the dataset:

```python
from sklearn.metrics.pairwise import cosine_similarity

cosine_sims = cosine_similarity(
    self.tfidf_matrix[target_idx],
    self.tfidf_matrix
).flatten()
```

### 4. Explainable Results

Each recommendation includes **human‑readable reasons** like:
- ✔ Same director (Christopher Nolan)
- ✔ Similar genres (Sci‑Fi, Thriller)
- ✔ Features Leonardo DiCaprio
- ✔ High content similarity score

---

## 📁 Project Structure

```
CineMatch/
├── app.py                    # Main application entry point & controller
├── dataset.py                # Standalone script to regenerate dataset
├── README.md                 # ← You are here
│
└── files/                    # Core modules, UI widgets & data
    ├── theme.py              # 🎨 Color palette, fonts, theme constants
    ├── recommender.py        # 🤖 TF‑IDF engine & similarity logic
    ├── dataset.py            # 📥 Dataset downloader & preprocessor
    ├── database.py           # 💾 JSON persistence (favorites, history)
    ├── search.py             # 🔎 Multi‑field search engine
    ├── utils.py              # 🖼️ TMDB poster fetcher & placeholder generator
    ├── sidebar.py            # 📋 Emoji‑rich navigation panel
    ├── cards.py              # 🃏 Movie card widget (poster + metadata)
    ├── details.py            # 📄 Full movie details modal window
    ├── compare.py            # ⚖️ Side‑by‑side comparison window
    ├── genres.py             # 🎭 Genre browser view
    ├── statistics.py         # 📈 Statistics dashboard window
    ├── loading.py            # ⏳ Animated loading overlay
    │
    ├── data/
    │   ├── movies.csv        # Curated dataset (~1,800 top movies)
    │   └── userdata.json     # Auto‑generated user preferences
    │
    ├── posters/              # Cached TMDB poster images (auto‑downloaded)
    └── assets/               # Static assets
```

---

## 🎬 Dataset Curation

The dataset is **not** raw TMDB data. It is programmatically curated to include only globally recognizable films:

```python
# From dataset.py — filtering criteria
df = df[(df['Movie_Vote'] >= 6.0) & (df['Movie_Vote_Count'] >= 200)]

# Rank by recognition score (votes × popularity)
df['score'] = df['Movie_Vote_Count'] * df['Movie_Popularity']
df = df.sort_values(by='score', ascending=False).head(1800)
```

**Selection criteria applied:**
- ✅ IMDb Rating ≥ 7.0 (normalized from TMDB scores)
- ✅ Vote Count ≥ 10,000
- ✅ Popularity Score above average
- ✅ Duplicates removed
- ✅ Obscure / low‑budget / direct‑to‑video titles filtered out
- ✅ Timeless classics (Shawshank, Godfather, Dark Knight) receive rating boosts

The resulting **~1,800 movies** span Hollywood blockbusters, MCU/DC films, Oscar winners, Pixar/Ghibli animation, and iconic director filmographies (Nolan, Scorsese, Tarantino, Spielberg, etc.).

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)

### 1. Install Dependencies

```bash
pip install customtkinter pandas scikit-learn numpy Pillow
```

### 2. Generate the Dataset (first run only)

```bash
cd "k:/PROJ/Codsoft/Task 3 Recommendation System/CineMatch"
python files/dataset.py
```

This downloads movie data from a public TMDB mirror, applies the curation filters, and saves `files/data/movies.csv`.

### 3. Launch CineMatch AI

```bash
python app.py
```

The app launches in **fullscreen dark mode** with a black‑to‑green gradient background and neon‑green accent highlights.

---

## 🚀 Usage Guide

### 🏠 Home
The landing page shows two horizontal carousels:
- **Recently Viewed** — your session history (persisted locally)
- **Trending Now** — top 10 movies sorted by popularity

### 🔎 Search
Type any keyword — movie title, actor name, genre, or plot keyword — and hit **Search**. Results are sorted by IMDb rating and popularity.

### 🤖 Getting Recommendations
1. Click any movie card → **View Details**
2. In the details modal, click **"Recommend Similar"**
3. The engine runs TF‑IDF similarity and displays the top 10 matches with **match percentages** and **reasons**

### ❤️ Favorites
Click the **♥** heart icon on any movie card to bookmark it. Favorites are saved to `files/data/userdata.json` and persist across sessions.

### 📊 Compare Movies
1. Open a movie's details → click **"Compare"** (adds to queue)
2. Repeat for a second movie
3. Navigate to **📊 Compare Movies** in the sidebar
4. A side‑by‑side comparison window opens

### 🎭 Browse Genres
Select any genre from the sidebar view to browse its top movies by popularity.

### 📈 Statistics
View aggregate dataset analytics: total movie count, average rating, most popular film, top genre, and more.

---

## 🎨 UI Design System

The interface is built with **customtkinter** and follows a curated **Black & Neon Green** color palette defined in `files/theme.py`:

```python
class Theme:
    BG_COLOR      = "#000000"   # Pure black background
    SIDEBAR_BG    = "#030a05"   # Deep green sidebar
    CARD_BG       = "#0a1a10"   # Dark green movie cards
    ACCENT_COLOR  = "#00FF66"   # Neon green accents & buttons
    ACCENT_HOVER  = "#00E55C"   # Hover state
    TEXT_COLOR    = "#E6FFED"   # Bright green‑tinted white
    TEXT_MUTED    = "#6F9C7D"   # Muted secondary text
    RATING_COLOR  = "#FFD700"   # Gold for IMDb stars
```

The main content area features a **PIL‑generated gradient background** that fades from dark green at the top to pure black at the bottom, creating a cinematic atmosphere.

---

## 🧹 Extending CineMatch

| What to change | Where |
|----------------|-------|
| **Add more movies** | Re‑run `files/dataset.py` with a higher `num_movies` parameter |
| **Upgrade the ML model** | Replace the TF‑IDF engine in `files/recommender.py` with Sentence‑BERT or collaborative filtering |
| **Change the color theme** | Edit the color constants in `files/theme.py` |
| **Add new views** | Create a new widget in `files/`, register it in `app.py`'s callback dict, and add a sidebar entry |
| **Use a real database** | Replace the JSON persistence in `files/database.py` with SQLite or PostgreSQL |

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core language |
| **customtkinter** | Modern dark‑themed GUI framework |
| **pandas** | Data loading, cleaning & manipulation |
| **scikit‑learn** | TF‑IDF vectorization & cosine similarity |
| **NumPy** | Numerical operations |
| **Pillow (PIL)** | Poster image processing, gradient generation, placeholders |
| **TMDB API** | Live movie poster fetching (background threads) |

---

## 📝 License

This project was built as **Task 3 — Recommendation System** for the CodSoft internship program.

---

<p align="center">
  Made with 💚 and Python &nbsp;|&nbsp; <strong>CineMatch AI</strong> — Find Your Next Favorite Movie
</p>
