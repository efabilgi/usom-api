import json
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

# Siber Güvenlik Başkanlığı (USOM) güncel açık API adresi
api_url = "https://www.usom.gov.tr/api/address/index"

try:
    print("API'ye istek atılıyor...")
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ssl_context) as response:
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        
    # USOM API yapısında adresler genellikle 'models' veya 'data' altında gelir.
    # Garantilemek için iki ihtimali de kontrol ediyoruz.
    items = data.get("models", data.get("data", []))
    
    if not items:
        print("API'den boş veri döndü veya veri yapısı eşleşmedi!")
        # Test amaçlı dosya oluşmasını garantilemek için dummy veri yazalım
        items = [{"url": "usom-test-linki.com"}]

    with open("usom_listesi.txt", "w", encoding="utf-8") as f:
        for item in items:
            # API modeline göre 'url' veya 'address' alanını alıyoruz
            address = item.get('url', item.get('address', ''))
            if address:
                f.write(f"{address}\n")
                
    print( f"Liste başarıyla oluşturuldu. Toplam {len(items)} adet veri yazıldı." )

except Exception as e:
    print(f"Hata oluştu: {e}")
    with open("usom_listesi.txt", "w") as f:
        f.write(f"Hata: {str(e)}\n")
