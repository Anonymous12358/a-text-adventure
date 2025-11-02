import dataclasses
import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Room:
    keys: int = 0
    coins: int = 0


@dataclass
class Rooms:
    north: Room = dataclasses.field(default_factory=Room)
    south: Room = dataclasses.field(default_factory=Room)
    locked: bool = False


mode = sys.argv[1]
with open("instructions.txt", 'r') as inpFile:
    instructions = [line.strip() for line in inpFile.readlines()]
program_counter = -1


def print_info(*args, **kwargs):
    if mode == "0":
        print(*args, **kwargs)


def get_instruction():
    global program_counter
    if mode == "0":
        return input()
    else:
        program_counter += 1
        if program_counter >= len(instructions):
            program_counter = instructions.index("loop")
        if instructions[program_counter] == "loop":
            program_counter += 1
        return instructions[program_counter]


rooms = defaultdict(Rooms)
has_coin = False
has_key = False
easting = 0
northing = 0
while True:
    locked = rooms[easting].locked
    room = rooms[easting].north if northing else rooms[easting].south
    if northing == 0:
        print_info("You are in an infinite east–west corridor. A merchant stands in each room, touting their wares.")
        if locked:
            print_info("To your north is a locked door.")
        else:
            print_info("To your north is an unlocked door, leading to an anteroom.")
    else:
        print_info("You are in an anteroom with a chest, containing infinitely many gold coins.")
        print_info("To your south, a door leads back into the corridor.")
    print_info("Enter a command ('help' for help)")
    command = get_instruction()
    match command.split(" "):
        case ("help", *_):
            print_info("Commands list:")
            print_info("walk north, walk south, walk west, walk east")
            print_info("pickup coin, pickup key")
            print_info("drop coin, drop key")
            print_info("talk to merchant")
            print_info("buy key, buy nuke")
            print_info("lock door")
            print_info("unlock door")
            print_info("sweep floors")
        case ("walk", direction):
            if direction == "north" and not locked:
                northing = 1
            elif direction == "south":
                northing = 0
            elif direction == "west" and northing == 0:
                easting -= 1
            elif direction == "east" and northing == 0:
                easting += 1
        case ("pickup", obj):
            if obj == "coin" and not has_coin:
                if room.coins >= 1:
                    room.coins -= 1
                    has_coin = True
                elif northing == 1:
                    has_coin = True
            elif obj == "key" and not has_key and room.keys >= 1:
                room.keys -= 1
                has_key = True
        case ("drop", obj):
            if obj == "coin" and has_coin:
                has_coin = False
                room.coins += 1
            elif obj == "key" and has_key:
                has_key = False
                room.keys += 1
        case ("talk", "to", "merchant"):
            if northing == 0:
                print_info("I sell keys and nuclear bombs for one coin each. My stock is infinite!")
                if has_coin:
                    print("You have a coin. Would you like to buy something?")
                else:
                    print("Come back when you have a coin.")
        case ("buy", "key"):
            if northing == 0 and has_coin and not has_key:
                has_coin = False
                has_key = True
        case ("buy", "nuke"):
            if northing == 0 and has_coin:
                print_info("The nuclear bomb explodes. Game over!")
                break
        case ("lock", "door"):
            if northing == 0:
                locked = True
        case ("unlock", "door"):
            if northing == 0 and has_key:
                locked = False
        case ("sweep", "floors"):
            room.keys = 0
            room.coins = 0
        case _:
            print_info("Unknown command. Type 'help' for a list of commands.")
