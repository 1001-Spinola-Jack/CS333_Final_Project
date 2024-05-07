import unittest
from io import StringIO
from unittest.mock import patch
from hangman import PlayHangman, DrawMan, IsLetterIn, IsInputValid, ChooseWord

class TestDrawMan(unittest.TestCase):
    def test_draw_hangman(self):
        with StringIO() as fake_out:
            DrawMan.draw_hangman(3)
            expected_output = """
                --------
                |      |
                |      O
                |     \\|/
                |      |
                |     / \\
                -
            """.strip()
            self.assertEqual(fake_out.getvalue().strip(), expected_output)

class TestIsLetterIn(unittest.TestCase):
    def setUp(self):
        self.word = 'hangman'
        self.is_letter_in = IsLetterIn(self.word)

    def test_is_letter_in(self):
        self.assertTrue(self.is_letter_in.is_letter_in('a'))
        self.assertFalse(self.is_letter_in.is_letter_in('z'))

    def test_get_masked_word(self):
        self.is_letter_in.guesses = ['a', 'n']
        self.assertEqual(self.is_letter_in.get_masked_word(), 'an___an')

    def test_is_word_guessed(self):
        self.is_letter_in.guesses = list(self.word)
        self.assertTrue(self.is_letter_in.is_word_guessed())
        self.assertFalse(self.is_letter_in.is_letter_in('z'))

class TestIsInputValid(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(IsInputValid().is_valid('a'))
        self.assertTrue(IsInputValid().is_valid('z'))
        self.assertFalse(IsInputValid().is_valid('A'))
        self.assertFalse(IsInputValid().is_valid('1'))
        self.assertFalse(IsInputValid().is_valid(''))

class TestChooseWord(unittest.TestCase):
    def test_choose(self):
        self.assertIn(ChooseWord().choose(), ['hangman', 'python', 'programming', 'computer', 'keyboard', 'internet', 'game', 'hang', 'man', 'play', 'guess', 'word', 'letter', 'code', 'fun'])

class TestPlayHangman(unittest.TestCase):
    def setUp(self):
        self.game = PlayHangman()


    def test_play_integration_out_of_attempts(self):
        with StringIO() as fake_out, patch('builtins.input', side_effect=['z'] * 7):  # Incorrect guesses to exhaust attempts
            self.game.play()
            self.assertIn("Game over! The word was: hangman", fake_out.getvalue().strip())

    def test_play_integration_draw_progress(self):
        with StringIO() as fake_out, patch('builtins.input', side_effect=['z', 'z', 'z', 'z', 'z', 'z']):  # Incorrect guesses to progress drawing
            self.game.play()
            self.assertIn("Game over! The word was: hangman", fake_out.getvalue().strip())

    def test_play_integration_correct_letters_revealed(self):
    # Define side effect for input function to return valid input repeatedly
        side_effect = ['h', 'a', 'n', 'g', 'm']  # Adjust the values as needed

        with StringIO() as fake_out, patch('builtins.input', side_effect=side_effect):
            self.game.play()
            # Check if the expected output is present in fake_out
            self.assertIn("Congratulations! You've guessed the word:", fake_out.getvalue())

    def test_play_integration_invalid_input_handling(self):
    # Define side effect for input function to return invalid input repeatedly
        side_effect = ['1', '2', '3', '4', '5', '6']  # Adjust the values as needed

        with StringIO() as fake_out, patch('builtins.input', side_effect=side_effect):
            self.game.play()
        # Add assertions to check the behavior of the game after invalid input


def test_play_integration_word_guessed(self):
    # Define side effect for input function to return valid input repeatedly
        side_effect = ['h', 'a', 'n', 'g', 'm']  # Add more values if needed

        with StringIO() as fake_out, patch('builtins.input', side_effect=side_effect):
            self.game.play()
            # Check if the expected output is present in fake_out
            self.assertIn("Congratulations! You've guessed the word:", fake_out.getvalue())




if __name__ == '__main__':
    unittest.main()
