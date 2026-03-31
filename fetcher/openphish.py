import requests
import mysql.connector
import mysql.connector.errors

def fetch_openphish_data():
    """Fetch phishing URLs from OpenPhish"""
    url = "https://openphish.com/feed.txt"
    
    try:
        print("📥 Fetching OpenPhish data...")
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch OpenPhish. Status: {response.status_code}")
            return

        urls = response.text.strip().split('\n')
        print(f"📊 Found {len(urls)} phishing URLs from OpenPhish")
        
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
            for idx, phish_url in enumerate(urls[:100]):  # Limit to 100
                try:
                    phish_url = phish_url.strip()
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
                        (phish_url, f'OP-{idx}', "online", "phishing", "OpenPhish", "phishing"))
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

        print(f"✅ OpenPhish: Successfully inserted {inserted} URLs")

    except requests.exceptions.Timeout:
        print("❌ OpenPhish request timed out")
    except Exception as e:
        print(f"❌ Error fetching OpenPhish: {e}")
