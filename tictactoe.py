#!/usr/bin/env python3
from enum import Enum
from typing import List, Optional
from copy import deepcopy
class Player(str, Enum):
    X = "X",
    O = "O"


class Diag(Enum):
    TOP_LEFT_TO_BOT_RIGHT = 0,
    TOP_RIGHT_TO_BOT_LEFT = 1


def main():
    play = True
    game_board = GameBoard()
    while play:
        game_board.play()
        again = str(input("Do you want to play again, type y to continue, any other input to stop: "))
        play = again == "y"
        game_board.reset()
    
    print("Bye!")

class Cell():
    def __init__(self, row: int, col: int) -> None:
        self.state: Optional[Player] = None
        self.row: int = row
        self.col: int = col

class GameBoard:
    def __init__(self):
        self.turn = Player.X
        self.turns: List[Cell] = []
        self.position: List[Cell] = []
        self.rows: List[List[Cell]] = [[], [], []]
        self.cols: List[List[Cell]] = [[], [], []]
        for row in range(3):
            for col in range(3):
                cell = Cell(row, col)
                self.position.append(cell)
                self.rows[row].append(cell)
                self.cols[col].append(cell)

    def play(self):
        while not self.finished():
            print('Input a square from 1-9 to move, x to undo')
            try:
                action = input(f"{self.turn.value} to play: ")
                self.move(action)
                self.display()
            except KeyboardInterrupt:
                return
            except:
                if action == "x":
                    last_action = self.turns.pop()
                    last_action.state = None
                    self.display()
                    self.turn = Player.X if self.turn == Player.O else Player.O
                    continue
                print('Invalid position')
        self.display_result()

    def reset(self):
        self.turn = Player.X
        for position in self.position:
            position.state = None

    def diag(self, diag: Diag) -> List[Cell]:
        cols = list(range(3))
        if diag == Diag.TOP_RIGHT_TO_BOT_LEFT:
            cols.reverse()
        return [row[col] for row, col in zip(self.rows, cols)]

    def move(self, action):
        position = int(action)

        if self.position[position - 1].state:
            print('Square already occupied')
            return

        self.position[position - 1].state = self.turn

        self.turn = Player.X if self.turn == Player.O else Player.O
        self.turns.append(self.position[position-1])

    def finished(self):
        if self.winner():
            return True

        return all(x.state for x in self.position)

    @staticmethod
    def calculate_list_result(player: Player, list: List[Cell]) -> bool:
        return  all(position.state == player for position in list)

    def winner(self) -> Optional[Player]:
        for player in list(Player):
            win_tests = deepcopy(self.rows) # Rows
            win_tests.extend(self.cols) # Cols
            win_tests.extend([self.diag(diag) for diag in list(Diag)]) # Diags

            for test in win_tests:
                if self.calculate_list_result(player, test):
                    return player

        return None

    def display(self):
        for row in self.rows:
            for cell in row:
                print(f"{cell.state}|" if cell.state else ' |', end='\n' if cell.col == 2 else '')

    def display_result(self):
        if winner:=self.winner():
            print(f"{winner} wins!")
        else:
            print('Draw')


if __name__ == '__main__':
    main()
