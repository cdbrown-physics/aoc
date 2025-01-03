#!/usr/bin/env python3

import logging
import argparse

from typing import List, Dict, Tuple

def get_data(file_path: str):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data

def next_space_match(row: int, col: int, map: Dict, char: str, direction: str) -> bool:
    if direction == "up":
        next_row = row - 1
        next_col = col
    elif direction == "down":
        next_row = row + 1
        next_col = col
    elif direction == "left":
        next_row = row
        next_col = col - 1
    elif direction == "right":
        next_row = row
        next_col = col + 1
    else:
        raise ValueError(f"Invalid direction used {direction}")
    if 0 <= next_row < len(map) and 0 <= next_col < len(map[0]):
        try:
            if map[next_row][next_col] == char:
                return True, next_row, next_col
            else:
                return False, None, None
        except:
           return False, None, None
    else:
        return False, None, None

def check_if_val_in_dict(groups_dict: Dict, new_coordinate: Tuple) -> Tuple[bool, int]:
    for key, value in groups_dict.items():
        if new_coordinate in value:
            return True, key
    return False, None
 
def get_regions(map):
    groups_dict: Dict[int, List[int]] = {}
    row_len: int = len(map[0])
    groups_key: int = 0 # Can't use characters because of repeats, just use numbers
    for row in range(len(map)):
        for col in range(row_len):
            position = (row, col)
            # Need to look at all the neighbors and if any of them are in an 
            # existing place, then add it to that region
            value_match, key = check_if_val_in_dict(groups_dict, position)
            if not value_match:
                # Then this is the first time I'm seeing this square. Create a
                # new 'region'. Key will be a number, value is list of tuple 
                # coordinates
                groups_dict[groups_key] = [position]
                char = map[row][col]
                for d in ["down", "right"]:
                    char_match, n_row, n_col = next_space_match(row, col, map, char, d)
                    if char_match:
                        # Then we're part of this group
                        groups_dict[groups_key].append((n_row, n_col))
                groups_key += 1 # Tick up the 'new' key value
            else:
                # We've seen this square before, need to add any neighbor 
                # matches, to it's existing region
                char = map[row][col]
                for d in ["up", "down", "left", "right"]:
                    char_match, n_row, n_col = next_space_match(row, col, map, char, d)
                    if char_match:
                        # Then we're part of this group
                        if (n_row, n_col) not in groups_dict[key]:
                            groups_dict[key].append((n_row, n_col))
    return groups_dict

def get_perimeter(region: List[Tuple[int]]) -> int:
    perimeter: int = 0
    for square in region:
        perimeter += 4
        s_row, s_col = square
        for other_square in region:
            o_row, o_col = other_square
            if s_row == o_row -1 and s_col == o_col:
                perimeter -= 1
            elif s_row == o_row + 1 and s_col == o_col:
                perimeter -= 1
            elif s_row == o_row and s_col == o_col - 1:
                perimeter -= 1
            elif s_row == o_row and s_col == o_col + 1:
                perimeter -= 1
    return perimeter

def PartOne(file_path: str):
    """How do I find regons? Start with the first character. Look at the 4 next
    to it. If they match then mark it as part of that region. Move to the next 
    square. If that coordinate is part of the dictionary, keep adding to that 
    one, else make a new entry, and do the four neighbors again."""
    map: List[str] = get_data(file_path)
    logging.debug(map)
    groups_dict = get_regions(map)
    logging.debug(groups_dict)
    # Now that I have the regions. I need to find the area, and parimater of that region.
    total_price: int = 0
    for key, value in groups_dict.items():
        area = len(value)
        logging.debug(f"Area of region {key} is {area}")
        perimeter = get_perimeter(value)
        logging.debug(f"Perimeter of region {key} is {perimeter}")
        total_price += (area * perimeter)
    print("Answer for part one is ", total_price)

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
