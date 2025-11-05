import requests
import json

# Test the API endpoints
def test_api():
    base_url = "http://localhost:5001"  # Adjust this to your backend URL
    
    # Test getting next token
    try:
        response = requests.get(f"{base_url}/api/next-token")
        print("Next token response:", response.status_code, response.json())
    except Exception as e:
        print("Error getting next token:", e)
    
    # Test submitting user data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "address": "123 Test Street",
        "contact_number": "123-456-7890",
        "work_description": "Test work description"
    }
    
    try:
        response = requests.post(f"{base_url}/api/submit", json=user_data)
        print("Submit user response:", response.status_code, response.json())
    except Exception as e:
        print("Error submitting user:", e)

if __name__ == "__main__":
    test_api()