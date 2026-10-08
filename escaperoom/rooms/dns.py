import base64
import codecs

from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor



class DNSRoom (Room):
    def __init__(self):
            super().__init__(
                "dns", 
                "The walls are covered with scribbled key=value pairs.\nItems here: dns.cfg",
                "Maybe it's worth checking the dns.cfg file."
            )


    def solve(self, gameState: GameState, transcriptor: Transcriptor, file_path: str):
        # check if the file path corresponds to the dns file and if it's not exit the function
        print(file_path.split("/")[-1] )
        if file_path.split("/")[-1] != "dns.cfg":
            print("There is no such item inside this room.")
            return

        print("[Room DNS] Decoding hints...")
        records = {}
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not self.is_valid_line(line):
                    continue
                (key, value) = self.parse_line(line)

                if ":" not in value:
                    continue
                (encoding, payload) = self.find_encoding(value)
                if encoding not in ["rot13+b64", "b64"]:
                    continue
                decoded_payload = self.decode(encoding, payload)
                records[key] = (encoding, decoded_payload)

        hint_id = self.find_hint(records)
        hint_record = records[hint_id]
        token = self.extract_token(hint_record[1])
        #print the results
        print(f'Decoded line: "{hint_record[1]}"')
        print(f"Token formed:" + token)
        #write to the transcript file 
        transcriptor.write_line(f"TOKEN[DNS]={token}")
        transcriptor.write_line(f"EVIDENCE[DNS].KEY={hint_id}")
        transcriptor.write_line(f"EVIDENCE[DNS].ENCODING={hint_record[0]}")
        transcriptor.write_line(f"EVIDENCE[DNS].DECODED_LINE={hint_record[1]}")
        # add the token and item to the gamestate
        gameState.tokens["DNS"] = token
        gameState.inventory.add("DNS")


    # line that checks for invalid lines or comments
    # returns a boolean indicating if its a valid line
    def is_valid_line(self, line):
        return not line.startswith("#") and "=" in line

    # splits a line into key and value at the = in the given line
    # assumes that is_valid_line is true
    # returns a tuple with the key and the value
    def parse_line(self, line): 
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        return (key, value)
    

        
    def find_encoding(self, value):
        encoding, payload = value.split(":", 1)
        encoding = encoding.strip()
        payload = payload.strip()
        
        return (encoding, payload)


    def decode(self, encoding, payload):
        if encoding == "rot13+b64":
            decoded_payload = codecs.decode(payload, "rot_13")
            return base64.b64decode(decoded_payload, validate=True).decode("utf-8")
        else:
            return base64.b64decode(payload, validate=True).decode("utf-8")

    def find_hint(self, records): 
        hint = "hint" + records["token_tag"][1].strip()
        return hint

    def extract_token(self, hint):
        words = hint.strip().rstrip(".").split()
        return words[-1]          



