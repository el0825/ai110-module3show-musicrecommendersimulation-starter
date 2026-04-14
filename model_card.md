# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeMatch 1.0

---

## 2. Goal / Task

This system tries to recommend songs from a small catalog based on a user’s preferred genre, mood, and energy level. It chooses songs that best match the listener’s taste profile using a simple scoring rule.

---

## 3. Data Used

The model uses a small CSV file of songs. Each song includes metadata like genre, mood, energy, tempo, valence, danceability, and acousticness. The dataset is limited in size and variety, so it has only a few examples of some styles and moods.

---

## 4. Algorithm Summary

Songs are scored using three main ideas. First, a song gets extra points if its genre matches the user’s favorite genre. Second, it gets extra points if its mood matches the user’s favorite mood. Third, the score increases when the song’s energy level is close to the user’s target energy. Higher scores mean a better match, and the system returns the top scoring songs.

---

## 5. Observed Behavior / Biases

The system often prefers songs with the closest energy level. That means energy can dominate the ranking, even when genre or mood are not a perfect fit. The recommendations also feel repetitive because the dataset is small and some songs appear in many profile results.

---

## 6. Evaluation Process

I tested the system with several user profiles, including high-energy pop, chill lofi, intense rock, and edge case profiles with conflicting or narrow preferences. I also ran a small experiment by changing the scoring weights so energy mattered more. This helped show which recommendations changed and why.

---

## 7. Intended Use and Non-Intended Use

Intended use:
- A simple music recommendation demo
- Educational exploration of scoring rules and bias

Not intended use:
- Real production recommendation services
- Large-scale music catalogs or live streaming systems

---

## 8. Ideas for Improvement

- Expand the song dataset so the model can find more diverse matches.
- Tune the score weights so genre, mood, and energy are balanced better.
- Add more features like tempo, danceability, or acousticness to make recommendations richer.

---

## 9. Personal Reflection

This project showed how a simple scoring system can feel smart but also miss important parts of music preference. I learned that small datasets and fixed weights can make a recommender repeat the same songs too often.
