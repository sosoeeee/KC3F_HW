import requests

url = 'http://127.0.0.1:3009/GetButton'
response = requests.get(url)
# variable = response.json()['variable']
print(response)
