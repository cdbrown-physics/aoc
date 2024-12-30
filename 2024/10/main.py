#!/usr/bin/env python3

import logging
import argparse

from typing import List, Dict, Tuple

def get_data(file_path: str) -> List[str]:
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

def next_step_good(row_index: int, col_index: int, map_list: List[str], value: int, direction: str):
    """Look in a set direction and see if it's a valid place to 'move'."""
    logging.debug(f"Starting at {row_index}, {col_index} with value {value}")
    next_value = value + 1
    good_step = False
    if direction == 'up':
        next_row = row_index -1
        next_col = col_index
    elif direction == "down":
        next_row = row_index + 1
        next_col = col_index
    elif direction == "left":
        next_row = row_index
        next_col = col_index - 1
    elif direction == "right":
        next_row = row_index
        next_col = col_index + 1
    if 0 <= next_row < len(map_list) and 0 <= next_col < len(map_list[0]):
        # We are in bounds
        if int(map_list[next_row][next_col]) == next_value:
            logging.debug(f"{next_row} {next_col} is good to step")
            good_step = True
        else:
            logging.debug(f"{next_row}, {next_col} is a bad step with value {int(map_list[next_row][next_col])}")
    return good_step

def step(row_index: int, col_index: int, direction: str) -> List[int]:
    if direction == 'up':
        return [row_index - 1, col_index]
    elif direction == "down":
        return [row_index + 1, col_index]
    elif direction == "left":
        return [row_index, col_index - 1]
    elif direction == "right":
        return [row_index, col_index + 1]
    else:
        raise ValueError(f"Invalid direction passed into 'step' method {direction}")

def walk_path(row_index: int, 
              col_index: int, 
              map_list: List[str], 
              value: int, 
              direction: str) -> Tuple[List[int], bool, int]:
    step_taken = False
    current_spot = [row_index, col_index]
    if next_step_good(row_index, col_index, map_list, value, direction):
        current_spot = step(row_index, col_index, direction)
        value += 1
        step_taken = True
        return current_spot, step_taken, value
    else:
        return current_spot, step_taken, value
                
def find_score(row_index: int, col_index: int, map_list: List[str]) -> int:
    # I'm starting at a zero. Need to see where we can step to.
    # There's 4 directions we can look. up/down/left/right
    value: int = 0
    score: int = 0
    current_spot = [row_index, col_index]
    hills_found = []
    directions = ["up", "down", "left", "right"]
    while True:
        for direction in directions:
            current_spot, step_taken, value = walk_path(current_spot[0], 
                                                        current_spot[1], 
                                                        map_list, 
                                                        value, 
                                                        direction)
        if value == 9:
            logging.debug(f"Found a hill top at {current_spot}")
            hills_found.append(current_spot)
            break
        
def PartOne(file_path: str):
    map_list = get_data(file_path)
    logging.debug(map_list)
    # Get the row and column for all of the zero's
    for row_index in range(len(map_list)):
        for col_index in range(len(map_list[row_index])):
            if map_list[row_index][col_index] == '0':
                # I'm starting at a zero, and want to find the 'sore' for that starting point
                path_score = find_score(row_index, col_index, map_list)

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
