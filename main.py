"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "test",
  "email": "test@test.com",
  "password": "qwerty"
}'

curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/7264c537-a407-4db3-8879-ba7122f24941' \
  -H 'accept: text/plain'
"""
from pprint import pprint
import requests

url = "http://5.63.153.31:5051/v1/account"
headers = {
    'accept': '*/*',
    'Content-Type': 'application/json'
}
json = {
    "login": "kirka",
    "email": "kononirin@yandex.ru",
    "password": "qwerty123"
}

response = requests.post(
    url=url,
    headers=headers,
    json=json
)

print(response.status_code)
pprint(response.json())
response_json = response.json()

# url = "http://5.63.153.31:5051/v1/account/7264c537-a407-4db3-8879-ba7122f24941"
# headers = {
#     'accept': 'text/plain',
# }
#
# response = requests.put(
#     url=url,
#     headers=headers,
# )
#
# print(response.status_code)
# pprint(response.json())
# response_json = response.json()
# print(response_json['resource']['rating']['quantity'])