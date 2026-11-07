import json,re,os,shutil,html,urllib.parse as up
D=json.load(open('data/site.json',encoding='utf-8'));O='dist'
T=str.maketrans("çğıöşüÇĞİÖŞÜ","cgiosuCGIOSU")
slug=lambda s:re.sub(r'[^a-z0-9]+','-',s.translate(T).lower()).strip('-')
e=html.escape;N=e(D['name']);dg=re.sub(r'\D','',D['phone']);tel='+90'+dg[1:]
WA='https://wa.me/90'+dg[1:]+'?text='+up.quote('Merhaba, pimapen için teklif almak istiyorum.')
U=D['site_url'].rstrip('/')
NAV=[('/','Ana Sayfa'),('/hizmetler/','Hizmetler'),('/fiyatlar/','Fiyatlar'),('/hizmet-bolgeleri/','Hizmet Bölgeleri'),('/hakkimizda/','Hakkımızda'),('/sss/','SSS'),('/iletisim/','İletişim')]
IC={'wrench':'<path d="M14 6a4 4 0 0 0 5 5l-9 9a2 2 0 0 1-3-3l9-9a4 4 0 0 0-2-2z"/>','window':'<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M4 12h16"/>','mesh':'<rect x="3" y="4" width="18" height="16"/><path d="M3 9h18M3 14h18M9 4v16M15 4v16"/>','balcony':'<rect x="3" y="4" width="18" height="12"/><path d="M9 4v12M15 4v12M3 20h18"/>','door':'<rect x="6" y="3" width="12" height="18"/><circle cx="15" cy="12" r="1"/>'}
ic=lambda n:f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC.get(n,IC["window"])}</svg>'
def cta():return f'<div class="row"><a class="btn" href="tel:{tel}">Hemen Ara</a><a class="btn wa" href="{WA}">WhatsApp\'tan Teklif İste</a></div>'
def sec(t,b,c=''):return f'<section class="s {c}"><div class="w"><h2>{t}</h2>{b}</div></section>'
def prices():return '<table><tbody>'+''.join(f'<tr><td>{e(p["label"])}</td><td class="pr">{e(p["price"])}</td></tr>' for p in D['prices'])+'</tbody></table><p class="mut">Fiyatlar bilgilendirme amaçlıdır; kesin ücret yerinde belirlenir.</p>'
def tags():return '<div class="tags">'+''.join(f'<a class="tag" href="/{slug(d["name"])}-pimapen-tamiri/">{e(d["name"])}</a>' for d in D['districts'])+'</div>'
def faq(n=99):return ''.join(f'<details><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>' for f in D['faq'][:n])
def cards():return '<div class="grid">'+''.join(f'<a class="card" href="/hizmetler/#{slug(s["title"])}">{ic(s["icon"])}<h3>{e(s["title"])}</h3><p>{e(s["desc"])}</p></a>' for s in D['services'])+'</div>'
WIN='<svg viewBox="0 0 220 220" role="img" aria-label="Pencere illüstrasyonu"><rect x="30" y="20" width="160" height="180" rx="8" fill="none" stroke="currentColor" stroke-width="8"/><path d="M110 20v180M30 110h160" stroke="currentColor" stroke-width="6"/><path d="M52 44l24 24" stroke="var(--acc)" stroke-width="6" stroke-linecap="round"/></svg>'
pages=[]
def page(url,title,desc,body,ld=''):
    pages.append(url);nav=''.join(f'<a href="{u}"{" aria-current=page" if u==url else ""}>{n}</a>' for u,n in NAV)
    h=f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{U}{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{U}{url}">
<link rel="stylesheet" href="/style.css">{ld}</head><body><a class="skip" href="#i">İçeriğe geç</a>
<header><div class="w hd"><a class="logo" href="/">{N}</a><button id="m" class="menu" aria-expanded="false" aria-controls="n" aria-label="Menü">☰</button><nav id="n">{nav}</nav><a class="btn call" href="tel:{tel}">Hemen Ara</a></div></header>
<main id="i">{body}</main>
<footer><div class="w"><p><b>{N}</b> · İzmir · <a href="tel:{tel}">{e(D["phone"])}</a></p><p>{e(D["hours_text"])}</p></div></footer>
<div class="bar"><a class="btn" href="tel:{tel}">Ara</a><a class="btn wa" href="{WA}">WhatsApp</a></div>
<script>var m=document.getElementById('m'),n=document.getElementById('n');m.onclick=function(){{var o=n.classList.toggle('open');m.setAttribute('aria-expanded',o)}}</script></body></html>'''
    p=O+url;os.makedirs(p,exist_ok=True);open(p+'index.html','w',encoding='utf-8').write(h)
shutil.rmtree(O,ignore_errors=True);os.makedirs(O)
shutil.copytree('admin',O+'/admin')
ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":D['name'],"telephone":tel,"url":U,"priceRange":"800-6000 TL","address":{"@type":"PostalAddress","addressRegion":"İzmir","addressCountry":"TR"},"areaServed":[{"@type":"AdministrativeArea","name":d['name']+', İzmir'} for d in D['districts']],"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":D['opens'],"closes":D['closes']}]},ensure_ascii=False)+'</script>'
hero=lambda h,p,extra='':f'<section class="hero"><div class="w hg"><div><h1>{h}</h1><p class="lead">{p}</p>{cta()}{extra}</div><div class="art">{WIN}</div></div></section>'
trust='<ul class="trust"><li>Ücretsiz keşif sözü vermiyoruz; fiyatı baştan açık söylüyoruz</li><li>Net fiyat aralığı</li><li>Yerinde servis</li></ul>'
trust='<ul class="trust"><li>Net fiyat aralığı</li><li>Yerinde servis</li><li>Görünür çalışma saatleri</li></ul>'
ba='<div class="grid2"><div class="ph">Önce fotoğrafı<br>(yer tutucu)</div><div class="ph">Sonra fotoğrafı<br>(yer tutucu)</div></div>'
page('/','İzmir Pimapen Tamiri ve PVC Kapı-Pencere Servisi | '+D['name'],'İzmir’de pimapen tamiri, montajı, sineklik ve cam balkon servisi. Net fiyat aralığı, yerinde servis. Hemen arayın veya WhatsApp’tan teklif isteyin.',
 hero('İzmir Pimapen Tamiri ve PVC Kapı-Pencere Servisi','Menteşe, kol, kilit ve conta arızalarında yerinde onarım. Fiyatı baştan söyleriz.',trust)+sec('Hizmetlerimiz',cards())+sec('Başlangıç fiyatları',prices(),'alt')+sec('Hizmet verdiğimiz ilçeler',tags())+sec('Önce / sonra',ba,'alt')+sec('Sık sorulan sorular',faq(3)+'<p><a href="/sss/">Tüm soruları gör</a></p>'),ld)
page('/hizmetler/','Hizmetler: Pimapen Tamiri, Montaj, Sineklik, Cam Balkon | '+D['name'],'Pimapen tamiri, montajı, sineklik, cam balkon ve PVC kapı işleri: ne yapıldığı ve ne zaman gerektiği.',
 sec('Hizmetler',''.join(f'<article id="{slug(s["title"])}" class="card big">{ic(s["icon"])}<h3>{e(s["title"])}</h3><p><b>Ne yapılır:</b> {e(s["desc"])}</p><p><b>Ne zaman gerekir:</b> {e(s["when"])}</p></article>' for s in D['services'])+cta()))
page('/fiyatlar/','Pimapen Tamir Fiyatları | '+D['name'],'Pimapen tamiri, menteşe, kol, kilit, conta ve sineklik için başlangıç fiyatları. Kesin ücret yerinde belirlenir.',sec('Başlangıç fiyatları',prices()+cta()))
page('/hizmet-bolgeleri/','Hizmet Bölgeleri: İzmir İlçeleri | '+D['name'],'Karabağlar, Buca, Bornova, Konak, Karşıyaka, Bayraklı, Çiğli ve Gaziemir’de pimapen servisi.',sec('Hizmet bölgeleri',tags()+cta()))
page('/hakkimizda/','Hakkımızda | '+D['name'],D['name']+', İzmir’de pimapen tamiri ve montajı yapan yerinde servis ekibidir.',sec('Hakkımızda',f'<p>{N}, İzmir’de PVC pencere ve kapı arızalarını yerinde onarır. Önce bakar, sonra net fiyatı söyler, onayınızla işe başlarız.</p><p>[Buraya kendi hikâyenizi, deneyim yılınızı ve çalışma biçiminizi ekleyin.]</p>'+cta()))
page('/sss/','Sık Sorulan Sorular | '+D['name'],'Pimapen tamiri fiyatı, keşif, aynı gün servis ve garanti hakkında sık sorulan sorular.',sec('Sık sorulan sorular',faq()+cta()),'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in D['faq']]},ensure_ascii=False)+'</script>')
page('/iletisim/','İletişim | '+D['name'],'Pimapen servisi için arayın veya WhatsApp’tan yazın. Çalışma saatleri ve hizmet bölgeleri.',sec('İletişim',f'<p>Telefon / WhatsApp: <a href="tel:{tel}"><b>{e(D["phone"])}</b></a></p><p>Çalışma saatleri: {e(D["hours_text"])}</p><p>Bölgeler: {", ".join(e(d["name"]) for d in D["districts"])}</p>'+cta()+'<form name="iletisim" method="POST" data-netlify="true"><label>Adınız<input name="ad" required autocomplete="name"></label><label>Telefon<input name="telefon" type="tel" required autocomplete="tel"></label><label>Mesajınız<textarea name="mesaj" rows="4" required></textarea></label><button class="btn" type="submit">Mesaj Gönder</button></form>'))
for d in D['districts']:
    n=d['name'];s=slug(n)
    page(f'/{s}-pimapen-tamiri/',f'{n} Pimapen Tamiri ve PVC Kapı-Pencere Servisi | {D["name"]}',f'{n}’de pimapen tamiri, montaj, sineklik ve cam balkon servisi. {d["note"][:90]}',
     hero(f'{n} Pimapen Tamiri',f'{n}’de PVC kapı-pencere arızalarına yerinde servis.')+sec(f'{n} için not',f'<p class="note">{e(d["note"])}</p>')+sec('Yaptığımız işler','<ul class="list">'+''.join(f'<li>{e(x["title"])}: {e(x["desc"])}</li>' for x in D['services'])+'</ul>'+cta(),'alt')+sec('Diğer ilçeler',tags()))
open(O+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{U}{u}</loc></url>' for u in pages)+'</urlset>')
open(O+'/robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {U}/sitemap.xml\n')
open(O+'/style.css','w').write(open('style.css').read())
print(len(pages),'sayfa')
