#!/usr/bin/env python3

import logging
import argparse

from typing import List, Dict, Tuple

class Walker:
    def __init__(self, row_index: int, col_index: int, map_list: List[str]):
        self.row: int = row_index
        self.col: int = col_index
        self.map: List[str] = map_list
        self.score: int = 0
        self.summits: List[int] = []
        self.forks: List[int] = []
        self.value = 0

    def next_step_good(self, direction) -> bool:
        if direction == "up":
            next_row = self.row - 1
            next_col = self.col
        elif direction == "down":
            next_row = self.row + 1
            next_col = self.col
        elif direction == "left":
            next_row = self.row
            next_col = self.col - 1
        elif direction == "right":
            next_row = self.row
            next_col = self.col + 1
        else:
            raise ValueError(f"Invalid direction used {direction}")
        if int(self.map[next_row][next_col]) == self.value + 1:
            return True
        else:
            return False
        
    def step(self, direction):
        if direction == "up":
            self.row -= 1
        elif direction == "down":
            self.row += 1
        elif direction == "left":
            self.col -= 1
        elif direction == "right":
            self.col += 1
        else:
            raise ValueError(f"Invalid direction used {direction}")

    def check_all_directions(self):
        directions = ["up", "down", "left", "right"]
        for d in directions:
            if self.next_step_good(d):
                


def get_data(file_path: str) -> List[str]:

    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
        
def PartOne(file_path: str):
    map_list = get_data(file_path)
    logging.debug(map_list)
    # Get the row and column for all of the zero's
    for row_index in range(len(map_list)):
        for col_index in range(len(map_list[row_index])):
            if map_list[row_index][col_index] == '0':
                # Make a new walker starting at this location
                walker = Walker(row_index, col_index, map_list)



def PartTwo(file_path: str):
    pass
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug level", default=20, type=int)
    parser.add_argument("-p", "--path", help="Path to the input file we want to use", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.debug)
    PartOne(args.path)
    PartTwo(args.path)
    
if __name__ == "__main__":
    main()
