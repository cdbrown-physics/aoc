#!/usr/bin/env python3

import logging
import argparse
import sys

from typing import List

def check_line(num_line: List[int]):
    last_num: int = 0
    # Check all increast or all decrease
    if num_line != sorted(num_line) and num_line != sorted(num_line, reverse=True):
        # Neither increasing or decreasing exit now
        logging.debug(f"{num_line} was neither increasing or decreasing")
        return False
    else:
        #Either increasing or decreasing, don't care which
        last_num = num_line[0]
        for n in num_line[1:]:
            diff = abs(n - last_num)
            if diff < 1 or diff > 3:
                logging.debug(f"{num_line} changes too fast: last_num={last_num}, n={n}")
                return False
            last_num = n
    return True

def second_check(num_line: List[int]):
    logging.debug(f"{num_line} Failed first trying second")
    for i in range(len(num_line)):
        tmp_num_line = num_line.copy()
        del tmp_num_line[i] # Remove a single entry
        if check_line(tmp_num_line): # Check again
            return True 
    return False

def PartOne(file_path: str):
    safe_count = 0
    with open(file_path, 'r') as file:
        for line in file:
            num_line = [int(n) for n in line.split()]
            logging.debug(num_line)
            b_safe = check_line(num_line)
            if b_safe:
                safe_count += 1
    print(f"Answer to part one: {safe_count}")
    
def PartTwo(file_path: str):
    safe_count = 0
    with open(file_path, 'r') as file:
        for line in file:
            num_line = [int(n) for n in line.split()]
            logging.debug(num_line)
            b_safe = check_line(num_line)
            if b_safe:
                safe_count += 1
            else:
                # Try removing bit
                b_second_safe = second_check(num_line)
                if b_second_safe:
                    safe_count += 1
    # print(f"Answer to part two: {safe_count}")
    
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