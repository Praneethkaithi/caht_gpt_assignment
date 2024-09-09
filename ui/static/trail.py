import requests
import json

# Step 1: Define your API key and URL
API_KEY = 'AIzaSyBz98U6j0wwVMIj3B-vS0Ynu9qVrxzpkEg'
API_URL = 'https://api.gemini.com/v1/your-endpoint'

# Step 2: Setup request headers including the API key for authentication
headers = {
    'Authorization': f'Bearer {API_KEY}',  # Token-based authentication
    'Content-Type': 'application/json'     # Set the content type to JSON
}

# Step 3: Define the input data that you will send to the API
data = {
    "input_data": "your_data_here"  # Replace with actual input for the model
}

# Step 4: Make the POST request to the API
response = requests.post(API_URL, headers=headers, json=data)

# Step 5: Process the response
if response.status_code == 200:
    # If request is successful, print the returned JSON data
    response_data = response.json()
    print("API Response:")
    print(json.dumps(response_data, indent=4))  # Pretty-print the response
else:
    # If the request failed, print the status code and error message
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")

