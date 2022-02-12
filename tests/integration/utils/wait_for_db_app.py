import sys
from datetime import datetime, timedelta
from time import sleep

import requests

if __name__ == "__main__":

    wait_until = datetime.now() + timedelta(minutes=1)

    while datetime.now() < wait_until:
        try:
            response = requests.get("http://app:8000/health_check/")
            if response.status_code == 200:
                sys.exit(0)
        except requests.exceptions.ConnectionError:
            pass
        sleep(1)

    sys.exit(1)
