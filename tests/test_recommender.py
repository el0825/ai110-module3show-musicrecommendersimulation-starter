import csv
import os
import tempfile

from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    load_songs,
    score_song,
    recommend_songs,
)


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_rewards_genre_mood_and_exact_energy():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    song = {
        "id": 1,
        "title": "Test Pop Track",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }

    score, reasons = score_song(user_prefs, song)

    assert score == 6.0
    assert "genre match" in reasons[0] or "genre match" in reasons[1]
    assert "mood match" in reasons[0] or "mood match" in reasons[1]
    assert any("energy close match" in reason for reason in reasons)


def test_recommend_songs_returns_top_k_sorted_list():
    songs = [
        {
            "id": 1,
            "title": "Close Energy Wrong Genre",
            "artist": "A",
            "genre": "rock",
            "mood": "sad",
            "energy": 0.8,
            "tempo_bpm": 100,
            "valence": 0.4,
            "danceability": 0.5,
            "acousticness": 0.3,
        },
        {
            "id": 2,
            "title": "Exact Genre Low Energy",
            "artist": "B",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.2,
            "tempo_bpm": 90,
            "valence": 0.7,
            "danceability": 0.6,
            "acousticness": 0.4,
        },
    ]
    user_prefs = {
        "favorite_genre": "electronic",
        "favorite_mood": "moody",
        "target_energy": 0.8,
    }

    results = recommend_songs(user_prefs, songs, k=1)

    assert len(results) == 1
    assert results[0][0]["title"] == "Close Energy Wrong Genre"
    assert results[0][1] > 0
    assert "energy close match" in results[0][2]


def test_recommend_songs_returns_empty_for_zero_k():
    songs = [
        {
            "id": 1,
            "title": "Any Song",
            "artist": "A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 100,
            "valence": 0.4,
            "danceability": 0.5,
            "acousticness": 0.3,
        }
    ]
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    results = recommend_songs(user_prefs, songs, k=0)
    assert results == []


def test_load_songs_reads_csv_correctly():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="", encoding="utf-8") as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow([
            "id",
            "title",
            "artist",
            "genre",
            "mood",
            "energy",
            "tempo_bpm",
            "valence",
            "danceability",
            "acousticness",
        ])
        writer.writerow(["1", "CSV Song", "Test", "pop", "happy", "0.8", "120", "0.9", "0.8", "0.2"])
        temp_path = temp_file.name

    try:
        results = load_songs(temp_path)
        assert len(results) == 1
        song = results[0]
        assert song["title"] == "CSV Song"
        assert song["genre"] == "pop"
        assert isinstance(song["energy"], float)
    finally:
        os.remove(temp_path)
