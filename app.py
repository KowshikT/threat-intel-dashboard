from flask import Flask, render_template
from flask import render_template_string
import mysql.connector
from flask import jsonify, request
from unblock_urls import unblock_url

app = Flask(__name__)

def get_db_data():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='threat_user',
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
                    <span class="status status-online">
                        <i class="fas fa-exclamation-circle"></i>Active
                    </span>
                {% else %}
                    <span class="status status-offline">
                        <i class="fas fa-ban"></i>Neutralized
                    </span>
                {% endif %}
            </td>
            <td><span class="target-badge">{{ row[3] }}</span></td>
            <td>
                <button class="unblock-btn" data-url="{{ row[0] }}">
                    Unblock
                </button>
            </td>
        </tr>
        {% endfor %}
    """, threats=data)

@app.route("/unblock", methods=["POST"])
def unblock_route():
    try:
        data = request.get_json() or {}
        url = data.get("url")

        if not url:
            return jsonify({"success": False, "message": "No URL provided"}), 400

        success, message = unblock_url(url)
        status_code = 200 if success else 500
        return jsonify({"success": success, "message": message}), status_code

    except Exception as e:
        # Failsafe so the frontend *always* gets JSON
        print(f"[UNBLOCK ERROR] {e}")
        return jsonify({"success": False, "message": f"Server error: {e}"}), 500
if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    app.run(debug=True)