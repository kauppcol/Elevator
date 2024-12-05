'''
A class simulating an elevator
Assumptions: The elevator is iniitally vacant and must be requested from the outside. Once occupied, the elevator will travel to all
             selected floors, stopping to pick up any outside requests that want to go in the same direction as the elevator. Once all
             selected floors have been reached, the elevator will travel to the earliest unprocessed request or otherwise stop if there
             are no pending requests.

Features not implemented: Actual logic for opening/closing/moving up and down, emergency button, weight limits, etc.
'''

import time
from threading import Thread

class Elevator:
    def __init__(self, num_floors):
        self.num_floors = num_floors
        self.curr_floor = 0
        self.floor_set = set()
        self.request_list = []
        self.max_floor = 0
        self.min_floor = num_floors
        self.direction = 'UP'
        self.is_moving = False
        self.is_available = True
    
    def request_floor(self, floor, dir):
        # Add floor to request list, go to floor if elevator is free
        if (floor, dir) not in self.request_list:
            self.request_list.append((floor, dir))
            if self.is_available:
                self.move_to_request(floor)
    
    def move_to_request(self, floor):
        # Move to requested floor, elevator is now occupied
        self.is_moving = True
        while self.curr_floor < floor:
            self.move_up()
        while self.curr_floor > floor:
            self.move_down()
        self.open_doors()
        self.is_available = False
        self.close_doors()
        self.is_moving = False


    def select_floor(self, floor):
        if self.curr_floor == floor:
                self.open_doors()
                self.close_doors()
        else:
            # Update min/max floor selected and start moving if not already
            self.floor_set.add(floor)
            self.max_floor = max(floor, self.max_floor)
            self.min_floor = min(floor, self.min_floor)
            if not self.is_moving:
                self.direction = 'UP' if self.curr_floor < floor else 'DOWN'
                thread = Thread(target=self.move)
                thread.start()

    def move(self):
        self.is_moving = True
        
        # Travel to all selected floors
        while self.floor_set:

            # Move elevator in current direction until min/max floor requested is reached 
            if self.direction == 'UP':
                self.move_up()
            elif self.direction == 'DOWN':
                self.move_down()

            # Stop at any selected floors
            if self.curr_floor in self.floor_set:
                self.floor_set.remove(self.curr_floor)
                self.open_doors()
                self.close_doors()

                # Reset min/max floor if reached and change direction
                if self.curr_floor == self.max_floor:
                    self.max_floor = 0
                    self.direction = 'DOWN'

                if self.curr_floor == self.min_floor:
                    self.min_floor = self.num_floors
                    self.direction = 'UP'
            
            # Stop at floors requested from outside elevator if going in same direction
            if (self.curr_floor, self.direction) in self.request_list:
                self.request_list.remove((self.curr_floor, self.direction))
                self.open_doors()
                self.close_doors()
        
        # Go to earliest requested floor once elevator is empty
        if self.request_list:
            pair = self.request_list.pop(0)
            self.move_to_request(pair[0])
        else:
            # No pending requests, elevator is fully available
            self.is_available = True
        self.is_moving = False

    def move_down(self):
        print(f"Going Down to floor {self.curr_floor - 1}")
        time.sleep(1)
        self.curr_floor -= 1

    def move_up(self):
        print(f"Going Up to floor {self.curr_floor + 1}")
        time.sleep(1)
        self.curr_floor += 1

    def open_doors(self):
        print(f"Opening doors for floor {self.curr_floor}")
        time.sleep(1)

    def close_doors(self):
        print(f"Closing doors for floor {self.curr_floor}")
        time.sleep(1)

    def print_commands(self):
        print("\nCOMMANDS:")
        print("Floor number and direction (e.g. 1 UP or 2 DOWN): request the elevator to your floor")
        print("Floor number (e.g. 1): select a floor to go to (once inside elevator)")
        print("Open: open doors")
        print("Close: close doors")
        print("Help: print commands")
        print("Exit: exit simulator\n")

def main():
    floors = int(input("Enter the number of floors (not including ground floor): "))
    elevator = Elevator(floors)
    elevator.print_commands()

    while True:
        command = input().capitalize()
        if (split:= command.split()) and len(split) == 2 and split[0].isdigit() and 0 <= int(split[0]) <= floors and (split[1].upper() == 'UP' or split[1].upper() == 'DOWN'):
            elevator.request_floor(int(split[0]), split[1].upper())
        elif command.isdigit() and 0 <= int(command) <= floors:
            elevator.select_floor(int(command))
        elif command == "Open":
            elevator.open_doors()
        elif command == "Close":
            elevator.close_doors()
        elif command == "Help":
            elevator.print_commands()
        elif command == "Exit":
            return
        else:
            print("Invalid command entered")

if __name__ == "__main__":
    main()