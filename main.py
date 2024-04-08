import json
import os
import random
from typing import TypedDict

class Word(TypedDict):
    name: str
    theme: str

class HangmanGame:
    def __init__(self) -> None:
        self.__word: str = self.__get_random_word()
        self.guesses: int = 0
        self.max_guesses: int = 6
        self.guessed_letters: list[str] = []
        self.letters: list[str] = []
        self.game_over: bool = False

    def __get_random_word(self) -> Word:
        with open("words_db.json") as file:
            words = json.load(file)
        return random.choice(words)
    
    def guess(letter: str): 
        pass 

game = HangmanGame()
# game.__get_random_word()
# print(game.__word)
