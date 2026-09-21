import json
import requests
from bs4 import BeautifulSoup

# Takip edilecek ürün listesi
PRODUCTS = [
    {"name": "iPhone 16 Pro Max 512GB", "url": "https://www.akakce.com/arama/?q=iphone+16+pro+max+512gb"},
    {"name": "PlayStation 5 Slim 1TB", "url": "https://www.akakce.com/arama/?q=playstation+5+slim"},
    {"name": "MacBook Pro M3 Max 16\"", "url": "https://www.akakce.com/arama/?q=macbook+pro+m3+max"},
    {"name": "Nike Air Jordan 1 High", "url": "https://www.akakce.com/arama/?q=air+jordan+1+high"},
    {"name": "Tesla Model Y Long Range", "url": "https://www.akakce.com/arama/?q=tesla+model+y"},
    {"name": "Samsung Galaxy S24 Ultra", "url": "https://www.akakce.com/arama/?q=galaxy+s24+ultra"},
    {"name": "AirPods Max Kulaklık", "url": "https://www.akakce.com/arama/?q=airpods+max"},
    {"name": "Nintendo Switch OLED", "url": "https://www.akakce.com/arama/?q=nintendo+switch+oled"},
    {"name": "Dyson V15 Detect Süpürge", "url": "https://www.akakce.com/arama/?q=dyson+v15"}
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def main():
    results = []
    print("Fiyat verileri taranıyor...")

    for p in PRODUCTS:
        try:
            res = requests.get(p["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            
            price_tag = soup.find("span", class_="pt_v8") or soup.find("span", class_="pr_v8")
            img_tag = soup.find("img", class_="p_v8") or soup.find("img", class_="i_v8")

            if price_tag:
                raw_price = price_tag.text.replace(".", "").replace(",", ".").replace("TL", "").strip()
                price = int(float(raw_price.split()[0]))
                img_url = img_tag["src"] if img_tag else ""
                if img_url and not img_url.startswith("http"):
                    img_url = "https:" + img_url

                results.append({
                    "name": p["name"],
                    "price": price,
                    "img": img_url or "https://via.placeholder.com/300"
                })
                print(f"✓ {p['name']}: {price} ₺")
        except Exception as e:
            print(f"✗ Hata ({p['name']}):", e)

    if results:
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("\nproducts.json başarıyla güncellendi!")

if __name__ == "__main__":
    main()
