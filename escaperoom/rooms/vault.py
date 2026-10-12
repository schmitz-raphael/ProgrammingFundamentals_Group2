import re

from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor

class VaultRoom(Room):
    def __init__(self):
        super().__init__(
            "vault",
            "You enter the Vault Corridor. \nA noisy dump scrolls past. Somewhere a SAFE{a-b-c} hides. \nItems here: vault_dump.txt",
            "Maybe it's worth checking the vault_dump.txt file.")
    #looking for pattern compiled once, reused for every line.
    find_SAFE = re.compile(r"SAFE\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}")

    def solve(self, gamestate: GameState, transcriptor: Transcriptor, file_path: str):
        SAFE_token, sample, checksum = None, None, None        
        
        print("[Room Vault] Scanning dump...")
        #using compiled regex
        with open(file_path, "r", encoding="utf-8") as vault_dump:   
            for line in vault_dump:
                match = self.find_SAFE.search(line)
                #searching for the candidate with a+b=c
                if match is not None:
                    a, b, c = (int(g) for g in match.groups())
                    if a+b==c:
                        SAFE_token = f"{a}-{b}-{c}"
                        checksum = f"{a}+{b}={c}"
                        sample = match.group(0)
                        break #first candidate satisfying the checksum
        #print results for the CLI
        self.CLI_results(SAFE_token, sample, checksum)

        #add transcripts
        self.transcript_lines(transcriptor, SAFE_token, sample, checksum)

        #add the token and item to the gamestate
        self.add_to_gamestate(gamestate, "SAFE", SAFE_token)

    #print results for the CLI
    def CLI_results (self, SAFE_token, sample, checksum):
        if SAFE_token is None:
            print ("[Room Vault] No valid candidate found.")
            return
        print(f"Found candidate: {sample}")
        print(f"Checksum: {checksum} (OK)")
        print(f"\nTOKEN[SAFE]={SAFE_token}")
        print(f'EVIDENCE[SAFE].MATCH="{sample}"')
        print(f"EVIDENCE[SAFE].CHECK={checksum}")


    #transcript lines
    def transcript_lines (self, transcriptor, SAFE_token, sample, checksum):
        transcriptor.write_line(f"TOKEN[SAFE]={SAFE_token}")
        transcriptor.write_line(f'EVIDENCE[SAFE].MATCH="{sample}"')
        transcriptor.write_line(f"EVIDENCE[SAFE].CHECK={checksum}")

    #add the token and item to the gamestate
    def add_to_gamestate(self, gamestate, token_name, token):
        gamestate.tokens[token_name] = token
        gamestate.inventory.add(token_name)
