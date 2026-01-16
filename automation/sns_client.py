import os
import tweepy
from dotenv import load_dotenv

# Try importing ThreadsClient, graceful fail if file missing during transition
try:
    from automation.threads_client import ThreadsClient
except ImportError:
    try:
        from threads_client import ThreadsClient
    except ImportError:
        ThreadsClient = None

load_dotenv()

class SNSClient:
    def __init__(self):
        # X (Twitter) Credentials
        self.x_api_key = os.getenv("X_API_KEY")
        self.x_api_secret = os.getenv("X_API_SECRET")
        self.x_access_token = os.getenv("X_ACCESS_TOKEN")
        self.x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        self.x_client = None
        self.threads_client = None
        
        self._authenticate_x()
        self._authenticate_threads()

    def _authenticate_x(self):
        """Authenticate with X API v2"""
        if self.x_api_key and self.x_api_secret and self.x_access_token and self.x_access_token_secret:
            try:
                self.x_client = tweepy.Client(
                    consumer_key=self.x_api_key,
                    consumer_secret=self.x_api_secret,
                    access_token=self.x_access_token,
                    access_token_secret=self.x_access_token_secret
                )
                print("Authenticated with X (Twitter) successfully.")
            except Exception as e:
                print(f"Failed to authenticate with X: {e}")
                self.x_client = None
        else:
            print("X credentials missing in .env. Skipping X authentication.")

    def _authenticate_threads(self):
        """Initialize Threads Client"""
        if ThreadsClient:
            try:
                self.threads_client = ThreadsClient()
                if not self.threads_client.valid:
                    self.threads_client = None
            except Exception as e:
                print(f"Failed to initialize Threads Client: {e}")
                self.threads_client = None
        else:
            print("ThreadsClient class not available.")

    def post_to_x(self, content):
        """
        Post text content to X.
        """
        if not self.x_client:
            print("X client not initialized.")
            return None
            
        try:
            response = self.x_client.create_tweet(text=content)
            print(f"Posted to X successfully. ID: {response.data['id']}")
            return response.data
        except Exception as e:
            print(f"Failed to post to X: {e}")
            return None

    def post_to_threads(self, content):
        """
        Post text content to Threads.
        """
        if not self.threads_client:
            print("Threads client not initialized.")
            return None
            
        try:
            return self.threads_client.create_single_thread(text=content)
        except Exception as e:
            print(f"Failed to post to Threads: {e}")
            return None

if __name__ == "__main__":
    # Test
    client = SNSClient()
    if client.x_client:
        print("X: Ready")
    if client.threads_client:
        print("Threads: Ready")
