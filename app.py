from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS
import sys

app = Flask(__name__)
# Enable CORS for all origins and methods
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'bank_db'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection, None
    except Exception as err:
        return None, str(err)

# Serve static files correctly
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Health Check API
@app.route('/api/health', methods=['GET'])
def health():
    conn, err = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'success': True, 'message': 'Backend & Database Connected!'})
    return jsonify({'success': False, 'message': f'DB Connection Error: {err}'})

# API Routes with robust error handling and buffered cursors
@app.route('/api/login', methods=['POST'])
def login():
    conn = None
    cursor = None
    try:
        data = request.json
        u, p = data.get('username'), data.get('password')
        conn, err = get_db_connection()
        if not conn: return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500
        
        # Using buffered=True to prevent "Unread result found" error
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
        user = cursor.fetchone()
        
        if user: return jsonify({'success': True, 'message': 'Login Successful'})
        return jsonify({'success': False, 'message': 'Invalid Username or Password'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server Error: {str(e)}'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    conn = None
    cursor = None
    try:
        data = request.json
        u, p = data.get('username'), data.get('password')
        conn, err = get_db_connection()
        if not conn: return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500
        
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (u,))
        if cursor.fetchone(): 
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (u, p))
        conn.commit()
        return jsonify({'success': True, 'message': 'User Registered Successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server Error: {str(e)}'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    conn = None
    cursor = None
    try:
        conn, err = get_db_connection()
        if not conn: return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500
        
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()
        return jsonify({'success': True, 'accounts': accounts})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server Error: {str(e)}'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/accounts/add', methods=['POST'])
def add_account():
    conn = None
    cursor = None
    try:
        data = request.json
        acc_no, name, balance = data.get('acc_no'), data.get('name'), data.get('balance')
        conn, err = get_db_connection()
        if not conn: return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500
        
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("INSERT INTO accounts (acc_no, name, balance) VALUES (%s, %s, %s)", (acc_no, name, balance))
        conn.commit()
        return jsonify({'success': True, 'message': 'Account added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/accounts/update', methods=['POST'])
def update_account():
    conn = None
    cursor = None
    try:
        data = request.json
        acc_no, name, balance = data.get('acc_no'), data.get('name'), data.get('balance')
        conn, err = get_db_connection()
        if not conn: return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500
        
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("UPDATE accounts SET name=%s, balance=%s WHERE acc_no=%s", (name, balance, acc_no))
        conn.commit()
        return jsonify({'success': True, 'message': 'Account updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/accounts/delete', methods=['POST'])
def delete_account():
    conn = None
    cursor = None
    try:
        data = request.json
        acc_no = data.get('acc_no')
        conn, err = get_db_connection()
        if not conn: return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500
        
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("DELETE FROM accounts WHERE acc_no=%s", (acc_no,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Account deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("BANKING BACKEND STARTING...")
    print("1. Ensure MySQL (XAMPP/WAMP) is running.")
    print("2. Database 'bank_db' must exist with tables.")
    print("3. Password is '12345'.")
    print("ACCESS URL: http://127.0.0.1:5000/")
    print("="*50 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
