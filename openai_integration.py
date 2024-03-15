from openai import OpenAI

#client = OpenAI(api_key='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')
import MySQLdb
import os



db = MySQLdb.connect(host="localhost", user="root", db="travel_project")
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'], 
)
def generate_sql_query(question,intent):
    schema_description = """Database Schema Description:

Table: accommodations

Columns:
hotelid (int): Unique identifier for each hotel.
name (varchar): The name of the hotel.
location (varchar): The location of the hotel.
price (varchar): The price range of the hotel.
amenities (text): The amenities offered by the hotel.
rating (int): The rating of the hotel.
Primary Key: hotelid

Table: local_transport

Columns:
transportid (int): Unique identifier for each transport option.
type (varchar): The type of local transport (e.g., bus, subway).
route_name (varchar): The name of the transport route.
operating_hours (varchar): The operating hours of the transport option.
price (decimal): The price of the transport option.
Primary Key: transportid

Table: points_of_interest

Columns:
pointid (int): Unique identifier for each point of interest.
name (varchar): The name of the point of interest.
location (varchar): The location of the point of interest.
description (text): A description of the point of interest.
type (varchar): The type of the point of interest (e.g., museum, park).
recommended_visit_duration (varchar): The recommended visit duration.
hotelid (int, optional): Foreign Key linking to accommodations for nearby hotels.
Primary Key: pointid
Foreign Key: hotelid references accommodations(hotelid)

Table: transport_options

Columns:
transportid (int): A unique identifier for each transport option. This serves as the primary key for the table, ensuring that each record represents a distinct transport option.
mode_of_transport (varchar(255)): Specifies the mode of transport, such as flight, train, bus, etc. This column allows users to understand the type of transport option available.
provider (varchar(255)): The name of the company or entity providing the transport service. This information helps users identify the operator of the service.
departure_time (datetime): The scheduled departure time of the transport option. This timestamp is crucial for planning and scheduling travel.
duration (varchar(255)): The expected duration of the transport from the starting point to the destination. The duration is stored as a varchar to accommodate various formats of representing time (e.g., '2 hours', '3h 15m').
price (decimal(10,2)): The cost of using the transport option. Stored as a decimal, this value includes up to two digits after the decimal point, allowing for precise representation of prices, including cents.
destination (varchar(255)): The final destination of the transport option, with a default value of 'New York'. This column facilitates searches and filters for transport options ending in a specific location.
origin (varchar(255)): The starting location of the transport option, with a default value of 'Boston'. This field helps users find transport options originating from a particular place.
Primary Key:
transportid: This field is designated as the primary key of the table, ensuring each transport option is uniquely identified by its transportid.

Instructions for GPT Model:
Your task is to generate SQL queries that strictly follow the above database schema. 

1. For each natural language question related to accommodations, local transportation options, points of interest, and broader transport options, generate an appropriate SQL query. 
2. **Table Relationships**: Understand and respect the relationships between tables, particularly foreign keys. For instance, the foreign key between the points_of_interest and accommodations tables allows for queries that join these tables based on the hotelid. This is crucial when a query involves both accommodations and points of interest in proximity. 
Important:points_of_interest table's hotelid is linked to the accommodations table's hotelid, indicating which hotels are near each point of interest. If the user query is asking for accommodations near an attraction in New York, use the concept of foreign keyhotelid in points_of_interest table to fetch the hotel.
3. Use placeholders for variable data like dates and times, which will be substituted with actual values later. 
4. For transport options, ignore departure_time constraints unless specifically mentioned in the user's request. Do not assume departure date as {current_date}. Ignore it if user hasnt mentioned their departure date.
5. There is no location attribute in transport_options.
6. Also infer the {intent} to correctly identify the table you need to use to get the data from.Exception, when user query is asking for accommodation near an attraction in New York, always query the points_of_interest table.  Remember to adapt your queries based on the user's intent and the specific details they provide, ensuring all queries are compatible with the schema provided. 
7. Only asnwer with the complete SQL query. Do not include any extraneous text. The query should be ready for execution against the described schema."
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": schema_description},
            {"role": "user", "content": question}
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(f"Generated SQL Query: {response.choices[0].message.content}")
    return response.choices[0].message.content

def execute_sql_query(sql_query):
    cursor = db.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print(f"Query Results: {results}")
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def generate_openai_response(user_query):
    prompt = f"You are a tarvel agent. Please provide a detailed answer for the following user query:\n\nUser query: {user_query}\n\nAnswer:"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_query}
            ])
        ''' prompt=prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0'''
        
        response_text = response.choices[0].message.content.strip()
        return response_text
    except Exception as e:
        print(f"An error occurred while querying OpenAI: {e}")
        return "I'm sorry, I couldn't process your request."

    
#question = "how can I travel from boston to New York"
#sql_query = generate_sql_query(question)
#print(f"Generated SQL Query: {sql_query}")
#results = execute_sql_query(sql_query)
#print(f"Query Results: {results}")