
from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.dns import DNSRoom
from escaperoom.rooms.intro import IntroRoom
from escaperoom.rooms.malware import MalwareRoom
from escaperoom.rooms.soc import SOCRoom
from escaperoom.rooms.vault import VaultRoom
from escaperoom.transcript import Transcriptor

class Engine:

    def __init__(self, transcript_name):
        self.gamestate = GameState()
        self.transcriptor = Transcriptor(transcript_name)
        self.rooms = {}
        self.init_rooms()

    def init_rooms(self):
        self.rooms["intro"] = IntroRoom()
        self.rooms["soc"] = SOCRoom()
        self.rooms["dns"] = DNSRoom()
        self.rooms["vault"] = VaultRoom()
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
                case "look":
                    print(self.rooms[self.gamestate.current_room].description)
                case "move":
                    if tokens[1] in self.rooms.keys():
                        #check if the player is not already in the room he wants to move to
                        if (self.gamestate.current_room == tokens[1]):
                            print("You are already inside this room.")
                        #player needs to be in the intro lobby to go to different rooms
                        elif (self.gameState.current_room != "intro" and tokens[1] != "intro"):
                            print("You need to return to the intro lobby before going to another room")
                        else:
                            #assign the current room to the room linked with the entered room name and save it to the gamestate
                            self.gamestate.current_room = tokens[1]
                    else:
                        print("This room does not exist. Enter look")

                case _:
                    print("Command not recognised. Enter 'help' to look for allowed commands")
        self.transcriptor.save_file()