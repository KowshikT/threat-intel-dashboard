import requests
import mysql.connector
import mysql.connector.errors

def fetch_phishtank_data():
    """Fetch phishing data from PhishTank"""
    url = "https://data.phishtank.com/data/online-valid.json"
    
    try:
        print("📥 Fetching PhishTank data...")
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch PhishTank. Status: {response.status_code}")
            return

        data = response.json()
        if not isinstance(data, list):
            print("❌ Unexpected PhishTank response format")
            return

        print(f"📊 Found {len(data)} phishing URLs from PhishTank")
        
        # Single connection for all operations
        db_conn = mysql.connector.connect(
            host="localhost",
            user="threat_user",
            password="koWsi67",
            database="threat_dashboard",
            autocommit=False
        )
        
        inserted = 0
        try:
            for phish in data[:100]:  # Limit to 100 for now
                try:
                    phish_url = phish.get('url', '').strip()
                    phish_id = phish.get('phish_id', 'PT-' + str(phish.get('id', 'unknown')))
                    
                    if not phish_url:
                        continue

                    # Fresh cursor per operation with single connection
                    db_cursor = db_conn.cursor(buffered=False)
                    try:
                        db_cursor.execute("""
                            INSERT IGNORE INTO phishing_urls 
                            (url, phish_id, online, target, source, threat_category)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (phish_url, str(phish_id)[:100], "online", "phishing", "PhishTank", "phishing"))
                        db_conn.commit()
                        if db_cursor.rowcount > 0:
                            print(f"✅ Inserted: {phish_url}")
                            inserted += 1
                        else:
                            print(f"⏭️ Skipped (duplicate): {phish_url}")
                    finally:
                        db_cursor.close()

                except mysql.connector.errors.ProgrammingError as pe:
                    if "Unread result found" in str(pe):
                        print(f"⏭️ Skipped (internal state): {phish_url}")
                    else:
                        print(f"⚠️ Error processing: {pe}")
                except Exception as e:
                    print(f"⚠️ Error processing: {e}")
        finally:
            db_conn.close()

        print(f"✅ PhishTank: Successfully inserted {inserted} URLs")

    except requests.exceptions.Timeout:
        print("❌ PhishTank request timed out")
    except Exception as e:
        print(f"❌ Error fetching PhishTank: {e}")
