"""Create a geometric robot rig for the animation example."""
import json,sys,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(sys.argv[1]);p.mkdir(parents=True,exist_ok=True)
def layer(name,draw):
 im=Image.new('RGBA',(512,512));draw(ImageDraw.Draw(im));im.save(p/name)
layer('body.png',lambda d:d.rounded_rectangle((197,292,315,390),30,fill='#292c32'))
layer('head.png',lambda d:d.rounded_rectangle((151,145,361,315),45,fill='#292c32'))
layer('eyes.png',lambda d:[d.rounded_rectangle((x,207,x+25,248),11,fill='#b3e7c9') for x in (201,286)])
try:font=ImageFont.truetype('DejaVuSansMono.ttf',10)
except OSError:font=ImageFont.load_default()
# Distribute letters by ellipse arc length rather than angle; orient to tangent.
im=Image.new('RGBA',(512,512)); text='PLAYFORGE · '*3
points=[]; dist=0; previous=None
for k in range(2001):
 a=2*math.pi*k/2000; xy=(256+132*math.cos(a),430+23*math.sin(a))
 if previous:dist+=math.hypot(xy[0]-previous[0],xy[1]-previous[1])
 points.append((dist,a,xy));previous=xy
for i,ch in enumerate(text):
 target=dist*i/len(text);_,a,(x,y)=min(points,key=lambda z:abs(z[0]-target))
 glyph=Image.new('RGBA',(40,40));ImageDraw.Draw(glyph).text((20,20),ch,font=font,fill='#5f625f',anchor='mm')
 angle=-math.degrees(math.atan2(23*math.cos(a),-132*math.sin(a)))
 glyph=glyph.rotate(angle,Image.Resampling.BICUBIC);im.alpha_composite(glyph,(round(x-20),round(y-20)))
im.save(p/'type.png')
(p/'rig.json').write_text(json.dumps(dict(size=512,frames=400,duration_ms=20,background='#f7f3eb',mode='hop',cycles=8,body='body.png',head='head.png',head_pivot=[256,315],ground=392,eyes=[dict(path='eyes.png',center=[256,228])],feet=[],overlay='type.png',camera=True),indent=2))
print(p/'rig.json')

