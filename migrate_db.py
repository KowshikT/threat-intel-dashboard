import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='threat_user',
    password='koWsi67',
    database='threat_dashboard'
)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE phishing_urls ADD COLUMN source VARCHAR(50)')
    print('✅ Added source column')
except Exception as e:
    print(f'ℹ️ source column: {e}')

try:
    cursor.execute('ALTER TABLE phishing_urls ADD COLUMN threat_category VARCHAR(100)')
    print('✅ Added threat_category column')
except Exception as e:
    print(f'ℹ️ threat_category column: {e}')

try:
    cursor.execute('ALTER TABLE phishing_urls ADD UNIQUE KEY unique_url (url(255))')
    print('✅ Added unique constraint')
except Exception as e:
    print(f'ℹ️ unique constraint: {e}')

conn.commit()
cursor.close()
conn.close()
print('✅ Database schema updated')
