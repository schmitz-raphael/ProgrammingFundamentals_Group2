# Cyber Escape Room

This project is a text-based cybersecurity escape room game. The game starts from the entry file `escape.py`.

## Run the project

From the project root, run:

```bash
python escape.py
```

This launches the game and starts the intro room.

## Optional command-line arguments

The launcher supports a few optional arguments:

```bash
python escape.py --start intro --data data --transcript run.txt
```

- `--start`: starting room name
- `--data`: folder containing room data files
- `--transcript`: file used to save the gameplay transcript

## Common commands while playing

- `help` - show all available commands
- `look` - describe the current room
- `move <room_name>` - move to another room
- `inspect <item>` - inspect an item in the current room
- `use <item>` - use an item
- `inventory` - show collected items
- `quit` - exit the game
