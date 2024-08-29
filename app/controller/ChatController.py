from app import app
from app.service.ApiService import ApiService
from flask import jsonify, request

class ChatController:

    @app.route('/chat', methods=['POST'], strict_slashes=False)
    def chatQuery():
        user_input = request.json.get("query")
        
        if not user_input:
            return jsonify({"status": "error", "code": 400, "message": "No query provided"}), 400
        else:
            return apiService.openai_api(user_input)    

# Instantiate the controller to ensure the route is registered
apiService = ApiService()

