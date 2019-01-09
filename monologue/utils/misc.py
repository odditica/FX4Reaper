from datetime import datetime

def print_full(msg):
    print(datetime.now().strftime("%H:%M:%S") + " || " + msg, end='', flush=True)
