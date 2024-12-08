#!/usr/bin/env python3

import logging
import argparse
from typing import List, Dict

class Node:
    def __init__(self, value, parent):
        self.value = value
        self.children = []
        self.parent = parent
    def __repr__(self) -> str:
        return f"Value: {self.value}"
    def __str__(self):
        return f"Value: {self.value}"
    def add_child(self, operator, next_val):
        if operator == 'add':
            child_val = int(self.value) + int(next_val)
        elif operator == 'mul':
            child_val = int(self.value) * int(next_val) 
        elif operator == '||':
            child_val = int(str(self.value) + next_val)
            
        logging.debug(f"Adding child {child_val} to Parent node {self.value}")
        new_child_node = Node(child_val, self)
        self.children.append(new_child_node)
        return new_child_node
        
        

class Tree:
    def __init__(self, numbers):
        self.numbers = numbers
        self.root = Node(numbers[0], None)
        self.levels: Dict[int, List[Node]] = {0: [self.root]}
        self.operators: List[str] = ['add', 'mul']
        self.max_level: int = 0
    def __rerp__(self):
        return f"Root: {self.root}\nLevels: {self.levels}"
    def __str__(self):
        return f"Root: {self.root}\nLevels: {self.levels}"
    def add_level(self, level_num: int):
        if self.levels.get(level_num):
            raise KeyError(f"Level {level_num} already exsits.")
        elif level_num != self.max_level + 1:
            raise KeyError(f"Trying to add too high of a level: {level_num}. Max level right now is {self.max_level}")
        else:
            # import pdb; pdb.set_trace()
            self.levels[level_num] = []
            for node in self.levels[self.max_level]:
                logging.debug(f"Looking now at node: {node}")
                # For each node in the max level, try and add children.
                for op in self.operators:
                    new_node = node.add_child(op, self.numbers[self.max_level + 1])
                    self.levels[level_num].append(new_node)
        self.max_level += 1
            
def get_data(file_path: str):
    # Becasue of part two we want to keep the numbers as strings.
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            test_val, numbers = line.split(':')
            test_val = int(test_val)
            # Keep the numbers
            numbers = [n for n in numbers.split()]
            if data.get(test_val):
                raise KeyError("Test value already exists")
            else:
                data[test_val] = numbers
    return data

def PartOne(file_path: str):
    # Going to assume that there wont be dupliate test_vals
    data: Dict[int, List[int]] = get_data(file_path)
    good_data: int = 0
    for test_val in data:
        # import pdb;pdb.set_trace()
        tree = Tree(data[test_val])
        logging.debug(f"Starting new tree with root: {tree.root}")
        for lev in range(1,len(tree.numbers)):
            logging.debug(f"Trying to add level {lev}")
            tree.add_level(lev)
        logging.debug(f"Done building tree: {tree}")
        # Now that the tree is built. I need to look at all the base nodes, and see if any of their values are equal to the key.
        leafs = tree.levels[tree.max_level]
        logging.debug(f"Leafs for the tree are: {leafs}")
        for leaf in leafs:
            if leaf.value == test_val:
                logging.debug(f"WE FOUND A WINNER! {leaf.value}")
                good_data += int(test_val)
                break
    print("Answer to part one: ", good_data)
    
def PartTwo(file_path: str):
    # Going to assume that there wont be dupliate test_vals
    data: Dict[int, List[int]] = get_data(file_path)
    good_data: int = 0
    for test_val in data:
        # import pdb;pdb.set_trace()
        tree = Tree(data[test_val])
        tree.operators.append('||')
        logging.debug(f"Starting new tree with root: {tree.root}")
        for lev in range(1,len(tree.numbers)):
            logging.debug(f"Trying to add level {lev}")
            tree.add_level(lev)
        logging.debug(f"Done building tree: {tree}")
        # Now that the tree is built. I need to look at all the base nodes, and see if any of their values are equal to the key.
        leafs = tree.levels[tree.max_level]
        logging.debug(f"Leafs for the tree are: {leafs}")
        logging.debug(f"Checking against: {test_val} of type: {type(test_val)}")
        for leaf in leafs:
            if leaf.value == test_val:
                logging.debug(f"WE FOUND A WINNER! {leaf.value}")
                good_data += test_val
                break
    print("Answer to part two: ", good_data)
    
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