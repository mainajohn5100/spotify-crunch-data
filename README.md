# Spotify Wrapped Generator

This Python script generates a Spotify Wrapped-like summary of your listening data, including your top artists, tracks, and albums, as well as an estimation of your total listening time.

## Prerequisites

* Python 3.6 or higher
* `spotipy` library (install with `pip install spotipy`)
* Spotify Developer account and application credentials (Client ID, Client Secret, Redirect URI)

## Setup
1.  **Clone the project**
    * Click this [link](https://github.com/mainajohn5100/spotify-crunch-data.git) to clone the project.

2.  **Activate the environment and Install spotipy:**
    ```bash
    source venv/bin/acivate
    pip install spotipy
    ```
3.  **Obtain Spotify API Credentials:**
    * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    * Create a new application.
    * Copy your Client ID and Client Secret.
    * Add a Redirect URI (e.g., `http://localhost:8080`) to your application's settings.
4.  **Configure the Script:**
    * Create a `.env` file in the root folder of the project.
    * Add these envirnment variables to the `.env` file:
      ```bash
          SPOTIFY_CLIENT_ID=CLIENT_ID
          SPOTIFY_CLIENT_SECRET=CLIENT_SECRET
          SPOTIFY_REDIRECT_URI=REDIRECT_URI
      ```
    * Replace the placeholder values for `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` with your actual credentials.

## Usage

1.  **Run the script:**
    ```bash
    python spotify_wrapped.py
    ```
2.  **Authorize the application:**
    * A browser window will open, prompting you to authorize the application to access your Spotify data.
    * Grant the necessary permissions.
3.  **View the results:**
    * The script will print the Spotify data summary to the console in JSON format.
    * A file named `spotify_wrapped.json` will be created in the same directory, containing the data.

## Output

The script generates the following data:

* **Top 10 Artists:** A list of your top 10 most played artists.
* **Top 20 Tracks:** A list of your top 20 most played tracks.
* **Top 10 Albums:** A list of your top 10 most played albums.
* **Total Minutes Listened (Recent):** An approximate total of minutes listened based on recent history.
* **Estimated Yearly Minutes Listened:** A very rough estimation of total minutes listened over a year, based on the recent data.
* The data is outputted in json format, both to the console, and to `spotify_wrapped.json`.

## Important Notes

* The "Estimated Yearly Minutes Listened" is a very rough approximation based on your recently played tracks. It is not an exact representation of your total listening time.
* The `current_user_recently_played` endpoint has a limit. Therefore, the total minutes listened is based on the most recent 50 tracks.
* This script requires your Spotify API credentials. Keep them secure.
* The script uses the `user-library-read`, `user-top-read`, and `user-read-recently-played` scopes to access your Spotify data.
* Error handling is implemented to catch potential `SpotifyException` errors and other general exceptions.
