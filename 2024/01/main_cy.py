#!/usr/bin/env python3
"""Base python file that is nothing fancy."""
import cython
import logging
import argparse
import sys

def make_lists(file_path:cython.basestring):
    list_one = []
    list_two = []
    with open(file_path, 'r') as file:
        for line in file:
            new_line = line.strip('\n')
            while '  ' in new_line:
                new_line = new_line.replace('  ', ' ')
            left, right = new_line.split()
            logging.debug(f"{left}, {right}")
            list_one.append(int(left))
            list_two.append(int(right))
    return list_one, list_two

def PartOne(file_path):
    left_list = []
    right_list = []
    distance = 0
    left_list, right_list = make_lists(file_path)
    left_list.sort()
    right_list.sort()
    logging.debug(left_list)
    logging.debug(right_list)
    for l, r in zip(left_list, right_list):
        distance += abs(l - r)
    print(f"Answer for part one is: {distance}")
    
def PartTwo(file_path):
    ref_list = []
    data_list = []
    similar = 0
    ref_list, data_list = make_lists(file_path)
    for n in ref_list:
        sim = data_list.count(n)
        similar += sim * n
    print(f"Answer for part two: {similar}")
    
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