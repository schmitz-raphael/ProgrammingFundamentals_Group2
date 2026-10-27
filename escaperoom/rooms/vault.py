"""Vault rooom: finds SAFE{a-b-c} candidate in the vault_dump.txt, where a+b=c."""
import re

from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor

class VaultRoom(Room):
    def __init__(self):
        super().__init__(
            "vault",
            "A noisy dump scrolls past. Somewhere a SAFE{a-b-c} hides. \nItems here: vault_dump.txt",
            "Maybe it's worth checking the vault_dump.txt file.",
            "Vault Corridor")
    #looking for pattern compiled once, reused for every line.
    find_SAFE = re.compile(r"SAFE\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}")

    def solve(self, gamestate: GameState, transcriptor: Transcriptor, file_path: str):
        
        """
        Find the SAFE{a-b-c} candidate that is a+b=c and record the results.
        
        Args:
            gamestate (GameState): Receives the token and inventory item.
            transcriptor (Transcriptor): Writer for the transcript lines.   
            file_path (str): Path to vault_dump.txt.
        
        Returns:
            None - Results are printed and written to the transcript and stored in gamestate.
        """    
        if file_path.split("/")[-1] != "vault_dump.txt":
            print("There is no such item inside this room.")
            return
    
        try:
            vault_dump = open(file_path, "r", encoding="utf-8")
        except OSError as error:
            print(f"[Room Vault] Cannot read {file_path}: {error}")
            return
        
        print("[Room Vault] Scanning dump...")
        SAFE_token, sample, checksum = None, None, None
        with vault_dump:   
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
        
        #no valid candidate found, SAFE_token is None
        if SAFE_token is None:
            print("[Room Vault] No valid candidate found.")
            return
        
        self.CLI_results(SAFE_token, sample, checksum)
        self.transcript_lines(transcriptor, SAFE_token, sample, checksum)
        self.add_to_gamestate(gamestate, "SAFE", SAFE_token)

    #print results for the CLI
    def CLI_results (self, SAFE_token, sample, checksum):
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
