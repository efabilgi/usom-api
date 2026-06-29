import json
import urllib.request

api_url = "https://www.siberguvenlik.gov.tr/api/zararli-baglantilar"

try:
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
    with open("usom_listesi.txt", "w") as f:
        for item in data.get("results", []):
            f.write(f"{item.get('url')}\n")
            
    print("Liste başarıyla güncellendi.")
except Exception as e:
    print(f"Hata oluştu: {e}")
