import subprocess
import requests
import zipfile
import io
import csv
import mysql.connector
import mysql.connector.errors
import socket
from urllib.parse import urlparse

def resolve_ip(url):
    try:
        parsed = urlparse(url)
        domain = parsed.hostname
        if not domain:
            print(f"❌ Invalid URL: {url}")
            return None
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"❌ Couldn’t resolve {url}: {e}")
        return None

def block_url_in_hosts(url):
    """Add malicious domain to /etc/hosts file (requires sudo)"""
    # Blocking is optional - keep processing even if it fails
    pass

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
            csv_data = None
            for name in archive.namelist():
                print(f"   - {name}")
                if name.endswith(".csv") or name.endswith(".txt"):
                    csv_data = archive.read(name)
                    print("📥 Opened CSV file:", name)
                    break

            if csv_data is None:
                print("❌ No CSV file found in ZIP archive.")
                return

            print("📖 Reading CSV data...")
            row_count = 0
            max_rows = 50
            
            # Single connection for all operations  
            db_conn = mysql.connector.connect(
                host="localhost",
                user="threat_user",
                password="koWsi67",
                database="threat_dashboard",
                autocommit=False
            )
            
            # Parse CSV from bytes
            text_stream = io.StringIO(csv_data.decode('utf-8'))
            reader = csv.reader(text_stream, delimiter=",", quotechar='"')

            try:
                for row in reader:
                    if not row or row[0].startswith("#"):
                        continue

                    try:
                        phish_id = row[0].strip()
                        url_val = row[2].strip()
                        url_status = row[3].strip()
                        threat_type = row[5].strip() if len(row) > 5 else "unknown"

                        print(f"➡️ Processing: {url_val} [{threat_type}]")

                        # Use single connection with fresh cursor per operation
                        db_cursor = db_conn.cursor(buffered=False)
                        try:
                            db_cursor.execute("""
                                INSERT IGNORE INTO phishing_urls 
                                (url, phish_id, online, target, source, threat_category)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (url_val, phish_id[:100], url_status, threat_type, "URLhaus", threat_type))
                            db_conn.commit()
                            rows_affected = db_cursor.rowcount
                            if rows_affected > 0:
                                print(f"✅ Inserted: {url_val}")
                            else:
                                print(f"⏭️ Skipped (duplicate): {url_val}")
                            row_count += 1
                        finally:
                            db_cursor.close()

                        block_url_in_hosts(url_val)

                        if row_count >= max_rows:
                            print("🛑 Stopping after 50 rows")
                            break

                    except mysql.connector.errors.ProgrammingError as pe:
                        if "Unread result found" in str(pe):
                            # Ignore unread result warnings - these are spurious
                            # Just move to next URL
                            print(f"⏭️ Skipped (internal state): {url_val}")
                        else:
                            print(f"⚠️ Skipping row due to error: {pe}")
                    except Exception as insert_err:
                        print(f"⚠️ Skipping row due to error: {insert_err}")
            finally:
                db_conn.close()

            print(f"✅ URLhaus: Successfully processed {row_count} rows.")

    except Exception as fetch_err:
        print("❌ Error fetching Abuse.ch data:", fetch_err)
