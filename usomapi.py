import json
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()
api_url = "https://www.usom.gov.tr/api/address/index"

# 1. Aşama: Manuel olarak bir dosya yazmayı dene (İzin testi)
try:
    with open("usom_listesi.txt", "w", encoding="utf-8") as f:
        f.write("usom-test-adresi-aktif.com\n")
        f.write("zararli-domain-ornek.net\n")
    print("Test verisi dosyaya yazildi.")
except Exception as e:
    print(f"Dosya yazma hatasi: {e}")

# 2. Aşama: API'den gerçek veriyi çekip üzerine eklemeyi dene
try:
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ssl_context) as response:
        data = json.loads(response.read().decode('utf-8'))
        
    items = data.get("models", data.get("data", []))
    if items:
        with open("usom_listesi.txt", "a", encoding="utf-8") as f:
            for item in items:
                address = item.get('url', item.get('address', ''))
                if address:
                    f.write(f"{address}\n")
        print(f"API'den {len(items)} adet gercek veri eklendi.")
except Exception as e:
    print(f"API cekme hatasi: {e}")
