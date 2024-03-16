from collections import Counter
import math

from typing import List


class ThugOnlineGame:
    max_length_board: int
    board: List[str] = []
    alphabet: List[str]
    is_computer: bool

    def __init__(self, max_length_board, alphabet, is_computer):
        self.max_length_board: int = max_length_board
        self.alphabet: List[str] = alphabet
        self.is_computer: bool = is_computer

    def are_multisets_equal(self, multiset1, multiset2):
        return Counter(multiset1) == Counter(multiset2)

    def is_repetition(self) -> bool:

        for i in range(1,math.floor(len(self.board)/2)+1):
            for j in range(len(self.board)-2*i+1):
                word_left = self.board[j:j+i]
                word_right = self.board[j+i:j+2*i]
                if self.are_multisets_equal(word_left,word_right):
                    self.print_matching_sequences(range(j,j+i),range(j+i,j+2*i))

                    return True
                # print("left: ",word_left, 'right', word_right)
            # print()

        return False
    def play(self) -> None:

        print("\033[95mHello. Welcome to ThugOnlineGame version Abelian. The board looks like this right now: {}\033[0m".format(self.board))
        round_number = 1
        while True:
            print("\033[94m====== ROUND {} ======\033[0m".format(round_number))
            position = self.computer_round()
            letter = self.player_round()
            self.board.insert(position,letter)
            print("Board after this round looks like this: ", self.board)
            if self.is_repetition():
                print("Computer won. Maybe next time you will win :)")
                break

            if len(self.board) == self.max_length_board:
                print("Obviously, you are smarter than computer. Congrats!")
                break
            round_number+=1
    def print_matching_sequences(self,ind_1,ind_2):
        print("You lost because there is matching sequence: ", end = " ")
        for index, letter in enumerate(self.board):
            if index in ind_1:
                print('\033[92m' + letter + '\033[0m', end=" ")
            elif index in ind_2:
                print('\033[95m' + letter + '\033[0m', end=" ")
            else:
                print(letter, end = " ")
        print()

    def player_round(self) -> str:
        print(f"Choose letter from available alphabet: {self.alphabet}")
        letter = input()
        return letter

    def print_board(self) -> None:
        print(f"board: {self.board}")

    def computer_round(self) -> int:
        if len(self.board) == 0 or len(self.board) == 1:
            position = len(self.board)
        else:
            position = 1
        print("Computer chooses this position: \033[0m\033[91m{}\033[0m".format(position))
        return position

thug = ThugOnlineGame(20,["a","b","c","d","e","f"], True)
thug.play()


