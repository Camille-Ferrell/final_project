import requests
from datetime import datetime
import librosa

class Song:
    def __init__(self, title, artist, bpm):
        self.title = title
        self.artist = artist
        self.bpm = bpm

class UpbeatSong(Song):
    def __init__(self, title, artist, bpm):
        super().__init__(title, artist, bpm)

class SlowSong(Song):
    def __init__(self, title, artist, bpm):
        super().__init__(title, artist, bpm)

class HolidaySong(Song):
    def __init__(self, title, artist, bpm):
        super().__init__(title, artist, bpm)

def get_weather_data(api_key: str = "4204310b04c096285fad8d4b5df1c49d", city: str = "Boston"):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "APPID": api_key}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad requests

        # Assuming the API response contains JSON data
        data = response.json()

        # Extracting relevant weather information (replace with actual data structure from the API)
        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]

        return f"The weather in {city} is {condition} with a temperature of {temperature}°C."

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

def get_calendar_date():
    return datetime.now().strftime("%Y-%m-%d")

def analyze_song_bpm(song_path):
    # Use Librosa to analyze the BPM of the song
    y, sr = librosa.load(song_path)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    bpm = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
    return bpm

class MusicLibrary:
    def __init__(self, library):
        self.library = library

    def analyze_song(self, song_path):
        bpm = analyze_song_bpm(song_path)
        return bpm

class WeatherAnalyzer:
    def __init__(self, weather_conditions):
        self.weather_conditions = weather_conditions

    def analyze_weather(self):
        if "clear" in self.weather_conditions.lower():
            return UpbeatSong("Sunny Song", "Artist", 120)
        elif "cloud" in self.weather_conditions.lower():
            return SlowSong("Cloudy Song", "Artist", 80)
        else:
            return UpbeatSong("Default Song", "Artist", 100)

class CalendarAnalyzer:
    def __init__(self, calendar_date):
        self.calendar_date = calendar_date

    def analyze_date(self):
        # Check for specific holidays and return a HolidaySong
        if "12-25" in self.calendar_date:
            return HolidaySong("Christmas Song", "Artist", 90)
        elif "10-31" in self.calendar_date:
            return HolidaySong("Halloween Song", "Artist", 100)
        else:
            return None

class SongRecommendation:
    def __init__(self, library, weather_conditions, calendar_date):
        self.music_library = MusicLibrary(library)
        self.weather_analyzer = WeatherAnalyzer(weather_conditions)
        self.calendar_analyzer = CalendarAnalyzer(calendar_date)

    def recommend_song(self, song_path):
        # Analyze the song's BPM
        bpm = self.music_library.analyze_song(song_path)

        # Analyze weather conditions
        weather_song = self.weather_analyzer.analyze_weather()

        # Analyze calendar date
        holiday_song = self.calendar_analyzer.analyze_date()

        # Choose the final recommended song based on conditions
        if holiday_song:
            return holiday_song
        elif bpm > 100:
            return UpbeatSong("High BPM Song", "Artist", bpm)
        else:
            return SlowSong("Low BPM Song", "Artist", bpm)

# Example Usage
api_key = "4204310b04c096285fad8d4b5df1c49d"
city = "Boston"
weather_data = get_weather_data(api_key, city)
calendar_date = get_calendar_date()
library = ["path/to/song1.mp3", "path/to/song2.mp3", "path/to/song3.mp3"]
song_recommendation = SongRecommendation(library, weather_data, calendar_date)
recommended_song = song_recommendation.recommend_song("path/to/user_selected_song.mp3")
print(f"Recommended Song: {recommended_song.title} by {recommended_song.artist} with BPM: {recommended_song.bpm}")
