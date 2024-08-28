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

# Setup API key securely
openai.api_key = ""

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

def cpu_intensive_task(n):
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result

# Main loop to handle queries from the user
while True:
    user_input = input(Color.YELLOW + "🤖 Enter your query (type 'quit' to exit): " + Color.RESET)
    
    if user_input.lower() == 'quit':
        print("Exiting...")
        break
    
    # Introduce a CPU-intensive task before processing the query
    print(Color.BLUE + "Performing CPU-intensive calculations..." + Color.RESET)
    cpu_result = cpu_intensive_task(10000)  # Adjust the number for higher CPU usage
    print(Color.BLUE + f"Result of CPU-intensive task: {cpu_result}" + Color.RESET)
    
    if query_engine:
        response = query_engine.query(user_input)
        response_text = str(response)
        line_width = 70
        wrapped_response = textwrap.fill(response_text, width=line_width)
        print(Color.GREEN + wrapped_response + Color.RESET)
    else:
        print(Color.RED + "Error: Query engine is not initialized." + Color.RESET)
