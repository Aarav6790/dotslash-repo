import requests

def check_website_access(url):
    try:
        response = requests.get(url, timeout=10)  # Timeout to avoid hanging
        if response.status_code == 200:
            print(f"Successfully accessed {url}.")
        else:
            print(f"Failed to access {url}. Status code: {response.status_code}")
    except requests.ConnectionError:
        print(f"Failed to connect to {url}.")
    except requests.Timeout:
        print(f"Request to {url} timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
check_website_access("https://www.google.com")
