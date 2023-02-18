import requests

url = "http://localhost:8000/food_items"
data = {
    "food_item": {
        "name": "Spaghetti",
    }
}
# files = {"file": open("spaghetti.jpg", "rb")}
response = requests.post(url, data=data)
print(response.json())