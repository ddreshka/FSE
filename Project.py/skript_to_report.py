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
products = response.json().get("products", [])

for item in products:
    prices = item.get("prices")
    if not prices or not prices.get("price_min"):
        continue

    if "DDR4" not in item.get("description", ""):
        continue

    price = float(prices["price_min"]["amount"])
    print(f"{item['full_name']} — {price} BYN")
