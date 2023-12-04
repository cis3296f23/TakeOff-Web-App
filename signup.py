from flask import Flask, request, jsonify, make_response
import cx_Oracle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Establish cx_Oracle connection to Oracle database
dsn_tns = cx_Oracle.makedsn('oracle1.cis.temple.edu', '1521', service_name='cisora')
username = 'tup09776'
password = '916080352'
try:
    oracle_connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
    oracle_cursor = oracle_connection.cursor()
    print("Oracle DB Connection Successful")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Oracle DB Error:", error.message)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        new_username = data.get('newUsername')
        password_hash = data.get('hashedPassword')

        # Check if the user already exists in the database
        query_check_user = "SELECT * FROM user_accounts WHERE username = :uname"
        oracle_cursor.execute(query_check_user, uname=new_username)
        existing_user = oracle_cursor.fetchone()

        if existing_user:
            response_data = {'message': 'User already exists'}
            status_code = 409  # Conflict: User already exists
        else:
            # Create a new user in the database
            query_create_user = "INSERT INTO user_accounts(username, password_hash) VALUES(:uname, :hashed_pwd)"
            try:
                oracle_cursor.execute(query_create_user, uname=new_username, hashed_pwd=password_hash)
                oracle_connection.commit()
                response_data = {'success': True, 'message': 'Account created successfully'}
                status_code = 201  # Created: Account created
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                oracle_connection.rollback()
                response_data = {'message': f'Error creating account: {error.message}'}
                status_code = 500  # Internal Server Error

        response = jsonify(response_data)
        return make_response(response, status_code)

if __name__ == '__main__':
  app.run(debug=True, port=5002)
