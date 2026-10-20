"""
clawd-moji · 01 movie-night
Generates the 10 animated Clawd stickers in ../gif/.

  pip install pillow
  python clawd_movies.py            # all 10
  python clawd_movies.py matrix     # just one

The "Free" text in shawshank uses the Zpix pixel font
(https://github.com/SolidZORO/zpix-pixel-font). Download zpix.ttf and put it next
to this script, or set ZPIX_FONT=/path/to/zpix.ttf.

Clawd rules kept in every frame: 15x16 body grid, colour #D77757 (official clawd_body),
1x2 black square eyes, no mouth.
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont
S=12; W,H=23,24; OX,OY=4,7
BODY='#D77757'; BODYD='#B85E44'; K='#1a1a1a'; BL='#F59A9A'; WH='#FFFFFF'
def base(dy=0, arms=True, eyes=True, legs=True):
    p={}
    for x in range(2,13):
        for y in range(6,13): p[(x,y+dy)]=BODY
    if arms:
        for x,y in [(0,9),(1,9),(0,10),(1,10),(13,9),(14,9),(13,10),(14,10)]: p[(x,y+dy)]=BODY
    if legs:
        for x in (3,5,9,11):
            for y in (13,14): p[(x,y)]=BODY
    if eyes:
        for x in (4,10):
            for y in (8,9): p[(x,y+dy)]=K
    return p
def put(p,pts,c,dy=0):
    for x,y in pts: p[(x,y+dy)]=c
def clear(p,pts,dy=0):
    for x,y in pts: p.pop((x,y+dy),None)
def rect(x0,y0,x1,y1): return [(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)]
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','gif')
FONT_PATH=os.environ.get('ZPIX_FONT',os.path.join(HERE,'zpix.ttf'))
def shift(p,dx,dy): return {(x+dx,y+dy):c for (x,y),c in p.items()}
def merge(back,front): q=dict(back); q.update(front); return q

TAU=2*math.pi; M=6
def clamp(x,a=0,b=1): return max(a,min(b,x))
def ease(t): t=clamp(t); return 0.5-0.5*math.cos(math.pi*t)
def kf(i,keys):
    if i<=keys[0][0]: return keys[0][1]
    for (a,va),(b,vb) in zip(keys,keys[1:]):
        if a<=i<=b: return va+(vb-va)*ease((i-a)/(b-a))
    return keys[-1][1]
def eyes(p,dx=0,ey=0,blink=False):
    for x in (4,10):
        for y in (8,9):
            if p.get((x,y))==K: p[(x,y)]=BODY
    for x in (4,10):
        for y in ((9,) if blink else (8,9)): p[(x+dx,y+ey)]=K
    return p
def canvas(pad=0):
    return Image.new('RGBA',((W+2*pad)*S,(H+2*pad)*S),(0,0,0,0))
def draw(img,p,pad=0):
    d=ImageDraw.Draw(img)
    for (x,y),c in p.items():
        X,Y=x+OX+pad,y+OY+pad
        if 0<=X<W+2*pad and 0<=Y<H+2*pad: d.rectangle([X*S,Y*S,(X+1)*S-1,(Y+1)*S-1],fill=c)
    return img
def xform(p,dx=0,dy=0,sx=1,sy=1,rot=0,piv=(7.5,15)):
    img=draw(canvas(M),p,M)
    Px,Py=(piv[0]+OX+M)*S,(piv[1]+OY+M)*S; Tx,Ty=dx*S,dy*S
    a=math.radians(rot); c,s=math.cos(a),math.sin(a)
    co=(c/sx,-s/sx,Px-(c*(Px+Tx)-s*(Py+Ty))/sx, s/sy,c/sy,Py-(s*(Px+Tx)+c*(Py+Ty))/sy)
    out=img.transform(img.size,Image.AFFINE,co,resample=Image.NEAREST)
    return out.crop((M*S,M*S,(M+W)*S,(M+H)*S))
def squash(v): return dict(sy=v,sx=1/math.sqrt(v))
def shadow(h=0,y=15,col='#D9D2CB'):
    w=9-4*clamp(h/3.5); x0=round(7.5-w/2); x1=round(7.5+w/2)-1
    return {(x,y):col for x in range(x0,x1+1)}
def comp(*layers):
    out=canvas()
    for L in layers:
        if L is None: continue
        if isinstance(L,dict): L=draw(canvas(),L)
        out.alpha_composite(L)
    return out
BANG='#E5484D'
def bang(x,y): return {(x,y):BANG,(x,y+1):BANG,(x,y+2):BANG,(x,y+4):BANG}

# ---------- 降临 ----------
def arrival():
    INK='#34343C'; cx,cy,r=7,3.6,8.2; blobs=[30,140,250,320]; pts=[]
    for x in range(-4,19):
        for y in range(-7,17):
            d=math.hypot(x-cx,y-cy); a=(math.degrees(math.atan2(y-cy,x-cx))+90)%360
            th=0.6+(0.9 if any(min(abs(a-b),360-abs(a-b))<14 for b in blobs) else 0)
            if abs(d-r)<th and not (300<a<335): pts.append(((x,y),a))
    fr=[]
    for i in range(60):
        draw_lim=360*ease(i/30); erase=360*ease((i-50)/10) if i>=50 else -1
        ring={k:INK for k,a in pts if a<=draw_lim and a>erase}
        if 30<=i<50 and (i//2)%2==0: ring.update({k:'#55556A' for k,a in pts if int(a+i*9)%60<8 and a>erase})
        ang=math.radians(draw_lim)
        p=base()
        if i<30: eyes(p,round(math.sin(ang)),-1 if math.cos(ang)>0.2 else 0); rot=-5*math.sin(ang); dy=0; sq=1
        else:
            eyes(p,0,-1 if i<42 else 0,blink=(i in (47,48)))
            rot=0; sq=kf(i,[(30,1),(33,0.78),(36,1.12),(38,1.05),(40,0.84),(43,1)]); dy=-kf(i,[(33,0),(37,2.6),(40,0)])
        if i>=44: sq=1+0.025*math.sin(TAU*(i-44)/16)
        ch=xform(p,0,dy,rot=rot,**squash(sq))
        pop={}
        if 36<=i<=41:
            for x,y in [(1,3),(0,2),(13,3),(14,2),(7,1),(7,0)]: pop[(x,y+round(dy))]=INK
        fr.append((comp(ring,shadow(-dy),ch,pop),60))
    fr[29]=(fr[29][0],300); fr[49]=(fr[49][0],500)
    return fr
# ---------- 星际穿越 ----------
def interstellar():
    fr=[]; cx,cy=14,-3
    for i in range(48):
        t=i/48; bh={}
        for x in range(8,19):
            for y in range(-7,2):
                d=math.hypot(x-cx,y-cy)
                if d<2.3: bh[(x,y)]='#000000'
                elif d<3.4: bh[(x,y)]='#FFF1C9' if (x*3+y+i//2)%5==0 else '#FFC66B'
        for x in range(8,19):
            if abs(x-cx)>2.3: bh[(x,cy)]='#FFE9B5' if (x+i//2)%3==0 else '#FFB13B'
        stars={}
        for k,(sx,sy) in enumerate([(-3,-5),(2,-6),(-2,1),(17,6),(-3,13),(16,14),(5,-4),(-4,7)]):
            ph=(i/48*2+k*0.37)%1
            if ph<0.75: stars[(sx,sy)]='#C9D3F2' if ph<0.5 else '#7F8BB3'
        s=base(); W1='#EEF1F6'; G1='#B8C0CC'
        glance=24<=i<31
        eyes(s,0 if glance else 1,0 if glance else -1,blink=(i in (32,33)))
        put(s,[(x,5) for x in range(2,13)]+[(1,y) for y in range(6,13)]+[(13,y) for y in range(6,13)]+rect(2,12,12,12),W1)
        put(s,[(1,5),(13,5),(1,12),(13,12),(4,12),(10,12),(7,4),(7,3)],G1); put(s,[(7,2)],'#FF5C5C' if (i//6)%2 else '#FFB0B0')
        ch=xform(s,0.6*math.cos(TAU*t),-1+1.3*math.sin(TAU*t),rot=11*math.sin(TAU*t+0.6),piv=(7.5,9))
        fr.append((comp(stars,bh,ch),70))
    return fr
# ---------- 肖申克 ----------
def _shawshank_base(lift=-2, pipe=None):
    fr=[]; R='#8FB8E0'; R2='#C7DDF2'
    drops=[(-3,-5),(2,-6),(8,-4),(13,-6),(17,-3),(-2,1),(5,0),(11,1),(16,4),(-3,8),(17,11),(4,3),(10,-1),(0,-2),(15,-1),(-1,12),(18,9),(7,6),(14,9)]
    UP=rect(0,7,1,8)  # official 'arms-up': same 2x2 stub, moved up
    MID=rect(0,8,1,9)
    for i in range(48):
        rain={}
        for k,(x,y) in enumerate(drops):
            yy=(y+2*i+k*5)%24-7
            for j in range(2): rain[(x-j,yy+j)]=R if j==0 else R2
        if i<9 or i>=44: p=eyes(base(),0,0 if i<6 or i>=46 else -1); arms='down'
        else:
            p=eyes(base(arms=False),0,-1,blink=(i in (30,31)))
            A=MID if (i<11 or i>=41) else UP
            if A is UP and 18<=i<40 and (i//3)%2: A=MID
            put(p,A+[(14-x,y) for x,y in A],BODY)
        sq=kf(i,[(8,1),(11,0.8),(15,1.14),(19,1.04),(40,1.04),(44,1)])
        if 19<=i<40: sq=1.04+0.03*math.sin(TAU*(i-19)/10)
        dy=-kf(i,[(11,0),(15,1.4),(19,0.3),(40,0.3),(44,0)])
        rot=3.5*math.sin(TAU*(i-19)/21) if 19<=i<40 else 0
        ch=xform(shift(p,0,lift),0,dy,rot=rot,piv=(7.5,15+lift),**squash(sq))
        bolt=None
        if i in (15,16,18):
            bolt={(q):'#FFF6C2' for q in [(15,-7),(14,-6),(15,-5),(14,-4),(13,-3),(14,-2)]}
        splash={}
        for k,x in enumerate((1,6,13)):
            if (i+k*4)%8<2: splash.update({(x-1,15):R2,(x+1,15):R2,(x,14):R2})
        fr.append((comp(rain,pipe,ch,bolt,splash),60))
    return fr
PIPE_C='#7D838B'; PIPE_H='#AEB4BC'; PIPE_D='#5B6068'
def pipe_layer():
    d={}
    put(d,rect(1,13,13,13),PIPE_H); put(d,rect(1,14,13,14),PIPE_C)
    put(d,rect(2,15,12,16),PIPE_D); put(d,[(1,14),(13,14)],PIPE_D)
    return d
def pipe_hole():
    return {(x,13):'#2A2D31' for x in range(2,13)}
def _shawshank_emerge(n=26):
    fr=[]; R='#8FB8E0'; R2='#C7DDF2'
    drops=[(-3,-5),(2,-6),(8,-4),(13,-6),(17,-3),(-2,1),(5,0),(11,1),(16,4),(-3,8),(17,11),(4,3),(10,-1),(0,-2),(15,-1),(-1,12),(18,9),(7,6),(14,9)]
    rim_y=(13+OY)*S
    for i in range(n):
        rain={}
        for k,(x,y) in enumerate(drops):
            yy=(y+2*(i-n)+k*5)%24-7
            for j in range(2): rain[(x-j,yy+j)]=R if j==0 else R2
        rise=kf(i,[(3,14),(9,9),(12,8),(17,1.5),(20,0)])
        p=eyes(base(),0 if i<14 else (-1 if i<18 else 1),-1 if i<17 else 0,blink=(i in (22,23)))
        sq=kf(i,[(17,1),(19,1.12),(21,0.9),(24,1)])
        wig=2.5*math.sin(TAU*i/6) if 4<=i<17 else 0
        ch=xform(shift(p,0,-2),wig*0.08,rise-0.6*(sq>1.05),rot=wig,piv=(7.5,13),**squash(sq))
        if rise>0.3:   # still partly inside the pipe: hide what's below the rim
            m=Image.new('L',ch.size,255); ImageDraw.Draw(m).rectangle([0,rim_y,ch.size[0],ch.size[1]],fill=0)
            ch.putalpha(Image.composite(ch.split()[3],m,m))
        drip={}
        if 12<=i<22:
            for k,(dx,ph) in enumerate(((2,0),(12,3),(7,6))):
                yy=7+((i-12+ph)%5)
                drip[(dx,yy+round(rise))]=R2
        fr.append((comp(rain,pipe_layer(),pipe_hole() if i<20 else None,ch,drip),60))
    return fr
# ---------- 泰坦尼克 ----------
def titanic():
    fr=[]; SH='#6B2840'; SH2='#8E3A57'; RY=-9
    for i in range(48):
        t=i/48
        # Rose: lifted overhead, arms spread, "I'm flying"
        r=eyes(base(arms=False),1,-1,blink=(i in (30,31)))
        arm=rect(0,7,1,8)  # official arms-up
        put(r,arm+[(14-x,y) for x,y in arm],BODY)
        # shawl hangs behind her: only the edges show at shoulders and sides, nothing across the front
        put(r,[(1,8),(13,8),(2,10),(12,10),(2,11),(12,11),(2,12),(12,12)],SH); put(r,[(2,9),(12,9)],SH2)
        for k in range(1,8):
            y=9+round(1.3*math.sin(TAU*3*t+k*0.9))+(k//3)
            put(r,[(-k,y)],SH if k%2 else SH2)
            if k<6: put(r,[(-k,y+1)],SH)
        r=shift(r,0,RY)
        # Jack: standing on the deck, holding her up
        j=eyes(base(arms=False),0,-1,blink=(i in (12,13)))
        fly=rect(0,7,1,8)
        put(j,fly+[(14-x,y) for x,y in fly],BODY)
        sway=1.5*math.sin(TAU*t)
        rl=xform(r,0,0,rot=sway,piv=(7.5,5.5))
        deck={}; put(deck,rect(-4,15,14,15),'#C99A5B'); put(deck,[(15,15),(16,15),(17,15)],'#C99A5B'); put(deck,rect(-4,16,15,16),'#2B3A55')
        put(deck,[(x,16) for x in range(-4,16) if (x+i)%5==0],'#3E5277')
        wind={}
        sh=round(i*46/48)
        for x,y,l in [(-3,-6,3),(10,-7,2),(-4,7,2),(16,6,3),(4,12,2),(15,-4,2)]:
            xx=(x-sh+4)%23-4
            for jx in range(l): wind[(xx+jx,y)]='#BFD8F0'
        fr.append((comp(wind,deck,j,rl),60))
    return fr
# ---------- 西游记 ----------
def wukong():
    fr=[]; G='#F2C94C'; GD='#C9971C'
    for i in range(48):
        t=i/48; s=math.sin(TAU*t)
        p=eyes(base(),1,0,blink=(i in (20,21)))
        put(p,rect(2,7,12,7),G); put(p,[(2,7),(12,7)],GD); put(p,[(1,6),(13,6)],G); put(p,[(0,5),(14,5)],GD)
        put(p,[(15,y) for y in range(0,14)],'#C8312E'); put(p,[(15,0),(15,1),(15,12),(15,13)],G); put(p,[(13,9),(14,9),(13,10),(14,10)],BODY)
        sq=1-0.07*max(0,-s)
        clawd=xform(p,0,0,**squash(sq))
        cloud={}
        for x in range(-1,17):
            top=14 if (x+i//2)%4 in (0,1) else 15
            for y in range(top,17): cloud[(x,y)]='#FFFFFF'
            cloud[(x,top-1)]='#B9D3EC'
        for x in range(-1,17): cloud[(x,16)]='#CFE3F5'; cloud[(x,17)]='#B9D3EC'
        for y in range(14,17): cloud[(-2,y)]='#B9D3EC'; cloud[(17,y)]='#B9D3EC'
        cl=draw(canvas(),cloud); cl.alpha_composite(clawd)
        # treat composite as a pixel layer again: transform the whole rider+cloud
        img=canvas(M); img.paste(cl,(M*S,M*S))
        rot=-6+2.5*s; dy=1.4*s-0.6
        Px,Py=(7.5+OX+M)*S,(15+OY+M)*S; a=math.radians(rot); c,sn=math.cos(a),math.sin(a)
        co=(c,-sn,Px-(c*Px-sn*(Py+dy*S)), sn,c,Py-(sn*Px+c*(Py+dy*S)))
        rider=img.transform(img.size,Image.AFFINE,co,resample=Image.NEAREST).crop((M*S,M*S,(M+W)*S,(M+H)*S))
        trail={}
        for k in range(3):
            ph=(t*3+k/3)%1; x=round(-1-ph*6); y=round(14+dy-ph*2)
            sz=2 if ph<0.5 else 1
            if ph<0.85:
                for a_ in range(sz):
                    for b_ in range(sz): trail[(x-a_,y+b_)]='#DCEAF7' if ph<0.4 else '#B9D3EC'
        lines={}
        for k,y in enumerate([1,5,10,-3]):
            x0=(-round(i*46/48)+k*7)%23-4
            for x in range(x0,x0+3): lines[(x,y)]='#CFE3F5'
        fr.append((comp(lines,trail,rider),60))
    return fr
# ---------- 第九区 ----------
def district9():
    fr=[]; HL='#5E646E'; HD='#3E434B'; PR='#7C8A5E'; PRD='#56633F'; FU='#1F1F1F'; SW='#8FC7F0'
    for i in range(64):
        ship={}
        for x in range(-4,19):
            ship[(x,-7)]=HD; ship[(x,-6)]=HL
            if -2<=x<=16: ship[(x,-5)]=HD
            if 1<=x<=13: ship[(x,-4)]=HL
        for x in range(2,13,3): ship[(x,-4)]='#FFC66B' if (i//4+x)%2 else '#8C7B5A'
        sh=xform(ship,0,0.5*math.sin(TAU*i/32),piv=(7,-5))
        p=base(); drop={}
        if i<14:
            fy=-3+12*(i/14)**2
            drop={(13,round(fy)):FU,(13,round(fy)+1):FU}
            eyes(p,0 if fy<2 else 1,-1 if fy<5 else 0)
        elif i<30: eyes(p,1,1,blink=(i in (26,27)))
        else: eyes(p,0,0)
        stage=clamp((i-15)/14)*7
        claw_up=(i>=44 and (i//3)%2==0)
        if i>=15:
            arm=[(13,9),(14,9),(13,10),(14,10)]
            put(p,arm[:min(4,int(stage)+1)],PR)
            if stage>=5:
                if claw_up: put(p,[(15,8),(16,7),(15,9),(16,8)],PR); put(p,[(17,5),(17,7),(16,6)],PRD)
                else: put(p,[(15,9),(15,10),(16,10)],PR); put(p,[(16,9)],PRD)
            if stage>=6 and not claw_up: put(p,[(17,8),(17,11)],PRD)
        if i in (14,15,16): put(p,[(15,7),(12,7),(16,9)],'#BFC4CF')
        sq=kf(i,[(13,1),(15,0.92),(18,1),(30,1),(33,0.78),(37,1.16),(40,1.05),(42,0.84),(45,1)])
        dy=-kf(i,[(33,0),(38,3.4),(42,0)])
        rot=kf(i,[(33,0),(37,-9),(42,0)])
        dx=0.45*math.sin(i*2.2) if (44<=i<60 or 22<=i<30) else 0
        ch=xform(p,dx,dy,rot=rot,**squash(sq))
        fx={}
        if 34<=i<60: fx.update(bang(7,0+round(dy)) if i<44 or (i//2)%2 else {})
        if i>=36:
            for k,(x,y) in enumerate([(1,5),(13,4),(0,7)]):
                ph=((i-36)/8+k/3)%1
                fx[(x+round((x-7)/6*ph*3),y+round(dy)-round(ph*2))]=SW
        fr.append((comp(sh,shadow(-dy),drop,ch,fx),60))
    fr[13]=(fr[13][0],120); fr[-1]=(fr[-1][0],500)
    return fr

def save(nm,fr):
    os.makedirs(OUT,exist_ok=True); gf=[]
    for im,_ in fr:
        a=im.split()[3]; pal=im.convert('RGB').convert('P',palette=Image.ADAPTIVE,colors=255)
        pal.paste(255,a.point(lambda v:255 if v<128 else 0)); gf.append(pal)
    gf[0].save(os.path.join(OUT,nm+'.gif'),save_all=True,append_images=gf[1:],duration=[d for _,d in fr],loop=0,transparency=255,disposal=2)
    print(nm, len(fr), 'frames')
FT=ImageFont.truetype(FONT_PATH,12)
def free_layer(i):
    img=canvas(); 
    word='Free'; starts=[15,17,19,21]; px=6
    total=sum(FT.getlength(c) for c in word); x=(W*S-total*px)/2
    for c,st in zip(word,starts):
        w=FT.getlength(c)
        if i>=st and i<44:
            off=kf(i,[(st,-2.0),(st+2,0.6),(st+4,0)])
            m=Image.new('L',(16,16),0); ImageDraw.Draw(m).text((0,0),c,font=FT,fill=255)
            m=m.point(lambda v:255 if v>100 else 0)
            for dx,dy,col in [(-1,0,'#34343C'),(1,0,'#34343C'),(0,-1,'#34343C'),(0,1,'#34343C'),(0,0,'#FFF6C2')]:
                big=m.resize((16*px,16*px),Image.NEAREST)
                layer=Image.new('RGBA',big.size,col); 
                img.paste(layer,(round(x+dx*px),round(S*1.2+(dy+off*2)*px)),big)
        x+=w*px
    return img
def shawshank():
    em=_shawshank_emerge()
    fr=_shawshank_base(pipe=pipe_layer())
    return em+[(comp(im,free_layer(i)),d) for i,(im,d) in enumerate(fr)]

def matrix():
    fr=[]; CO='#1C1C22'; CO2='#34343F'
    cols=[(-3,0),(0,9),(3,4),(6,15),(9,7),(12,19),(15,2),(18,11),(-1,17),(16,22)]
    for i in range(60):
        rain={}
        for k,(x,y0) in enumerate(cols):
            head=(y0+round(i*0.8))%30-7
            for j in range(6):
                y=head-j
                if (y+k)%2==0 or j==0: rain[(x,y)]='#7CFF9B' if j==0 else ('#22A35A' if j<3 else '#145C30')
        p=eyes(base(),-1 if 10<=i<46 else 0,-1 if 10<=i<46 else 0,blink=(i in (54,55)))
        put(p,rect(2,11,12,12),CO); put(p,[(1,y) for y in range(10,15)]+[(13,y) for y in range(10,15)]+[(2,13),(12,13),(2,14),(12,14),(0,9),(0,10),(14,9),(14,10)],CO)
        put(p,[(7,11),(7,12),(2,11),(12,11)],CO2)
        fl=1 if (i//3)%2 else 0
        put(p,[(0,14+fl),(14,14+fl),(1,15),(13,15)],CO)
        lean=kf(i,[(8,0),(16,58),(44,58),(52,0)])
        if 16<=i<44: lean+=2.5*math.sin(TAU*(i-16)/14)
        sq=kf(i,[(44,1),(48,1.1),(52,0.88),(55,1)])
        ch=xform(p,-kf(i,[(8,0),(16,1),(44,1),(52,0)]),0,rot=lean,**squash(sq))
        bul={}
        for k,(by,st) in enumerate([(7,10),(9,16),(5,22)]):
            if i>=st:
                bx=19-(i-st)*0.55
                if bx>-6:
                    x=round(bx); bul[(x,by)]='#C3C9D3'; bul[(x+1,by)]='#8A919C'
                    for r in range(1,4):
                        rx=x+1+r*3
                        if rx<=19:
                            col='#9FB4D9' if r==1 else '#C9D3F2'
                            for dy in range(-r+1 if r>1 else 0,r if r>1 else 1): pass
                            bul[(rx,by-1)]=col; bul[(rx,by+1)]=col
                            if r>1: bul[(rx+1,by-2)]=col; bul[(rx+1,by+2)]=col
        fr.append((comp(rain,shadow(0),ch,bul),60))
    fr[30]=(fr[30][0],200)
    return fr

def coco():
    fr=[]; FL=['#FF5DA2','#9B5DE5','#00BBF9','#FF9F1C','#F15BB5','#00F5D4']
    for i in range(48):
        t=i/48; beat=(i%12)/12
        # papel picado swaying
        pp={}
        for x in range(-4,19):
            sag=round(1.2*math.sin(math.pi*(x+4)/22)+0.6*math.sin(TAU*t+x*0.3))
            pp[(x,-7+sag)]='#5A3E36'
            if (x+4)%4!=3:
                c=FL[((x+4)//4)%6]
                pp[(x,-6+sag)]=c
                if (x+4)%4==1: pp[(x,-5+sag)]=c
        p=eyes(base(arms=False),0,0,blink=(i in (29,30)))
        GW='#F4EFE6'; GO='#C9B79C'; NK='#7A4A2A'
        G=[]
        def gp(pts,c): put(p,[(x,y+2) for x,y in pts],c)
        gp([(x,10) for x in range(-1,7)],NK); gp([(-2,9),(-1,9),(-2,10)],NK)
        gp(rect(7,10,11,12)+[(8,9),(9,9),(10,9),(8,13),(9,13),(10,13),(6,11),(12,11)],GW)
        gp([(7,9),(11,9),(6,10),(12,10),(6,12),(12,12),(7,13),(11,13)],GO); gp([(9,11)],'#3A2A22')
        put(p,[(0,10),(1,10),(0,11),(1,11)],BODY)
        down=beat<0.5
        put(p,[(13,11),(14,11),(13,12),(12,12)] if down else [(13,10),(14,10),(13,11),(14,9)],BODY)
        bounce=kf(beat*12,[(0,0.88),(2,1.06),(5,1),(12,1)]) if True else 1
        ch=xform(p,0,-0.4*math.sin(TAU*2*t)**2,rot=5*math.sin(TAU*t),**squash(bounce))
        pet={}
        for k,(x0,ph0) in enumerate([(-3,0),(1,0.3),(5,0.6),(10,0.15),(14,0.45),(17,0.75),(8,0.9),(-1,0.55)]):
            ph=(t*2+ph0)%1; y=round(16-ph*22); x=round(x0+1.2*math.sin(TAU*(ph*2+k*0.2)))
            pet[(x,y)]='#FF9F1C' if k%2 else '#FFB627'
            if ph<0.6: pet[(x+1,y)]='#FFD166'
        notes={}
        for k in range(2):
            ph=((i+k*24)%48)/24
            if ph<1:
                nx=15+k*2-round(ph*1.5); ny=round(6-ph*6)
                put(notes,[(nx,ny),(nx,ny-1),(nx,ny-2),(nx+1,ny-2),(nx-1,ny)],'#FFD166' if ph<0.7 else '#FFE8A8')
        fr.append((comp(pp,pet,shadow(0),ch,notes),60))
    return fr


# ---------- X战警 · 金刚狼 ----------
def wolverine():
    fr=[]; HR='#26262B'; HR2='#3D3D45'; CL='#FFFFFF'; CL2='#A3AEBC'
    hair=[(x,5) for x in range(2,13)]+[(2,4),(3,4),(1,4),(1,3),(0,2),(0,3),(12,4),(11,4),(13,4),(13,3),(14,2),(14,3),(6,4),(7,4),(8,4),(7,3)]
    burns=[(2,6),(2,7),(2,8),(12,6),(12,7),(12,8)]
    pops=[14,22,30]          # 欻 欻 欻
    for i in range(56):
        p=eyes(base(),-1 if i<8 else 0, 0, blink=(i in (46,47)))
        put(p,hair,HR); put(p,[(1,3),(13,3),(7,3)],HR2); put(p,burns,HR)
        n=sum(1 for st in pops if i>=st) if i<44 else 0
        ret=i>=44
        claws={}
        if n or ret:
            for k,(y0,sl) in enumerate(((9,-1),(9,0),(10,1))):   # three blades fanning out of the fist
                if ret: L=max(0,round(4*(1-ease((i-44)/5))))
                elif k<n: L=round(kf(i-pops[k],[(0,1),(2,4)]))
                else: L=0
                for d in range(L):
                    y=y0+(sl if d>=1 else 0)+(sl if d>=3 else 0)
                    c=CL if d==L-1 else CL2
                    claws[(-1-d,y)]=c; claws[(15+d,y)]=c
        p.update(claws)
        # glint running along the claws while they're all out
        if 32<=i<42:
            g=(i-32)//2
            for x in (-1-g,15+g):
                if (x,9) in p and p[(x,9)]==CL2: p[(x,9)]='#E6ECF3'
        jolt=0; sq=1
        for st in pops:
            if st-3<=i<st: sq=min(sq,kf(i,[(st-3,1),(st-1,0.86)]))
            if st<=i<st+4: sq=kf(i,[(st,1.12),(st+2,0.97),(st+4,1)]); jolt=(1 if (i-st)%2==0 else -1)*0.4
        ch=xform(p,jolt,-0.3*(sq>1.05),**squash(sq))
        spark={}
        for st in pops:
            if st<=i<st+3:
                r=i-st+1
                if r<3:
                    for sx in (-3,17):
                        spark.update({(sx,5-r):'#FFD166',(sx,5+r):'#FFD166',(sx-r,5):'#FFD166',(sx+r,5):'#FFD166'})
        fr.append((comp(shadow(0),ch,spark),60))
    return fr

# ---------- 电锯惊魂 ----------
def saw():
    import random
    rnd=random.Random(7); fr=[]
    FR='#4A4A52'; FR2='#2E2E34'; SC='#1B211C'; SL='#232B24'
    X0,Y0,X1,Y1=-2,-3,16,12
    for i in range(60):
        tv={}
        put(tv,[(x,y) for x in range(X0-1,X1+2) for y in (Y0-1,Y1+1)]+[(x,y) for y in range(Y0-1,Y1+2) for x in (X0-1,X1+1)],FR)
        put(tv,[(x,Y1+1) for x in range(X0-1,X1+2)],FR2)
        # ceiling mount instead of TV antennas/feet
        put(tv,[(x,y) for x in (7,8) for y in (Y0-2,Y0-3)],FR2)
        put(tv,[(x,Y0-4) for x in range(5,11)],FR)
        on=8<=i<54
        if on:  # CCTV viewfinder corners + blinking REC dot
            G='#8FA58F'
            for cx,cy,sx,sy in ((X0,Y0,1,1),(X1,Y0,-1,1),(X0,Y1,1,-1),(X1,Y1,-1,-1)):
                put(tv,[(cx,cy),(cx+sx,cy),(cx,cy+sy)],G)
            if (i//6)%2==0: put(tv,[(X0+1,Y1-1)],'#E0323A')
        scr={}
        for y in range(Y0,Y1+1):
            for x in range(X0,X1+1):
                if i<8 or 50<=i<54 and rnd.random()<0.35:
                    v=rnd.choice(['#2A2A2A','#6A6A6A','#A8A8A8','#DADADA'])
                    scr[(x,y)]=v
                else: scr[(x,y)]=SL if y%2 else SC
        if i in (8,9): scr={k:('#DADADA' if (k[1]+i)%3==0 else v) for k,v in scr.items()}
        # Clawd inside, lit from below, slowly leaning in
        ch=None
        if on:
            p=eyes(base(dy=-2,legs=False),0 if i<24 else (1 if i<40 else 0),-2,blink=(i in (37,38)))
            for y in (11,12): 
                for x in (3,5,9,11): p[(x,y)]=BODY
            dark={}
            for (x,y),c in p.items():
                if c==BODY: dark[(x,y)]=BODYD if y<=5 else BODY
                else: dark[(x,y)]=c
            z=kf(i,[(10,1),(44,1.14)])
            rot=kf(i,[(20,0),(28,-7),(40,-7),(46,0)])
            dx=0
            if 50<=i<54: dx=rnd.choice([-1.5,1.5,0.8])
            ch=xform(dark,dx,0,sx=z,sy=z,rot=rot,piv=(7.5,8))
            # keep him inside the glass
            m=Image.new('L',ch.size,0)
            ImageDraw.Draw(m).rectangle([(X0+OX)*S,(Y0+OY)*S,(X1+1+OX)*S-1,(Y1+1+OY)*S-1],fill=255)
            a=ch.split()[3]; ch.putalpha(Image.composite(a,m,m))
            # scanlines over him
            sl=Image.new('RGBA',ch.size,(0,0,0,0)); d=ImageDraw.Draw(sl)
            for y in range(Y0,Y1+1,2): d.rectangle([(X0+OX)*S,(y+OY)*S,(X1+1+OX)*S-1,(y+OY)*S+2],fill=(0,0,0,32))
            ch.alpha_composite(sl)
        # CRT switch-off: collapse to a line, then a dot
        if i>=54:
            scr={}
            k=i-54
            if k<3:
                for x in range(X0+k*3,X1+1-k*3): scr[(x,4)]='#F2F2F2'
            elif k<5: scr={(7,4):'#FFFFFF',(8,4):'#F2F2F2'}
            for y in range(Y0,Y1+1):
                for x in range(X0,X1+1): scr.setdefault((x,y),'#0E110E')
        txt=None
        if 14<=i<50:
            txt=Image.new('RGBA',canvas().size,(0,0,0,0)); word='PLAY GAME'; px=3
            shown=word[:max(0,min(len(word),(i-14)//2+1))]
            total=FT.getlength(word); x0=(X0+OX)*S+((X1-X0+1)*S-total*px)/2; y0=(Y0+OY)*S+6
            if not (44<=i<50 and i%2):
                m=Image.new('L',(int(total)+2,16),0); ImageDraw.Draw(m).text((0,0),shown,font=FT,fill=255)
                m=m.point(lambda v:255 if v>100 else 0).resize(((int(total)+2)*px,16*px),Image.NEAREST)
                txt.paste(Image.new('RGBA',m.size,'#E0323A'),(round(x0),round(y0)),m)
        if on:
            if txt is None: txt=Image.new('RGBA',canvas().size,(0,0,0,0))
            m=Image.new('L',(24,16),0); ImageDraw.Draw(m).text((0,0),'REC',font=FT,fill=255)
            m=m.point(lambda v:255 if v>100 else 0).resize((48,32),Image.NEAREST)
            txt.paste(Image.new('RGBA',m.size,'#C8D4C8'),((X0+2+OX)*S+4,(Y1-1+OY)*S-6),m)
        fr.append((comp(scr,ch,txt,tv),60))
    fr[40]=(fr[40][0],400)
    return fr

ALL=['arrival','interstellar','shawshank','titanic','wukong','district9','matrix','coco','wolverine','saw']
if __name__=='__main__':
    for nm in (sys.argv[1:] or ALL):
        save(nm,globals()[nm]())
