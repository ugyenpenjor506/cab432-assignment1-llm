import os
import openai
from llama_index.core import Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.service_context import ServiceContext
from llama_index.llms.openai import OpenAI
import textwrap
from flask import jsonify
from app.service.DatabaseService import DatabaseService

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

class ApiService:
    
    @staticmethod
    def cpu_intensive_query_processing(response_text):
        # Simulating a CPU-intensive text processing task
        result = 0
        for _ in range(5000):
            # Perform complex string manipulations or other CPU-intensive operations
            result += sum(ord(char) for char in response_text)
            response_text = response_text[::-1]  # Reverse the text as a mock operation
        return result
    
    def openai_api(self, user_input, conversation_id, query_id):
        
        try:
            # Setup API key securely from environment variable
            openai.api_key = api_key

            if openai.api_key is None:
                return jsonify({"status": "error", "code": 500, "message": "OPENAI_API_KEY environment variable is not set."}), 500

            # Load documents from a file
            file_path = "experiment-dataset.pdf"
            if not os.path.exists(file_path):
                return jsonify({"status": "error", "code": 404, "message": f"File not found: {file_path}"}), 404

            documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

            # Create a document by concatenating text from all loaded documents
            document = Document(text="\n\n".join([doc.text for doc in documents]))

            # Initialize service context and query engine
            llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
            service_context = ServiceContext.from_defaults(
                llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
            )

            index = VectorStoreIndex.from_documents([document], service_context=service_context)
            query_engine = index.as_query_engine()

            if query_engine:
                response = query_engine.query(user_input)
                response_text = str(response)

                # Introduce a CPU-intensive task related to query processing
                cpu_result = apiService.cpu_intensive_query_processing(response_text)

                line_width = 70
                wrapped_response = textwrap.fill(response_text, width=line_width)
                
                databaseService.create_response(conversation_id, query_id, response_text)
                return jsonify({
                    "status": "success",
                    "code": 200,
                    "response": wrapped_response,
                    "cpu_result": cpu_result
                }), 200
            else:
                return jsonify({"status": "error", "code": 500, "message": "Query engine is not initialized"}), 500

        except ValueError as e:
            return jsonify({"status": "error", "code": 500, "message": str(e)}), 500

        except Exception as e:
            # General exception handler for unexpected errors
            return jsonify({"status": "error", "code": 500, "message": f"An unexpected error occurred: {str(e)}"}), 500
        return None


apiService = ApiService()   
databaseService = DatabaseService()