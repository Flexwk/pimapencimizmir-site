import json,re,os,shutil,html,urllib.parse as up

GTM_ID='GTM-M3PCGJ6F'   # Google Ads'in verdiği etiket kapsayıcısı
ADS_ID=''               # AW-... ile başlayan kimlik. Doluysa GTM yerine bu kullanılır
CONV={'phone_click':'','whatsapp_click':'','form_submit':''}   # her biri AW-xxx/yyy biçiminde
TRKJS="""(function(){var G='__G__',A='__A__',L=__L__,K='pz_consent',b=document.getElementById('cb');
function g(){try{return localStorage.getItem(K)}catch(e){return null}}
function st(v){try{localStorage.setItem(K,v)}catch(e){}}
function load(){if(window.__t)return;window.__t=1;window.dataLayer=window.dataLayer||[];var s=document.createElement('script');s.async=1;
if(A){window.gtag=function(){dataLayer.push(arguments)};s.src='https://www.googletagmanager.com/gtag/js?id='+A;gtag('js',new Date());gtag('config',A)}
else{dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});s.src='https://www.googletagmanager.com/gtm.js?id='+G}
document.head.appendChild(s)}
function ev(n){if(g()!=='1')return;window.dataLayer=window.dataLayer||[];dataLayer.push({event:n});if(A&&window.gtag&&L[n])gtag('event','conversion',{send_to:L[n]})}
var c=g();if(c==='1')load();else if(!c&&b)b.hidden=false;
document.getElementById('cy').onclick=function(){st('1');b.hidden=true;load();if(location.pathname==='/tesekkurler/')ev('form_submit')};
document.getElementById('cn').onclick=function(){st('0');b.hidden=true};
var k=document.getElementById('ck');if(k)k.onclick=function(e){e.preventDefault();b.hidden=false};
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';if(h.indexOf('tel:')===0)ev('phone_click');else if(h.indexOf('wa.me')>-1)ev('whatsapp_click')});
if(location.pathname==='/tesekkurler/'&&c==='1')ev('form_submit')})();"""
if GTM_ID or ADS_ID:
    TRK=TRKJS.replace('__G__',GTM_ID).replace('__A__',ADS_ID).replace('__L__',json.dumps(CONV))
    CB='<div id="cb" class="cb" role="dialog" aria-label="Çerez tercihleri" hidden><p>Siteyi geliştirmek ve reklamlarımızın etkisini ölçmek için çerez kullanabiliriz. Ayrıntılar: <a href="/gizlilik/">Gizlilik ve Çerezler</a>.</p><div class="row"><button id="cy" class="btn" type="button">Kabul et</button><button id="cn" class="btn o" type="button">Reddet</button></div></div>'
    CKL=' · <a href="#" id="ck">Çerez tercihleri</a>'
else:
    TRK=CB=CKL=''
