import psycopg2

from flask import Flask, jsonify


app = Flask(__name__)


DB_HOST = "localhost"
DB_NAME = "Zones"
DB_USER = "postgres"
DB_PASS = "dost"

def connect_pdb():
    conn = psycopg2.connect ( host = DB_HOST,
                              database = DB_NAME,
                              user = DB_USER,
                              password = DB_PASS)
    return conn



@app.route("/")
def getdata():
    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cities_20241010_muz LIMIT 500;")  # Corrected typo
        state = cursor.fetchall()
        
        

        cursor.close()
        conn.close()
        
        return jsonify(state)  
    
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500
