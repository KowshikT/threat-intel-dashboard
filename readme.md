🚨 Threat Intelligence Dashboard

A real-time Threat Intelligence & Firewall Control Dashboard built using Flask, MariaDB, and UFW.
It automatically fetches malicious URLs from Abuse.ch (URLhaus), blocks their IPs at the OS firewall level, and provides a web-based interface to monitor and unblock threats interactively.

✨ Key Features

✅ Real-time malicious URL ingestion from Abuse.ch URLhaus

✅ Automatic outbound IP blocking using UFW

✅ Persistent storage using MariaDB/MySQL

✅ Live Flask-based web dashboard

✅ Auto-refreshing table (every 30 seconds)

✅ One-click Unblock from the dashboard

✅ Status display: Active / Neutralized

✅ Secure database access with a dedicated DB user

🛠 Tech Stack

Backend: Python, Flask

Database: MariaDB / MySQL

Firewall: UFW (Linux)

Frontend: HTML, CSS, JavaScript

Threat Feed: Abuse.ch URLhaus

Scheduler: Custom Python background task

⚙️ Setup Instructions
1️⃣ Clone the Repository

Then -> cd threat-intel-dashboard

2️⃣ Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3️⃣ Start MariaDB / MySQL

sudo systemctl start mysql
or
sudo systemctl start mariadb

4️⃣ Initialize the Database

mysql -u root -p < db/init_db.sql

5️⃣ Create a Dedicated Database User (Recommended)

Login to MariaDB:

sudo mysql

CREATE USER 'threat_user'@'localhost' IDENTIFIED BY 'StrongPass123';
GRANT ALL PRIVILEGES ON threat_dashboard.* TO 'threat_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

Update DB credentials in:

app.py

fetcher/abusech.py

unblock_urls.py

🔐 Firewall Permission Setup (IMPORTANT)

To allow the dashboard to unblock URLs without running Flask as root, configure sudo:

Step 1: Find UFW path

which ufw

Example output:
/usr/sbin/ufw

Step 2: Edit sudoers file

sudo visudo

Add this at the bottom (replace path if needed):

albatross ALL=(ALL) NOPASSWD: /usr/sbin/ufw

✅ Prevents password prompts
✅ Prevents backend hanging
✅ Enables instant unblock from the dashboard

▶️ Running the Application
Start the Threat Fetcher & Auto Blocker

source venv/bin/activate
python scheduler.py

Start the Flask Dashboard

In a new terminal:

source venv/bin/activate
python app.py

Open in your browser:

http://127.0.0.1:5000/

🔁 System Workflow
🔹 Threat Fetching & Auto-Blocking

Scheduler calls fetch_abusech_data()

Latest malicious URLs are downloaded from Abuse.ch

Data is parsed and inserted into MariaDB

Each domain is resolved to an IP

IP is blocked using:

ufw deny out to <IP>
