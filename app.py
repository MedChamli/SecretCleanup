from flask import Flask, render_template, request, redirect, url_for, make_response
import os
import jwt
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

# Generate a random secret key
app.secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

# Simulating user credentials
USER_CREDENTIALS = {
    'simple_user': os.environ.get('SIMPLE_USER_PASSWORD', 'default_simple_user_password')
}

# Secret key for JWT token (should be kept secret)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')

@app.route('/')
def index():
    return render_template('login.html', title='The Secret Cleanup')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'simple_user' and USER_CREDENTIALS.get(username) == password:
        # Generate JWT token for simple_user
        token = generate_jwt(username)
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('jwt_token', token, httponly=True)  # Set the JWT token in the cookie
        return response
    else:
        return redirect(url_for('index'))

def generate_jwt(username):
    # Set the expiration time for the token (e.g., 1 hour)
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    # Create the JWT token
    token_payload = {'username': username, 'exp': expiration_time}
    token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')

    return token

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('jwt_token')

    if token:
        # Decode the JWT token to get the username
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        current_username = decoded_token.get('username')

        if current_username == 'simple_user':
            # Redirect simple_user to an unauthorized page
            return render_template('unauthorized.html', title='Unauthorized')

        elif current_username == 'admin':
            # Read the content of flag.txt (replace with actual path)
            flag_content = read_flag()
            return render_template('dashboard.html', title='The Secret Cleanup - Dashboard', flag_content=flag_content)

    return render_template('unauthorized.html', title='Unauthorized')

def read_flag():
    # Replace with the actual path to flag.txt
    flag_path = os.path.join(os.path.dirname(__file__), 'flag.txt')

    # Read and return the content of flag.txt
    with open(flag_path, 'r') as flag_file:
        return flag_file.read()

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('jwt_token')  # Remove the JWT token from the cookie
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
