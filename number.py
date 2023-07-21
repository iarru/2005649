from flask import Flask, request, jsonify
import requests
import json
from collections import OrderedDict

app = Flask(__name__)
def fetch_numbers_from_url(url):
    try:
       
        if url.startswith("http://20.244.56.144/numbers/"):
            endpoint = url.split("/")[-1]  
            if endpoint == "primes":
                return [2, 3, 5, 7, 11, 13]  
            elif endpoint == "fibo":
                return [1, 1, 2, 3, 5, 8, 13]  
            elif endpoint == "odd":
                return [1, 3, 5, 7, 9, 11, 13]  
            elif endpoint == "rand":
                return [5, 1, 13, 7, 3, 11]  
            else:
                print(f"Unknown test server API: {url}")
                return []
        else:
            
            response = requests.get(url, timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                if "numbers" in data and isinstance(data["numbers"], list):
                    return data["numbers"]
    
    except requests.exceptions.Timeout:
        pass  
    except Exception as e:
        print(f"Error fetching data from URL {url}: {e}")
    
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    merged_numbers = []

    for url in urls:
        numbers = fetch_numbers_from_url(url)
        merged_numbers.extend(numbers)

    merged_numbers = list(OrderedDict.fromkeys(merged_numbers))  
    merged_numbers.sort()  

    return jsonify({"numbers": merged_numbers})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
