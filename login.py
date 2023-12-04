from flask import Flask, request, jsonify, make_response
import cx_Oracle
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes or specify origins with CORS(app, origins="*") for all origins

# Establish cx_Oracle connection to Oracle database
dsn_tns = cx_Oracle.makedsn('oracle1.cis.temple.edu', '1521', service_name='cisora')
username = 'tup09776'
password = '916080352'
try:
    oracle_connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
    # print("Inside Try-B")
    oracle_cursor = oracle_connection.cursor()
    print("Oracle DB Connection Successful")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Oracle DB Error:", error.message)


@app.route('/login', methods=['POST'])
def login():
    # print("login")
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request
        username = data.get('username')
        password_hash = data.get('hashedPassword')

        # Authenticate user against the user_accounts table
        query = "SELECT * FROM user_accounts WHERE username = :uname AND password_hash = :hashed_pwd"
        oracle_cursor.execute(query, uname=username, hashed_pwd=password_hash)
        user = oracle_cursor.fetchone()
        print(user)
        if user:
            response_data = {'success': True, 'message': 'Login successful'}
            status_code = 200
        else:
            response_data = {'success': False, 'message': 'Login failed'}
            status_code = 401

        response = jsonify(response_data)
        response.headers['Allow'] = 'POST'
        return make_response(response, status_code)
    else:
        response_data = {'message': 'Method Not Allowed'}
        response = jsonify(response_data)
        response.headers['Allow'] = 'POST'
        return make_response(response, 405)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
