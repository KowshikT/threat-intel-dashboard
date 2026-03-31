import time
from fetcher.abusech import fetch_abusech_data
from fetcher.phishtank import fetch_phishtank_data
from fetcher.openphish import fetch_openphish_data
from fetcher.malwaredomains import fetch_malware_domains

FETCH_INTERVAL = 30  # every 30 seconds

def main():
    while True:
        print("\n" + "="*60)
        print("🔄 Starting threat intelligence data fetch cycle...")
        print("="*60)
        
        try:
            print("\n1️⃣ Fetching URLhaus (Malware) data...")
            fetch_abusech_data()
        except Exception as e:
            print(f"❌ URLhaus fetch failed: {e}")
        
        try:
            print("\n2️⃣ Fetching PhishTank (Phishing) data...")
            fetch_phishtank_data()
        except Exception as e:
            print(f"❌ PhishTank fetch failed: {e}")
        
        try:
            print("\n3️⃣ Fetching OpenPhish (Phishing) data...")
            fetch_openphish_data()
        except Exception as e:
            print(f"❌ OpenPhish fetch failed: {e}")
        
        try:
            print("\n4️⃣ Fetching Malware Domains data...")
            fetch_malware_domains()
        except Exception as e:
            print(f"❌ Malware Domains fetch failed: {e}")
        
        print("\n" + "="*60)
        print("✅ Fetch cycle complete. Waiting for next cycle...")
        print(f"⏳ Next fetch in {FETCH_INTERVAL} seconds")
        print("="*60 + "\n")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
