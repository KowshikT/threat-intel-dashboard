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

    parsed = urlparse(url)
    domain = parsed.hostname
    
    if not domain:
        msg = f"Invalid URL: {url}"
        print(f"[UNBLOCK ERROR] {msg}")
        return False, msg

    # Remove from /etc/hosts file
    try:
        # Use sed to remove the line from /etc/hosts
        cmd = ["sudo", "sed", "-i", f"/127.0.0.1 {domain}/d", "/etc/hosts"]
        print(f"[UNBLOCK] Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            msg = f"Failed to remove from /etc/hosts: {result.stderr.strip()}"
            print(f"[UNBLOCK ERROR] {msg}")
            return False, msg

        msg = f"Unblocked {url} by removing from /etc/hosts"
        print(f"[UNBLOCK OK] {msg}")
        return True, msg
        
    except subprocess.TimeoutExpired:
        msg = "Unblock command timed out"
        print(f"[UNBLOCK ERROR] {msg}")
        return False, msg
    except Exception as e:
        msg = f"Error during unblock: {str(e)}"
        print(f"[UNBLOCK ERROR] {msg}")
        return False, msg

if __name__ == "__main__":
    u = input("Enter URL to unblock: ")
    print(unblock_url(u))