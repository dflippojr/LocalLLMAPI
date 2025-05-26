import requests
import json
import time
import sys

def ensure_model_loaded():
    try:
        # Check if model exists
        response = requests.get('http://localhost:11434/api/tags')
        response.raise_for_status()
        models = response.json()['models']
        
        # Check if deepseek-r1 is already loaded
        if not any(model['name'] == 'deepseek-r1' for model in models):
            print("Pulling deepseek-r1 model...")
            response = requests.post('http://localhost:11434/api/pull',
                                  json={"name": "deepseek-r1"})
            response.raise_for_status()
            print("Model loaded successfully!")
        else:
            print("Model already loaded!")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama server. Please ensure Ollama is running.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        sys.exit(1)

def query_model(prompt):
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "deepseek-r1",
                                   "prompt": prompt,
                                   "stream": False
                               })
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"Error querying model: {str(e)}")
        return None

def main():
    # Ensure model is loaded
    ensure_model_loaded()
    
    print("\nReady to chat with deepseek-r1 model.")
    print("Type your queries (type 'exit' to quit):")
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'exit':
                break
                
            response = query_model(user_input)
            if response:
                print("\nResponse:", response)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
