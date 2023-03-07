# SSH Brute Forcing Script 

1. Run the command `pip install -r requirements.txt` or `poetry install --only main` to install all the packages required in your virtual environment.
2. Run `python main.py` this will run the program

### Basic Attack
``` bash
python main.py -i 10.13.3.21 -u usernames.txt -p passwords.txt
```

### Basic Attack and specifying the log file location
``` bash
python main.py -i 10.13.3.21 -u usernames.txt -p passwords.txt -l log.txt
```

### Basic Attack for specific ports
``` bash
python main.py -i 10.13.3.21 -u usernames.txt -p passwords.txt -port 2222
```

you can use `python main.py -h` to show all argument