import random
from collections import Counter
import math
from datetime import datetime
import os
from typing import List


class ThueOnlineGame:
    max_length_board: int
    board: List[str] = []
    alphabet: List[str]
    game_history: str = ""
    A_1: set = set()
    A_2: set = set()

    def __init__(self, max_length_board, alphabet):
        self.max_length_board: int = max_length_board
        self.alphabet: List[str] = alphabet


    @staticmethod
    def are_multisets_equal(multiset1, multiset2):
        return Counter(multiset1) == Counter(multiset2)

    @staticmethod
    def is_repetition(board) -> List:

        for i in range(1, math.floor(len(board)/2)+1):
            for j in range(len(board)-2*i+1):
                word_left = board[j:j+i]
                word_right = board[j+i:j+2*i]
                if ThueOnlineGame.are_multisets_equal(word_left, word_right):
                    return [True, range(j, j+i), range(j+i, j+2*i)]
                # print("left: ",word_left, 'right', word_right)
            # print()

        return [False]

    def play(self) -> None:

        print("\033[95mHello. Welcome to ThugOnlineGame version Abelian. The board looks "
              "like this right now: {}\033[0m".format(self.board))
        round_number = 1
        while True:
            print("\033[94m====== ROUND {} ======\033[0m".format(round_number))
            position = self.computer_round_tactic_2()
            letter = self.player_round()
            self.board.insert(position, letter)
            print("Board after this round looks like this: ", self.board)
            if self.is_repetition(self.board)[0]:
                self.print_matching_sequences(self.is_repetition(self.board)[1], self.is_repetition(self.board)[2])
                print("Computer won. Maybe next time you will win :)")
                self.update_game_history(round_number, position, letter)
                self.update_game_history("Computer won because there is repetition")
                break

            if len(self.board) == self.max_length_board:
                print("Obviously, you are smarter than computer. Congrats!")
                self.update_game_history(round_number, position, letter)
                self.update_game_history("Player won because board has max length")
                break
            self.update_game_history(round_number, position, letter)
            round_number += 1

        want_save_game = input("Do you want to save game? [y/n]")
        if want_save_game == "y":
            self.save_game()

    def update_game_history(self, round_number_or_info, position="", letter="") -> None:
        if position=="" and letter =="":
            self.game_history+= round_number_or_info
            return
        self.game_history += f"ROUND {round_number_or_info} \n"
        self.game_history += f"Position = {position}" + f". Letter = {letter} \n"
        self.game_history += f"Board = {self.board} \n \n"

    def save_game(self):
        formatted_datetime = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        path = f'games_history\game_{formatted_datetime}.txt'

        with open(path, 'w') as f:
            f.write(self.game_history)
            print("Game saved succesfully")

    def print_matching_sequences(self, ind_1, ind_2):
        print("You lost because there is matching sequence: ", end=" ")
        for index, letter in enumerate(self.board):
            if index in ind_1:
                print('\033[92m' + letter + '\033[0m', end=" ")
            elif index in ind_2:
                print('\033[95m' + letter + '\033[0m', end=" ")
            else:
                print(letter, end=" ")
        print()

    def player_round(self) -> str:
        print(f"Choose letter from available alphabet: {self.alphabet}")
        letter = input()
        while letter not in self.alphabet:
            print(f"This letter {letter} is not in {self.alphabet}. Please provide letter once again")
            letter = input()

        return letter

    def computer_round(self) -> int:
        if len(self.board) == 0 or len(self.board) == 1:
            position = len(self.board)
        else:
            for pos in range(len(self.board)+1):
                losing_position_counter = 0
                for letter in self.alphabet:
                    board_tmp = self.board.copy()
                    board_tmp.insert(pos, letter)
                    if self.is_repetition(board_tmp)[0]:
                        losing_position_counter += 1
                if losing_position_counter == len(self.alphabet):
                    print("hehe - you lost :)")
                    position = pos
                else:
                    position = 1
        print("Computer chooses this position: \033[0m\033[91m{}\033[0m".format(position))
        return position

    def computer_round_tactic_2(self) -> int:
        if len(self.board) == 0 or len(self.board) == 1:
            print("Computer chooses this position: \033[0m\033[91m{}\033[0m".format(len(self.board)))
            return len(self.board)
        if len(self.board)==2:
            self.A_1.add(self.board[0])
            self.A_2.add(self.board[1])
        else:
            letter_to_be_added = self.get_letter_from_board_not_in_A_1_A_2()
            if letter_to_be_added is not None:
                if len(self.A_1) > len(self.A_2):
                    self.A_2.add(letter_to_be_added)
                else:
                    self.A_1.add(letter_to_be_added)

        for i in range(len(self.board)):
            if self.board[i] in self.A_2:
                print("Computer chooses this position: \033[0m\033[91m{}\033[0m".format(i))
                return i

    def get_letter_from_board_not_in_A_1_A_2(self):
        for letter in self.board:
            if (letter not in self.A_1) and (letter not in self.A_2):
                return letter
        return None


thug = ThueOnlineGame(20, ["a", "b", "c", "d"])
thug.play()

