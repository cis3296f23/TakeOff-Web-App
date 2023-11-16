from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  # Import the CORS module
import secrets

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes or specify origins with CORS(app, origins="*") for all origins

# In-memory storage for tokens (for demonstration purposes)
token_store = {}

# Handle POST request to '/login'
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request
        username = data.get('username')
        hashed_password = data.get('hashedPassword')

        # Here, you would typically handle authentication logic
        # For example, check credentials against a database

        # Dummy response for demonstration
        if username == 'john_doe' and hashed_password == '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8':
            # Generate a token for the authenticated user
            token = secrets.token_hex(16)
            token_store[token] = username
            response_data = {'success': True, 'message': 'Login successful', 'token': token}
            status_code = 200
        else:
            response_data = {'success': False, 'message': 'Login failed'}
            status_code = 401

        response = jsonify(response_data)
        response.headers['Allow'] = 'POST'  # Set Allow header for POST method
        return make_response(response, status_code)
    else:
        # Handle other methods (e.g., if someone tries a different method for /login)
        response_data = {'message': 'Method Not Allowed'}
        response = jsonify(response_data)
        response.headers['Allow'] = 'POST'  # Set Allow header for POST method
        return make_response(response, 405)

if __name__ == '__main__':
    print("Running")
    app.run(debug=True)  # Run the app
