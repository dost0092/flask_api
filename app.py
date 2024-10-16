import psycopg2
from flask import Flask, jsonify, request, render_template
from config import Config
from datetime import datetime



app = Flask(__name__)
app.config.from_object(Config)



def connect_pdb():
    try:
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASS']
        )
        print('Connection successful')
        return conn
    except psycopg2.OperationalError as e:
        print(f"OperationalError: {e}")
        return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None



def format_city_data(city):
    return {
        "id": city[0],
        "name": city[1],
        "county": city[2],
        "state": city[3],
        "date_created": city[4],
        "date_modified": city[5]
    }


# build query according to the basequery(city_name, state_name etc)
def build_query(base_query, filters):
    params = []
    if filters.get("city_id"):
        base_query += " AND id = %s"
        params.append(filters["city_id"])
    if filters.get("state_name"):
        base_query += " AND state ILIKE %s"
        params.append(f"%{filters['state_name']}%")
    if filters.get("city_name"):
        base_query += " AND name ILIKE %s"
        params.append(f"%{filters['city_name']}%")
    if filters.get("modified_after"):
        base_query += " AND date_modified > %s"
        params.append(filters["modified_after"])
    return base_query, params



def get_pagination_info(total_items, limit, page):
    total_pages = (total_items + limit - 1) // limit
    return total_pages



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/cities", methods=["GET"])
def get_all_cities():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=100, type=int)

    filters = {
        "city_id": request.args.get("city_id"),
        "state_name": request.args.get("state_name"),
        "city_name": request.args.get("city_name"),
        "modified_after": request.args.get("modified_after")
    }

    # give the offset where start from the pages
    offset = (page - 1) * limit
    conn = connect_pdb()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        query = "SELECT id, name, county, state, date_created, date_modified FROM cities_data WHERE TRUE"
        query, params = build_query(query, filters)

        cursor.execute(f"SELECT COUNT(*) FROM ({query}) AS subquery;", tuple(params))
        total_cities = cursor.fetchone()[0]
        
        total_pages = get_pagination_info(total_cities, limit, page)

        query += " LIMIT %s OFFSET %s;"
        params.extend([limit, offset])

        cursor.execute(query, tuple(params))
        cities = cursor.fetchall()

        cursor.close()
        conn.close()

        city_list = [format_city_data(city) for city in cities]

        meta = {
            "page": page,
            "limit": limit,
            "total_cities": total_cities,
            "total_pages": total_pages,
            "cities": city_list
        }
        
        return jsonify(meta)

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

        result = format_city_data(data)
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

        total_pages = get_pagination_info(total_cities, limit, page)

        cursor.execute("""
            SELECT id, name, county, state, date_created, date_modified 
            FROM cities_data 
            WHERE date_modified > %s 
            LIMIT %s OFFSET %s;
        """, (date, limit, offset))
        
        cities = cursor.fetchall()

        cursor.close()
        conn.close()

        city_list = [format_city_data(city) for city in cities]

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
