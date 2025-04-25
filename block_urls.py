import mysql.connector
import socket
import subprocess

from urllib.parse import urlparse

def fetch_urls():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="koWsi67",
        database="threat_dashboard"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM phishing_urls ORDER BY id DESC ")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]


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


def block_ip(ip):
    try:
        cmd = ["sudo", "ufw", "deny", "out", "to", ip]
        subprocess.run(cmd, check=True)
        print(f"🛡️ Blocked outbound to {ip}")
    except subprocess.CalledProcessError:
        print(f"⚠️ Failed to block {ip} — might already be blocked")

def main():
    urls = fetch_urls()
    print(f"🔍 Processing {len(urls)} URLs...")
    for url in urls:
        ip = resolve_ip(url)
        if ip:
            block_ip(ip)

if __name__ == "__main__":
    main()
