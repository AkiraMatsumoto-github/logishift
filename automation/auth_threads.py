import os
import requests
import http.server
import socketserver
import webbrowser
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
REDIRECT_URI = "https://localhost/"  # Adjust if using a different redirect URI in App Settings but localhost is standard for tests
# Note: Threads API requires HTTPS for redirect. Localhost might need self-signed cert or simply copy-pasting the code manually if strict.
# actually, usually http://localhost is allowed for development, but documentation says https.
# We will start a simple server and ask user to paste the code if redirect fails or just parse the URL.

def get_auth_code(client_id, redirect_uri, scope):
    auth_url = "https://threads.net/oauth/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code"
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    print(f"\n--- Step 1: Authorization ---")
    print(f"Please visit the following URL to authorize the app:")
    print(f"\n{url}\n")
    print("After authorization, you will be redirected to a URL starting with your Redirect URI.")
    print("Please paste the full redirected URL here (or just the 'code' parameter):")
    
    redirected_url = input("Redirected URL: ").strip()
    
    parsed = urllib.parse.urlparse(redirected_url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    # support pasting just the code or the full url
    if 'code' in query_params:
        return query_params['code'][0]
    elif 'code' not in redirected_url:
        # assume entire string is code if simpler format
        return redirected_url
    else:
        # direct paste
        return redirected_url

def exchange_for_token(client_id, client_secret, redirect_uri, code):
    token_url = "https://graph.threads.net/oauth/access_token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": code
    }
    
    print(f"\n--- Step 2: Exchanging code for Short-Lived Token ---")
    response = requests.post(token_url, data=payload)
    
    if response.status_code != 200:
        print(f"Error getting token: {response.text}")
        return None, None
        
    data = response.json()
    access_token = data.get('access_token')
    user_id = data.get('user_id')
    return access_token, user_id

def get_long_lived_token(client_secret, access_token):
    url = "https://graph.threads.net/access_token"
    params = {
        "grant_type": "th_exchange_token",
        "client_secret": client_secret,
        "access_token": access_token
    }
    
    print(f"\n--- Step 3: Exchanging for Long-Lived Token ---")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error getting long-lived token: {response.text}")
        return None
        
    data = response.json()
    return data.get('access_token')

def main():
    print("=== Threads API Authentication Helper ===")
    print("This script helps you obtain your Access Token and User ID.")
    print("You need your App ID and App Secret from the Meta Developer Dashboard.\n")
    
    client_id = input("Enter App ID (Client ID): ").strip()
    client_secret = input("Enter App Secret (Client Secret): ").strip()
    
    # Default scope for posting
    scope = "threads_basic,threads_content_publish"
    
    # Step 1: Get Auth Code
    # Ideally should match what's set in console.
    # We'll use a manually pasted code approach to avoid HTTPS local server complexity
    redirect_uri = input("Enter Redirect URI (as set in App Dashboard, e.g., https://localhost/): ").strip()
    
    code = get_auth_code(client_id, redirect_uri, scope)
    if not code:
        print("Failed to get auth code.")
        return

    # Step 2: Get Short Lived Token
    short_token, user_id = exchange_for_token(client_id, client_secret, redirect_uri, code)
    if not short_token:
        print("Failed to get short-lived token.")
        return
        
    print(f"Short-lived Token: {short_token[:10]}...")
    print(f"User ID: {user_id}")
    
    # Step 3: Get Long Lived Token
    long_token = get_long_lived_token(client_secret, short_token)
    
    if long_token:
        print("\n" + "="*50)
        print("SUCCESS! Add these to your .env file:")
        print("="*50)
        print(f"THREADS_APP_ID={client_id}")
        print(f"THREADS_APP_SECRET={client_secret}")
        print(f"THREADS_USER_ID={user_id}")
        print(f"THREADS_ACCESS_TOKEN={long_token}")
        print("="*50)
    else:
        print("Failed to get long-lived token.")

if __name__ == "__main__":
    main()
