import os
import openai
import textwrap
from llama_index.core import Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.service_context import ServiceContext
from llama_index.llms.openai import OpenAI


class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

# Setup API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Load documents from a file
file_path = "dummy_ict_company_data.pdf"
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

def cpu_intensive_query_processing(response_text):
    # Simulating a CPU-intensive text processing task
    result = 0
    for _ in range(5000):
        # Perform complex string manipulations or other CPU-intensive operations
        result += sum(ord(char) for char in response_text)
        response_text = response_text[::-1]  # Reverse the text as a mock operation
    return result

# Main loop to handle queries from the user
while True:
    user_input = input(Color.YELLOW + "🤖 Enter your query (type 'quit' to exit): " + Color.RESET)
    
    if user_input.lower() == 'quit':
        print("Exiting...")
        break
    
    if query_engine:
        response = query_engine.query(user_input)
        response_text = str(response)
        
        # Introduce a CPU-intensive task related to query processing
        print(Color.BLUE + "Performing CPU-intensive query processing..." + Color.RESET)
        cpu_result = cpu_intensive_query_processing(response_text)
        print(Color.BLUE + f"Result of CPU-intensive query processing: {cpu_result}" + Color.RESET)
        
        line_width = 70
        wrapped_response = textwrap.fill(response_text, width=line_width)
        print(Color.GREEN + wrapped_response + Color.RESET)
    else:
        print(Color.RED + "Error: Query engine is not initialized." + Color.RESET)
