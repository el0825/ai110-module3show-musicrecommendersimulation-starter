"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_profiles = [
        (
            "High Energy Pop",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.9,
            },
        ),
        (
            "Chill Lofi",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "calm",
                "target_energy": 0.3,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.8,
            },
        ),
        (
            "Conflicting High Energy / Sad Mood",
            {
                "favorite_genre": "electronic",
                "favorite_mood": "sad",
                "target_energy": 0.95,
            },
        ),
        (
            "Narrow Acoustic Midnight",
            {
                "favorite_genre": "acoustic",
                "favorite_mood": "melancholy",
                "target_energy": 0.1,
            },
        ),
    ]

    for profile_name, user_prefs in user_profiles:
        print(f"\n=== {profile_name} Profile ===")
        print(f"Preferences: genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
              f"target_energy={user_prefs['target_energy']}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        for index, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{index}. {song['title']} — Score: {score:.2f}")
            print(f"   Reasons: {explanation}")

        # Observation: Check whether the top songs match the profile's genre and mood.
        # For "High Energy Pop", the best recommendations should be upbeat pop tracks.
        # For "Chill Lofi", the system may still return songs with similar energy but
        # mismatched mood if the mood scoring is too weak.
        # For "Deep Intense Rock", the best matches should prioritize rock and intense songs.
        # For the conflicting profile, this edge case shows whether the recommender
        # handles opposite signals from energy and mood at the same time.
        # For the narrow acoustic profile, the system may expose a weakness if
        # acoustic or melancholy tracks are rare in the dataset.

    # After running the script, compare the printed recommendations and note
    # any surprising results or scoring logic issues.


if __name__ == "__main__":
    main()
