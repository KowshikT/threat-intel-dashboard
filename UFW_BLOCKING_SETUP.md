# UFW Firewall Blocking Setup

## Overview
The threat dashboard now includes UFW firewall blocking functionality to actively block malicious URLs at the network level.

## How It Works

### Blocking URLs
When URLs are fetched from threat intelligence sources (especially via Abuse.ch), the system:
1. Resolves the domain to an IP address using DNS
2. Adds a UFW firewall rule to block all traffic from that IP: `sudo ufw deny from <IP>`
3. Logs the blocking action

### Unblocking URLs
When a user clicks "Unblock" on the dashboard:
1. Resolves the URL's domain to an IP address
2. Removes the UFW firewall rule: `sudo ufw delete deny from <IP>`
3. Logs the unblocking action

## Requirements

### 1. UFW Must Be Enabled
```bash
sudo ufw status

# If not enabled, enable it:
sudo ufw enable
```

### 2. Sudo Permissions for UFW Commands
The application needs to run UFW commands with sudo. Configure sudoers to allow the application user to run UFW without password prompt:

```bash
# Add this to sudoers (use visudo):
sudo visudo

# Add these lines at the end:
www-data ALL=(ALL) NOPASSWD: /usr/sbin/ufw
albatross ALL=(ALL) NOPASSWD: /usr/sbin/ufw
```

Or for the specific user running the Flask app:
```bash
sudo visudo
# Add: <username> ALL=(ALL) NOPASSWD: /usr/sbin/ufw
```

### 3. Configure UFW Defaults
```bash
# Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh     # Don't lock yourself out!
sudo ufw allow 5000   # For Flask dashboard (or your app port)
```

## Testing

### Test URL Resolution
```bash
cd /home/albatross/threat-intel-dashboard
source venv/bin/activate
python3 -c "from unblock_urls import resolve_ip; print(resolve_ip('https://example.com'))"
```

### Test Blocking Command (will fail without proper permissions)
```bash
python3 -c "from unblock_urls import block_url_in_ufw; print(block_url_in_ufw('https://example.com'))"
```

### If Permissions Work
You should see output like:
```
✅ Blocked https://example.com (IP: 104.18.27.120) using UFW firewall
```

## Verification

### Check Active UFW Rules
```bash
sudo ufw status verbose
# Should show rules like: 
# deny in from 93.184.216.34 anywhere
```

### Check Blocked Domains
```bash
sudo ufw status numbered | grep deny
```

### Remove a Specific Rule
```bash
sudo ufw delete deny from <IP>
```

## Important Notes

1. **Network Impact**: Blocking IPs affects all users on the network, not just the dashboard user
2. **Shared Infrastructure**: If multiple services use the same IP, blocking affects all of them
3. **Logging**: Check UFW logs for blocked attempts:
   ```bash
   sudo grep UFW /var/log/syslog
   ```
4. **Performance**: Each block/unblock operation requires a sudo command with a ~5 second timeout

## Troubleshooting

### "Permission denied" Errors
- Verify user is in sudoers for UFW
- Test: `sudo -l | grep ufw`
- Make sure NOPASSWD is configured

### "No rules" When Unblocking
- This means the rule doesn't exist (already unblocked)
- The application handles this gracefully

### UFW Not Responding
- Check if UFW is enabled: `sudo ufw status`
- Restart UFW: `sudo ufw reload`

## Implementation Files Modified

1. **unblock_urls.py** - Added `block_url_in_ufw()` function for firewall blocking
2. **fetcher/abusech.py** - Updated to use UFW blocking instead of /etc/hosts
3. **app.py** - Uses unblock_url() for the dashboard unblock button

## Future Improvements

- Database logging of blocked/unblocked IPs
- Automatic rule expiration
- Bulk block/unblock operations
- IP reputation scoring
