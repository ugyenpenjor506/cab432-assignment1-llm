from app import app
from app.service.ApiService import ApiService
from app.service.DatabaseService import DatabaseService
import jwt
from flask import jsonify, request
from functools import wraps
from flask_cors import CORS

# Enable CORS for all routes
CORS(app)

class ChatController:
    
    # Decorator to secure routes with JWT
    def token_required(f):
        # Secret key for encoding and decoding the JWT (same as used in the login route)
        SECRET_KEY = 'hg54376*6'
        
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Check if the Authorization header is present
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                token = auth_header.split(" ")[1]  # Expecting 'Bearer <token>'
            
            if not token:
                return jsonify({"status": "error", "code": 401, "message": "Token is missing"}), 401
            
            try:
                # Decode the token
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_user_id = data['user_id']
            except jwt.ExpiredSignatureError:
                return jsonify({"status": "error", "code": 401, "message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"status": "error", "code": 401, "message": "Invalid token"}), 401
            
            # Pass the current_user_id to the route
            return f(current_user_id, *args, **kwargs)
        
        return decorated

    @app.route('/chat', methods=['POST'], strict_slashes=False)
    @token_required
    def chatQuery(current_user_id):
        
        # Create a conversation and get the result
        create_conversation = databaseService.create_conversation(current_user_id)
        
        if create_conversation is None:
            return jsonify({"status": "error", "code": 500, "message": "Failed to create conversation"}), 500

        # Now you can safely access the ConversationID
        user_input = request.json.get("query")
        create_query = databaseService.create_query(create_conversation.ConversationID, user_input)
        
        if not user_input:
            return jsonify({"status": "error", "code": 400, "message": "No query provided"}), 400
        else:
            return apiService.openai_api(user_input, create_conversation.ConversationID, create_query.QueryID)
   

# Instantiate the controller to ensure the route is registered
apiService = ApiService()
databaseService = DatabaseService()
