
from flask_mysqldb import MySQL
import spacy
from flask import current_app,jsonify


def fetch_accommodations(location,mysql):

    sql = "SELECT name, location, price, amenities FROM accommodations"
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (f"%{location}%",))
    results = cursor.fetchall()
    return [format_accommodations_results(row) for row in results]
def format_accommodations_results(row):
    if not row:
        return None
    response_data=  {
        "name": row[0],
        "location": row[1],
        "price": row[2],
        "amenities": row[3]
    }
    return response_data


def fetch_transport_options(location,mysql):
    #mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()
    sql = "SELECT mode_of_transport, provider, departure_time,duration, price FROM transport_options"
    cursor.execute(sql)
    results = cursor.fetchall()
    return [format_transport_results(row) for row in results]
def format_transport_results(row):
    if not row:
        return None
    response_data=  {
        "mode_of_transport": row[0],
        "provider": row[1],
        "departure_time": row[2],
        "duration": row[3],
        "price": row[4]
    }
    return response_data

def fetch_points_of_interest(location,mysql):
    #mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()
    sql = "SELECT name, location, description,type,recommended_visit_duration FROM points_of_interest"
    cursor.execute(sql, (f"%{location}%",))
    results = cursor.fetchall()
    return [format_poi_results(row) for row in results]
def format_poi_results(row):
    if not row:
        return None
    response_data=  {
        "name": row[0],
        "location": row[1],
        "description": row[2],

        "type":row[3],
        "recommended_visit_duration":row[4]
    }
    return response_data

def fetch_local_transport(city,mysql):
    #mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()
    sql = "SELECT type, route_name, operating_hours, price FROM local_transport"
    cursor.execute(sql, (f"%{city}%",))
    results = cursor.fetchall()
    return [format_local_transport_results(row) for row in results]
def format_local_transport_results(row):
    if not row:
        return None
    response_data= {
        "type": row[0],
        "route_name": row[1],
        "operating_hours": row[2],
        "price": row[3]
    }
    return response_data
