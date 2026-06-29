import json
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

# Güncel USOM API adresi
api_url = "https://www.usom.gov.tr/api/address/index"

try:
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ssl_context) as response:
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        
    items = data.get("models", data.get("data", []))
    
    if not items:
        # Eğer API boş dönerse FortiGate hata almasın diye test satırı ekliyoruz
        items = [{"url": "usom-test-linki.com"}]

    with open("usom_listesi.txt", "w", encoding="utf-8") as f:
        for item in items:
            address = item.get('url', item.get('address', ''))
            if address:
                f.write(f"{address}\n")
                
    print("Liste basariyla olusturuldu.")
except Exception as e:
    with open("usom_listesi.txt", "w") as f:
        f.write(f"Hata: {str(e)}\n")
