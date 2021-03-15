import sys
import time
import datetime

def main():
    try:
        now = time.time()
        while True:
            if now < int(time.time()):
                now = int(time.time())
                print(datetime.datetime.fromtimestamp(now))
    except KeyboardInterrupt:
        sys.exit(0)
