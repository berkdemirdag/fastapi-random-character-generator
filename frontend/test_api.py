import requests

def test_endpoint():
    url = "http://127.0.0.1:8000/generate_character"
    payload = {
        "race": "human",
        "gender": "male"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print(f"Failed with status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_endpoint()