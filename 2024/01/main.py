#!/usr/bin/env python3

import logging
import argparse
import sys

def make_lists(args):
    list_one = []
    list_two = []
    with open(args.path, 'r') as file:
        for line in file:
            new_line = line.strip('\n')
            while '  ' in new_line:
                new_line = new_line.replace('  ', ' ')
            left, right = new_line.split()
            logging.debug(f"{left}, {right}")
            list_one.append(int(left))
            list_two.append(int(right))
    return list_one, list_two

def PartOne(args):
    left_list = []
    right_list = []
    distance = 0
    left_list, right_list = make_lists(args)
    left_list.sort()
    right_list.sort()
    logging.debug(left_list)
    logging.debug(right_list)
    for l, r in zip(left_list, right_list):
        distance += abs(l - r)
    print(f"Answer for part one is: {distance}")
    
def PartTwo(args):
    ref_list = []
    data_list = []
    similar = 0
    ref_list, data_list = make_lists(args)
    for n in ref_list:
        sim = data_list.count(n)
        similar += sim * n
    print(f"Answer for part two: {similar}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug level", default=20, type=int)
    parser.add_argument("-p", "--path", help="Path to the input file we want to use", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.debug)
    PartOne(args)
    PartTwo(args)