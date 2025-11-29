import urllib.request
import json

try:
    with urllib.request.urlopen('http://localhost:8000/feed') as response:
        if response.status == 200:
            data = response.read()
            posts = json.loads(data)
            if posts:
                print("First post keys:", posts[0].keys())
                print("First post ID:", posts[0].get('id'), posts[0].get('_id'))
            else:
                print("No posts found in feed.")
        else:
            print(f"Failed to get feed: {response.status}")
except Exception as e:
    print(f"Error: {e}")
