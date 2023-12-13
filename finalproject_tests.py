import unittest
from unittest.mock import patch, Mock
from datetime import date
from finalproject import (
    Song,
    MusicLibrary,
    Analyzer,
    WeatherAnalyzer,
    CalendarAnalyzer,
    SongRecommendation,
)


class TestSong(unittest.TestCase):
    def test_song_creation(self):
        song = Song("The A Team", " Ed Sheeran", 85, " No Association")
        self.assertEqual(song.title, "The A Team")
        self.assertEqual(song.artist, " Ed Sheeran")
        self.assertEqual(song.bpm, 85)
        self.assertEqual(song.holiday_association, " No Association")


class TestMusicLibrary(unittest.TestCase):
    def test_library_creation(self):
        songs = [Song("Prom", " SZA", 120, " No Association")]
        music_library = MusicLibrary(songs)
        self.assertEqual(music_library.songs, songs)

    def test_load_library_from_csv(self):
        # Creating a temporary CSV file for testing
        csv_content = """Song, Artist(s), BPM, Holiday Association
Prom, SZA, 120, No Association
"""
        with patch("builtins.open", open(read_data=csv_content)) as mock_file:
            library = MusicLibrary.load_library_from_csv("test.csv")

        mock_file.assert_called_once_with("test.csv", "r")
        self.assertEqual(len(library), 1)
        self.assertEqual(library[0].title, "Prom")
        self.assertEqual(library[0].artist, " SZA")
        self.assertEqual(library[0].bpm, 120)
        self.assertEqual(library[0].holiday_association, " No Association")


class TestAnalyzer(unittest.TestCase):
    def test_get_random_song(self):
        songs = [
            Song("Moscow Mule", " Bad Bunny", 100),
            Song("Colorado", " Reneé Rapp", 120),
            Song("All I Want For Christmas Is You", " Mariah Carey", 150),
        ]
        analyzer = Analyzer()
        random_song = analyzer.get_random_song(songs)
        self.assertIn(random_song, songs)


class TestWeatherAnalyzer(unittest.TestCase):
    @patch("builtins.input", return_value="TestCity")
    def test_get_user_input(self, mock_input):
        weather_analyzer = WeatherAnalyzer("TestAPIKey")
        city = weather_analyzer.get_user_input()
        self.assertEqual(city, "TestCity")

    @patch("requests.get")
    def test_get_weather_data(self, mock_get):
        # Mocking the response from the API
        mock_response = Mock()
        mock_response.json.return_value = {
            "main": {"temp": 25},
            "weather": [{"description": "clear sky"}],
        }
        mock_get.return_value = mock_response

        weather_analyzer = WeatherAnalyzer("4204310b04c096285fad8d4b5df1c49d")
        weather_data = weather_analyzer.get_weather_data("Boston")

        self.assertIn("Clear sky", weather_data)
        self.assertIn("25", weather_data)

    def test_analyze_weather(self):
        songs = [
            Song("Cheap Thrills", " Sia", 90),
            Song("Billie Bossa Nova", " Billie Eilish", 100),
            Song("Never Be Like You", " Flume", 120),
        ]
        weather_analyzer = WeatherAnalyzer("4204310b04c096285fad8d4b5df1c49d")
        weather_analyzer.get_user_input = Mock(return_value="Boston")
        weather_analyzer.get_weather_data = Mock(return_value="The weather in TestCity is Clear sky with a temperature of 25°F.")

        matching_song = weather_analyzer.analyze_weather(songs)
        self.assertIn(matching_song, songs)


class TestCalendarAnalyzer(unittest.TestCase):
    def test_get_calendar_date(self):
        calendar_date = CalendarAnalyzer.get_calendar_date()
        self.assertIsInstance(calendar_date, str)

    def test_analyze_date(self):
        library = [
            Song("O Holy Night", " Josh Groban", 88, " Christmas"),
            Song("The Monster Mash", "Bobby Boris Pickett", 70, " Halloween"),
            Song("Photograph", "Ed Sheeran", 108, " Valentine's Day"),
        ]
        calendar_analyzer = CalendarAnalyzer(date(2023, 12, 25))

        matching_songs = calendar_analyzer.analyze_date(library)
        self.assertEqual(len(matching_songs), 1)
        self.assertEqual(matching_songs[0].holiday_association, " Christmas")


class TestSongRecommendation(unittest.TestCase):
    def test_recommend_song(self):
        library = [
            Song("Do You Hear What I Hear?", " Bing Crosby", 101, " Christmas"),
            Song("Ghostbusters", " Ray Parker Jr.", 115, " Halloween"),
            Song("Love Language", " SZA", 65, " Valentine's Day"),
        ]
        weather_analyzer = WeatherAnalyzer("4204310b04c096285fad8d4b5df1c49d")
        calendar_analyzer = CalendarAnalyzer(date(2023, 12, 25))

        song_recommendation = SongRecommendation(library, weather_analyzer, calendar_analyzer)
        recommended_song = song_recommendation.recommend_song()

        self.assertIn(recommended_song, library)


if __name__ == "__main__":
    unittest.main()
