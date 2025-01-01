#!/usr/bin/env python3

import logging
import argparse

from typing import List, Dict, Tuple

class Walker:
    def __init__(self, row_index: int, col_index: int, map_list: List[str], part:int = 1):
        self.row: int = row_index
        self.col: int = col_index
        self.map: List[str] = map_list
        self.score: int = 0
        self.summits: List[int] = []
        self.forks: List[int] = []
        self.value = 0
        self.possible_steps = []
        self.forks: Dict[List[int], List[str]] = {}
        self.part = part

    def next_step_good(self, direction: str) -> bool:
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
        if 0 <= next_row < len(self.map) and 0 <= next_col < len(self.map[0]):
            try:
                if int(self.map[next_row][next_col]) == self.value + 1:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False
        
    def step(self, direction: str):
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
        self.value += 1

    def check_all_directions(self):
        directions = ["up", "down", "left", "right"]
        could_step: List[str] = []
        for d in directions:
            if self.next_step_good(d):
                could_step.append(d)
        return could_step

    def back_to_fork(self):
        """Go back to the highest value of fork."""
        max_key = 0
        for key in self.forks:
            if key[2] >= max_key:
                self.row = key[0]
                self.col = key[1]
                self.value = key[2]
                max_key = self.value
        logging.debug(f"Going back to {self.row} {self.col}")


    def walk_path(self):
        while True:
            logging.debug(f"Keys {self.forks}")
            if self.value == 9:
                logging.debug(f"Found a summit at {self.row} {self.col}")
                if self.part == 1:
                    if (self.row, self.col) not in self.summits:
                        self.summits.append((self.row, self.col))
                        self.score += 1
                else:
                    self.score += 1
                self.back_to_fork()
            self.possible_steps = self.check_all_directions()
            if len(self.possible_steps) == 0:
                logging.debug(f"No good steps to take at {self.row} {self.col}")
                if self.forks:
                    self.back_to_fork()
                else:
                    return
            elif len(self.possible_steps) == 1:
                # If there's only one possible step, then just take it.
                logging.debug(f"Only one good possible step to take at {self.row} {self.col}")
                self.step(self.possible_steps[0])
                self.possible_steps.pop()
            else:
                # Make a note of the fork in the road.
                logging.debug(f"Multiple paths to take from {self.row} {self.col}. Value {self.value}")
                fork_key = (self.row, self.col, self.value)
                if fork_key not in self.forks:
                    logging.debug(f"Adding key {fork_key}")
                    self.forks[fork_key] = self.possible_steps.copy()
                # Move in one of those directions, lets pick -1 direction.
                self.step(self.forks[fork_key][-1])
                self.forks[fork_key].pop() # Now that I've gone down that path, remove it from forks
                if len(self.forks[fork_key]) == 0:
                    # No more paths to look down after this, remove it from list of forks.
                    del self.forks[fork_key] 
    
def get_data(file_path: str) -> List[str]:
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
        
def PartOne(file_path: str):
    map_list = get_data(file_path)
    logging.debug(map_list)
    total_score: int = 0
    # Get the row and column for all of the zero's
    for row_index in range(len(map_list)):
        for col_index in range(len(map_list[row_index])):
            if map_list[row_index][col_index] == '0':
                # Make a new walker starting at this location
                walker = Walker(row_index, col_index, map_list, 1)
                walker.walk_path()
                total_score += walker.score
    print(f"Answer to part one: {total_score}")

def PartTwo(file_path: str):
    """Don't know if this method will work. Might need to do a linked list type of thing?
    Problem is that if the dictionary has a key. then I fall on that spot again.
    Maybe I just always use the highest value?"""
    map_list = get_data(file_path)
    logging.debug(map_list)
    total_score: int = 0
    # Get the row and column for all of the zero's
    for row_index in range(len(map_list)):
        for col_index in range(len(map_list[row_index])):
            if map_list[row_index][col_index] == '0':
                # Make a new walker starting at this location
                walker = Walker(row_index, col_index, map_list, part=2)
                walker.walk_path()
                total_score += walker.score
    print(f"Answer to part two: {total_score}")
    
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
