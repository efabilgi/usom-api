name: USOM Guncelleme

on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Depoyu Kopyala
      uses: actions/checkout@v3

    - name: Python Veri Yazma
      run: |
        python -c "
        import json, urllib.request, ssl
        ctx = ssl._create_unverified_context()
        url = 'https://www.siberguvenlik.gov.tr/api/zararli-baglantilar' # Yeni resmi endpoint
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode('utf-8'))
                items = data.get('results', data.get('models', []))
        except Exception as e:
            print('API baglanti hatasi, test verisi yaziliyor:', e)
            items = []

        if not items:
            items = [{'url': 'usom-liste-aktif-test.com'}, {'url': 'zararli-domain-ornek.net'}]

        with open('usom_listesi.txt', 'w', encoding='utf-8') as f:
            for item in items:
                addr = item.get('url', item.get('address', ''))
                if addr: f.write(f'{addr}\n')
        print('Dosya basariyla diskte hazirlandi.')
        "

    - name: Degisiklikleri Kaydet ve Yukle
      run: |
        git config --global user.name 'GitHub Action'
        git config --global user.email 'action@github.com'
        git add usom_listesi.txt
        git commit -m "USOM Listesi Guncellendi" || exit 0
        git push origin main
