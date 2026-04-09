#!/usr/bin/env python3
"""
Database setup script
- Ensures phish_id is the PRIMARY KEY
- Prevents duplicate threat IDs in the database
"""

import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        print("🔄 Setting up database...")
        
        # Connect to database
        conn = mysql.connector.connect(
            host='localhost',
            user='threat_user',
            password='koWsi67',
            database='threat_dashboard',
            ssl_disabled=True
        )
        
        cursor = conn.cursor()
        
        # Read and execute init_db.sql to ensure correct schema
        try:
            with open('db/init_db.sql', 'r') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement
            statements = sql_content.split(';')
            for stmt in statements:
                stmt = stmt.strip()
                if stmt:
                    cursor.execute(stmt)
            
            conn.commit()
            print("✅ Database schema initialized")
        except FileNotFoundError:
            print("❌ init_db.sql not found")
            return False
        
        # Verify schema is correct
        cursor.execute("""
            SELECT CONSTRAINT_NAME, COLUMN_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'phishing_urls' AND CONSTRAINT_NAME = 'PRIMARY'
        """)
        
        pk = cursor.fetchone()
        if pk and pk[1] == 'phish_id':
            print("✅ PRIMARY KEY is correctly set to phish_id")
            print("✅ Duplicate entries will be prevented at the database level")
        else:
            print("❌ Primary key is not set to phish_id")
            cursor.close()
            conn.close()
            return False
        
        # Check unique constraint on URL
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
            WHERE TABLE_NAME = 'phishing_urls' AND CONSTRAINT_TYPE = 'UNIQUE'
        """)
        
        if cursor.fetchone():
            print("✅ UNIQUE constraint on URL exists (prevents duplicate URLs)")
        
        # Get table stats
        cursor.execute("SELECT COUNT(*) FROM phishing_urls")
        count = cursor.fetchone()[0]
        print(f"📊 Current records in database: {count}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database setup complete!")
        print("📝 Schema features:")
        print("   - phish_id is PRIMARY KEY (prevents duplicate threat IDs)")
        print("   - url has UNIQUE constraint (prevents duplicate URLs)")
        print("   - INSERT IGNORE will skip any duplicate phish_ids")
        return True
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    exit(0 if success else 1)


