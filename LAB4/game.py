import random
from words import WORDS, HINTS
from stats import SessionStats

DIFFICULTIES = {
    "easy": {"lives": 8, "base_score": 3, "hint_penalty": 1},
    "medium": {"lives": 6, "base_score": 5, "hint_penalty": 1},
    "hard": {"lives": 4, "base_score": 8, "hint_penalty": 2},
}


class HangmanGame:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.stats = SessionStats()
        self.difficulty = "medium"
        self.category = "technology"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 6
        self.hint_used = False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.secret)

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        if (
            not isinstance(letter, str)
            or len(letter) != 1
            or not letter.isascii()
            or not letter.isalpha()
        ):
            return "Enter one letter."
        letter = letter.lower()
        if letter in self.guessed or letter in self.wrong:
            return "Already guessed."
        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."
        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return None
        self.hint_used = True
        penalty = DIFFICULTIES[self.difficulty]["hint_penalty"]
        self.score = max(0, self.score - penalty)
        return HINTS.get(self.secret, "No hint available.")

    def play_round(self):
        self.start_round()
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print("Lives:", self.lives, "Score:", self.score, "Streak:", self.streak)
            raw = input("Letter, /hint, or /quit: ").strip().lower()
            if raw == "/quit":
                return False
            if raw == "/hint":
                hint = self.use_hint()
                print(hint if hint else "Hint already used.")
                continue
            print(self.guess(raw))

        if self.won():
            self.streak += 1
            base_score = DIFFICULTIES[self.difficulty]["base_score"]
            self.score += base_score + self.streak
            self.stats.record(True, self.streak)
            print("Solved:", self.secret)
            return True

        self.streak = 0
        self.stats.record(False, self.streak)
        print("Out of lives. The word was:", self.secret)
        return True

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")
        while True:
            print("\nCategories:", ", ".join(WORDS))
            print("Difficulties:", ", ".join(DIFFICULTIES))
            difficulty = input("Choose difficulty or q: ").strip().lower()
            if difficulty == "q":
                return
            if difficulty not in DIFFICULTIES:
                print("Unknown difficulty.")
                continue
            raw = input("Choose category or q: ").strip().lower()
            if raw == "q":
                return
            if raw not in WORDS:
                print("Unknown category.")
                continue
            self.difficulty = difficulty
            self.category = raw
            if not self.play_round():
                return
            again = input("Another round? [y/n]: ").strip().lower()
            if again != "y":
                print(
                    "Final score:", self.score,
                    " Streak:", self.streak,
                    " Rounds:", self.stats.rounds,
                    " Wins:", self.stats.wins,
                    " Best streak:", self.stats.best_streak,
                )
                return
