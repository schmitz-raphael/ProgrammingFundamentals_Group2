import sys

from escaperoom.Engine.engine import Engine



def main(argv):
    print("Hello world")
    engine = Engine("run.txt")
    engine.play()



if __name__ == "__main__":
    main(sys.argv)