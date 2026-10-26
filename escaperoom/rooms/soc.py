"""SOC Triage Desk Room finds the /24 subnet with the most failed SSH logins."""
import re, ipaddress
import random

from datetime import datetime
from collections import Counter, defaultdict

from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor

class SOCRoom(Room):
    """Room that parses the auth.log file and builds the KEYPAD token"""

    def __init__(self):
        super().__init__("soc", 
                         "A cluttered screen shows failed SSH login attempts. \nItems here: auth.log",
                         "Maybe it's worth checking the auth.log file.",
                         "SOC Triage Desk") 
        
    def solve(self, gamestate: GameState, transcriptor: Transcriptor, file_path: str):
        """Parse the auth.log file, find the subnet with the most failed SSH logins and build the KEYPAD token.
        
        Args:
            gamestate (GameState): Receives the token and inventory item.
            transcriptor (Transcriptor): Writer for the transcript lines.
            file_path (str): Path to the auth.log file.
            
            Returns:
                None - Results are printed and written to the transcript and stored in gamestate.
            """
        
        try:
            auth_log = open(file_path, "r", encoding="utf-8")
        except OSError as error:
            print(f"[Room SOC] Cannot read {file_path}: {error}")
            return
        
        skipped_line = 0
        failed_subnet = Counter()
        subnet_ip = defaultdict(Counter)
        sample_dic = defaultdict(list)

        with auth_log:
            print("[Room SOC] Parsing logs...")
                
            for line in auth_log:
                #record form in file
                #<TIMESTAMP> <HOST> sshd[<PID>]: <Failed|Accepted> password for <USER> from <IPv4> port <PORT> protocol 2
                #       0       1       2               3               4     5    6    7      8    9     10      11    12
                words = line.split()

                if not self.valid_record(words):
                    skipped_line += 1
                    continue #count the skipped line and skip the rest of the loop

                status = words[3]
                ip = words[8]
                if status == "Failed":
                    #subnet /24 out of ip                                    
                    subnet = self.subnet_24(ip) 
                    #dictionary/counter: group subnets and counting
                    failed_subnet[subnet] += 1
                    #dictionary/counter: subnet and counting same IP in each subnet
                    subnet_ip[subnet][ip] +=1
                    #dictionary IP and lines that belongs to that IP - to extract sample
                    sample_dic[ip].append(line.strip())   
       
        if not failed_subnet:
            print("[Room SOC] No failed SSH login attempts found.")
            return
        
        #find the largest failure subnet with the largest failure count (lfs)
        top_subnet, count_lfs = failed_subnet.most_common(1)[0] 
       
        #find the most frequent source IP inside that subnet
        top_ip = subnet_ip[top_subnet].most_common(1)[0][0]
        
        #login line with winning IP without newline
        sample_valid = random.choice(sample_dic[top_ip])
        
        #last octet from most frequent IP
        last_octet_top_ip = self.last_octet(top_ip)
                
        #generating token KEYPAD
        KEYPAD_token = f"{last_octet_top_ip}{count_lfs}"

        self.CLI_results(top_ip, last_octet_top_ip, KEYPAD_token, top_subnet, count_lfs, sample_valid, skipped_line)
        self.transcript_lines(transcriptor, KEYPAD_token, top_subnet, count_lfs, sample_valid, skipped_line)
        self.add_to_gamestate(gamestate, "KEYPAD", KEYPAD_token)

    def valid_record(self, records):
        """
        Detect the valid record. Check that a split log line has required fields in correct form. 
        
        Args:
            records (list[str]): The words in one log line

        Returns:
            bool: True if valid, False if malformed.
        """
        return(
            len(records) == 13
            and self.timestamp_check(records[0])
            and self.extract_pid(records[2]) is not None
            and records[3] in ("Failed", "Accepted")
            and records[4:6] == ["password", "for"]
            and records[7] == "from"
            and self.ip_check(records[8])
            and records[9] == "port"
            and records[10].isdigit()
            and records[11] == "protocol"
            and records[12] == "2"
        )

    #method that checks if timestamp is valid
    def timestamp_check(self, text):
        try:
            datetime.fromisoformat(text)
            return True
        except ValueError:
            return False

    #method that extracts PID from sshd[<PID>] 
    pid_pattern = re.compile(r"sshd\[(\d+)\]:")         
    def extract_pid(self, text):
        found_text = self.pid_pattern.fullmatch(text)
        if found_text is None:
            return None
        return found_text.group(1)
    
    #method that checks if IPv4 address is valid
    def ip_check(self, ip): 
        try:
            ipresult = ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False
        
    #method that extracts the subnet 24 from IPv4
    def subnet_24(self, ip): 
        return ".".join(ip.split(".")[:3]) + ".0/24"
    
    #method that extracts last octet from IPv4 address
    def last_octet(self, ip):
        return ip.split(".")[-1]

    def CLI_results (self, top_ip, last_octet_top_ip, keypad_token, subnet_24, count_, sample, not_valid):
        """
        Print the results to the command line interface.
                
        Args:
            top_ip (str): Most frequent IP address in the top subnet.
            last_octet_top_ip (str): Last octet of the top IP address.      
            keypad_token (str): KEYPAD token.
            subnet_24 (str): The /24 subnet with the most failed SSH logins.
            count_ (int): Total failed attempts in the top subnet.
            sample (str): Sample failed-log line from top subnet.
            not_valid (int): Number of malformed log lines skipped.
                
        Returns:
            None
        """
        print(f"{count_} failed attempts found in {subnet_24}")
        print(f"Top IP is {top_ip} (last octet={last_octet_top_ip})")
        print(f"Token formed: {keypad_token}")
        print(f"\nTOKEN[KEYPAD]={keypad_token}")
        print(f"EVIDENCE[KEYPAD].TOP24={subnet_24}")
        print(f"EVIDENCE[KEYPAD].COUNT={count_}")
        print(f"EVIDENCE[KEYPAD].SAMPLE={sample}")
        print(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={not_valid}")    
    
    #transcript    
    def transcript_lines (self, transcriptor, keypad_token, subnet_24, count_, sample, not_valid):
        transcriptor.write_line(f"TOKEN[KEYPAD]={keypad_token}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].TOP24={subnet_24}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].COUNT={count_}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].SAMPLE={sample}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={not_valid}")

    #add the token and item to the gamestate
    def add_to_gamestate(self, gamestate, token_name, token):
        gamestate.tokens[token_name] = token
        gamestate.inventory.add(token_name)
