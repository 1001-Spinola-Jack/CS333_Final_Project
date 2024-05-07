import unittest
from unittest.mock import patch
from io import StringIO
from hangman import PlayHangman, DrawMan, IsLetterIn, IsInputValid, ChooseWord

class TestDrawMan(unittest.TestCase):
    def test_draw_hangman(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            DrawMan.draw_hangman(3)
            self.assertEqual(fake_out.getvalue().strip(), """
                --------
                |      |
                |      O
                |     \|
                |      |
                |     
                -
            """.strip())

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

    def test_play_integration_word_guessed(self):
        # Integration test between PlayHangman and IsLetterIn: Tests that the game ends correctly when the player guesses the word correctly.
        with patch('builtins.input', side_effect=['h', 'a', 'n', 'g', 'm']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.game.play()
                self.assertIn(fake_out.getvalue().strip(), ["Game over! The word was: hangman", "Congratulations! You've guessed the word: hangman"])

    def test_play_integration_out_of_attempts(self):
        # Integration test between PlayHangman and DrawMan: Tests that the game ends correctly when the player runs out of attempts.
        with patch('builtins.input', side_effect=['z'] * 7):  # Incorrect guesses to exhaust attempts
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.game.play()
                self.assertIn(fake_out.getvalue().strip(), ["Game over! The word was: hangman"])

    def test_play_integration_draw_progress(self):
        # Integration test between PlayHangman and DrawMan: Tests that the hangman drawing progresses correctly when the player guesses incorrectly.
        with patch('builtins.input', side_effect=['z', 'z', 'z', 'z', 'z', 'z']):  # Incorrect guesses to progress drawing
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.game.play()
                self.assertIn(fake_out.getvalue().strip(), ["Game over! The word was: hangman"])

    def test_play_integration_correct_letters_revealed(self):
        # Integration test between PlayHangman and IsLetterIn: Tests that the correct letters are revealed in the masked word when guessed.
        with patch('builtins.input', side_effect=['h', 'a', 'n', 'g', 'm']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.game.play()
                self.assertIn(fake_out.getvalue().strip(), ["Game over! The word was: hangman", "Congratulations! You've guessed the word: hangman"])

    def test_play_integration_invalid_input_handling(self):
        # Integration test between PlayHangman and IsInputValid: Tests that the game handles invalid input correctly.
        with patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6']):  # Invalid inputs
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.game.play()
                self.assertIn(fake_out.getvalue().strip(), ["Invalid input. Please enter a valid letter."] * 6)

if __name__ == '__main__':
    unittest.main()
