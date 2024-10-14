import psycopg2
from flask import Flask, jsonify, request, render_template 
from config import Config  
from datetime import datetime

app = Flask(__name__)


app.config.from_object(Config)

def connect_pdb():
    conn = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS']
    )
    return conn

@app.route("/")
def index():
    return render_template("index.html") 
@app.route("/cities", methods=["GET"])
def get_all_cities():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=100, type=int)
    
    
    city_id = request.args.get("city_id")
    state_name = request.args.get("state_name")
    city_name = request.args.get("city_name")
    modified_after = request.args.get("modified_after")

   
    offset = (page - 1) * limit

    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()

       
        query = "SELECT id, name, county, state, date_created, date_modified FROM cities_data WHERE TRUE"
        params = []

       
        if city_id:
            query += " AND id = %s"
            params.append(city_id)

        if state_name:
            query += " AND state ILIKE %s"
            params.append(f"%{state_name}%")

        if city_name:
            query += " AND name ILIKE %s"
            params.append(f"%{city_name}%")

        if modified_after:
            query += " AND date_modified > %s"
            params.append(modified_after)

        
        cursor.execute(f"SELECT COUNT(*) FROM ({query}) AS subquery;", tuple(params))
        total_cities = cursor.fetchone()[0]

  
        total_pages = (total_cities + limit - 1) // limit 

       
        query += " LIMIT %s OFFSET %s;"
        params.extend([limit, offset])
        
        cursor.execute(query, tuple(params))
        cities = cursor.fetchall()

        cursor.close()
        conn.close()

      
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

   
        response = {
            "page": page,
            "limit": limit,
            "total_cities": total_cities,  
            "total_pages": total_pages, 
            "cities": city_list
        }
        
        return jsonify(response)

    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500


@app.route("/city/<int:city_id>", methods=["GET"])  
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

    
    offset = (page - 1) * limit

    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()

       
        cursor.execute("SELECT COUNT(*) FROM cities_data WHERE date_modified > %s;", (date,))
        total_cities = cursor.fetchone()[0]

        
        total_pages = (total_cities + limit - 1) // limit  

     
        cursor.execute("""
            SELECT id, name, county, state, date_created, date_modified 
            FROM cities_data 
            WHERE date_modified > %s 
            LIMIT %s OFFSET %s;
        """, (date, limit, offset))
        
        cities = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
      
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

      
        response = {
            "page": page,
            "limit": limit,
            "total_cities": total_cities,  
            "total_pages": total_pages, 
            "cities": city_list
        }
        
        return jsonify(response)

    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
