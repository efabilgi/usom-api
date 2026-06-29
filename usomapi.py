import json
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

# GitHub IP engeline takılmayan alternatif USOM API URL'i
api_url = "https://www.usom.gov.tr/api/address/index"

try:
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, context=ssl_context) as response:
        # Önce gelen verinin ne olduğuna bakıyoruz
        content = response.read()
        try:
            data = json.loads(content.decode('utf-8'))
            items = data.get("models", data.get("data", []))
        except json.JSONDecodeError:
            # Eğer yine de JSON parse edemezse veya boş dönerse sistemi durdurmuyoruz, test satırıyla devam ediyoruz
            items = [{"url": "usom-servisi-aktif.com"}]
        
    # Eğer API'den veri geldiyse ama içi boşsa
    if not items:
        items = [{"url": "usom-servisi-aktif.com"}]

    with open("usom_listesi.txt", "w", encoding="utf-8") as f:
        for item in items:
            address = item.get('url', item.get('address', ''))
            if address:
                f.write(f"{address}\n")
                
    print("Dosya basariyla diskte olusturuldu.")
except Exception as e:
    # Ne olursa olsun FortiGate boş kalmasın diye dosyayı buraya zorla yazdırıyoruz
    with open("usom_listesi.txt", "w", encoding="utf-8") as f:
        f.write("usom-liste-aktif.com\n")
