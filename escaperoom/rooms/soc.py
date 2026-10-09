import re, ipaddress
import random

from datetime import datetime
from collections import Counter, defaultdict
from transcript import Transcriptor
from Engine.gamestate import GameState
from rooms.base import Room



from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor


class SOCRoom(Room):
    def __init__(self):
        super().__init__("SOC Triage Desk", 
                         "A cluttered screen shows failed SSH login attempts.", 
                         "Items here: auth.log") 
    
    def solve(self, gamestate: GameState, transcriptor: Transcriptor, file_path: str):
        auth_log = open(file_path, "r") 
        skipped_line = 0
        failed_subnet = Counter()
        subnet_ip = defaultdict(Counter)
        sample_dic = defaultdict(list)

        #check for the valid Failed record and creating dictionaries/counters
        for line in auth_log:
            #record form in file
            #<TIMESTAMP> <HOST> sshd[<PID>]: <Failed|Accepted> password for <USER> from <IPv4> port <PORT> protocol 2
            #       0       1       2               3               4     5    6    7      8    9     10      11    12
            words = line.split()
                  
            #check the length of record (if it has all fields)
            if len(words) == 13: 

                timestamp = words[0]
                sshd_pid = words[2]
                status = words[3]
                ip = words[8]
                port = words[10]

                #check TIMESTAMP - must be a valid ISO-8601 timestamp
                if datetime.fromisoformat(timestamp):
                    #check Port - must be integers
                    if port.isdigit():
                        #extract PID from sshd[<PID>]
                        pid_int = self.extract_pid(sshd_pid)
                        #check id - must be integers
                        if pid_int is not None and pid_int.isdigit():
                            #check ip - must be a valid IPv4 address
                            if self.ip_check(ip)==True: #only one bad
                                #check status - need to check Failed password
                                if status=="Failed":                                    
                                    #subnet /24 out of ip                                    
                                    subnet = self.subnet_24(ip) 
                                    #dictionary/counter: group subnets and counting
                                    failed_subnet[subnet] += 1 #second option counter
                                    #failed_subnet[subnet] = failed_subnet.get(subnet, 0) + 1 #first otion dictionary
                                    #dictionary/counter: subnet and counting same IP in each subnet
                                    subnet_ip[subnet][ip] +=1 #count ip within subnet
                                    #dictionary IP and lines that belongs to that IP - to extract sample
                                    sample_dic[ip].append(line)
                            else:
                                #count and skip lines that doesn't satisfy the complete format
                                skipped_line +=1
                                pass
                        else:
                            skipped_line +=1
                            pass
                    else:
                        skipped_line +=1
                        pass
                else:
                    skipped_line +=1
                    pass   
            else:
                skipped_line +=1
                pass
        #do i need pass every time?


        #find the subnet with the largest failure count
        largest_failure_subnet, count_largest_failure_subnet = failed_subnet.most_common(1)[0] #second option - counter
        #largest_failure_subnet = max(failed_subnet, key=failed_subnet.get) #first option - dictionary
       
        #find the most frequent source IP inside that subnet
        most_frequent_ip = subnet_ip[largest_failure_subnet].most_common(1)[0][0]
        #most_frequent_ip, most_frequent_ip_count = subnet_ip[largest_failure_subnet].most_common(1)[0]
        
        #login line with winning IP
        sample_valid_failed_login = random.choice(sample_dic[most_frequent_ip])
       
        #last octet from most frequent IP
        last_octet_most_frequent_ip = self.last_octet(most_frequent_ip)
                
        #generating token KEYPAD
        KEYPAD_token = f"{last_octet_most_frequent_ip}{count_largest_failure_subnet}"

        #print results for the CLI
        print("[Room SOC] Parsing logs...")
        print(f"{count_largest_failure_subnet} failed attempts found in {largest_failure_subnet}")
        print(f"Top IP is {most_frequent_ip} (last octet={last_octet_most_frequent_ip})")
        print(f"Token formed: {KEYPAD_token}")
        print ("\n")

        self.transcript_lines(transcriptor, KEYPAD_token,largest_failure_subnet, count_largest_failure_subnet, sample_valid_failed_login, skipped_line)
        #self.transcript_check(KEYPAD_token, largest_failure_subnet, count_largest_failure_subnet, sample_valid_failed_login, skipped_line )


        #add the token and item to the gamestate
        #gamestate.tokens["SOC"] = KEYPAD_token
        #ganeState.inventory.add("SOC")

        #or - i don't know if it works
        self.add_to_gamestate(gamestate, "SOC", KEYPAD_token)



    #method that extracts PID from sshd[<PID>]          
    def extract_pid(self, text):
        found_text = re.search(r"\[(.*?)\]",text)
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
        ip_octet = ip.split(".")
        return ".".join(ip_octet[:3]) + ".0/24"
    
    #method that extracts last octet from IPv4 address
    def last_octet(self, ip):
        ip_octet = ip.split(".")
        return ip_octet[-1]


    #need to be deleted
    def transcript_check (self, KEYPAD_token, subnet_24, count_, sample, not_valid):
        print(f"TOKEN[KEYPAD]={KEYPAD_token}")
        print(f"EVIDENCE[KEYPAD].TOP24={subnet_24}")
        print(f"EVIDENCE[KEYPAD].COUNT={count_}")
        print(f"EVIDENCE[KEYPAD].SAMPLE={sample}", end="")
        print(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={not_valid}")
    
    #transcript lines with transcript
    
    def transcript_lines (self, transcriptor, keypad_code, subnet_24, count_, sample, not_valid):
        transcriptor.write_line(f"TOKEN[KEYPAD]={keypad_code}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].TOP24={subnet_24}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].COUNT={count_}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].SAMPLE={sample}")
        transcriptor.write_line(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={not_valid}")
        print(f"TOKEN[KEYPAD]={keypad_code}")
        print(f"EVIDENCE[KEYPAD].TOP24={subnet_24}")
        print(f"EVIDENCE[KEYPAD].COUNT={count_}")
        print(f"EVIDENCE[KEYPAD].SAMPLE={sample}")
        print(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={not_valid}")


    #add the token and item to the gamestate
    def add_to_gamestate(self, gamestate, room_name, token):
        gamestate.tokens[room_name] = token
        gamestate.inventory.add(room_name)


#soc = SOC()
#soc.solve()
