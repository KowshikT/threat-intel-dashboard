import time
from fetcher.abusech import fetch_abusech_data

FETCH_INTERVAL = 60  # every 1 minutes

def main():
    while True:
        print("⏳ Fetching Abuse.ch data...")
        fetch_abusech_data()
        print("✅ Done. Waiting for next fetch cycle...")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
