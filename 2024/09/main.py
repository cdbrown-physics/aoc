#!/usr/bin/env python3

import logging
import argparse
import sys

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

def move_file(file_dict: Dict[int, Tuple[int]], free_dict: Dict[int, int], free_index: int, file_index: int):
    # import pdb; pdb.set_trace()
    file_size = file_dict[file_index][0]
    new_free_index = free_index + file_size
    if free_dict[free_index] - file_size > 0:
        free_dict[new_free_index] = free_dict[free_index] - file_size
    # Move the starting index of the file that's been moved
    if free_index in file_dict:
        logging.error(f"Trying to add file to index that already esists {free_index}")
        logging.error(f"{file_dict}")
        sys.exit(-1)
    file_dict[free_index] = file_dict[file_index]
    # Delete the old values
    del file_dict[file_index]
    del free_dict[free_index]
    # Sort the dictionaries again to make sure we're ok
    free_dict = dict(sorted(free_dict.items()))
    file_dict = dict(sorted(file_dict.items()))
    logging.debug(f"After moving free_dict: {free_dict} file_dict: {file_dict}")
    return file_dict, free_dict

def sort_two(file_dict: Dict[int, Tuple[int]], free_dict: Dict[int, int]) -> Tuple[Dict[int, Tuple[int]], Dict[int, int]]:
    """Rather than getting one character of free space, need to look for a whole section. Look for the lowest key, and 
    see if it fits the file I want to move. 
    Going to assume that the 'free_dict' dictionary is 'ordered'
    file_dict: dictionary of files. Key is the starting index space, and the two tuple values are the size and file index"""
    # import pdb; pdb.set_trace()
    list_of_indexs = sorted(file_dict.keys())
    for k in reversed(list_of_indexs):
        free_dict = dict(sorted(free_dict.items()))
        for free_index in free_dict:
            if free_index > k:
                logging.debug("Stop looking for free space. Cannot move right")
                break
            logging.debug(f"Looking to see if file {k} can move to {free_index}")
            if free_dict[free_index] >= file_dict[k][0]:
                logging.debug(f"Room to move file")
                # There is space to move the file to the free spot
                file_dict, free_dict = move_file(file_dict, free_dict, free_index, k)
                break
            # If there's no space on this free space, then move on to the next one.
    # File dictionary should be sorted now.
    return file_dict, free_dict

def get_checksum(the_list: List[str]) -> int:
    check_sum = 0
    for n in range(len(the_list)):
        if the_list[n] > 0:
            check_sum += n * the_list[n]
    return check_sum

def get_checksum_two(file_dict: Dict[int, Tuple[int]]):
    answer: int = 0
    for file_starting_index in file_dict:
        file_size = file_dict[file_starting_index][0]
        file_id = file_dict[file_starting_index][1]
        curent_index = file_starting_index
        for _ in range(file_size):
            answer += curent_index * file_id
            curent_index += 1
    return answer
         
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
    file_index = 0
    free_dict = {}
    file_dict = {}
    file_id = 0
    # Rather than making a list, make a dictionary type thing with the space avalible? 
    # OR same data setup, but keep track of the free spaces with a dictionary {starting_index: size}
    for char in line:
        # logging.debug(f"{char} {file_free}")
        if file_free % 2:
            # if char != '0':
            file_dict[file_index] = (int(char), file_id)
            file_index += int(char)
            file_id += 1
            file_free += 1
        else:
            if char != '0':
                free_dict[file_index] = int(char)
            file_index += int(char)
            file_free += 1
    logging.debug(free_dict)
    start = dt.now()
    og_file_dict = file_dict.copy()
    og_free_dict = free_dict.copy()
    file_dict, free_dict = sort_two(file_dict, free_dict)
    logging.debug(f"Post sorting file_dict: {file_dict}, free_dict: {free_dict}")
    print("While loop took: ", dt.now() - start)
    import pdb; pdb.set_trace()
    answer = get_checksum_two(file_dict)
    print("Answer to part two is: ", answer)

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
