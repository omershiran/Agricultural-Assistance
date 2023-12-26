from flask import Flask, request, jsonify

app = Flask(__name__)

# Assuming dbBridge is a module with function usernamePasswordMatch

@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    username = req_data.get('username')
    password = req_data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    response = usernamePasswordMatch(username, password)

    if response == 0:
        # Successful login
        return jsonify({'message': 'Login successful'}), 200
    else:
        # Invalid credentials
        return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
