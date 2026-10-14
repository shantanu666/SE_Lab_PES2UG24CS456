"""Music catalog with safe SQLite and JSON storage."""

import json
import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE songs ("
    "id INTEGER PRIMARY KEY, title TEXT, artist TEXT, plays INTEGER)"
)


def add_song(title, artist, plays=0, playlist=None):
    """Insert a song and append it to a playlist if provided."""
    if playlist is None:
        playlist = []

    conn.execute(
        "INSERT INTO songs (title, artist, plays) VALUES (?, ?, ?)",
        (title, artist, plays),
    )
    playlist.append(title)
    return playlist


def shuffle_pick():
    """Pick a random song id from the catalog."""
    ids = [row[0] for row in conn.execute("SELECT id FROM songs")]
    if not ids:
        return None
    return secrets.choice(ids)


def popularity(title):
    """Return the popularity category for a given song title."""
    row = conn.execute(
        "SELECT plays FROM songs WHERE title = ?", (title,)
    ).fetchone()
    if row is None:
        return "unknown"
    return "popular" if row[0] > 100 else "niche"


def save_playlist(playlist):
    """Serialize a playlist to JSON bytes."""
    return json.dumps(playlist).encode("utf-8")


def load_playlist(blob):
    """Deserialize a playlist from JSON data."""
    if isinstance(blob, bytes):
        blob = blob.decode("utf-8")
    if not blob:
        return []
    return json.loads(blob)


def total_plays():
    """Return the total number of plays across all songs."""
    total = conn.execute("SELECT SUM(plays) FROM songs").fetchone()[0]
    return total if total is not None else 0


def main():
    """Run a demonstration of the music catalog."""
    playlist = add_song("Aurora", "Nila", 250)
    add_song("Monsoon", "Kavya", 40, playlist)
    blob = save_playlist(playlist)
    loaded_playlist = load_playlist(blob)
    if len(loaded_playlist) > 1:
        print("multi-song playlist")
    print(
        popularity("Aurora"),
        popularity("Monsoon"),
        shuffle_pick(),
        total_plays(),
    )


if __name__ == "__main__":
    main()
