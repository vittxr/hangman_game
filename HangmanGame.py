import json
import random
from hangman_sprites import hangman_sprites
from custom_types import Word


class HangmanGame:
    def __init__(self) -> None:
        self.__word: Word = self.__get_random_word()
        self.theme: str = self.__word.get("theme")
        self.word_length = len(self.__word.get("name"))
        self.masked_word = ["_"] * self.word_length
        self.guesses: int = 0
        self.max_guesses: int = 6
        self.guessed_letters: list[str] = []
        self.letters: list[str] = []
        self.game_over: bool = False
        self.is_player_victorious: bool = False
        self.endgame_message: None | str = None

    def __get_random_word(self) -> Word:
        with open("./db/words.json", mode="r") as file:
            words = json.load(file)
        return random.choice(words)

    def __finish_game(self, is_winner: bool) -> None:
        self.is_player_victorious = is_winner
        self.game_over = True
        if is_winner:
            self.endgame_message = "Parabéns! Você acertou a palavra"
        else:
            self.endgame_message = (
                f"Infelizmente você errou. A palavra era '{self.__word.get('name')}'"
            )

    def guess_letter(self, letter: str) -> None:
        if len(letter) > 1:
            raise ValueError("Você deve inserir apenas um caractere")

        self.letters.append(letter)

        if letter in self.__word.get("name"):
            for letter_idx, _letter in enumerate(self.__word.get("name")):
                if _letter == letter:
                    print("letter_idx", letter_idx)
                    self.masked_word[letter_idx] = _letter
                    self.guessed_letters.append(_letter)

            if self.word_length == len(self.guessed_letters):
                self.__finish_game(is_winner=True)
        else:
            self.guesses += 1
            if self.guesses == self.max_guesses:
                self.__finish_game(is_winner=False)

    def guess_word(self, word: str) -> None:
        if word.rstrip() == self.__word.get("name"):
            return self.__finish_game(is_winner=True)

        self.guesses += 1
        if self.guesses == self.max_guesses:
            return self.__finish_game(is_winner=False)
