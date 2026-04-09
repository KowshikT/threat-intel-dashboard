import socket
import subprocess
from urllib.parse import urlparse

def resolve_ip(url: str):
    try:
        parsed = urlparse(url)
        domain = parsed.hostname
        if not domain:
            return None, "Invalid URL, no hostname"
        ip = socket.gethostbyname(domain)
        return ip, None
    except Exception as e:
        return None, str(e)

def unblock_url(url: str):
    print(f"[UNBLOCK] Requested unblock for {url}")

    ip, err = resolve_ip(url)
    if err or not ip:
        msg = f"Could not resolve IP for {url}: {err}"
        print(msg)
        return False, msg

    # IMPORTANT: no 'sudo' here, or it'll hang waiting for password
    cmd = ["sudo", "ufw", "delete", "deny", "out", "to", ip]
    print(f"[UNBLOCK] Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,  # prevent hanging forever
        )
    except subprocess.TimeoutExpired:
        msg = "UFW command timed out"
        print(f"[UNBLOCK ERROR] {msg}")
        return False, msg

    if result.returncode != 0:
        msg = f"UFW failed: {result.stderr.strip()}"
        print(f"[UNBLOCK ERROR] {msg}")
        return False, msg

    msg = f"Unblocked {url} ({ip})"
    print(f"[UNBLOCK OK] {msg}")
    return True, msg

if __name__ == "__main__":
    u = input("Enter URL to unblock: ")
    print(unblock_url(u))