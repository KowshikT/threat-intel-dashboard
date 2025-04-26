from gc import get_count
import requests
import zipfile
import io
import csv
import mysql.connector

def fetch_abusech_data():
    url = "https://urlhaus.abuse.ch/downloads/csv/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("❌ Failed to fetch Abuse.ch ZIP file.")
            return

        zip_content = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_content) as archive:
            print("🧾 ZIP archive contains:")
            csv_file = None
            for name in archive.namelist():
                print(f"   - {name}")
                if name.endswith(".csv") or name.endswith(".txt"):
                    csv_file = archive.open(name)
                    print("📥 Opened CSV file:", name)
                    break

            if csv_file is None:
                print("❌ No CSV file found in ZIP archive.")
                return

            print("📖 Reading CSV data...")
            row_count = 0
            max_rows = 10 
            # Use csv.DictReader for safe parsing
            text_stream = io.TextIOWrapper(csv_file, encoding="utf-8", newline='')
            reader = csv.reader(
                (line for line in text_stream if not line.startswith("#")),
                delimiter=",", quotechar='"'
            )
              
            for row in reader:
                if not row or row[0].startswith("#"):
                    continue
            
                try:
                    phish_id = row[0].strip()
                    url_val = row[2].strip()
                    url_status = row[3].strip()
                    threat_type = row[5].strip()
            
                    print(f"➡️ Processing row {row_count + 1}: {url_val} [{threat_type}]")
            
                    # Save to DB
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="koWsi67",
                        database="threat_dashboard"
                    )
                    cursor = conn.cursor()
                    cursor.execute("""
                            INSERT INTO phishing_urls (url, phish_id, online, target)
                            VALUES (%s, %s, %s, %s)""",
                            (url_val, phish_id[:100], url_status, threat_type))
                    if cursor.rowcount == 0:
                        print(f"⚠️ Duplicate entry skipped: {phish_id}")
    
                    conn.commit()
                    cursor.close()
                    conn.close()
            
                    row_count += 1
                    if row_count >= max_rows:
                        print("🛑 Stopping after 10 rows (debug mode)")
                        break
            
                except Exception as insert_err:
                    print(f"⚠️ Skipping row due to error: {insert_err}")
            
            

            print(f"✅ Successfully inserted {row_count} rows into the database.")


    except Exception as fetch_err:
        print("❌ Error fetching Abuse.ch data:", fetch_err)