
class Transcriptor:
    def __init__(self, filename):
        self.file = open(filename, "w")

    def write_line(self, line):
        self.file.writelines(line + "\n")
        

    def save_file (self):
        self.file.close()