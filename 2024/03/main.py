#!/usr/bin/env python3

import logging
import argparse
import sys
import re

from typing import List

def PartOne(file_path: str):
    answer = 0
    matches = []
    pattern = r"mul\((\d+),(\d+)\)"
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        matches.extend(re.findall(pattern, line))
        logging.debug(matches)
    # I've got matches of all of numbers, need to turn them into numbers. 
    for match in matches: 
        # List of tuples
        answer += int(match[0]) * int(match[1])
        logging.debug(answer)
    print(f"Answer to part one: {answer}")


def PartTwo(file_path: str):
    answer = 0
    matches = []
    # regex will return a list of 4 entires, based on the order of the regex patern. These are the indexes of what gets
    # found at what point.
    mul_a = 0
    mul_b = 1
    do_index = 2
    dont_index = 3
    b_multiply = True
    pattern = r"mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))"
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        matches.extend(re.findall(pattern, line))
        logging.debug(matches)
    # I've got matches of all of numbers, need to turn them into numbers. 
    for match in matches: 
        logging.debug(match)
        # List of tuples
        if match[do_index]:
            b_multiply = True
        elif match[dont_index]:
            b_multiply = False
        elif b_multiply:
            answer += int(match[mul_a]) * int(match[mul_b])
        else:
            continue

        logging.debug(answer)
    print(f"Answer to part two: {answer}")
    
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