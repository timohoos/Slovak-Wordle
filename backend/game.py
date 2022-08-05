from collections import Counter


class Game:
    def __init__(self, word):
        self.word = word
        self.correct = False
        self.overall_state = {
            "ĺ": "not used",
            "ľ": "not used",
            "š": "not used",
            "č": "not used",
            "ť": "not used",
            "ž": "not used",
            "ď": "not used",
            "ý": "not used",
            "á": "not used",
            "é": "not used",
            "ó": "not used",
            "q": "not used",
            "w": "not used",
            "e": "not used",
            "r": "not used",
            "t": "not used",
            "z": "not used",
            "u": "not used",
            "i": "not used",
            "o": "not used",
            "p": "not used",
            "ú": "not used",
            "ä": "not used",
            "a": "not used",
            "s": "not used",
            "d": "not used",
            "f": "not used",
            "g": "not used",
            "h": "not used",
            "j": "not used",
            "k": "not used",
            "l": "not used",
            "ô": "not used",
            "ň": "not used",
            "y": "not used",
            "x": "not used",
            "c": "not used",
            "v": "not used",
            "b": "not used",
            "n": "not used",
            "m": "not used"
        }
        self.guesses_state = []

    def check_word(self, guess, letter_count, guess_state):
        correct = True

        for i in range(len(guess)):
            if self.word[i] == guess[i]:
                letter = self.word[i]
                letter_count[letter] -= 1
                self.overall_state[letter] = "correct placement"
                guess_state[i] = "correct placement"
            else:
                correct = False

        return correct

    def check_letters(self, guess, letter_count, guess_state):
        for i, letter in enumerate(guess):
            if guess_state[i] == "correct placement":
                continue
            if letter in letter_count:
                if letter_count[letter] > 0:
                    letter_count[letter] -= 1
                    if self.overall_state != "correct placement":
                        self.overall_state[letter] = "wrong_placement"
                    guess_state[i] = "wrong placement"
            else:
                self.overall_state[letter] = "not present"

    def add_guess(self, guess):
        guess_state = ["not present" for _ in range(len(guess))]
        letter_count = Counter(self.word)
        self.correct = self.check_word(guess, letter_count, guess_state)
        self.check_letters(guess, letter_count, guess_state)
        self.guesses_state.append(guess_state)

    def add_guesses(self, guesses):
        for guess in guesses:
            self.add_guess(guess)
