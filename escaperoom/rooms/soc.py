from base import Room
from datetime import datetime

class SOC (Room):
    def __init__(self):
        super().__init__("SOC Triage Desk", "A cluttered screen shows failed SSH login attempts. Items here: auth.log") 

    def solve(self):
        auth_log = open("escaperoom/data/auth.log")  
        for line in auth_log:
            words = line.split()
            if (len(words) != 13):
                pass
            if not datetime.fromisoformat(words[0]):
                pass
            




soc = SOC()

soc.solve()