import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            # Skip rows that are completely empty or only whitespace.
            if not any(value and value.strip() for value in row.values()):
                continue

            song = {
                "id": int(row["id"].strip()),
                "title": row["title"].strip(),
                "artist": row["artist"].strip(),
                "genre": row["genre"].strip(),
                "mood": row["mood"].strip(),
                "energy": float(row["energy"].strip()),
                "tempo_bpm": float(row["tempo_bpm"].strip()),
                "valence": float(row["valence"].strip()),
                "danceability": float(row["danceability"].strip()),
                "acousticness": float(row["acousticness"].strip()),
            }
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Reward exact genre matches, but reduce the weight slightly for this experiment.
    # This lets energy similarity play a larger role in the final ranking.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    # Reward exact mood matches.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Increase the energy influence so it matters about twice as much as before.
    # The score still stays non-negative and is easier to compare with genre/mood.
    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0.0, 4.0 - energy_diff * 4.0)
    score += energy_score
    reasons.append(f"energy close match (+{energy_score:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs: List[Tuple[Dict, float, str]] = []

    # Score every song using score_song() and store the full reason list.
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    # Sort by score descending so the best matches come first.
    scored_songs.sort(key=lambda item: item[1], reverse=True)

    # Return only the top k recommendations.
    return scored_songs[:k]
