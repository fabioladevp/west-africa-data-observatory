import requests

url = "https://api.worldbank.org/v2/country/TGO/indicator/NY.GDP.MKTP.CD"

params = {
    "format": "json",
    "per_page": 10
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

for observation in data[1]:
    year = observation["date"]
    value = observation["value"]

    print(year, value)