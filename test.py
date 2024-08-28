import os
import openai
import textwrap
from llama_index.core import Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.service_context import ServiceContext
from llama_index.llms.openai import OpenAI
import numpy as np  # For additional processing
import hashlib  # For simulating additional text processing

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

# Setup API key securely
openai.api_key = "sk-zjEa7bYQ9IPKJJp4qSw4pK0eMGKlYYKMGACwyjF7-8T3BlbkFJS1c5W4aP3y6EyJ5lRdF8xzyTtjL6pJv1QqfLxI1nwA"

# Load documents from a file
file_path = "QUT_filtered.pdf"
documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

# Function to simulate a CPU-intensive task by processing document text
def process_document_text(text):
    # Simulate heavy text processing by repeatedly hashing the document text
    for _ in range(1000):  # Increase the number of iterations to increase CPU load
        text = hashlib.sha256(text.encode()).hexdigest()
    return text

# Create a document by concatenating and processing text from all loaded documents
processed_texts = [process_document_text(doc.text) for doc in documents]
document = Document(text="\n\n".join(processed_texts))

# Initialize service context and query engine
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
)

index = VectorStoreIndex.from_documents([document], service_context=service_context)
query_engine = index.as_query_engine()

# Function to simulate a CPU-intensive task during query processing
def intensive_query_processing(query):
    # Simulate complex computations related to query processing
    query_vector = np.random.rand(1000)  # Simulate a query vector
    document_vector = np.random.rand(1000)  # Simulate a document vector
    similarity_score = np.dot(query_vector, document_vector)  # Simulate similarity calculation
    return similarity_score

# Main loop to handle queries from the user
while True:

    user_input = input(Color.YELLOW + "🤖 Enter your query (type 'quit' to exit): " + Color.RESET)

    if user_input.lower() == 'quit':
        print("Exiting...")
        break

    # Introduce the CPU-intensive task during query processing
    similarity_score = intensive_query_processing(user_input)

    if query_engine:
        response = query_engine.query(user_input)
        response_text = str(response) + f"\n\nSimilarity Score: {similarity_score}"
        line_width = 70
        wrapped_response = textwrap.fill(response_text, width=line_width)
        print(Color.GREEN + wrapped_response + Color.RESET)
    else:
        print(Color.RED + "Error: Query engine is not initialized." + Color.RESET)
