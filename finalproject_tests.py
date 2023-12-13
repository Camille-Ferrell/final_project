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
        songs = [Song("TestSong", "TestArtist", 120, "TestHoliday")]
        music_library = MusicLibrary(songs)
        self.assertEqual(music_library.songs, songs)

    def test_load_library_from_csv(self):
        # Creating a temporary CSV file for testing
        csv_content = """Song, Artist(s), BPM, Holiday Association
TestSong, TestArtist, 120, TestHoliday
"""
        with patch("builtins.open", mock_open(read_data=csv_content)) as mock_file:
            library = MusicLibrary.load_library_from_csv("test.csv")

        mock_file.assert_called_once_with("test.csv", "r")
        self.assertEqual(len(library), 1)
        self.assertEqual(library[0].title, "TestSong")
        self.assertEqual(library[0].artist, "TestArtist")
        self.assertEqual(library[0].bpm, 120)
        self.assertEqual(library[0].holiday_association, "TestHoliday")


class TestAnalyzer(unittest.TestCase):
    def test_get_random_song(self):
        songs = [
            Song("Song1", "Artist1", 100),
            Song("Song2", "Artist2", 120),
            Song("Song3", "Artist3", 150),
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
            "weather": [{"description": "Clear sky"}],
        }
        mock_get.return_value = mock_response

        weather_analyzer = WeatherAnalyzer("TestAPIKey")
        weather_data = weather_analyzer.get_weather_data("TestCity")

        self.assertIn("Clear sky", weather_data)
        self.assertIn("25", weather_data)

    def test_analyze_weather(self):
        songs = [
            Song("Song1", "Artist1", 90),
            Song("Song2", "Artist2", 100),
            Song("Song3", "Artist3", 120),
        ]
        weather_analyzer = WeatherAnalyzer("TestAPIKey")
        weather_analyzer.get_user_input = Mock(return_value="TestCity")
        weather_analyzer.get_weather_data = Mock(return_value="The weather in TestCity is Clear sky with a temperature of 25°F.")

        matching_song = weather_analyzer.analyze_weather(songs)
        self.assertIn(matching_song, songs)


class TestCalendarAnalyzer(unittest.TestCase):
    def test_get_calendar_date(self):
        calendar_date = CalendarAnalyzer.get_calendar_date()
        self.assertIsInstance(calendar_date, str)

    def test_analyze_date(self):
        library = [
            Song("ChristmasSong", "Artist1", 120, "Christmas"),
            Song("HalloweenSong", "Artist2", 100, "Halloween"),
            Song("ValentinesSong", "Artist3", 110, "Valentine's Day"),
        ]
        calendar_analyzer = CalendarAnalyzer(date(2023, 12, 25))

        matching_songs = calendar_analyzer.analyze_date(library)
        self.assertEqual(len(matching_songs), 1)
        self.assertEqual(matching_songs[0].holiday_association, "Christmas")


class TestSongRecommendation(unittest.TestCase):
    def test_recommend_song(self):
        library = [
            Song("ChristmasSong", "Artist1", 120, "Christmas"),
            Song("HalloweenSong", "Artist2", 100, "Halloween"),
            Song("ValentinesSong", "Artist3", 110, "Valentine's Day"),
        ]
        weather_analyzer = WeatherAnalyzer("TestAPIKey")
        calendar_analyzer = CalendarAnalyzer(date(2023, 12, 25))

        song_recommendation = SongRecommendation(library, weather_analyzer, calendar_analyzer)
        recommended_song = song_recommendation.recommend_song()

        self.assertIn(recommended_song, library)


if __name__ == "__main__":
    unittest.main()
