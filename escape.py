import sys

from escaperoom.Engine.engine import Engine



def main(argv):
    engine = Engine("run.txt")
    engine.play()



if __name__ == "__main__":
    main(sys.argv)