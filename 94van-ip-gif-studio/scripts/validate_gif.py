"""Decode every frame and report actual timing, dimensions and content diversity."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

def validate(path, expected_frames=None, expected_dt=None, expected_size=None):
    im=Image.open(path)
    if im.format!='GIF':raise ValueError('Not a GIF')
    if expected_size is not None and im.size!=(expected_size,expected_size):raise ValueError('Unexpected image dimensions')
    loop=im.info.get('loop')
    durations=[];hashes=set();first=last=None
    for i in range(im.n_frames):
        im.seek(i);frame=im.convert('RGB');frame.load()
        if first is None:first=frame.copy()
        last=frame;durations.append(im.info.get('duration',0));hashes.add(hashlib.sha256(frame.tobytes()).hexdigest())
    if len(durations)<2 or len(hashes)<2:raise ValueError('Static or duplicated-only output')
    if min(durations)<=0:raise ValueError('Missing or zero duration')
    if expected_frames is not None and len(durations)!=expected_frames:raise ValueError(f'Frame count {len(durations)} != {expected_frames}')
    if expected_dt is not None and any(d!=expected_dt for d in durations):raise ValueError('Unexpected frame timing')
    if loop!=0:raise ValueError('Expected infinite loop')
    return dict(file=Path(path).name,size=list(im.size),frames=len(durations),unique_frames=len(hashes),duration_ms_values=sorted(set(durations)),total_ms=sum(durations),average_fps=1000*len(durations)/sum(durations),loop=0,seam_mean_absolute_rgb_difference=sum(ImageStat.Stat(ImageChops.difference(first,last)).mean)/3,bytes=Path(path).stat().st_size,sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest())

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('paths',nargs='+');p.add_argument('--frames',type=int);p.add_argument('--duration-ms',type=int);p.add_argument('--size',type=int);a=p.parse_args()
    print(json.dumps([validate(x,a.frames,a.duration_ms,a.size) for x in a.paths],ensure_ascii=False,indent=2))

