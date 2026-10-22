import sys
from PIL import Image, ImageDraw
import numpy as np
S=sys.argv[1] if len(sys.argv)>1 else '.'
PAPER=np.array([246,243,236],np.float32)
im=Image.open(f'{S}/build/hi-1.png').convert('RGB')
a=np.array(im).astype(np.float32)
L=a.mean(axis=2)
# outside region = white connected to border
b=Image.fromarray(np.where(L<235,0,255).astype(np.uint8))
b=Image.fromarray(np.pad(np.array(b),2,constant_values=255)).convert('RGB')
ImageDraw.floodfill(b,(0,0),(128,0,0))
outside=(np.array(b)[2:-2,2:-2,0]==128)
alpha=np.where(outside,np.clip((252-L)/(252-200),0,1),1.0)
# tint whites to paper: multiply
t=a/255.0
rgb=t*PAPER
rgba=np.dstack([rgb, alpha*255]).astype(np.uint8)
full=Image.fromarray(rgba,'RGBA')
O=(1100,200)
fun=[(670,85),(770,110),(650,420),(700,700),(722,875),(640,852),(520,810),(325,724),(178,632),(175,622),(500,370),(550,360)]
parts={
 'crivel':[(60,30),(1600,30),(1600,170),(1560,580),(1290,700),(1250,900),(60,900)],
 'descr':[(100,980),(920,980),(920,1420),(100,1420)],
 'firma':[(1960,2420),(2680,2420),(2680,2780),(1960,2780)],
 'imbuto':[(x+O[0],y+O[1]) for x,y in fun],
}
masks={}
for k,p in parts.items():
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon(p,fill=255); masks[k]=m
masks['crivel'].paste(0,mask=masks['imbuto'])
scene=Image.new('L',im.size,255)
for k in ['crivel','descr','firma']: scene.paste(0,mask=masks[k])
ImageDraw.Draw(scene).rectangle((0,0,1200,960),fill=0)
masks['scena']=scene
sm=scene.copy(); sm.paste(0,mask=masks['imbuto']); masks['scena_noimbuto']=sm
for k,m in masks.items():
    p=full.copy(); al=np.array(p.split()[3]).astype(np.float32)*(np.array(m)/255.)
    p.putalpha(Image.fromarray(al.astype(np.uint8)))
    p.save(f'{S}/livelli/{k}.png'); print(k,p.getbbox())
# full label too
full.save(f'{S}/livelli/etichetta.png')
