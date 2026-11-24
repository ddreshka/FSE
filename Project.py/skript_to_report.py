import json
import re
import time
import requests

url = "https://catalog.onliner.by/sdapi/catalog.api/search/dram"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


def get_gb(text: str) -> int | None:
    kit = re.search(r"(\d+)\s*[xх*]\s*(\d+)\s*ГБ", text, re.IGNORECASE)
    if kit:
        return int(kit.group(1)) * int(kit.group(2))
    single = re.search(r"(\d+)\s*ГБ", text, re.IGNORECASE)
    if single:
        return int(single.group(1))
    return None


def scan_ddr4_ram(pages_to_scan: int = 100) -> list[dict]:
    results = []

    for page in range(1, pages_to_scan + 1):
        print(f"\r⏳ Сканирование каталога Onliner.by: страница {page} из {pages_to_scan}", end="", flush=True)
        params = {
            f"dramkit{chr(91)}0{chr(93)}": "ddr4dimm",
            "dramkit[operation]": "union",
            "order": "price:asc",
            "page": page,
        }
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        products = response.json().get("products", [])

        if not products:
            break

        for item in products:
            prices = item.get("prices")
            if not prices or not prices.get("price_min"):
                continue

            desc = item.get("description", "")
            if "DDR4" not in desc:
                continue

            price = float(prices["price_min"]["amount"])
            volume = get_gb(desc)

            if volume and volume > 0:
                results.append({
                    "name": item.get("full_name"),
                    "volume_gb": volume,
                    "price_byn": price,
                    "price_per_gb": round(price / volume, 2),
                    "url": item.get("html_url"),
                })
        time.sleep(0.5)

    print("\r ✅ Сканирование завершено!                                      ")
    results.sort(key=lambda x: x["price_per_gb"])
    return results


def print_ui(deals: list[dict]) -> None:
    best = deals[0]
    line = "=" * 78

    print(f"\n{line}")
    print(" 🏆 САМАЯ ВЫГОДНАЯ ОПЕРАТИВНАЯ ПАМЯТЬ DDR4 НА ONLINER.BY")
    print(line)
    print(f" Модель      : {best['name']}")
    print(f" Объем       : {best['volume_gb']} ГБ")
    print(f" Цена        : {best['price_byn']:.2f} BYN")
    print(f" Выгода      : {best['price_per_gb']:.2f} BYN за 1 ГБ")
    print(f" Ссылка      : {best['url']}")
    print(f"{line}\n")

    print(" ТОП-5 ПРЕДЛОЖЕНИЙ ПО ЦЕНЕ ЗА 1 ГБ:")
    print(f" {'№':<3} | {'BYN/ГБ':<8} | {'Цена':<10} | {'Объем':<7} | {'Модель'}")
    print("-" * 78)
    for idx, item in enumerate(deals[:5], start=1):
        name_short = item['name'][:38] + "..." if len(item['name']) > 41 else item['name']
        print(f" {idx:<3} | {item['price_per_gb']:<8.2f} | {item['price_byn']:<10.2f} | {item['volume_gb']:>4} ГБ | {name_short}")
    print("-" * 78)


def main():
    print("=" * 78)
    print(" 🔍 ПОИСК ВЫГОДНОЙ ОПЕРАТИВНОЙ ПАМЯТИ DDR4 (ONLINER.BY)")
    print("=" * 78)

    try:
        deals = scan_ddr4_ram(pages_to_scan=100)
    except requests.RequestException as e:
        print(f"\n[❌] Ошибка сети при обращении к Onliner: {e}")
        return

    if not deals:
        print("\n[⚠️] Не удалось найти подходящие предложения DDR4.")
        return

    print_ui(deals)

if __name__ == "__main__":
    main()
