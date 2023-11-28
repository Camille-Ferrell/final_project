import requests
from datetime import datetime
import librosa
import csv

class MusicLibrary:
    def __init__(self, songs):
        self.songs = songs

    @classmethod
    def load_library_from_csv(cls,file_path):
        library = []
        try:
            with open(file_path,'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for column in csv_reader:
                    song = Song(
                        title=column['Song'],
                        artist=column[' Artist(s)'],
                        bpm=int(column[' BPM']),
                        holiday_association=column[' Holiday Association']
                    )
                    library.append(song)
            print(f"Library loaded from {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error loading library: {e}")
        return cls(library)

    def display_library(self):
        for song in self.songs:
            print(f"{song.title} by {song.artist} ({song.bpm} BPM)")

class Song:
    def __init__(self, title, artist, bpm, holiday_association=None):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.holiday_association = holiday_association

class WeatherAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_user_input(self):
        city = input("Enter the city for weather analysis: ")
        return city
    
    def get_weather_data(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "APPID": self.api_key}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad requests

            # Assuming the API response contains JSON data
            data = response.json()

            # Extracting relevant weather information (replace with actual data structure from the API)
            temperature = data["main"]["temp"]
            condition = data["weather"][0]["description"]

            return f"The weather in {self.city} is {condition} with a temperature of {temperature}°C."

        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

    def analyze_weather(self):
        city = self.get_user_input()
        weather_data = self.get_weather_data(city)
        # Replace this with your logic based on weather condition
        # Extracting relevant weather information
        temperature = int(weather_data.split('°')[0].split(':')[-1])
        condition = weather_data.split('is ')[1].split(' with')[0].lower()

        #My logic based on weather conditions
        if "clear" in condition or "sunny" in condition:
            if temperature > 60:
                return Song("Sunny and Warm Song", "Artist", 120)
            else:
                return Song("Sunny and Cool Song", "Artist", 110)
        elif "partly cloudy" in condition or "partly sunny" in condition:
            return Song("Partly Cloudy Song", "Artist", 100)
        elif "cloudy" in condition or "rainy" in condition or "foggy" in condition or "snowy" in condition:
            return Song("Rainy Day Song", "Artist", 89)
        else:
            # Default case, return a default song
            return Song("Default Song", "Artist", 100)

class CalendarAnalyzer:
    def __init__(self, calendar_date):
        self.calendar_date = calendar_date

    @staticmethod
    def get_calendar_date():
        return datetime.now().strftime("%Y-%m-%d")

    def analyze_date(self):
        # Check for specific holidays and return a HolidaySong
        if "12-25" in self.calendar_date:
            return Song("Christmas Song", "Artist", 90)
        elif "10-31" in self.calendar_date:
            return Song("Halloween Song", "Artist", 100)
        else:
            return None

class SongRecommendation:
    def __init__(self, library, weather_analyzer, calendar_analyzer):
        self.music_library = library
        self.weather_analyzer = weather_analyzer
        self.calendar_analyzer = calendar_analyzer

    def recommend_song(self):
        # Analyze weather conditions
        weather_song = self.weather_analyzer.analyze_weather()

        # Analyze calendar date
        holiday_song = self.calendar_analyzer.analyze_date()

        # Choose the final recommended song based on conditions
        if holiday_song:
            return holiday_song
        else:
            return weather_song


                       
#Example Usage
api_key = "4204310b04c096285fad8d4b5df1c49d"
file_path = "Music_Library.csv"
weather_analyzer = WeatherAnalyzer(api_key)
calendar_date = CalendarAnalyzer.get_calendar_date()
library = MusicLibrary.load_library_from_csv(file_path)
song_recommendation = SongRecommendation(library, weather_analyzer, CalendarAnalyzer(calendar_date))
recommended_song = song_recommendation.recommend_song()
print(f"Recommended Song: {recommended_song.title} by {recommended_song.artist} with BPM: {recommended_song.bpm}")

