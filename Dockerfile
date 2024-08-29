# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /LLMAPP

# Set environment variable for OpenAI API Key
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Copy the requirements file and install dependencies
ADD requirements.txt /LLMAPP
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
ADD . /LLMAPP

# Expose the correct port (5005) that the Flask app will run on
EXPOSE 5005

# Set the entry point to run the Flask app
ENTRYPOINT ["python3"]
CMD ["main.py"]
