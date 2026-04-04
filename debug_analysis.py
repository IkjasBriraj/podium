import asyncio
import os
import sys

# Ensure backend matches path
sys.path.append(os.getcwd())

from backend.app.services.ollama_service import OllamaService

async def test_ollama():
    print("1. Testing Ollama connection...")
    service = OllamaService()
    try:
        # Test basic generation
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.post(service.api_url, json={
                "model": "llava:7b",
                "prompt": "hello",
                "stream": False
            })
            print(f"Ollama Status: {resp.status_code}")
            if resp.status_code == 200:
                print("Ollama Response:", resp.json().get('response', '')[:50] + "...")
            else:
                print("Ollama Error:", resp.text)
    except Exception as e:
        print(f"CRITICAL: Could not connect to Ollama: {e}")

    print("\n2. Testing OpenCV...")
    try:
        import cv2
        print(f"OpenCV Version: {cv2.__version__}")
        # Create a dummy blank video to test reading
        # This part is hard without a real file, but we verify import
    except ImportError as e:
        print(f"CRITICAL: OpenCV Import Error: {e}")
    except Exception as e:
        print(f"OpenCV Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama())
