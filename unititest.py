import unittest
import time
from unittest.mock import patch, MagicMock
from androgynous import Androgynous
from mood import HappyMood, AngryMood, BoredMood, NeutralMood, SadMood
# test mo to ami, pero change mo yung mga chinange mo

class TestAndrogynous(unittest.TestCase):
    def setUp(self):
        self.player = Androgynous()

        # Mock database connection for all tests
        self.db_patcher = patch('androgynous.create_connection')
        self.mock_db = self.db_patcher.start()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        self.mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

    def tearDown(self):
        self.db_patcher.stop()

    def test_initial_state(self):
        self.assertEqual(self.player._age, 0)
        self.assertEqual(self.player._energy, 100)
        self.assertEqual(self.player._health, 100)
        self.assertEqual(self.player._hunger, 100)
        self.assertEqual(self.player._mood, 100)
        self.assertEqual(self.player._hygiene, 100)
        self.assertEqual(self.player.name, "Ziddy")

    def test_player_eats(self):
        # Test eating liked food
        self.player._hunger = 50
        self.player._energy = 50
        self.player.hunger_level = 2
        self.player.player_eats("apple")
        self.assertEqual(self.player._hunger, 80)
        self.assertEqual(self.player._energy, 55)
        self.assertEqual(self.player.hunger_level, 1)

        # Test eating disliked food
        self.player.dislikes = ["rotten"]
        self.player._health = 100
        self.player.player_eats("rotten")
        self.assertEqual(self.player._health, 85)

    def test_player_moves(self):
        self.player._energy = 50
        self.player.moving = True
        self.player.player_moves()
        self.assertEqual(self.player._energy, 45)
        self.assertFalse(self.player.moving)

    def test_player_plays(self):
        self.player._energy = 50
        self.player.player_plays()
        self.assertEqual(self.player._energy, 30)

    def test_player_sleeps(self):
        self.player._age = 5
        self.player._energy = 50
        self.player.sleep_level = 2
        self.player.player_sleeps()
        self.assertEqual(self.player._age, 6)
        self.assertEqual(self.player._energy, 60)
        self.assertEqual(self.player.sleep_level, 1)

    def test_player_poops(self):
        self.player._hygiene = 100
        self.player.potty_level = 2
        self.player.player_poops()
        self.assertEqual(self.player._hygiene, 75)
        self.assertEqual(self.player.potty_level, 1)

    def test_player_showers(self):
        self.player._hygiene = 50
        self.player.shower_level = 2
        self.player.player_showers()
        self.assertEqual(self.player._hygiene, 80)
        self.assertEqual(self.player.shower_level, 1)

    def test_health_check(self):
        # Test hunger below 75 triggers move
        self.player._hunger = 70
        self.player._energy = 50
        self.player.moving = False
        self.player.health_check()
        self.assertEqual(self.player._energy, 45)

        # Test game over when hunger is 0
        self.player._hunger = 0
        with self.assertRaises(SystemExit):
            self.player.health_check()

    def test_update_mood(self):
        # Test mood transitions
        self.player._mood = 80
        self.player.update_mood()
        self.assertIsInstance(self.player.mood, HappyMood)

        self.player._mood = 60
        self.player.update_mood()
        self.assertIsInstance(self.player.mood, NeutralMood)

        self.player._mood = 40
        self.player.update_mood()
        self.assertIsInstance(self.player.mood, BoredMood)

        self.player._mood = 20
        self.player.update_mood()
        self.assertIsInstance(self.player.mood, SadMood)

        self.player._mood = 5
        self.player.update_mood()
        self.assertIsInstance(self.player.mood, AngryMood)

    def test_save_and_load(self):
        # Setup test data
        self.player.name = "TestPlayer"
        self.player.hunger_level = 3
        self.player.shower_level = 2
        self.player.sleep_level = 1
        self.player.potty_level = 4
        self.player._mood = 75
        self.player._age = 10

        # Mock database response for load
        mock_cursor = self.player._mock_db().cursor.return_value
        mock_cursor.fetchone.return_value = (
            "TestPlayer", 3, 2, 1, 4, 75, 10
        )

        # Test save
        self.player.save_to_db()
        mock_cursor.execute.assert_any_call("DELETE FROM player_data")

        # Test load
        self.player.load_from_db()
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.hunger_level, 3)
        self.assertEqual(self.player.shower_level, 2)
        self.assertEqual(self.player.sleep_level, 1)
        self.assertEqual(self.player.potty_level, 4)
        self.assertEqual(self.player._mood, 75)
        self.assertEqual(self.player._age, 10)


if __name__ == '__main__':
    unittest.main()