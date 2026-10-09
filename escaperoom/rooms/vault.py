import re


#from escaperoom.transcript import Transcriptor  # it is not working
import sys
import os
parent_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(parent_folder)
from transcript import Transcriptor
from Engine.gamestate import GameState
from rooms.base import Room

"""
from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor
"""

class VaultRoom(Room):
    def __init__(self):
        super().__init__(
            "You enter the Vault Corridor.", 
            "A noisy dump scrolls past. \nSomewhere a SAFE{a-b-c} hides.", 
            "Items here: vault_dump.txt")

    find_SAFE = re.compile(r"SAFE\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}")

    #def solve(self):
    def solve(self, gamestate: GameState, transcriptor: Transcriptor, file_path: str):
        SAFE_token, sample, checksum = None, None, None        
        
        #with open("escaperoom/data/vault_dump.txt", encoding="utf-8") as vault_dump:
        with open(file_path, "r", encoding="utf-8") as vault_dump:   
            for line in vault_dump:
                match = self.find_SAFE.search(line)
                #words = self.valid_extract_info(line)
                if match is not None:
                    a, b, c = (int(g) for g in match.groups())
                    """
                    #the same as above
                    a = int(words.group(1))
                    b = int(words.group(2))
                    c = int(words.group(3))"""
                    if a+b==c:
                        SAFE_token = f"{a}-{b}-{c}"
                        checksum = f"{a}+{b}={c}"
                        sample = match.group(0)
                        break

        #need to be deleted
        self.transcript_check(SAFE_token, sample, checksum)

        #add transcripts
        self.transcript_lines(transcriptor, SAFE_token, sample, checksum)


        #add the token and item to the gamestate
        #gamestate.tokens["Vault"] = SAFE_token
        #ganeState.inventory.add("Vault")

        #or - i don't know if it works
        self.add_to_gamestate(gamestate, "Vault", SAFE_token)


        #print results for the CLI
        print("[Room Vault] Scanning dump...")
        if SAFE_token is None:
            print ("[Room Vault] No valid candidate found.")
            return

        print(f"Found candidate: {sample}")
        print(f"Checksum: {checksum} (OK)")


    def transcript_check (self, SAFE_token, sample, checksum):
        print(f"TOKEN[SAFE]={SAFE_token}")
        print(f'EVIDENCE[SAFE].MATCH="{sample}"')
        print(f"EVIDENCE[SAFE].CHECK={checksum}")

    #transcript lines with transcript
    
    def transcript_lines (self, transcriptor, SAFE_token, sample, checksum):
        transcriptor.write_line(f"TOKEN[SAFE]={SAFE_token}")
        transcriptor.write_line(f'EVIDENCE[SAFE].MATCH="{sample}"')
        transcriptor.write_line(f"EVIDENCE[SAFE].CHECK={checksum}")

    #add the token and item to the gamestate

    def add_to_gamestate(self, gamestate, room_name, token):
        gamestate.tokens[room_name] = token
        gamestate.inventory.add(room_name)

        
  
#vault = Vault()
#vault.solve()