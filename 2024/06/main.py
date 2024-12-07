#!/usr/bin/env python3

import logging
import argparse

from datetime import datetime as dt
from typing import List, Dict

MAX_STEPS = 10**5

class Guard:
    def __init__(self, room_map: List[str]):
        self.position = {'row': '', 'col': ''}
        self.room_map = room_map
        self.direction = "up"
        self.starting_positions = {'row': '', 'col': ''}
        self.original_map = room_map.copy()
    
    def set_starting_position(self):
        # Get the index's of the guards starting position. row and column/element
        for row in range(len(self.room_map)):
            for element in range(len(self.room_map[row])):
                if self.room_map[row][element] in "^<>v":
                    self.position['row'] = row
                    self.position['col'] = element
                    self.starting_positions['row'] = row
                    self.starting_positions['col'] = element
                    return 
                else:
                    # logging.debug(f"Nothing found in {row},{element}")
                    pass
                    
    def mark_x(self):
        """String are immutable, so in order to replace the old character with an X we need to make a new string.
        I know the column I want to replace so using everything excluding self.position['col'] and then adding the X,
        then everything after that should do the trick. """
        # import pdb; pdb.set_trace()
        self.room_map[self.position['row']] = self.room_map[self.position['row']][0:self.position['col']] + \
                                              'X' + \
                                              self.room_map[self.position['row']][self.position['col'] + 1:]
    
    def move(self):
        if self.direction == 'up':
            # Check the next space, if not a '#' then set guard position to be that.
            if self.room_map[self.position['row'] - 1][self.position['col']] == '#':
                if self.position['row'] - 1 < 0:
                    raise IndexError("This problem can't have negative index")
                self.direction = "right"
            else:
                self.mark_x()
                self.position['row'] -= 1
        elif self.direction == "right":
            if self.room_map[self.position['row']][self.position['col'] + 1] == '#':
                self.direction = "down"
            else:
                self.mark_x()
                self.position['col'] += 1
        elif self.direction == "down":
            if self.room_map[self.position['row'] + 1][self.position['col']] == '#':
                self.direction = "left"
            else:
                self.mark_x()
                self.position['row'] += 1
        elif self.direction == "left":
            if self.room_map[self.position['row']][self.position['col'] - 1] == '#':
                if self.position['col'] - 1 < 0:
                    raise IndexError("This problem can't have negative index")
                self.direction = "up"
            else:
                self.mark_x()
                self.position['col'] -= 1
        else:
            raise ValueError(f"Invalid direction: {self.direction}")
    
    def print_map(self):
        for line in self.room_map:
            print(line)

def get_room_map(file_path: str) -> List[str]:
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
             
            
def PartOne(guard: Guard):
    logging.debug(guard.position)
    guard.set_starting_position()
    answer = 0 # Start at one because code exists when about to leave, so 1 shy
    while (0 < guard.position["row"] < len(guard.room_map)) or (0 < guard.position['col'] < len(guard.room_map[0])):
        logging.debug("Starting loop")
        try:
            guard.move()
        except IndexError:
            logging.debug(guard.position)
            guard.mark_x() # Mark one last X
            # We should be out of the room now
            for row in guard.room_map:
                answer += row.count('X')
            break
    print("Answer to part one: ", answer)
    return guard
    
def PartTwo(guard: Guard):
    answer = 0
    path_walked: Dict[int, List[int]] = {}
    # Get all the steps taken on the normal rout 
    for row in range(len(guard.room_map)):
        steps = [int(i) for i, litteral in enumerate(guard.room_map[row]) if litteral == 'X']
        path_walked[row] = steps
    logging.debug(path_walked)
    start = dt.now()
    for row in path_walked:
        for spot in path_walked[row]:
            tmp_map = guard.original_map.copy()
            logging.debug(f"{row}, {spot}, {type(row)}, {type(spot)}")
            # Place an object but ontop of the guard.
            # import pdb; pdb.set_trace()
            tmp_map[row] = tmp_map[row][0:spot] + '#' + tmp_map[row][spot + 1:]
            tmp_guard = Guard(tmp_map)
            tmp_guard.set_starting_position()
            if not tmp_guard.position['row']:
                continue
            step_count: int = 0
            logging.debug(f"{row}, {spot}")
            logging.debug(tmp_guard.position["row"])
            while (0 < tmp_guard.position["row"] < len(tmp_guard.room_map)) or (0 < tmp_guard.position['col'] < len(tmp_guard.room_map[0])):
                # logging.debug("Starting loop")
                try:
                    tmp_guard.move()
                    step_count += 1
                except IndexError:
                    logging.debug(tmp_guard.position)
                    # We should be out of the room now
                    logging.debug(f"Placing an object at {row} {spot} did not keep the guard in a loop")
                    break
                if step_count > MAX_STEPS:
                    logging.debug(f"Got stuck in a loop with object placed at row:{row} col:{spot}")
                    answer += 1
                    break
            logging.debug("Moving onto the next position")
            del tmp_guard
            del tmp_map
    print("main loop took: ", dt.now() - start)
    print("Answer to part two: ", answer)
                    
            
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug level", default=20, type=int)
    parser.add_argument("-p", "--path", help="Path to the input file we want to use", default = "",type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.debug)
    room_map = get_room_map(args.path)
    guard = Guard(room_map)
    guard = PartOne(guard)
    PartTwo(guard)
    
if __name__ == "__main__":
    main()