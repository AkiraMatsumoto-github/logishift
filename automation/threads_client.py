import os
import requests
import json

class ThreadsClient:
    def __init__(self):
        self.api_url = "https://graph.threads.net/v1.0"
        self.user_id = os.getenv("THREADS_USER_ID")
        self.access_token = os.getenv("THREADS_ACCESS_TOKEN")
        
        if not self.user_id or not self.access_token:
            print("Threads credentials missing. Skiping initialization.")
            self.valild = False
        else:
            self.valid = True
            print("Threads Client initialized.")

    def create_single_thread(self, text, url=None):
        """
        Create a single-post thread.
        
        Args:
            text (str): The content of the post.
            url (str, optional): A URL to attach (will generate a link card).
            
        Returns:
            dict: The response from the API containing the media ID, or None if failed.
        """
        if not self.valid:
            print("Threads client is not valid.")
            return None

        # 1. Create Media Container
        container_url = f"{self.api_url}/{self.user_id}/threads"
        
        payload = {
            "media_type": "TEXT",
            "text": text,
            "access_token": self.access_token
        }
        
        # Threads API allows passing a URL directly in the text for link preview,
        # but pure text media_type works best. 
        # If specific attachment behavior is needed, separate logic might be required.
        # For now, we assume the URL is inside the text, which Threads parses automatically.
        
        try:
            # Step 1: Create Container
            print(f"Creating Threads container...")
            response = requests.post(container_url, data=payload)
            
            if response.status_code != 200:
                print(f"Failed to create container: {response.text}")
                return None
            
            container_id = response.json().get('id')
            if not container_id:
                print("No container ID returned.")
                return None
                
            print(f"Container created: {container_id}")
            
            # Step 2: Publish Container
            publish_url = f"{self.api_url}/{self.user_id}/threads_publish"
            publish_payload = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            
            print(f"Publishing Thread...")
            pub_response = requests.post(publish_url, data=publish_payload)
            
            if pub_response.status_code != 200:
                print(f"Failed to publish thread: {pub_response.text}")
                return None
                
            result = pub_response.json()
            print(f"Thread published successfully. ID: {result.get('id')}")
            return result
            
        except Exception as e:
            print(f"Threads posting failed: {e}")
            return None

if __name__ == "__main__":
    # Test
    from dotenv import load_dotenv
    load_dotenv()
    
    client = ThreadsClient()
    if client.valid:
        # Dry run or simple test? 
        # Be careful not to spam.
        pass
