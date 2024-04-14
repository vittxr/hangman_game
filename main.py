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
        if self.guesses == self.max_guesses:
            return self.__finish_game(is_winner=False)

        if word == self.__word.get("name"):
            self.__finish_game(is_winner=True)


class GameUI:
    def __init__(self):
        self.start()

    def start(self) -> None:
        opt = None
        while opt != "3":
            print("\n[1] Jogar")
            print("[2] Consultar tabela de pontuações")
            print("[3] Sair")

            opt = input()

            match opt:
                case "1":
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
                        wins_count = 1
                        if players_scores.get(player_name):
                            if players_scores.get(player_name).get("wins_count"):
                                wins_count = (
                                    players_scores[player_name]["wins_count"] + 1
                                )

                        players_scores[player_name] = {
                            **players_scores.get(player_name, {}),
                            "wins_count": wins_count,
                        }
                    else:
                        loses_count = 1

                        if players_scores.get(player_name):
                            if players_scores.get(player_name).get("loses_count"):
                                loses_count = (
                                    players_scores[player_name]["loses_count"] + 1
                                )

                        players_scores[player_name] = {
                            **players_scores.get(player_name, {}),
                            "loses_count": loses_count,
                        }

                    os.system("clear")

                    print(f"JOGO FINALIZADO, {player_name}")
                    print(game.endgame_message)
                    print("\nStatus do jogador: ")
                    print(
                        "\tNúmero de vitórias: ",
                        players_scores.get(player_name).get("wins_count", 0),
                    )
                    print(
                        "\tNúmero de derrotas:",
                        players_scores.get(player_name).get("loses_count", 0),
                    )

                    with open("./db/players_scores.json", "w") as f:
                        json.dump(players_scores, f)

                case "2":
                    with open("./db/players_scores.json", mode="r") as file:
                        players_scores = json.load(file)
                        sorted_players = sorted(
                            players_scores.items(),
                            key=lambda x: x[1].get(
                                "wins_count", x[1].get("loses_count", 0)
                            ),
                            reverse=True,
                        )

                        for player, stats in sorted_players:
                            print(
                                f"\n{player}: \n\tQtd. de vitórias: {stats.get('wins_count', 0)} \n\tQtd. de derrotas: {stats.get('loses_count', 0)}"
                            )
                case "3":
                    exit()

                case _:
                    print("opção inválida")


GameUI()
