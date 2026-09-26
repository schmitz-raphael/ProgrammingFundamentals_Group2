
from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.intro import IntroRoom
from escaperoom.rooms.malware import MalwareRoom
from escaperoom.transcript import Transcriptor


from dataclasses import dataclass, asdict
import json

class Engine:

    def __init__(self, transcript_name):
        self.gamestate = GameState()
        self.transcriptor = Transcriptor(transcript_name)
        self.rooms = {}
        self.init_rooms()


    # TODO: Assign room instances once they're implemented
    def init_rooms(self):
        self.rooms["intro"] = IntroRoom()
        self.rooms["soc"] = None
        self.rooms["dns"] = None
        self.rooms["vault"] = None
        self.rooms["malware"] = MalwareRoom()


    def play(self):
        print("[Game] Cyber Escape Room started. Type 'help' for commands.")
        while True:
            command = input("> ")
            tokens = command.split()
            match tokens[0]:
                case "quit":
                    print("[Game] Goodbye. Transcript written to run.txt")
                    break
                # Simply prints the room description of the room set in the gamestate  
                case "look":
                    print(self.rooms[self.gamestate.current_room].description)
                case "move":
                    if (len(tokens > 1)):
                        self.move(tokens[1])
                    else:
                        print("Please enter the name of a room.")
                case "inspect":
                    if (len(tokens > 1)):
                        self.inspect(tokens[1])
                    else:
                        print("Please enter the name of the item you want to inspect.")
                case "use":
                    if (len(tokens > 1)):
                        self.use(tokens[1])
                    else:
                        print("Please enter the name of the item you want to use.")
                case "inventory":
                    self.print_inventory()
                case "hint":
                    self.hint()
                case "save":
                    if (len(tokens > 1)):
                        self.save(tokens[1])
                    else:
                        print("Please enter a filename for your save file.")
                    self.save(tokens[1])
                case "load":
                    if (len(tokens > 1)):
                        self.load_save(tokens[1])
                    else:
                        print("Please enter the name of the file you want to load.")
                case "help":
                    self.help()
                case _:
                    print("Command not recognised. Enter 'help' to look for allowed commands")
        self.transcriptor.save_file()

    def help(self):
        print("Available commands:")
        print("look - prints the description of the current room")
        print("move <room_name> - moves to the specified room")
        print("inspect <item_name> - inspects the specified item in the current room")
        print("use <item_name> - uses the specified item in the current room")
        print("inventory - shows the items in your inventory")
        print("hint - a small help if you're stuck")
        print("save <file> - saves the current game state to a file")
        print("load <file> - loads a game state from a file")
        print("quit - exits the game")

    def move(self, room_name):
        if room_name in self.rooms.keys():
            #check if the player is not already in the room he wants to move to
            if (self.gamestate.current_room == room_name):
                print("You are already inside this room.")
            #player needs to be in the intro lobby to go to different rooms
            elif (self.gamestate.current_room != "intro" and room_name != "intro"):
                print("You need to return to the intro lobby before going to another room")
            else:
                #assign the current room to the room linked with the entered room name and save it to the gamestate
                self.gamestate.current_room = room_name
        else:
            print("This room does not exist. Enter look")

    def inspect(self, item_name):
        try:
            file_path = "escaperoom/data/" + item_name
            if self.gamestate.current_room != "final":
                self.rooms[self.gamestate.current_room].solve(self.gamestate, self.transcriptor, file_path)
        except:
            print("You can't inspect this item in this room.")
    def print_inventory(self):
        print("Inventory:")
        for item in self.gamestate.inventory:
            print(f"- {item}")

    def use(self, file_name: str):
        if (self.gamestate.current_room == "final" and file_name == "gate"):
            self.rooms[self.gamestate.current_room].solve(self.gamestate, self.transcriptor, "finale_gate.txt")
        else:
            print("You can't use this item here.")
    def hint(self):
        print(self.rooms[self.gamestate.current_room].hint)


    def save(self, file_name):
        try:
            with open(file_name, "w") as f:
                data = asdict(self.gamestate)
                data["inventory"] = list(data["inventory"])
                json.dump(data, f, indent=4)
        except:
            print("Error occured while saving")

    def load_save(self, file_name):
        try:
            with open(file_name, "r") as f:
                data = json.load(f)

            data["inventory"] = set(data["inventory"])

            self.gamestate = GameState(**data)

        except Exception as e:
            print(f"Error occurred while loading: {e}")
