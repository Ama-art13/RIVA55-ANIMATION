import base64,sys,json,os
from PIL import Image
S=sys.argv[1] if len(sys.argv)>1 else '.'; a=f'{S}/livelli'
p=Image.open(f'{a}/scena.png'); al=p.split()[3].point(lambda v:255 if v>8 else 0); p.crop(al.getbbox()).save(f'{a}/scena.webp',quality=86,method=6)
e=Image.open(f'{a}/etichetta.png'); al=e.split()[3].point(lambda v:255 if v>8 else 0); bb=al.getbbox()
bg=Image.new('RGBA',e.size,(246,243,236,255)); bg.alpha_composite(e); c=bg.crop((bb[0]-30,bb[1]-30,bb[2]+30,bb[3]+30)); c=c.resize((420,round(420*c.height/c.width)),Image.LANCZOS); c.convert('RGB').save(f'{a}/etichetta.webp',quality=88); print('label mini',c.size)
assets={k:'data:image/webp;base64,'+base64.b64encode(open(f'{a}/{k}.webp','rb').read()).decode() for k in ['scena','imbuto','crivel','descr','firma','etichetta']}
src=open(f'{S}/anteprima/src.html').read().replace('const A = {/*ASSETS*/};','const A = '+json.dumps(assets)+';')
open(f'{S}/anteprima/crivel-carosello.html','w').write(src)
os.makedirs(f'{S}/build',exist_ok=True)
open(f'{S}/build/local.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+src+'</body></html>')
print(len(src)//1024,'KB')
