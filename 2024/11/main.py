#!/usr/bin/env python3

import logging
import argparse
from datetime import datetime as dt
from multiprocessing import Pool, cpu_count
from typing import List, Dict

NEW_NUMBERS: List[str] = [-1]*(10**8)

def get_data(file_path: str) -> List[int]:
    with open(file_path, 'r') as file:
        numbers = file.readline()
    numbers = [int(n) for n in numbers[0].split()]
    return numbers

def blink(numbers: List[str]) -> List[str]:
    # Rule 1: If zero make it 1
    # Rule 2: Number of digits een, split in two
    # Rule 3: Multiply by 2024
    # Append is slow, make list upfront and add
    # new_numbers: List[str] = [-1]*(len(numbers)*2)
    index = 0
    for n in numbers:
        str_n = str(n)
        l_str_n = len(str_n)
        if n == 0:
            # new_numbers.append(1)
            NEW_NUMBERS[index] = 1
            index += 1
        elif not l_str_n % 2:
            half_point = int(l_str_n/2)
            first_half = int(str_n[:half_point])
            second_half = int(str_n[half_point:])
            # new_numbers.append(first_half)
            # new_numbers.append(second_half)
            NEW_NUMBERS[index] = first_half
            index += 1
            NEW_NUMBERS[index] = second_half
            index += 1
        else:
            # new_numbers.append(n*2024)
            NEW_NUMBERS[index] = n * 2024
            index += 1
    return [n for n in NEW_NUMBERS if n >= 0]
    
def PartOne(file_path: str, blinks: int):
    numbers = get_data(file_path)
    for i in range(blinks):
        numbers = blink(numbers)
    print(f"Length of list after {blinks} blinks is {len(numbers)}")
    
def blink_number(args) -> int:
    blinks, number = args
    for i in range(blinks):
        number = blink(number)
    return len(number)

def PartTwo(file_path: str, blinks: int):
    """Any single digit number, loops"""
    numbers = get_data(file_path)
    logging.debug(f"{numbers}")
    answer = 0
    # Scales poorly, probably because of lots of memory moving around. Lets try
    # taking it piece wise. Take just one number, and blink it 75 times? Then 
    # do it for the next number?
    tasks = [(blinks, [n]) for n in numbers]
    with Pool(cpu_count()) as pool:
        results = pool.map(blink_number, tasks)
    answer = sum(results)
    print(f"Length of list after {blinks} blinks is {answer}")
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug level", default=20, type=int)
    parser.add_argument("-p", "--path", help="Path to the input file we want to use", type=str)
    parser.add_argument("-b", "--blinks", type = int)
    args = parser.parse_args()
    logging.basicConfig(level=args.debug)
    start = dt.now()
    blinks: int = args.blinks
    PartOne(args.path, blinks)
    print("Part one took: ", dt.now() - start)
    # start = dt.now()
    # PartTwo(args.path, blinks)
    # print("Part one took: ", dt.now() - start)
    
if __name__ == "__main__":
    main()
