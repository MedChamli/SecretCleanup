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