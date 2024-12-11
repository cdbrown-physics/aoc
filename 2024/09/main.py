#!/usr/bin/env python3

import logging
import argparse

from datetime import datetime as dt
from typing import List, Dict, Tuple

def sort_element(the_list: List[str]) -> Tuple[List[str], bool]:
    free_space = next((c for c,v in enumerate(the_list) if v == -1), None)
    keep_sorting = False
    if free_space is not None: 
        data_to_move = next((i for i, v in enumerate(reversed(the_list)) if v != -1), None)
        # Because I reversed the list, I need to get the actual index in the original list.
        data_to_move = len(the_list) - 1 - data_to_move
        logging.debug(f"The free space is at {free_space}. The data to move is at {data_to_move}")
        if data_to_move > free_space:
            keep_sorting = True
            the_list[free_space] = the_list[data_to_move]
            the_list[data_to_move] = -1
    return the_list, keep_sorting

def sort_two(the_list: List[str]) -> Tuple[List[str], bool]:
    """Rather than getting one character of free space, need to look for a whole section"""
    

def get_checksum(the_list: List[str]) -> int:
    check_sum = 0
    for n in range(len(the_list)):
        if the_list[n] > 0:
            check_sum += n * the_list[n]
    return check_sum
         
def PartOne(file_path: str):
    with open(file_path, 'r') as file:
        line = file.readline() # Input is only 1 line file.
    file_free = 1
    the_list = [] # Can't do a string need to deal with numbers greater than ascii
    file_id = 0
    for char in line:
        logging.debug(f"{char} {file_free}")
        if file_free % 2:
            the_list = the_list + [file_id]*int(char)
            file_id += 1
            file_free += 1
        else:
            the_list = the_list + [-1]*int(char)
            file_free += 1
    logging.debug(the_list)
    keep_sorting = True
    start = dt.now()
    while keep_sorting:
        the_list, keep_sorting = sort_element(the_list)
    logging.debug(the_list)
    print("While loop took: ", dt.now() - start)
    # Now get 
    answer = get_checksum(the_list)
    
    print("Answer to part one is: ", answer)
            
def PartTwo(file_path: str):
    with open(file_path, 'r') as file:
        line = file.readline() # Input is only 1 line file.
    file_free = 1
    the_list = [] # Can't do a string need to deal with numbers greater than ascii
    free_dict = {}
    file_dict = {}
    file_id = 0
    # Rather than making a list, make a dictionary type thing with the space avalible? 
    # OR same data setup, but keep track of the free spaces with a dictionary {starting_index: size}
    for char in line:
        logging.debug(f"{char} {file_free}")
        if file_free % 2:
            file_dict[len(the_list)] = (int(char), file_id)
            the_list = the_list + [file_id]*int(char)
            file_id += 1
            file_free += 1
        else:
            free_dict[len(the_list)] = int(char)
            the_list = the_list + [-1]*int(char)
            file_free += 1
    logging.debug(the_list)
    logging.debug(free_dict)
    keep_sorting = True
    start = dt.now()
    while keep_sorting:
        the_list, keep_sorting = sort_two(file_dict, free_dict)
    logging.debug(the_list)
    print("While loop took: ", dt.now() - start)
    # Now get 
    answer = get_checksum(the_list)
    
    print("Answer to part one is: ", answer)

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug level", default=20, type=int)
    parser.add_argument("-p", "--path", help="Path to the input file we want to use", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.debug)
    # PartOne(args.path)
    PartTwo(args.path)
    
if __name__ == "__main__":
    main()
