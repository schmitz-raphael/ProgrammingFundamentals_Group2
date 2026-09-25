
class Transcript:
    def __init__(self, filename):
        self.file = open(filename, "rw")

    def write_line(self, line):
        self.file.writelines(line)

    def save_file (self):
        self.file.close()