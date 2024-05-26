import os
from dotenv import load_dotenv, find_dotenv
from icecream import ic

# Load the environment variables from the .env file
load_dotenv(find_dotenv())

# Fetch the 'data' environment variable
data = os.getenv('data')

# Print the loaded data for debugging
ic("Loaded data from .env:", data)

# Check if the data variable was fetched correctly
if data is None:
    raise ValueError("The 'data' environment variable is not set. Please check your .env file.")
