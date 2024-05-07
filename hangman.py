import random

class PlayHangman:
    def __init__(self):
        self.word = ChooseWord().choose()
        self.remaining_attempts = 6
        self.game_over = False
        self.draw_man = DrawMan()
        self.is_letter_in = IsLetterIn(self.word)

    def play(self):
        while not self.game_over:
            print("Current Word:", self.is_letter_in.get_masked_word())
            guess = input("Guess a letter: ").lower()
            if not IsInputValid().is_valid(guess):
                print("Invalid input. Please enter a valid letter.")
                continue
            if self.is_letter_in.is_letter_in(guess):
                print("Correct guess!")
                if self.is_letter_in.is_word_guessed():
                    self.game_over = True
                    print("Congratulations! You've guessed the word:", self.word)
            else:
                print("Incorrect guess!")
                self.remaining_attempts -= 1
                if self.remaining_attempts == 0:
                    self.game_over = True
                    print("Game over! The word was:", self.word)
            self.draw_man.draw_hangman(self.remaining_attempts)
            if self.is_letter_in.get_masked_word() == self.word:
                self.game_over = True
                print("Congratulations! You've guessed the word:", self.word)


class DrawMan:
    @staticmethod
    def draw_hangman(remaining_attempts):
        stages = [ 
            r"""
                --------
                |      |
                |      O
                |     \\|
                |      |
                |     / \\
                -
            """,
            r"""
                --------
                |      |
                |      O
                |     \\|
                |      |
                |     / 
                -
            """,
            r"""
                --------
                |      |
                |      O
                |     \\|
                |      |
                |      
                -
            """,
            r"""
                --------
                |      |
                |      O
                |     \|
                |      |
                |     
                -
            """,
            r"""
                --------
                |      |
                |      O
                |      |
                |      |
                |     
                -
            """,
            r"""
                --------
                |      |
                |      O
                |    
                |      
                |     
                -
            """,
            r"""
                --------
                |      |
                |      
                |    
                |      
                |     
                -
            """
        ]
        print(stages[remaining_attempts])



class IsLetterIn:
    def __init__(self, word):
        self.word = word
        self.guesses = []

    def is_letter_in(self, letter):
        self.guesses.append(letter)
        return letter in self.word

    def get_masked_word(self):
        return ''.join([char if char in self.guesses else '_' for char in self.word])

    def is_word_guessed(self):
        return set(self.word) == set(self.guesses)


class IsInputValid:
    @staticmethod
    def is_valid(letter):
        return len(letter) == 1 and letter.isalpha() and letter.islower()


class ChooseWord:
    @staticmethod
    def choose():
        word_pool = ['hangman', 'python', 'programming', 'computer', 'keyboard', 'internet', 'game', 'hang', 'man', 'play', 'guess', 'word', 'letter', 'code', 'fun']
        return random.choice(word_pool)


# Main
def main():
    game = PlayHangman()
    game.play()


if __name__ == "__main__":
    main()
