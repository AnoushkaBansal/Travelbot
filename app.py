
from flask import Flask, request, jsonify, render_template
from db_queries import fetch_accommodations, fetch_transport_options, fetch_points_of_interest, fetch_local_transport
from intent_recognition import recognize_intent
from flask_mysqldb import MySQL
from bert_intent import preprocess_query, predict_intent, get_intent_label
from openai_integration import generate_sql_query,execute_sql_query,generate_openai_response
mysql = MySQL()
CONFIDENCE_THRESHOLD = 0.7


class Config:
 
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'travel_project'
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    MYSQL_DB = 'travel_project'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    mysql.init_app(app) 
    print("Extensions after MySQL init:", app.extensions.keys())

    @app.route('/')
    def index():
        return render_template('index.html')




    @app.route('/process_query', methods=['POST'])
    def process_query():
        data = request.json
        user_query = data['query']
        response = handle_query(user_query)
        print(f"Response type: {type(response)}")
        print(response)
        
        return jsonify(response)

    @app.route('/query', methods=['POST'])
    def handle_query(user_query):
        user_query = request.json.get('query')
        preprocessed_query = preprocess_query(user_query)
        predicted_intent_num , confidence = predict_intent(preprocessed_query)
        intent_label = get_intent_label(predicted_intent_num,confidence)
        print(f"Predicted intent label: {intent_label}")
        if intent_label == "general_intent":
        # Query is out-of-scope, use GPT or another service for general response
            response = generate_openai_response(user_query)

        elif intent_label == "find_accommodation":
            intent="accommodations"
            gpt_response = generate_sql_query(user_query,intent)
            sqlresponse=execute_sql_query(gpt_response)
            if not sqlresponse:
                return {"message": "No accommodations found matching your criteria."}
            response = {
                "accommodations": [
                    {"hotelid": row[0], "name": row[1], "location": row[2], "price": row[3], "amenities": row[4], "rating": row[5]} for row in sqlresponse
                ]
                }


            
        elif intent_label == "query_local_transport":
            intent="local_transport"
            gpt_response = generate_sql_query(user_query,intent)
            sqlresponse=execute_sql_query(gpt_response)
            if not sqlresponse:
                return {"message": "No local transport options found matching your criteria."}
            response = {
                "local_transport": [
                    {"transportid": row[0], "type": row[1], "route_name": row[2], "operating_hours": row[3], "price": row[4]} for row in sqlresponse
                ]
            }

    

        elif intent_label == "find_poi":
            intent="points_of_interest"
            gpt_response = generate_sql_query(user_query,intent)
            sqlresponse=execute_sql_query(gpt_response)
                
            if not sqlresponse:
                return {"message": "No points of interest found matching your criteria."}
            def is_numeric(s):
                try:
                    float(s)  # for int, long and float
                except ValueError:
                    return False
                return True

            response = {"points_of_interest": []}
            for row in sqlresponse:
                if is_numeric(str(row[0])):  # Convert to string in case it's not already
                    response["points_of_interest"].append({
                        "id": row[0],
                        "name": row[1],
                        "location": row[2],
                        "type": row[3],
                        "entry_fee": row[4],
                        "operating_hours": row[5]
                    })
                else:
                    response["points_of_interest"].append({
                        "name": row[0],
                        "location": row[1],
                        "type": row[2],
                        "entry_fee": row[3],
                        "operating_hours": row[4]
                    })
            """response = {
                "points_of_interest": [
                    {"name": row[0], "location": row[1],  "type": row[2], "entry_fee": row[3], "operating_hours": row[4]} for row in sqlresponse
                ]}"""
                

        elif intent_label == "book_transport":
            intent="transport_options"
            gpt_response = generate_sql_query(user_query,intent)
            sqlresponse=execute_sql_query(gpt_response)
            if not sqlresponse:
                return {"message": "No transport options found matching your criteria."}
            response = {
                "transport_options": [
                    {"transportid": row[0], "mode_of_transport": row[1], "provider": row[2], "departure_time": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None, "duration": row[4], "price": row[5]} for row in sqlresponse
                ]
            }
       


        return response

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    