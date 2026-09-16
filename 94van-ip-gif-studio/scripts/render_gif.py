"""Small explicit-layer 2D GIF renderer; no automatic segmentation or video generation."""
import argparse, io, json, math, os
from pathlib import Path
from PIL import Image, ImageDraw
R = Image.Resampling.BICUBIC

def smooth(x):
    x=max(0., min(1., x)); return x*x*(3-2*x)

def blink(t, times):
    for start in times:
        q=t-start
        if 0<=q<.07:return 1-.96*smooth(q/.07)
        if .07<=q<.11:return .04
        if .11<=q<.24:return .04+.96*smooth((q-.11)/.13)
    return 1.

def warp(im, sx=1., sy=1., center=None, dy=0):
    cx,cy=center or (im.width/2,im.height/2)
    return im.transform(im.size,Image.Transform.AFFINE,(1/sx,0,cx-cx/sx,0,1/sy,cy-(cy+dy)/sy),R)

def render(config, target):
    c=json.loads(Path(config).read_text()); root=Path(config).parent
    n=c.get('size',512); count=c.get('frames',400); dt=c.get('duration_ms',20); cycles=c.get('cycles',8)
    if any(type(v) is not int for v in (n,count,dt,cycles)):raise ValueError('size, frames, duration_ms, cycles must be integers')
    if n<32 or n>2048 or count<2 or dt<10 or dt%10:raise ValueError('Invalid size, frames, or GIF duration (10ms multiples required)')
    if not isinstance(cycles,int) or cycles<1:raise ValueError('cycles must be a positive integer')
    mode=c.get('mode','hop')
    if mode not in ('expression','hop','walk','crawl'):raise ValueError('Unknown mode')
    if not (c.get('body') or c.get('head')):raise ValueError('A body or head layer is required')
    minimum={'walk':2,'crawl':3}.get(mode,0)
    if len(c.get('feet',[]))<minimum:raise ValueError(f'{mode} requires at least {minimum} explicit foot layers')
    def load(name):
        im=Image.open(root/name).convert('RGBA')
        if im.size!=(n,n):raise ValueError(f'{name}: expected {n}x{n}')
        return im
    blank=lambda:Image.new('RGBA',(n,n))
    body=load(c['body']) if c.get('body') else blank()
    head=load(c['head']) if c.get('head') else blank()
    eyes=[(load(e['path']),e['center']) for e in c.get('eyes',[])]
    feet=[(load(f['path']),f['pivot'],f.get('phase',0)) for f in c.get('feet',[])]
    overlay=load(c['overlay']) if c.get('overlay') else blank()
    ground=c.get('ground',n*.77); pivot=c.get('head_pivot',[n/2,n*.6]); frames=[]
    for i in range(count):
        t=i*dt/1000; u=i/count; q=(u*cycles)%1; phase=2*math.pi*q
        face=head.copy(); openness=blink(t,c.get('blink_times',[.55,2.48,4.42,4.73,6.53]))
        for eye,center in eyes:face.alpha_composite(warp(eye,sy=openness,center=center))
        nod=3.0*math.sin(2*math.pi*2*u)
        if c.get('head'):face=face.rotate(nod,R,center=tuple(pivot))
        actor=blank()
        for foot,hip,offset in feet:
            angle=(10 if mode=='crawl' else 15)*math.sin(phase+offset) if mode in ('walk','crawl') else 0
            actor.alpha_composite(foot.rotate(angle,R,center=tuple(hip)))
        actor.alpha_composite(body);actor.alpha_composite(face)
        jump=0; sx=sy=1
        if mode=='hop':
            pre=math.sin(math.pi*q/.18)**2 if q<.18 else 0
            air=math.sin(math.pi*(q-.18)/.70) if .18<=q<.88 else 0
            land=math.sin(math.pi*(q-.88)/.12)**2 if q>=.88 else 0
            compress=.14*pre+.18*land; stretch=.07*math.sin(math.pi*(q-.18)/.70)**2 if air>0 else 0
            sy=1-compress+stretch; sx=1+.65*compress-.4*stretch; jump=n*.06*air
        elif mode in ('walk','crawl'):jump=n*.006*(1-math.cos(2*phase))
        actor=warp(actor,sx,sy,(n/2,ground),-jump)
        bg=Image.new('RGBA',(n,n),c.get('background','#f7f3eb')); ground_layer=blank(); d=ImageDraw.Draw(ground_layer)
        radius=n*.12*(1-.3*jump/(n*.06)); d.ellipse((n/2-radius,ground-4,n/2+radius,ground+8),fill=(60,60,60,int(35*(1-.55*jump/(n*.06)))))
        if mode!='expression':
            spacing=n/5; offset=(u*spacing*8)%spacing
            for k in range(-1,7):
                x=k*spacing-offset;d.line((x,ground+n*.08,x+8,ground+n*.08),fill=(100,100,100,35),width=1)
        bg.alpha_composite(ground_layer); bg.alpha_composite(actor)
        if c.get('camera',True):
            zoom=.96+.12*(smooth(u/.75) if u<.75 else 1-smooth((u-.75)/.25))
            bg=warp(bg,zoom,zoom,(n/2,n/2))
            canvas=Image.new('RGBA',(n,n),c.get('background','#f7f3eb'));canvas.alpha_composite(bg);bg=canvas
        bg.alpha_composite(overlay);frames.append(bg.convert('RGB'))
    # A sampled common palette prevents per-frame color flicker.
    samples=[frames[j].resize((64,64)) for j in range(0,count,max(1,count//20))]
    strip=Image.new('RGB',(64*len(samples),64))
    for j,s in enumerate(samples):strip.paste(s,(j*64,0))
    palette=strip.quantize(colors=192)
    encoded=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    out=io.BytesIO();encoded[0].save(out,format='GIF',save_all=True,append_images=encoded[1:],duration=dt,loop=0,disposal=2,optimize=False)
    path=Path(target);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.pending');tmp.write_bytes(out.getvalue());os.replace(tmp,path)
    print(path)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('config');p.add_argument('output');a=p.parse_args();render(a.config,a.output)

