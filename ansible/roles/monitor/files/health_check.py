import urllib.request
import datetime
import sys

URL = "http://localhost:5000/health"


def check():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with urllib.request.urlopen(URL, timeout=5) as response:
            if response.status == 200:
                print(f"[{timestamp}] OK - {URL} returned 200")
            else:
                print(f"[{timestamp}] WARN - {URL} returned {response.status}")
    except Exception as e:
        print(f"[{timestamp}] FAIL - {URL} unreachable: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check()