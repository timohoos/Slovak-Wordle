from collections import Counter
from enum import Enum


class State(str, Enum):
    NOT_USED = "not used"
    NOT_PRESENT = "not present"
    WRONG_PLACEMENT = "wrong placement"
    CORRECT_PLACEMENT = "correct placement"


class Game:
    MAX_GUESSES = 6

    def __init__(self, word):
        self.word = word
        self.correct = False
        self.overall_state = {letter: State.NOT_USED for letter in
                              "aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž"}
        self.guesses_state = []

    def check_word(self, guess, letter_count, guess_state):
        correct = True

        for i in range(len(guess)):
            if self.word[i] == guess[i]:
                letter = self.word[i]
                letter_count[letter] -= 1
                self.overall_state[letter] = State.CORRECT_PLACEMENT
                guess_state[i] = State.CORRECT_PLACEMENT
            else:
                correct = False

        return correct

    def check_letters(self, guess, letter_count, guess_state):
        for i, letter in enumerate(guess):
            if guess_state[i] == State.CORRECT_PLACEMENT:
                continue
            if letter in letter_count:
                if letter_count[letter] > 0:
                    letter_count[letter] -= 1
                    if self.overall_state != State.CORRECT_PLACEMENT:
                        self.overall_state[letter] = State.WRONG_PLACEMENT
                    guess_state[i] = State.WRONG_PLACEMENT
            else:
                self.overall_state[letter] = State.NOT_PRESENT

    def add_guess(self, guess):
        guess_state = [State.NOT_PRESENT for _ in range(len(guess))]
        letter_count = Counter(self.word)
        self.correct = self.check_word(guess, letter_count, guess_state)
        self.check_letters(guess, letter_count, guess_state)
        guess_info = {
            "guess": guess,
            "guess_state": guess_state
        }
        self.guesses_state.append(guess_info)

    def add_guesses(self, guesses):
        for guess in guesses:
            self.add_guess(guess)
