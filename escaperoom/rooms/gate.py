
from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor
import hashlib
import hmac

class FinalGate (Room):
    def __init__(self):
        super().__init__(
                        "gate", 
                        "You stand before the Final Gate. The console asks for proof.",
                        "You must be in possession of all the tokens before proceeding."
                    )

    def solve(self, gameState: GameState, transcriptor: Transcriptor, file_path: str):
        if (len(gameState.tokens) < 4):
            print("You are not in possession of all the tokens")
            return
        print("Collected tokens:", ", ".join(f"{key}={value}" for key, value in gameState.tokens.items()))
        gate_data = {}
        for line in open(file_path, "r"):
            line = line.strip()
            gate_data[line.split("=")[0]] = line.split("=")[1]

        MSG = f"{gate_data["group_id"]}|"
        print(gate_data)
        MSG += "-".join(str(gameState.tokens[token]) for token in gate_data["token_order"].split(","))
        HMAC = hmac.new(gate_data["hmac_key"].encode("utf-8"), MSG.encode("utf-8"), hashlib.sha256).hexdigest()
        print("FINAL_GATE=PENDING")
        print(f"MSG=<g{MSG}>")
        print(f"HMAC=<{HMAC}>")
        transcriptor.write_line("FINAL_GATE=PENDING")
        transcriptor.write_line(f"MSG=<g{MSG}>")
        transcriptor.write_line(f"HMAC=<{HMAC}>")