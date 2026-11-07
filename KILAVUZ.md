# Kılavuz

## Bilgileri nereden değiştirim?
`data/site.json` dosyası: işletme adı, telefon, saatler, hizmetler, fiyatlar, ilçeler (+ özel notları), SSS. Ya da yönetim paneli: `siteadresiniz.com/admin/`.
Değişiklikten sonra `python3 build.py` çalıştırın; `dist/` klasörü yayına hazır sitedir.

## Yayına alma (önerilen: GitHub + Netlify, ücretsiz)
1. Bu klasörü GitHub'a yeni bir depo olarak yükleyin.
2. netlify.com → Add new site → Import from Git → depoyu seçin. Build command: `python3 build.py`, Publish directory: `dist`.
3. `data/site.json` içinde `site_url` alanını gerçek alan adınızla değiştirin.
4. Alan adı: Netlify → Domain management → Add custom domain; alan adı sağlayıcınızda Netlify'ın verdiği DNS/CNAME kayıtlarını girin. HTTPS otomatik açılır.
5. Cloudflare Pages / GitHub Pages da çalışır (build: `python3 build.py`, çıktı: `dist`), ancak panel girişi için ek OAuth kurulumu gerekir.

## Yönetim paneli (Decap CMS)
1. `admin/config.yml` içinde `repo:` satırına `KULLANICI/DEPO` yazın.
2. Netlify → Site configuration → Access & security → OAuth → GitHub'ı etkinleştirin.
3. `/admin/` adresine gidin, GitHub ile girin (yalnız depoya yazma yetkisi olan hesap girebilir). Alanları düzenleyip Publish deyin; site birkaç dakikada güncellenir.
4. Mesaj formu Netlify Forms ile çalışır (Netlify panelinde Forms bölümünde görünür).
