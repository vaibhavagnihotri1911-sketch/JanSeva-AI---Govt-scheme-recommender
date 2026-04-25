#to connect the database
# import psycopg2

# try:
#     connection = psycopg2.connect(
#         host="localhost",
#         database="india_schemes_db",
#         user="postgres",
#         password="Sneha@123",
#         port="5433"
#     )

#     cursor = connection.cursor()
#     cursor.execute("SELECT version();")
#     db_version = cursor.fetchone()
#     print("Connected to:", db_version)

#     cursor.close()
#     connection.close()

# except Exception as e:
#     print("Error connecting to database:", e)


#calling the function from utils
from db_utils import insert_scheme

sample_scheme = {
    "scheme_name": "Automated Test Scheme",
    "description_short": "Inserted using function",
    "central_or_state": "Central",
    "state_name": "All India",
    "ministry": "Test Ministry",
    "status": "active"
}

insert_scheme(sample_scheme)