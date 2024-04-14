import os
import json
import random
from typing import TypedDict
from hangman_sprites import hangman_sprites


class Word(TypedDict):
    name: str
    theme: str


class HangmanGame:
    def __init__(self) -> None:
        self.__word: Word = self.__get_random_word()
        self.theme: str = self.__word.get("theme")
        self.word_length = len(self.__word.get("name"))
        self.masked_word = ["_"] * self.word_length
        self.guesses: int = 0
        self.max_guesses: int = 7
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
        self.is_player_victorious = True
        self.game_over = True
        if is_winner:
            self.endgame_message = "Parabéns! Você acertou a palavra"
        else:
            self.endgame_message = (
                f"Infelizmente você errou. A palavra era {self.__word.get('name')}"
            )

    # TODO: add decorator to check if letter is string.
    def guess_letter(self, letter: str) -> None:
        if len(letter) > 1:
            raise ValueError("Você deve inserir apenas um caractere")

        self.letters.append(letter)

        if letter in self.__word.get("name"):
            letter_idx = self.__word.get("name").index(letter)
            self.masked_word[letter_idx] = letter

            self.guessed_letters.append(letter)
            if self.word_length == len(self.guessed_letters):
                self.__finish_game(is_winner=True)
        else:
            self.guesses += 1
            if self.guesses == self.max_guesses:
                self.__finish_game(is_winner=False)

    def guess_word(self, word: str) -> None:
        self.guesses += 1
        if word == self.__word:
            self.__finish_game(is_winner=True)


# TODO: All text should be stored in a file called text.py
class GameUI:
    def __init__(self):
        self.start()

    def start(self) -> None:
        game = HangmanGame()
        with open("./db/players_scores.json", mode="r") as file:
            players_scores = json.load(file)

        player_name = input("Digite o nome do jogador: ")

        while not game.game_over:
            print(f"TEMA - {game.theme}")
            print(hangman_sprites[game.guesses])

            print(" ".join(game.masked_word))

            print("[1] - Adivinhar letra")
            print("[2] - Adivinhar palavra")
            option = input()

            try:
                match option:
                    case "1":
                        print("Digite a letra: ")
                        char = input()
                        game.guess_letter(char)
                    case "2":
                        print("Digite a palavra")
                        word = input()
                        game.guess_word(word)
                    case _:
                        print("Opção inválida!")
            except Exception as e:
                print(e)

        if game.is_player_victorious:
            win_count = 1
            if players_scores.get(player_name):
                win_count = players_scores[player_name]["win_count"] + 1

            players_scores[player_name] = {"win_count": win_count}
        else:
            loses_count = 1
            if players_scores.get(player_name):
                win_count = players_scores[player_name]["loses_count"] + 1

            players_scores[player_name] = {"loses_count": loses_count}

        os.system("cls")
        print(f"JOGO FINALIZADO, {player_name} \n")
        print(game.endgame_message)
        print("Status do jogador: ")
        print("Número de vitórias: ", players_scores.get(player_name).get("win_count"))
        print(
            "Número de derrotas: ", players_scores.get(player_name).get("loses_count")
        )

        with open("./db/players_scores") as f:
            f.write(players_scores)


GameUI()