D=json.load(open('data/site.json',encoding='utf-8'));O='dist'
T=str.maketrans("çğıöşüÇĞİÖŞÜ","cgiosuCGIOSU")
slug=lambda s:re.sub(r'[^a-z0-9]+','-',s.translate(T).lower()).strip('-')
e=html.escape;N=e(D['name']);dg=re.sub(r'\D','',D['phone']);tel='+90'+dg[1:]
WA='https://wa.me/90'+dg[1:]+'?text='+up.quote('Merhaba, pimapen için teklif almak istiyorum.')
U=D['site_url'].rstrip('/')
NAV=[('/','Ana Sayfa'),('/hizmetler/','Hizmetler'),('/fiyatlar/','Fiyatlar'),('/islerimiz/','İşlerimiz'),('/hizmet-bolgeleri/','Hizmet Bölgeleri'),('/hakkimizda/','Hakkımızda'),('/sss/','SSS'),('/iletisim/','İletişim')]
IC={'wrench':'<path d="M14 6a4 4 0 0 0 5 5l-9 9a2 2 0 0 1-3-3l9-9a4 4 0 0 0-2-2z"/>','window':'<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M4 12h16"/>','mesh':'<rect x="3" y="4" width="18" height="16"/><path d="M3 9h18M3 14h18M9 4v16M15 4v16"/>','balcony':'<rect x="3" y="4" width="18" height="12"/><path d="M9 4v12M15 4v12M3 20h18"/>','door':'<rect x="6" y="3" width="12" height="18"/><circle cx="15" cy="12" r="1"/>'}
ic=lambda n:f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC.get(n,IC["window"])}</svg>'
def cta():return f'<div class="row"><a class="btn" href="tel:{tel}">Hemen Ara</a><a class="btn wa" href="{WA}">WhatsApp\'tan Teklif İste</a></div>'
def sec(t,b,c=''):return f'<section class="s {c}"><div class="w"><h2>{t}</h2>{b}</div></section>'
def prices():return '<table><tbody>'+''.join(f'<tr><td>{e(p["label"])}</td><td class="pr">{e(p["price"])}</td></tr>' for p in D['prices'])+'</tbody></table><p class="mut">Fiyatlar bilgilendirme amaçlıdır; kesin ücret yerinde belirlenir.</p>'
def tags():return '<div class="tags">'+''.join(f'<a class="tag" href="/{slug(d["name"])}-pimapen-tamiri/">{e(d["name"])}</a>' for d in D['districts'])+'</div>'
def faq(n=99):return ''.join(f'<details><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>' for f in D['faq'][:n])
def cards():return '<div class="grid">'+''.join(f'<a class="card" href="/hizmetler/#{slug(s["title"])}">{ic(s["icon"])}<h3>{e(s["title"])}</h3><p>{e(s["desc"])}</p></a>' for s in D['services'])+'</div>'
WIN='<svg viewBox="0 0 220 220" role="img" aria-label="Pencere illüstrasyonu"><rect x="30" y="20" width="160" height="180" rx="8" fill="none" stroke="currentColor" stroke-width="8"/><path d="M110 20v180M30 110h160" stroke="currentColor" stroke-width="6"/><path d="M52 44l24 24" stroke="var(--acc)" stroke-width="6" stroke-linecap="round"/></svg>'
def brands():
    B=[b for b in (D.get('brands') or []) if b.get('name')]
    if not B:return ''
    it=''.join('<div class="bi">'+(f'<img src="{e(b["logo"])}" alt="{e(b["name"])}" loading="lazy">' if b.get('logo') else f'<span class="bn">{e(b["name"])}</span>')+'</div>' for b in B)
    hf=it*max(1,-(-8//len(B)))
    return f'<section class="s brands"><div class="w"><h2>Çalıştığımız Markalar</h2></div><div class="mq" role="group" aria-label="Çalıştığımız markalar"><div class="mt"><div class="hf">{hf}</div><div class="hf dup" aria-hidden="true">{hf}</div></div></div></section>'
BR=brands()
def about():
    t=(D.get('about') or '').strip()
    P=[x.strip() for x in re.split(r'\n\s*\n',t) if x.strip()] if t else [
     D['name']+', İzmir’de PVC pencere ve kapı sistemleri için yerinde tamir, bakım ve montaj hizmeti verir. Menteşe, kol, kilit ve conta arızalarından sineklik ve cam balkon mekanizmalarına kadar günlük hayatta en sık karşılaşılan işlerle ilgileniriz.',
     'Çalışma şeklimiz basit: arızayı yerinde görürüz, gerekeni ve maliyetini işe başlamadan önce söyleriz, siz onay verdikten sonra çalışırız. Fiyat aralıklarımızı sitede açıkça yayınlıyoruz; kesin ücret yerinde belirlenir.',
     'Çalışma saatlerimiz: '+D['hours_text']+'. Hizmet verdiğimiz ilçeler Hizmet Bölgeleri sayfasında listelenmiştir. Aramak veya WhatsApp’tan yazmak için aşağıdaki butonları kullanabilirsiniz.']
    return ''.join('<p>'+e(x)+'</p>' for x in P)
pages=[]
def page(url,title,desc,body,ld='',ni=0):
    nim='<meta name="robots" content="noindex">' if ni else '';(pages.append(url) if not ni else 0);nav=''.join(f'<a href="{u}"{" aria-current=page" if u==url else ""}>{n}</a>' for u,n in NAV)
    h=f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{U}{url}">{nim}
<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{U}{url}">
{ICON}<meta name="theme-color" content="#0b2a5b"><link rel="stylesheet" href="/style.css">{ld}</head><body><a class="skip" href="#i">İçeriğe geç</a>
<header><div class="w hd"><a class="logo" href="/">{N}</a><button id="m" class="menu" aria-expanded="false" aria-controls="n" aria-label="Menü">☰</button><nav id="n">{nav}</nav><a class="btn call" href="tel:{tel}">Hemen Ara</a></div></header>
<main id="i">{body}</main>{BR}
<footer><div class="w"><p><b>{N}</b> · İzmir · <a href="tel:{tel}">{e(D["phone"])}</a></p><p>{e(D["hours_text"])}</p><p><a href="/gizlilik/">Gizlilik ve Çerezler</a>{CKL}</p></div></footer>
<div class="bar"><a class="btn" href="tel:{tel}">Ara</a><a class="btn wa" href="{WA}">WhatsApp</a></div>
{CB}<script>{TRK}</script>
<script>var m=document.getElementById('m'),n=document.getElementById('n');m.onclick=function(){{var o=n.classList.toggle('open');m.setAttribute('aria-expanded',o)}}</script></body></html>'''
    p=O+url;os.makedirs(p,exist_ok=True);open(p+'index.html','w',encoding='utf-8').write(h)
shutil.rmtree(O,ignore_errors=True);os.makedirs(O)
shutil.copytree('admin',O+'/admin')
if os.path.isdir('static/img'):shutil.copytree('static/img',O+'/img')
if os.path.exists('favicon.png'):
    shutil.copy('favicon.png',O+'/favicon.png');ICON='<link rel="icon" type="image/png" href="/favicon.png"><link rel="apple-touch-icon" href="/favicon.png">'
else:
    open(O+'/favicon.svg','w',encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0b2a5b"/><rect x="16" y="12" width="32" height="40" rx="3" fill="none" stroke="#fff" stroke-width="4"/><path d="M32 12v40M16 32h32" stroke="#fff" stroke-width="3"/><circle cx="41" cy="22" r="3" fill="#ff6b1a"/></svg>')
    ICON='<link rel="icon" type="image/svg+xml" href="/favicon.svg">'

ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":D['name'],"telephone":tel,"url":U,"priceRange":"800-6000 TL","address":{"@type":"PostalAddress","addressRegion":"İzmir","addressCountry":"TR"},"areaServed":[{"@type":"AdministrativeArea","name":d['name']+', İzmir'} for d in D['districts']],"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":D['opens'],"closes":D['closes']}]},ensure_ascii=False)+'</script>'
hero=lambda h,p,extra='':f'<section class="hero"><div class="w hg"><div><h1>{h}</h1><p class="lead">{p}</p>{cta()}{extra}</div><div class="art">{WIN}</div></div></section>'
trust='<ul class="trust"><li>Ücretsiz keşif sözü vermiyoruz; fiyatı baştan açık söylüyoruz</li><li>Net fiyat aralığı</li><li>Yerinde servis</li></ul>'
trust='<ul class="trust"><li>Net fiyat aralığı</li><li>Yerinde servis</li><li>Görünür çalışma saatleri</li></ul>'
ba='<div class="grid2"><div class="ph">Önce fotoğrafı<br>(yer tutucu)</div><div class="ph">Sonra fotoğrafı<br>(yer tutucu)</div></div>'
def gal(n=None):
    G=(D.get('gallery') or [])[:n]
    if not G:return ba
    return '<div class="gl">'+''.join(f'<figure class="gi"><div class="grid2"><div><img src="{e(g["before"])}" alt="{e(g.get("title",""))} önce" loading="lazy"></div><div><img src="{e(g["after"])}" alt="{e(g.get("title",""))} sonra" loading="lazy"></div></div><figcaption>{e(g.get("title",""))}</figcaption></figure>' for g in G)+'</div>'
page('/','İzmir Pimapen Tamiri ve PVC Kapı-Pencere Servisi | '+D['name'],'İzmir’de pimapen tamiri, montajı, sineklik ve cam balkon servisi. Net fiyat aralığı, yerinde servis. Hemen arayın veya WhatsApp’tan teklif isteyin.',
 hero('İzmir Pimapen Tamiri ve PVC Kapı-Pencere Servisi','Menteşe, kol, kilit ve conta arızalarında yerinde onarım. Fiyatı baştan söyleriz.',trust)+sec('Hizmetlerimiz',cards())+sec('Başlangıç fiyatları',prices(),'alt')+sec('Hizmet verdiğimiz ilçeler',tags())+sec('Önce / sonra',gal(2)+'<p><a class="btn o" href="/islerimiz/">Tüm işlerimizi gör</a></p>','alt')+sec('Sık sorulan sorular',faq(3)+'<p><a href="/sss/">Tüm soruları gör</a></p>'),ld)
page('/islerimiz/','İşlerimiz: Önce ve Sonra Fotoğrafları | '+D['name'],'İzmir’de yaptığımız pimapen tamiri, montaj ve cam balkon işlerinden önce ve sonra fotoğrafları.',sec('İşlerimiz',gal()+cta()))
PRIV=('<p><b>Veri sorumlusu:</b> '+e(D['name'])+'. İletişim: '+e(D['phone'])+' veya <a href="/iletisim/">İletişim</a> sayfamız.</p>'
'<h3>Hangi verileri işliyoruz?</h3><p>İletişim formunu doldurduğunuzda yazdığınız ad, telefon numarası ve mesajınız. Bizi aradığınızda veya WhatsApp’tan yazdığınızda telefon numaranız ve mesajlarınız. Sitede dolaşırken, onay vermeniz hâlinde, ziyaretinize ilişkin teknik ve kullanım bilgileri (çerezler aracılığıyla).</p>'
'<h3>Ne amaçla kullanıyoruz?</h3><p>Taleplerinize dönüş yapmak, teklif hazırlamak, hizmeti yürütmek ve sitemizin ile reklamlarımızın performansını ölçmek.</p>'
'<h3>Çerezler</h3><p>Siteyi ziyaret ettiğinizde sizden bir tercih isteriz. <b>Kabul et</b> derseniz Google’ın ölçüm ve reklam etiketleri çalışır, <b>Reddet</b> derseniz bu etiketler yüklenmez. Tercihinizi sayfa altındaki “Çerez tercihleri” bağlantısından istediğiniz zaman değiştirebilirsiniz.</p>'
'<h3>Verileriniz kimlerle paylaşılır?</h3><p>Sitenin barındırılması, form mesajlarının alınması ve ölçüm hizmetleri için altyapı sağlayıcılarıyla (ör. Netlify, Google) paylaşılabilir. Bu sağlayıcılar verileri yurt dışındaki sunucularda da işleyebilir.</p>'
'<h3>Ne kadar saklıyoruz?</h3><p>Verilerinizi işleme amacının gerektirdiği süre boyunca ve yasal yükümlülüklerimiz kapsamında saklarız.</p>'
'<h3>Haklarınız</h3><p>6698 sayılı KVKK’nın 11. maddesi uyarınca verilerinizin işlenip işlenmediğini öğrenme, düzeltilmesini veya silinmesini isteme gibi haklara sahipsiniz. Taleplerinizi telefonla veya iletişim sayfamızdan iletebilirsiniz.</p>')
page('/gizlilik/','Gizlilik ve Çerezler | '+D['name'],'Kişisel verilerin işlenmesi ve çerez kullanımı hakkında bilgilendirme.',sec('Gizlilik ve Çerezler',PRIV))
page('/tesekkurler/','Teşekkürler | '+D['name'],'Mesajınız alındı.',sec('Mesajınız alındı','<p>Mesajınız bize ulaştı. Çalışma saatlerimiz içinde size dönüş yapmaya çalışacağız. Acil durumda arayabilirsiniz.</p>'+cta()),ni=1)
page('/hizmetler/','Hizmetler: Pimapen Tamiri, Montaj, Sineklik, Cam Balkon | '+D['name'],'Pimapen tamiri, montajı, sineklik, cam balkon ve PVC kapı işleri: ne yapıldığı ve ne zaman gerektiği.',
 sec('Hizmetler',''.join(f'<article id="{slug(s["title"])}" class="card big">{ic(s["icon"])}<h3>{e(s["title"])}</h3><p><b>Ne yapılır:</b> {e(s["desc"])}</p><p><b>Ne zaman gerekir:</b> {e(s["when"])}</p></article>' for s in D['services'])+cta()))
page('/fiyatlar/','Pimapen Tamir Fiyatları | '+D['name'],'Pimapen tamiri, menteşe, kol, kilit, conta ve sineklik için başlangıç fiyatları. Kesin ücret yerinde belirlenir.',sec('Başlangıç fiyatları',prices()+cta()))
page('/hizmet-bolgeleri/','Hizmet Bölgeleri: İzmir İlçeleri | '+D['name'],'Karabağlar, Buca, Bornova, Konak, Karşıyaka, Bayraklı, Çiğli ve Gaziemir’de pimapen servisi.',sec('Hizmet bölgeleri',tags()+cta()))
page('/hakkimizda/','Hakkımızda | '+D['name'],D['name']+', İzmir’de pimapen tamiri ve montajı yapan yerinde servis ekibidir.',sec('Hakkımızda',about()+cta()))
page('/sss/','Sık Sorulan Sorular | '+D['name'],'Pimapen tamiri fiyatı, keşif, aynı gün servis ve garanti hakkında sık sorulan sorular.',sec('Sık sorulan sorular',faq()+cta()),'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in D['faq']]},ensure_ascii=False)+'</script>')
page('/iletisim/','İletişim | '+D['name'],'Pimapen servisi için arayın veya WhatsApp’tan yazın. Çalışma saatleri ve hizmet bölgeleri.',sec('İletişim',f'<p>Telefon / WhatsApp: <a href="tel:{tel}"><b>{e(D["phone"])}</b></a></p><p>Çalışma saatleri: {e(D["hours_text"])}</p><p>Bölgeler: {", ".join(e(d["name"]) for d in D["districts"])}</p>'+cta()+'<form name="iletisim" method="POST" action="/tesekkurler/" data-netlify="true"><label>Adınız<input name="ad" required autocomplete="name"></label><label>Telefon<input name="telefon" type="tel" required autocomplete="tel"></label><label>Mesajınız<textarea name="mesaj" rows="4" required></textarea></label><button class="btn" type="submit">Mesaj Gönder</button></form>'))
for d in D['districts']:
    n=d['name'];s=slug(n)
    page(f'/{s}-pimapen-tamiri/',f'{n} Pimapen Tamiri ve PVC Kapı-Pencere Servisi | {D["name"]}',f'{n}’de pimapen tamiri, montaj, sineklik ve cam balkon servisi. {d["note"][:90]}',
     hero(f'{n} Pimapen Tamiri',f'{n}’de PVC kapı-pencere arızalarına yerinde servis.')+sec(f'{n} için not',f'<p class="note">{e(d["note"])}</p>')+sec('Yaptığımız işler','<ul class="list">'+''.join(f'<li>{e(x["title"])}: {e(x["desc"])}</li>' for x in D['services'])+'</ul>'+cta(),'alt')+sec('Diğer ilçeler',tags()))
open(O+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{U}{u}</loc></url>' for u in pages)+'</urlset>')
open(O+'/robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {U}/sitemap.xml\n')
X='.cb{position:fixed;left:12px;right:12px;bottom:12px;z-index:20;max-width:560px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 8px 30px rgba(0,0,0,.25)}.cb[hidden]{display:none}.cb p{margin:0 0 10px;font-size:15px}@media(max-width:900px){.cb{bottom:78px}}.mq{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}.mt{display:flex;width:max-content;animation:mq 35s linear infinite}.mq:hover .mt{animation-play-state:paused}.hf{display:flex}.bi{flex:none;display:flex;align-items:center;justify-content:center;min-width:160px;height:72px;padding:0 24px;margin-right:16px;border:1px solid var(--line);border-radius:12px;background:var(--card)}.bi img{max-height:44px;max-width:140px;object-fit:contain}.bn{font-weight:800;font-size:18px;color:var(--mut);white-space:nowrap}@keyframes mq{to{transform:translateX(-50%)}}@media(prefers-reduced-motion:reduce){.mq{overflow-x:auto;-webkit-mask-image:none;mask-image:none}.dup{display:none}}nav a{padding:12px 8px}.btn.o{background:transparent;color:var(--fg);border:2px solid currentColor}.btn.o:hover{border-color:var(--acc)}.gi{margin:0 0 24px}.gi img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:14px;display:block}.gi .grid2>div{position:relative}.lb{position:absolute;left:10px;top:10px;background:var(--hd);color:#fff;padding:2px 10px;border-radius:99px;font-size:14px}.gi figcaption{margin-top:8px;color:var(--mut);font-size:15px}'
open(O+'/style.css','w').write(open('style.css').read()+X)
print(len(pages),'sayfa')
