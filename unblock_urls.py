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

def block_url_in_ufw(url: str):
    """Block a URL using UFW firewall by blocking the resolved IP"""
    try:
        ip, error = resolve_ip(url)
        if error or not ip:
            print(f"[BLOCK ERROR] Could not resolve {url}: {error}")
            return False, f"Could not resolve IP: {error}"
        
        # Add UFW rule to deny the IP
        cmd = ["sudo", "ufw", "deny", "from", ip]
        print(f"[BLOCK] Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            msg = f"Failed to block IP {ip}: {result.stderr.strip()}"
            print(f"[BLOCK ERROR] {msg}")
            return False, msg
        
        msg = f"Blocked {url} (IP: {ip}) using UFW firewall"
        print(f"[BLOCK OK] {msg}")
        return True, msg
        
    except subprocess.TimeoutExpired:
        msg = "Block command timed out"
        print(f"[BLOCK ERROR] {msg}")
        return False, msg
    except Exception as e:
        msg = f"Error during block: {str(e)}"
        print(f"[BLOCK ERROR] {msg}")
        return False, msg

def unblock_url(url: str):
    """Unblock a URL by removing UFW firewall rule for the resolved IP"""
    print(f"[UNBLOCK] Requested unblock for {url}")

    parsed = urlparse(url)
    domain = parsed.hostname
    
    if not domain:
        msg = f"Invalid URL: {url}"
        print(f"[UNBLOCK ERROR] {msg}")
        return False, msg

    # Resolve IP and remove UFW rule
    try:
        ip, error = resolve_ip(url)
        if error or not ip:
            msg = f"Could not resolve {url}: {error}"
            print(f"[UNBLOCK ERROR] {msg}")
            return False, msg
        
        # Remove UFW rule for this IP
        cmd = ["sudo", "ufw", "delete", "deny", "from", ip]
        print(f"[UNBLOCK] Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            # Check if rule doesn't exist (which is OK when unblocking)
            if "No rules" in result.stderr or "Could not find rule" in result.stderr:
                msg = f"Unblocked {url} (IP: {ip}) - rule was not found (already unblocked)"
                print(f"[UNBLOCK OK] {msg}")
                return True, msg
            
            msg = f"Failed to unblock IP {ip}: {result.stderr.strip()}"
            print(f"[UNBLOCK ERROR] {msg}")
            return False, msg

        msg = f"Unblocked {url} (IP: {ip}) by removing UFW firewall rule"
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