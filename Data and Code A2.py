# Mood Melody — Simple Mood → Song Recommender (Kaggle-ready)

import csv
import os
import random

CSV_PATH = "kaggle_songs.csv"

def load_songs(csv_path=CSV_PATH):
    """
    Loads songs from a CSV. Expected columns (any of these names work):
      - mood / tag / mood_tag
      - track_name / name / title
    Only 'mood' and 'track title' are required.
    """
    songs = []
    if not os.path.exists(csv_path):
        return songs

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mood = (row.get("mood") or row.get("tag") or row.get("mood_tag") or "").strip().lower()
            title = (row.get("track_name") or row.get("name") or row.get("title") or "").strip()
            if mood and title:
                songs.append({"mood": mood, "title": title})
    return songs

def pick_songs(all_songs, mood, n=3):
    """Pick up to n songs for a given mood. Falls back to repeats if pool < n."""
    pool = [s["title"] for s in all_songs if s["mood"] == mood]
    if not pool:
        return []
    if len(pool) >= n:
        return random.sample(pool, n)
    return [random.choice(pool) for _ in range(n)]

# Small fallback list so the app always works even without a CSV.
FALLBACK = {
    "happy": [
        "Happy — Pharrell Williams", "Uptown Funk — Mark Ronson ft. Bruno Mars", "Good as Hell — Lizzo",
        "Can’t Stop the Feeling! — Justin Timberlake"
    ],
    "sad": [
        "Someone Like You — Adele", "Fix You — Coldplay", "Let Her Go — Passenger", "When I Was Your Man — Bruno Mars"
    ],
    "angry": [
        "Smells Like Teen Spirit — Nirvana", "In the End — Linkin Park", "Killing in the Name — Rage Against the Machine"
    ],
    "relaxed": [
        "Weightless — Marconi Union", "Banana Pancakes — Jack Johnson", "Holocene — Bon Iver", "Sunflower — Rex Orange County"
    ],
    "energetic": [
        "Tití Me Preguntó — Bad Bunny", "Turn Down for What — DJ Snake & Lil Jon", "Titanium — David Guetta ft. Sia"
    ],
    "tired": [
        "River Flows in You — Yiruma", "Clair de Lune — Debussy", "Night Owl — Galimatias", "Breathe Me — Sia"
    ]
}

def main():
    print("🎶 Welcome to Mood Melody!")
    print("Answer a couple of quick questions and I’ll suggest songs.\n")

    name = input("Your name: ").strip() or "Friend"

    # Keep the choices simple for first-time use:
    VALID_MOODS = ["happy", "sad", "angry", "relaxed", "energetic", "tired"]
    mood = input(f"How are you feeling? {VALID_MOODS}: ").strip().lower()
    if mood not in VALID_MOODS:
        print("I don't know that mood yet — I’ll try my best with general picks.\n")

    # Try Kaggle CSV first; if empty/missing, use FALLBACK
    kaggle_songs = load_songs(CSV_PATH)
    using_kaggle = len(kaggle_songs) > 0

    print("\n🎧 Recommendations:")
    if using_kaggle:
        # If user gave a mood we know, try CSV → else fallback
        recs = pick_songs(kaggle_songs, mood, n=3)
        if not recs:  # No rows for that mood in CSV
            recs = random.sample(FALLBACK.get(mood, sum(FALLBACK.values(), [])), k=3)
        print("• (from Kaggle) " + "\n• (from Kaggle) ".join(recs))
    else:
        # Pure fallback
        pool = FALLBACK.get(mood)
        if not pool:
            # If unknown mood, mix from everything
            all_titles = sum(FALLBACK.values(), [])
            recs = random.sample(all_titles, k=min(3, len(all_titles)))
        else:
            recs = random.sample(pool, k=min(3, len(pool)))
        print("• " + "\n• ".join(recs))

    print(f"\nThanks, {name}! Enjoy the music 🎵")

if __name__ == "__main__":
    main()
