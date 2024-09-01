from app import app
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_cors import CORS

from app.model.Model import db, User

# Enable CORS for all routes
CORS(app)

class UserController:
    
    @app.route('/create_user', methods=['POST'])
    def create_user():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                "error": "Username and password are required",
                "status": "fail",
                "code": 400
            }), 400

        # Check if a user with the same username or email already exists
        existing_user = User.query.filter((User.UserName == username) | (User.UserEmail == email)).first()
        if existing_user:
            return jsonify({
                "error": "Username or email already exists",
                "status": "fail",
                "code": 409
            }), 409

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user instance
        new_user = User(UserName=username, UserEmail=email, Password=hashed_password)

        # Add the user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                "message": "User created successfully",
                "status": "success",
                "code": 200
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "error": str(e),
                "status": "fail",
                "code": 500
            }), 500
            

    
    @app.route('/login', methods=['POST'])
    def login():
        SECRET_KEY = 'hg54376*6'
        data = request.get_json()
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        if not username_or_email or not password:
            return jsonify({
                "error": "Username/email and password are required",
                "status": "fail",
                "code": 400
            }), 400

        # Check if the user exists by username or email
        user = User.query.filter((User.UserName == username_or_email) | (User.UserEmail == username_or_email)).first()

        if user and check_password_hash(user.Password, password):
            # Login successful, generate JWT token
            token = jwt.encode({
                'user_id': user.UserID,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")

            # Return user information except for the password
            return jsonify({
                "message": "Login successful",
                "status": "success",
                "code": 200,
                "token": token,
                "user": {
                    "UserID": user.UserID,
                    "UserName": user.UserName,
                    "UserEmail": user.UserEmail,
                    "CreatedAt": user.CreatedAt.isoformat()  # Convert datetime to string
                }
            }), 200
        else:
            # Login failed
            return jsonify({
                "error": "Invalid username/email or password",
                "status": "fail",
                "code": 401
            }), 401