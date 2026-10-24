import sys
import argparse
from escaperoom.Engine.engine import Engine



def main(argv):
    parser = argparse.ArgumentParser(description="Escape room")
    parser.add_argument("--start", default = "intro")
    parser.add_argument("--data", default="data")
    parser.add_argument("--transcript", default="run.txt")
    args = parser.parse_args(argv[1:])
    engine = Engine(args.transcript)
    engine.play()



if __name__ == "__main__":
    main(sys.argv)