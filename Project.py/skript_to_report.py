import requests

url = "https://catalog.onliner.by/sdapi/catalog.api/search/dram"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}
params = {
    "dramkit[0]": "ddr4dimm",
    "dramkit[operation]": "union",
}

response = requests.get(url, params=params, headers=headers, timeout=15)
print("Статус ответа:", response.status_code)

data = response.json()
print("Всего найдено:", data.get("total"))
print("Первый товар:", data["products"][0]["full_name"])