#!/usr/bin/env python3

import logging
import argparse
import string

from typing import List, Dict, Tuple

def get_antennas(file_path: str) -> List[List[str]]:
    data = []
    global MAP_WIDTH
    global MAP_HIGHT
    # Can't do flat data, need to know if something is to far to the left or right and a flat data set want do that. 
    with open(file_path, 'r') as file:
        for line in file:
           data.append(line.strip())
    MAP_WIDTH = len(data[0])
    MAP_HIGHT = len(data)
    return data

def node_in_map(node:Tuple[int]):
    return 0 <= node[0] < MAP_WIDTH and 0 <= node[1] < MAP_HIGHT
        
def find_antinodes(antanne_positions: List[Tuple[int]]):
    """In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency
    - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas 
    with the same frequency, there are two antinodes, one on either side of them."""
    node_count: int = 0
    for a in range(len(antanne_positions)):
        base_ant = antanne_positions[a]
        for second_ant in antanne_positions[a+1:]:
            logging.debug(f"Looking at {base_ant}, {second_ant}")
            rise = base_ant[1] - second_ant[1]
            run = base_ant[0] - second_ant[0]
            # Check all 4 possible positions
            node1 = (base_ant[0] + run, base_ant[1] + rise)
            node2 = (base_ant[0] - run, base_ant[1] - rise)
            node3 = (second_ant[0] + run, second_ant[1] + rise)
            node4 = (second_ant[0] - run, second_ant[1] - rise)
            if node1 != second_ant and node_in_map(node1) and not node_dict.get(node1):
                logging.debug(f"Found node1 at {node1}")
                node_dict[node1] = True
                node_count += 1
            elif node2 != second_ant and node_in_map(node2) and not node_dict.get(node2):
                logging.debug(f"Found a node2 at {node2}")
                node_dict[node2] = True
                node_count += 1
            if node3 != base_ant and node_in_map(node3) and not node_dict.get(node3):
                logging.debug(f"Found a node3 at {node3}")
                node_dict[node3] = True
                node_count += 1
            elif node4 != base_ant and node_in_map(node4) and not node_dict.get(node4):
                logging.debug(f"Found a node4 at {node4}")
                node_dict[node4] = True
                node_count += 1
    return node_count

def find_antinodes_h(antanne_positions: List[Tuple[int]]):
    """In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency
    - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas 
    with the same frequency, there are two antinodes, one on either side of them."""
    node_count: int = 0
    for a in range(len(antanne_positions)):
        base_ant = antanne_positions[a]
        for second_ant in antanne_positions[a+1:]:
            if not node_dict.get(base_ant):
                node_dict[base_ant] =True
                node_count += 1
            logging.debug(f"Looking at {base_ant}, {second_ant}")
            rise = base_ant[1] - second_ant[1]
            run = base_ant[0] - second_ant[0]
            # Check all possible positions
            loop=1
            while True:
                node = (base_ant[0] + run*loop, base_ant[1] + rise*loop)
                if not node_in_map(node):
                    break
                elif not node_dict.get(node):
                    logging.debug(f"Found a node at {node}")
                    node_dict[node] = True
                    node_count += 1
                else:
                    pass
                loop += 1
            # Reset and go the other direction 
            loop = 1
            while True:
                node = (base_ant[0] - run*loop, base_ant[1] - rise*loop)
                if not node_in_map(node):
                    break
                elif not node_dict.get(node):
                    logging.debug(f"Found a node at {node}")
                    node_dict[node] = True
                    node_count += 1
                else:
                    pass
                loop += 1
    return node_count
                
def PartOne(file_path: str):
    data = get_antennas(file_path)
    antannes:str = string.ascii_letters + string.digits
    answer = 0
    global node_dict
    node_dict = {}
    for antanne in antannes:
        # Get all antanne positions
        logging.debug(f"Looking for antinodes for {antanne}.")
        # Store the data as col, row so that it's (x, y)
        antanne_positions: List[Tuple[int]] = [(col, row) for row in range(len(data)) for col in range(len(data[row])) if data[row][col] == antanne]
        if logging.DEBUG and len(antanne_positions) > 0 :
            logging.debug(f"For antanne {antanne} we found {antanne_positions}")
        answer += find_antinodes(antanne_positions)
    print(f"Answer to part one: {answer}")
    del node_dict

    
def PartTwo(file_path: str):
    data = get_antennas(file_path)
    antannes:str = string.ascii_letters + string.digits
    answer = 0
    global node_dict
    node_dict = {}
    for antanne in antannes:
        # Get all antanne positions
        logging.debug(f"Looking for antinodes for {antanne}.")
        # Store the data as col, row so that it's (x, y)
        antanne_positions: List[Tuple[int]] = [(col, row) for row in range(len(data)) for col in range(len(data[row])) if data[row][col] == antanne]
        if logging.DEBUG and len(antanne_positions) > 0 :
            logging.debug(f"For antanne {antanne} we found {antanne_positions}")
        answer += find_antinodes_h(antanne_positions)
    print(f"Answer to part one: {answer}")
    
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