import json
import random
from typing import TypedDict


class Word(TypedDict):
    name: str
    theme: str


class HangmanGame:
    def __init__(self) -> None:
        self.__word: Word = self.__get_random_word()
        self.word_length = len(self.__word.get("name"))
        self.guesses: int = 0
        self.max_guesses: int = 6
        self.guessed_letters: list[str] = []
        self.letters: list[str] = []
        self.game_over: bool = False

    def __get_random_word(self) -> Word:
        with open("words_db.json") as file:
            words = json.load(file)
        return random.choice(words)

    # TODO: add decorator to check if letter is string.
    def guess(self, letter: str):
        self.letters.append(letter)
        if letter in self.__word:
            return self.guessed_letters.append(letter)
        else:
            self.guesses += 1
            if self.guesses == self.max_guesses:
                self.game_over = True


game = HangmanGame()
print("word_length: ", game.word_length)
# game.__get_random_word()
# print(game.__word)
