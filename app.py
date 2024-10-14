import psycopg2
from flask import Flask, jsonify, request
from config import Config  # Import the Config class
from datetime import datetime

app = Flask(__name__)

# Load the config settings
app.config.from_object(Config)

def connect_pdb():
    conn = psycopg2.connect(host=app.config['DB_HOST'],
                            database=app.config['DB_NAME'],
                            user=app.config['DB_USER'],
                            password=app.config['DB_PASS'])
    return conn
@app.route("/")
def get_all_cities():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=100, type=int)

    # Calculate the offset for pagination
    offset = (page - 1) * limit

    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()

        # Count total cities in the database
        cursor.execute("SELECT COUNT(*) FROM cities_data;")
        total_cities = cursor.fetchone()[0]

        # Calculate total pages
        total_pages = (total_cities + limit - 1) // limit  # Using integer division to round up

        cursor.execute("""
            SELECT id, name, county, state, date_created, date_modified
            FROM cities_data 
            LIMIT %s OFFSET %s;
        """, (limit, offset))
        
        cities = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convert to a list of dictionaries for easier JSON serialization
        city_list = []
        for city in cities:
            city_list.append({
                "id": city[0],
                "name": city[1],
                "county": city[2],
                "state": city[3],
                "date_created": city[4],
                "date_modified": city[5]
            })

        # Create a response object with pagination info
        response = {
            "page": page,
            "limit": limit,
            "total_cities": total_cities,  # Total number of cities in the database
            "total_pages": total_pages,  # Total number of pages
            "cities": city_list
        }
        
        return jsonify(response)

    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500

@app.route("/<int:city_id>", methods=["GET"])
def get_city_by_id(city_id):
    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, county, state, date_created, date_modified FROM cities_data WHERE id = %s;", (city_id,))
        data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if data is None:
            return jsonify({"error": "City not found"}), 404
        
        result = {
            "id": data[0],
            "name": data[1],
            "county": data[2],
            "state": data[3],
            "date_created": data[4],
            "date_modified": data[5]
        }

        return jsonify(result) 
    
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500


@app.route("/modified_after", methods=["GET"])
def get_cities_modified_after():
    date = request.args.get("date")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=100, type=int)

    # Calculate the offset for pagination
    offset = (page - 1) * limit

    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()

        # Count total cities that have been modified after the specified date
        cursor.execute("SELECT COUNT(*) FROM cities_data WHERE date_modified > %s;", (date,))
        total_cities = cursor.fetchone()[0]

        # Calculate total pages
        total_pages = (total_cities + limit - 1) // limit  # Using integer division to round up

        # Query to fetch the cities modified after the specified date
        cursor.execute("""
            SELECT id, name, county, state, date_created, date_modified 
            FROM cities_data 
            WHERE date_modified > %s 
            LIMIT %s OFFSET %s;
        """, (date, limit, offset))
        
        cities = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convert to a list of dictionaries for easier JSON serialization
        city_list = []
        for city in cities:
            city_list.append({
                "id": city[0],
                "name": city[1],
                "county": city[2],
                "state": city[3],
                "date_created": city[4],
                "date_modified": city[5]
            })

        # Create a response object with pagination info and total counts
        response = {
            "page": page,
            "limit": limit,
            "total_cities": total_cities,  # Total number of cities that match the criteria
            "total_pages": total_pages,  # Total number of pages
            "cities": city_list
        }
        
        return jsonify(response)

    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
