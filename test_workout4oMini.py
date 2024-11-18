import unittest
from unittest.mock import patch
import time
from workout_4oMini import Metronome

class TestMetronome(unittest.TestCase):

    @patch('time.time', return_value=100)  # Mock time to control time flow
    def test_toggle_timer_start(self, mock_time):
        metronome = Metronome()
        metronome.toggle_timer()
        self.assertTrue(metronome.timer_active)
        self.assertEqual(metronome.start_time, 100)

    @patch('time.time', return_value=150)  # Mock time to control time flow
    def test_get_elapsed_time(self, mock_time):
        metronome = Metronome()
        metronome.toggle_timer()  # Start timer
        mock_time.return_value = 120
        elapsed_time = metronome.get_elapsed_time()
        self.assertEqual(elapsed_time, 20)

    @patch('time.time', side_effect=[100, 110, 120, 130])
    def test_update_bpm(self, mock_time):
        metronome = Metronome()
        metronome.update_bpm(100)
        metronome.update_bpm(110)
        metronome.update_bpm(120)
        metronome.update_bpm(130)
        self.assertEqual(metronome.bpm, 60)  # 60 BPM expected with 1 second intervals

    def test_counter_up(self):
        metronome = Metronome()
        metronome.update_counter("up")
        self.assertEqual(metronome.counter, 1)

    def test_counter_down(self):
        metronome = Metronome()
        metronome.update_counter("down")
        self.assertEqual(metronome.counter, -1)

    def test_format_elapsed_time(self):
        metronome = Metronome()
        with patch('time.time', return_value=100):
            metronome.toggle_timer()
            with patch('time.time', return_value=120):
                self.assertEqual(metronome.format_elapsed_time(), "00:20")

    def test_format_bpm(self):
        metronome = Metronome()
        metronome.bpm = 120
        self.assertEqual(metronome.format_bpm(), "120")
        metronome.bpm = 0
        self.assertEqual(metronome.format_bpm(), "--")


if __name__ == "__main__":
    unittest.main()
