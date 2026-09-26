
from escaperoom.Engine.gamestate import GameState
from escaperoom.transcript import Transcriptor

class Engine:

    def __init__(self, transcript_name):
        self.gamestate = GameState()
        self.transcriptor = Transcriptor(transcript_name)
        self.rooms = {}
        self.init_rooms()


    # TODO: Assign room instances once they're implemented
    def init_rooms(self):
        self.rooms["intro"] = None
        self.rooms["soc"] = None
        self.rooms["dns"] = None
        self.rooms["vault"] = None
        self.rooms["malware"] = None


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
                    self.move(tokens[1])
                case "help":
                    self.help()
                case "inventory":
                    print("Inventory: ", self.gamestate.inventory)
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
        print("save <file> - saves the current game state to a file")
        print("load <file>- loads a game state from a file")
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