import requests

def send_get_request(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text  # You can return the response content or other relevant information
    except requests.exceptions.RequestException as e:
        print(f"Failed to send GET request: {e}")
        return None

# API endpoint URL
api_url = "https://wondrous-pudding-b2d415.netlify.app/api/push/cry"

# Send GET request and print the response
response_content = send_get_request(api_url)
if response_content is not None:
    print(f"Response from the server:\n{response_content}")
