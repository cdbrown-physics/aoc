#!/usr/bin/env python3
"""Scanning for XMAS in data"""
import logging
import argparse

from typing import List, Tuple

def scan_direction(x_index: Tuple[int], lines:List[str], direction:str)->bool:
    logging.debug(f"Checking{x_index}")
    line_ref = x_index[0]
    x_ref = x_index[1]
    if direction == 'right':
        a = b = c = 0
        d,e,f = 1,2,3
    elif direction == 'left':
        a = b = c = 0
        d,e,f = -1,-2,-3
    elif direction == "up":
        a,b,c = -1,-2,-3
        d = e = f = 0
    elif direction == "down":
        a,b,c = 1,2,3
        d=e=f=0
    elif direction == "diag_up_right":
        a,b,c = -1,-2,-3
        d,e,f = 1,2,3
    elif direction == "diag_up_left":
        a,b,c = -1,-2,-3
        d,e,f = -1,-2,-3
    elif direction == "diag_down_right":
        a,b,c = 1,2,3
        d,e,f = 1,2,3
    elif direction == "diag_down_left":
        a,b,c = 1,2,3
        d,e,f = -1,-2,-3
    else:
        logging.warning("Bad direction passed as input")
        raise ValueError
    try:
        # For the first time python negative indexing has hurt me.
        if (line_ref + a) < 0 or  (line_ref + b) < 0 or (line_ref + c) < 0:
            raise IndexError
        if (x_ref + d) < 0 or (x_ref + e) < 0 or (x_ref + f) < 0:
            raise IndexError
        m_char = lines[line_ref + a][x_ref + d]
        a_char = lines[line_ref + b][x_ref + e]
        s_char = lines[line_ref + c][x_ref + f]
        
        if m_char == 'M' and a_char == 'A' and s_char == 'S':
            logging.debug(f"found solution x_index: {x_index} going direction {direction}")
            logging.debug(f"mchar: {m_char} achar: {a_char} schar: {s_char}")
            return True
    except IndexError:
        logging.debug(f"Checking {direction}brings index out of range. Must be false")
        return False

def scan_mas(a_index: Tuple[int], lines:List[str])->bool:
    line_ref = a_index[0]
    a_ref = a_index[1]
    try:
        # For the first time python negative indexing has hurt me.
        if (line_ref - 1) < 0 or (a_ref - 1) < 0:
            raise IndexError
        top_left = lines[line_ref - 1][a_ref - 1]
        top_right = lines[line_ref - 1][a_ref + 1]
        bot_left = lines[line_ref + 1][a_ref - 1]
        bot_right = lines[line_ref + 1][a_ref + 1]
        if top_right in 'AX\n' or top_left in 'AX\n' or bot_left in 'AX\n' or bot_right in 'AX\n':
            return False
        elif top_left == bot_right or top_right == bot_left: 
            return False
        elif top_left == bot_left and top_right == bot_right:
            return True
        elif top_left == top_right and bot_left == bot_right:
            return True
        else:
            logging.warning("I didn't think of this path")
            logging.warning(f"\n{top_left} . {top_right}\n. A .\n{bot_left} . {bot_right}")
            
    except IndexError:
        logging.debug(f"Checking {a_index}brings index out of range. Must be false")
        return False
    
def PartOne(file_path: str):
    answer = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = tuple(lines) # Lines need to be read only
    x_indexs = []
    for idx in range(len(lines)):
        x_indexs.extend([(idx, i) for i, c in enumerate(lines[idx]) if c == 'X'])
        logging.debug(x_indexs)
    directions = ['right','left','up','down','diag_up_right',"diag_up_left","diag_down_right","diag_down_left"]
    for x_index in x_indexs:
        for direction in directions:
            if scan_direction(x_index, lines, direction):
                answer += 1
                logging.debug(answer)
    print(f"Answer to part one: {answer}")
    
def PartTwo(file_path: str):
    answer = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = tuple(lines) # Lines need to be read only
    a_indexs = []
    for idx in range(len(lines)):
        a_indexs.extend([(idx, i) for i, c in enumerate(lines[idx]) if c == 'A'])
        logging.debug(a_indexs)
    for a_index in a_indexs:
        if scan_mas(a_index, lines):
            answer += 1
            logging.debug(answer)
    print(f"Answer to part one: {answer}")
    
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