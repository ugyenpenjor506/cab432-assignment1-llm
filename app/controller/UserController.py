from app import app
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from app.model.Model import db, User

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
