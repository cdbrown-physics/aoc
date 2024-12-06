#!/usr/bin/env python3

import logging
import argparse

from datetime import datetime as dt
from typing import List

def read_data(file_path: str):
    rules = {} # Dictionay of rules if base: after_numbers
    pages = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip('\n')
            if '|' in line: 
                # Then it's a rule line
                base, before = [n for n in line.split('|')]
                if base in rules:
                    rules[base].append(before)
                else:
                    rules[base] = [before]
            elif line: # Make sure line ins't empty
                pages.append(line.split(','))
    return rules, pages

def rotate_list(list: List):
    return list[1:] + list[:1]

def PartOne(rules: dict, pages: List[str]):
    logging.debug(rules)
    logging.debug(pages)
    answer = 0
    for page in pages:
        page_ok = True
        for p in range(len(page) - 1):
            # page[p] is the key I want to use
            ref_page = page[p]
            # Make sure all the pages after this are there.
            check_pages = page[p+1:] 
            rule_pages = rules.get(ref_page)
            if rule_pages is None:
                page_ok = False
                break
            if not all(n in rule_pages for n in check_pages):
                page_ok = False
                break
        # We didn't break
        if page_ok:
            logging.debug(f"Page {page} is ok.")
            #Now that it's ok, find the middle of it
            middle_index = (len(page) - 1 ) // 2
            logging.debug(f"middle index {middle_index}")
            answer += int(page[middle_index])
    # Now that I have the OK pages, I need the middle of all of them.
    print("Answer to part one: ", answer)
    
def PartTwo(rules: dict, pages: List[str]):
    logging.debug(rules)
    logging.debug(pages)
    answer = 0
    for page in pages:
        page_ok = True
        for p in range(len(page) - 1):
            # page[p] is the key I want to use
            ref_page = page[p]
            # Make sure all the pages after this are there.
            check_pages = page[p+1:] 
            rule_pages = rules.get(ref_page)
            if rule_pages is None:
                page_ok = False
                break
            if not all(n in rule_pages for n in check_pages):
                page_ok = False
                break
        # This page is bad, we need to try and fix it. 
        if not page_ok:
            logging.debug(f"Bad page is {page}.")
            correct_page = []
            while len(page) > 0:
                check_number = page[0]
                check_pages = page[1:] 
                rule_pages = rules.get(check_number)
                if all(n in rule_pages for n in check_pages):
                    # Number is next in the list
                    correct_page.append(check_number)
                    # Remove from page
                    page.pop(0)
                # If only one element left, just add it.
                if len(page) == 1:
                    correct_page.append(page[0])
                    page.pop(0)
                # If that wasn't the next number, rotate the list
                page = rotate_list(page)
                    
            #Now that it's ok, find the middle of it
            middle_index = (len(correct_page) - 1 ) // 2
            logging.debug(f"middle index {middle_index}")
            answer += int(correct_page[middle_index])
    # Now that I have the OK pages, I need the middle of all of them.
    print("Answer to part one: ", answer)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug level", default=20, type=int)
    parser.add_argument("-p", "--path", help="Path to the input file we want to use", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.debug)
    rules, pages = read_data(args.path)
    # start_one = dt.now()
    PartOne(rules, pages)
    # print("Time for part one", dt.now() - start_one)
    # start_two = dt.now()
    PartTwo(rules, pages)
    # print("Time for part two", dt.now() - start_two)
    
if __name__ == "__main__":
    main()