from flask import Flask, render_template
from flask import render_template_string
import mysql.connector

app = Flask(__name__)

def get_db_data():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='koWsi67',
            database='threat_dashboard'
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT url, phish_id, online, target
            FROM phishing_urls
            ORDER BY id DESC
            LIMIT 50
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        print(f"Fetched {len(rows)} rows from database.")
        return rows
    except Exception as e:
        print("Error fetching data:", e)
        return []

@app.route('/')
def index():
    data = get_db_data()
    return render_template('index.html', threats=data)

@app.route('/refresh-table')
def refresh_table():
    data = get_db_data()
    return render_template_string("""
        {% for row in threats %}
        <tr>
            <td class="url-cell">{{ row[0] }}</td>
            <td class="phish-id">{{ row[1] }}</td>
            <td>
                {% if row[2] == "online" %}
                    <span class="status status-online">Active</span>
                {% else %}
                    <span class="status status-offline">Neutralized</span>
                {% endif %}
            </td>
            <td><span class="target-badge">{{ row[3] }}</span></td>
        </tr>
        {% endfor %}
    """, threats=data)

from block_urls import main as block_threats

@app.route('/block', methods=['POST'])
def block_threats_route():
    try:
        block_threats()
        return render_template('block_result.html')
    except Exception as e:
        return f"❌ Blocking failed: {e}", 500


if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    app.run(debug=True)