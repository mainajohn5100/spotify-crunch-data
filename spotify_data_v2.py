import os
from collections import Counter
from datetime import datetime
import asyncio
import aiohttp
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID") or "your_client_id"
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET") or "your_client_secret"
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI") or "http://localhost:8888/callback"

# Scope for the data you want to access
SCOPE = "user-library-read user-top-read user-read-recently-played"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Global variables for concurrency and timeout
sem = asyncio.Semaphore(10)  # Limit concurrency
TIMEOUT = aiohttp.ClientTimeout(total=60)  # Set total timeout

async def fetch_with_retries(session, url, headers, retries=3):
    """Fetch a URL with retry logic."""
    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()  # Raise error for HTTP codes 4xx/5xx
                return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == retries:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

async def fetch_recently_played_batch(offset, limit):
    """Fetch a batch of recently played tracks asynchronously."""
    async with sem:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            headers = {
                "Authorization": f"Bearer {sp.auth_manager.get_cached_token()['access_token']}"
            }
            url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}&offset={offset}"
            return await fetch_with_retries(session, url, headers)

async def fetch_recently_played_all():
    """Fetch all recently played data (up to 10,000 tracks)."""
    print("Fetching recently played data (up to the last 10,000 tracks)...")
    tasks = []
    limit = 50

    for offset in range(0, 10000, limit):
        tasks.append(fetch_recently_played_batch(offset, limit))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out failed responses
    successful_results = [res for res in results if not isinstance(res, Exception)]
    print(f"Successfully fetched {len(successful_results) * limit} tracks.")
    return [item for result in successful_results for item in result.get("items", [])]

def calculate_yearly_playback(data):
    """Calculate playback statistics for the current year."""
    total_minutes = 0
    song_counts = Counter()
    day_counts = Counter()
    album_counts = Counter()
    artist_counts = Counter()

    for item in data:
        track = item["track"]
        played_at = datetime.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        duration_minutes = track["duration_ms"] / 60000

        if played_at.year == datetime.now().year:
            total_minutes += duration_minutes
            song_counts[track["name"]] += 1
            day_counts[played_at.date()] += 1
            album_counts[track["album"]["name"]] += 1
            for artist in track["artists"]:
                artist_counts[artist["name"]] += 1

    return total_minutes, song_counts, day_counts, album_counts, artist_counts

async def fetch_and_display_top_data():
    """Fetch and display playback statistics."""
    data = await fetch_recently_played_all()
    total_minutes, song_counts, day_counts, album_counts, artist_counts = calculate_yearly_playback(data)

    print(f"\nTotal Minutes Played This Year: {round(total_minutes)}")
    print(f"Total Number of Songs Played: {sum(song_counts.values())}")

    print("\nTop 20 Songs:")
    for i, (song, count) in enumerate(song_counts.most_common(20), 1):
        print(f"{i}. {song} (Played {count} times)")

    print("\nTop 20 Albums:")
    for i, (album, count) in enumerate(album_counts.most_common(20), 1):
        print(f"{i}. {album} (Played {count} times)")

    print("\nTop 5 Most Streamed Days:")
    for i, (day, count) in enumerate(day_counts.most_common(5), 1):
        print(f"{i}. {day} (Played {count} times)")

    print("\nTop 5 Most Streamed Artists:")
    for i, (artist, count) in enumerate(artist_counts.most_common(5), 1):
        print(f"{i}. {artist} (Played {count} times)")

if __name__ == "__main__":
    asyncio.run(fetch_and_display_top_data())
