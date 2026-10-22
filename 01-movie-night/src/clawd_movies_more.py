"""clawd-moji 01 movie-night, part 2: 8 more stickers (阿克正传 蜘蛛克 哈利波克 星克大战 行克走克 克门的世界 侏罗克公园 痴克)."""
import os, sys, math
os.environ.setdefault('ZPIX_FONT','/workspace/work/fonts/zpix.ttf')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import clawd_movies as cm
from clawd_movies import *
from PIL import Image, ImageDraw
UP=rect(0,7,1,8); MID=rect(0,8,1,9); DOWN=rect(0,9,1,10)
def mirror(pts): return [(14-x,y) for x,y in pts]
def arms(p,left=DOWN,right=DOWN):
    clear(p,rect(0,7,1,10)+rect(13,7,14,10))
    put(p,left,BODY); put(p,mirror(right),BODY); return p
def face(p,mode='n',dx=0,ey=0,blink=False):
    if mode=='n': return eyes(p,dx,ey,blink)
    for x in range(2,13):
        for y in range(6,12):
            if p.get((x,y))==K: p[(x,y)]=BODY
    if mode=='hap':
        for ex in (4,10): put(p,[(ex-1+dx,9+ey),(ex+dx,8+ey),(ex+1+dx,9+ey)],K)
    else:
        put(p,[(3,7),(4,8),(3,9),(11,7),(10,8),(11,9)],K)
    return p
def render(p,cs,ax,ay,rot=0,sx=1,sy=1,flip=False):
    img=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); d=ImageDraw.Draw(img)
    for (x,y),c in p.items():
        xx=(14-x) if flip else x
        X=math.floor(ax+(xx-7.5)*cs+0.5); Y=math.floor(ay+(y-15)*cs+0.5)
        d.rectangle([X,Y,X+cs-1,Y+cs-1],fill=c)
    if rot or sx!=1 or sy!=1:
        a=math.radians(rot); c,s_=math.cos(a),math.sin(a); Px,Py=ax,ay
        co=(c/sx,-s_/sx,Px-(c*Px-s_*Py)/sx, s_/sy,c/sy,Py-(s_*Px+c*Py)/sy)
        img=img.transform(img.size,Image.AFFINE,co,resample=Image.NEAREST)
    return img
def text_layer(s,px,cx,y,col,ol='#FFFFFF'):
    img=canvas(); w=int(FT.getlength(s))+2
    m=Image.new('L',(w,16),0); ImageDraw.Draw(m).text((0,0),s,font=FT,fill=255)
    m=m.point(lambda v:255 if v>100 else 0); bb=m.getbbox() or (0,0,w,16); m=m.resize((w*px,16*px),Image.NEAREST)
    x0=round(cx-(bb[0]+bb[2])*px/2)
    if ol:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
            img.paste(Image.new('RGBA',m.size,ol),(x0+dx*px,y+dy*px),m)
    img.paste(Image.new('RGBA',m.size,col),(x0,y),m)
    return img
def line_pts(x0,y0,ang,L):
    a=math.radians(ang); return [(round(x0+math.cos(a)*k),round(y0-math.sin(a)*k)) for k in range(1,L+1)]

# ---------- 阿甘正传 ----------
def forrest():
    fr=[]; CAP='#C8312E'; CAPD='#9E2321'; ROAD='#B9B1A8'; GH='#EBB7A3'
    for i in range(48):
        ph=i%8
        p=eyes(base(legs=False),1,0,blink=(i in (30,31)))
        put(p,rect(2,5,12,5)+rect(3,4,11,4),CAP); put(p,[(13,5),(14,5),(15,5)],CAPD); put(p,[(7,3)],CAPD)
        A=ph<4
        put(p,DOWN if A else MID,BODY); put(p,mirror(MID if A else DOWN),BODY)
        legs={}
        L1=[(2,13),(3,14),(8,13),(9,14)]; L2=[(5,13),(5,14),(11,13),(12,14)]
        legs.update({q:BODY for q in (L1 if A else L2)})
        ghost={}
        for q in (L2 if A else L1): ghost[(q[0]-1,q[1])]=GH
        for x in range(-4,2):
            if (x+ph)%3==0: ghost[(x,13+(x%2))]='#E5DDD5'
        bob=-0.6 if ph in (1,2,5,6) else 0
        body=xform(merge(merge({},ghost),merge(p,legs)),0,bob)
        bib=Image.new('RGBA',canvas().size,(0,0,0,0)); d=ImageDraw.Draw(bib)
        bx,by=(8+OX)*S,(10+OY)*S+round(bob*S)+6
        d.rectangle([bx,by,bx+4*S-1,by+2*S+5],fill='#FFFFFF')
        d.rectangle([bx+2,by+2,bx+5,by+5],fill='#B8B8B8'); d.rectangle([bx+4*S-6,by+2,bx+4*S-3,by+5],fill='#B8B8B8')
        bib.alpha_composite(text_layer('15',2,bx+2*S,by+4,'#C8312E',None))
        road={}
        for x in range(-4,19):
            road[(x,15)]=ROAD
            if (x+i)%6<2: road[(x,16)]='#8F877E'
        fx=round(18-i*0.5); fy=round(-5+1.5*math.sin(TAU*i/24))
        feather={(fx,fy):'#FFFFFF',(fx+1,fy):'#FFFFFF',(fx+2,fy-1):'#FFFFFF',(fx+3,fy-1):'#F2F2F2',(fx+1,fy+1):'#E6E6E6',(fx+2,fy):'#E6E6E6',(fx-1,fy+1):'#B9B9B9',(fx+4,fy-2):'#B9B9B9'}
        fr.append((comp(road,feather,body,bib),60))
    return fr

# ---------- 蜘蛛侠 ----------
def spider():
    fr=[]; RD='#D23A3A'; RW='#8E1F24'; BU='#2D5BB0'; WEB='#E6E6E6'
    for i in range(52):
        wave=24<=i<44
        p=face(base(),'hap' if 26<=i<44 else 'n',0,0 if i<20 else 1 if i<24 else 0,blink=(i in (46,47)))
        for (x,y),c in list(p.items()):
            if c==BODY: p[(x,y)]=RD if y<=9 else BU
        put(p,[(7,6),(7,7),(5,6),(9,6),(3,7),(11,7),(2,8),(12,8)],RW)
        if wave:
            clear(p,rect(13,7,14,10))
            put(p,mirror(UP if (i//3)%2 else DOWN),RD)
        q={(x,20-y):c for (x,y),c in p.items()}
        for y in range(-30,7): q[(7,y)]=WEB
        enter=kf(i,[(0,-22),(10,0)])
        sy=kf(i,[(9,1),(11,1.12),(14,0.92),(17,1)])
        rot=7*math.sin(TAU*(i-14)/28)*kf(i,[(14,0),(18,1),(44,1),(52,0.4)]) if i>=14 else 0
        ch=xform(q,0,enter,sy=sy,sx=1,rot=rot,piv=(7.5,-7))
        fr.append((comp(ch),60))
    return fr

# ---------- 哈利波特 ----------
def harry():
    fr=[]; HR='#2A221E'; GL='#6E6E78'; WD='#7A4A2A'; GO='#F2C94C'; WH2='#FFF6C2'
    stars=[(-2,-4),(3,-6),(16,-5),(-3,3),(17,2),(11,-6)]
    for i in range(56):
        p=eyes(base(),0 if i<14 else (1 if i<40 else 0),-1 if 14<=i<40 else 0,blink=(i in (48,49)))
        put(p,rect(2,5,12,5)+[(3,4),(5,4),(6,4),(9,4),(11,4),(2,6),(12,6),(1,5),(13,5)],HR)
        put(p,[(8,6),(7,7)],'#B03A3A')
        for ex in (4,10): put(p,[(ex,7),(ex-1,8),(ex+1,8),(ex-1,9),(ex+1,9)],GL)
        put(p,[(6,8),(8,8)],GL)
        pose=0 if i<12 else (1 if i<16 else 2 if i<20 else 3)
        clear(p,rect(13,7,14,10))
        R=[DOWN,MID,UP,UP][pose]; put(p,mirror(R),BODY)
        ang=[20,60,100,70][pose]; hy=R[0][1]
        wand=line_pts(14.5,hy,ang,4)
        put(p,wand,WD)
        lit=i>=20
        if lit:
            tip=line_pts(14.5,hy,ang,5)[-1]; p[tip]=WH2 if (i//2)%2 else '#FFFFFF'
        sq=kf(i,[(16,1),(18,0.9),(21,1.08),(24,1)])
        ch=xform(p,0,-0.4*(sq>1.04),**squash(sq))
        fx={}
        for k,(sx,sy) in enumerate(stars):
            t0=22+k*3
            if i>=t0:
                age=i-t0; c=GO if age%6<3 else WH2
                fx[(sx,sy)]='#FFFFFF' if age<2 else c
                if age<2 or age%6==0:
                    for d in ((1,0),(-1,0),(0,1),(0,-1)): fx[(sx+d[0],sy+d[1])]=c
        if i>=26:
            for k in range(5):
                a=TAU*k/5+i*0.1; tx,ty=round(15.5+math.cos(a)*1.5),round(-1+math.sin(a)*1.5)
        sx=round(-2+19*((i*0.6)%28)/28); sy=round(9-3*abs(math.sin(TAU*i/20)))
        if i<44:
            fx[(sx,sy)]=GO; fx[(sx+1,sy)]=GO
            wing='#FFFFFF' if i%2 else '#DDDDDD'
            fx[(sx-1,sy-(i%2))]=wing; fx[(sx+2,sy-(i%2))]=wing
        fr.append((comp(shadow(0),ch,fx),60))
    return fr

# ---------- 星球大战 ----------
def starwars():
    fr=[]; CK='#5A3B26'; CK2='#7A5236'; HL='#9AA0A8'; HD='#4A4E55'; BL1='#7FD4FF'; BC='#EAFBFF'
    for i in range(56):
        p=eyes(base(),1 if i<10 else 0,0,blink=(i in (50,51)))
        put(p,[(1,y) for y in range(6,13)]+[(13,y) for y in range(6,13)],CK)
        put(p,rect(2,5,12,5)+[(1,5),(13,5)],CK); put(p,[(3,4),(4,4),(10,4),(11,4)]+[(x,4) for x in range(5,10)],CK2)
        fl=(i//3)%2
        put(p,[(1,13),(13,13),(0,13+fl),(14,13+fl)],CK)
        clear(p,rect(13,7,14,10)); put(p,mirror(MID),BODY)
        hx,hy=15,8
        put(p,[(hx,hy),(hx,hy+1)],HL); put(p,[(hx,hy+2)],HD)
        L=0
        if i>=8: L=round(kf(i,[(8,0),(12,8)]))
        if i>=48: L=round(kf(i,[(48,8),(52,0)]))
        ang=90
        if 18<=i<40: ang=90-kf(i,[(18,0),(22,80),(26,10),(30,130),(34,40),(40,0)])+0
        fx={}
        if L:
            pts=line_pts(hx,hy,ang,L)
            if 18<=i<40:
                prev=90-kf(i-1,[(18,0),(22,80),(26,10),(30,130),(34,40),(40,0)])
                for q in line_pts(hx,hy,(ang+prev)/2,L): fx[q]='#D6F3FF'
            for k,q in enumerate(pts): fx[q]='#8FDCFF' if (k+i)%4 else '#C9F1FF'
            fx[pts[-1]]='#FFFFFF'
        sq=kf(i,[(6,1),(8,0.9),(11,1.08),(14,1)])
        ch=xform(p,0,0,**squash(sq))
        st={}
        for k,(x,y) in enumerate([(-3,-5),(2,-6),(8,-4),(-2,2),(17,-6),(12,-6),(-4,9)]):
            if (i//4+k)%3: st[(x,y)]='#C9D3F2'
        fr.append((comp(st,shadow(0),ch,fx),60))
    return fr

# ---------- 行尸走肉 ----------
def walkingdead():
    fr=[]; HT='#B08A5A'; HTD='#7A5C38'; BAND='#4A3828'; GUN='#6E737B'; GUD='#3E4248'; ZB='#7E9474'; ZBD='#5B6E52'; DIRT='#8B6A4A'
    for i in range(60):
        look=-1 if i<12 else (1 if i<20 else (1 if i<44 else 0))
        p=eyes(base(),look,0,blink=(i in (54,55)))
        put(p,rect(-1,5,15,5),HT); put(p,rect(3,3,11,4),HT); put(p,rect(3,4,11,4),BAND); put(p,[(-1,5),(15,5)],HTD); put(p,[(7,3)],HTD)
        put(p,[(3,11)],'#F2C94C')
        aim=26<=i<46
        clear(p,rect(13,7,14,10)); put(p,mirror(MID if aim else DOWN),BODY)
        gy=8 if aim else 9
        put(p,[(15,gy),(16,gy),(17,gy)],GUN); put(p,[(15,gy+1)],GUD); put(p,[(18,gy)],GUD)
        jump=-kf(i,[(22,0),(24,2.4),(27,0)])
        sq=kf(i,[(21,1),(22,0.85),(24,1.15),(27,0.88),(29,1)])
        dx=0.3*math.sin(i*2.5) if 6<=i<20 else 0
        ch=xform(p,dx,jump,**squash(sq))
        fx={}
        if 8<=i<20 and (i//2)%2==0: fx.update({(13,4):'#8FC7F0',(13,5):'#8FC7F0'})
        if 23<=i<34: fx.update(bang(7,-2+round(jump)))
        hand={}
        rise=kf(i,[(16,0),(22,4),(44,4),(50,0)])
        for k in range(round(rise)):
            y=14-k; hand[(17,y)]=ZB; hand[(18,y)]=ZB
        if rise>=3.5:
            hand.update({(16,10):ZB,(17,9):ZB,(18,9):ZB,(16,9):ZBD,(18,10):ZBD})
            if (i//4)%2: hand[(16,8)]=ZB
        dirt={(x,15):DIRT for x in range(-4,19)}
        if 16<=i<22 or 44<=i<50: dirt.update({(16,14):DIRT,(19,14):DIRT})
        fr.append((comp(dirt,hand,shadow(-jump,y=14,col='#6E5238'),ch,fx),60))
    return fr

# ---------- 楚门的世界 ----------
def truman():
    fr=[]; SKY='#9ED0F2'; CL='#FFFFFF'; DR='#1E2230'; FRM='#F4F4F4'; ST='#7FB6DE'
    words=[(0,'早安！'),(16,'午安！'),(32,'晚安！')]
    for i in range(64):
        bg={}
        for x in range(-4,19):
            for y in range(-7,14): bg[(x,y)]=SKY
        for cx,cy,w in [(-2,-4,5),(12,-6,6),(14,4,4),(-3,7,4)]:
            for x in range(cx,cx+w): bg[(x,cy)]=CL; bg[(x,cy+1)]=CL
            for x in range(cx+1,cx+w-1): bg[(x,cy-1)]=CL
        for x in range(1,14):
            for y in range(2,14): bg[(x,y)]=FRM if x in (1,13) or y==2 else DR
        for k,y in enumerate((14,15,16)):
            for x in range(-1-k,16+k): bg[(x,y)]=ST if y%2==0 else '#A9CDEB'
        seg=min(2,i//16)
        local=i-16*seg
        bow=seg==2 and 4<=i-32<26
        p=face(base(),'hap' if bow else 'n',0,0,blink=(i in (12,13)))
        if not bow and local<12:
            clear(p,rect(13,7,14,10)); put(p,mirror(UP if (i//3)%2 else MID),BODY)
        if bow:
            sq=kf(i-32,[(4,1),(8,0.78),(20,0.78),(26,1)]); rot=0; dy=0
        else:
            sq=kf(local,[(0,1),(2,1.1),(4,0.95),(6,1)]); rot=4*math.sin(TAU*i/16); dy=-kf(local,[(0,0),(2,0.8),(5,0)])
        ch=xform(p,0,dy,rot=rot,**squash(sq))
        tl=None
        st,wd=words[seg]
        if not (seg==2 and i>=58):
            tl=text_layer(wd,4,W*S//2,round(S*3.4+kf(i-st,[(0,-8),(3,4),(5,0)])),'#34343C')
        fr.append((comp(bg,ch,tl),70))
    fr[-1]=(fr[-1][0],400)
    return fr

# ---------- 侏罗纪公园 ----------
def jurassic():
    fr=[]; G='#5E8C46'; GD='#3F6631'; BE='#9DBE6E'; TH='#FFFFFF'
    for i in range(48):
        ph=i%12; stride=ph<6
        rx={}
        rows={5:(-1,11),6:(-4,12),7:(-4,13),8:(-4,13),9:(-4,13),10:(-3,13),11:(0,11)}
        for y,(a,b) in rows.items():
            for x in range(a,b+1): rx[(x,y)]=G
        for x in range(2,12): rx[(x,10)]=BE; rx[(x,9)]=BE if 4<=x<=10 else rx[(x,9)]
        for x in range(-4,6): rx[(x,5 if x>0 else 6)]=GD
        jaw=(i//6)%2
        head={0:(13,17),1:(12,18),2:(12,18),3:(12,18)}
        for y,(a,b) in head.items():
            for x in range(a,b+1): rx[(x,y)]=G
        for x in range(10,14):
            for y in range(3,8): rx[(x,y)]=G
        rx[(16,1)]=K; rx[(15,0)]=GD
        if jaw:
            for x in (14,16,18): rx[(x,4)]=TH
            for x in range(12,18): rx[(x,5)]=G
        else:
            for x in range(12,19): rx[(x,4)]=G
            for x in (15,17): rx[(x,4)]=TH
        rx.update({(14,7):G,(15,7):G,(15,8):GD})
        back=[(2,12),(2,13),(1,14),(2,14),(3,14)] if stride else [(4,12),(5,13),(5,14),(6,14),(4,14)]
        front=[(9,12),(10,13),(10,14),(11,14),(9,14)] if not stride else [(7,12),(7,13),(7,14),(8,14),(6,14)]
        for q in back: rx[q]=GD
        for q in front: rx[q]=G
        bob=-0.5 if ph in (2,3,8,9) else 0
        c=face(base(arms=False),'hap',1 if ph<6 else 0,0,blink=(i in (22,23,44,45)))
        cheer=(i//3)%2
        put(c,UP if cheer else MID,BODY); put(c,mirror(UP if cheer else MID),BODY)  # 双手欢呼
        c=shift(c,-4,-9)
        cy=-1.0 if ph in (1,2,7,8) else 0
        dino=xform(rx,0,bob,rot=2.2*math.sin(TAU*i/12),piv=(6,14))
        rider=xform(c,0,bob+cy,rot=-4*math.sin(TAU*i/12),sx=1.12,sy=1.12,piv=(3,5))
        dust={}
        for k in range(3):
            pp=((i/12)+k/3)%1; x=round(-1-pp*4); y=14-round(pp*2)
            if pp<0.8: dust[(x,y)]='#D9CBB5'; dust[(x-1,y)]='#E8DDCC'
        ground={(x,15):'#C7B596' for x in range(-4,19)}
        fr.append((comp(ground,dust,dino,rider),60))
    return fr

# ---------- 痴迷 ----------
def obsession():
    fr=[]; TW='#8A7A45'; LF='#8DB86A'; BX='#5B3A6E'; BXL='#C9A44C'; MO='#7FB069'; MOD='#4E7A3C'; CO='#F2C94C'; COD='#C9971C'
    rain=[(-3,0),(1,7),(5,3),(9,10),(13,1),(16,6),(-1,13),(11,15),(3,18),(15,12),(7,21),(-4,9),(17,17)]
    for i in range(64):
        snapped=i>=20
        p=eyes(base(),0,-1 if i<20 else (-1 if (i//6)%2 else 0),blink=(i in (14,15)))
        clear(p,rect(13,7,14,10))
        R=MID if i<10 else UP
        if snapped: R=UP if (i//3)%2 else MID
        put(p,mirror(R),BODY)
        hy=R[0][1]
        fx={}
        if not snapped:
            bend=0 if i<12 else min(2,(i-12)//3)
            pts=line_pts(14.5,hy,90-bend*12,6)
            for k,q in enumerate(pts): p[q]=TW
            p[(pts[2][0]+1,pts[2][1])]=LF; p[(pts[4][0]-1,pts[4][1])]=LF
        else:
            for q in line_pts(14.5,hy,90,3): p[q]=TW
            if i<30:
                k=i-20; fx[(16+k//2,hy-4-k//3)]=TW; fx[(17+k//2,hy-5-k//3+k//4)]=TW
        if 20<=i<24:
            for d in ((0,-1),(1,0),(-1,0),(0,1),(1,-1),(-1,-1)):
                fx[(15+d[0]*(i-19),hy-3+d[1]*(i-19))]='#FFF6C2'
        sq=kf(i,[(18,1),(20,0.85),(23,1.12),(26,1)])
        hop=-kf(i,[(30,0),(34,1.8),(38,0),(42,1.8),(46,0)]) if 30<=i<50 else 0
        ch=xform(p,0,hop+(-0.4 if sq>1.05 else 0),**squash(sq))
        box={}
        put(box,rect(-3,12,0,14),BX); put(box,[(-3,12),(0,12),(-2,13),(-1,13)],BXL)
        put(box,[(-4,11),(-3,10),(-2,10),(-1,11)],BX)
        money={}
        if snapped:
            for k,(x,y0) in enumerate(rain):
                y=round((i-20)*0.7)+y0-30
                yy=y%26-7 if (i-20)*0.7+y0-30>=-7 else None
                if yy is None: continue
                xx=x+round(math.sin(TAU*(i/16+k*0.3)))
                if k%2:
                    money.update({(xx,yy):MO,(xx+1,yy):MO,(xx+2,yy):MO,(xx+1,yy):MOD})
                else:
                    money.update({(xx,yy):CO,(xx+1,yy):CO,(xx,yy+1):COD,(xx+1,yy+1):COD})
                    money[(xx,yy)]='#D77757'
        fr.append((comp(box,shadow(-hop),ch,fx,money),60))
    fr[19]=(fr[19][0],300)
    return fr


# ================= v2 (revisions 2026-10-22) =================
def hand(p,x,y,c=BODY):
    put(p,rect(x,y,x+1,y+1),c); return p
def heart(x,y,c,c2):
    return {(x,y):c,(x+2,y):c,(x,y+1):c,(x+1,y+1):c2,(x+2,y+1):c,(x+1,y+2):c}
def thick(x0,y0,ang,L,core,edge):
    d={}; a=math.radians(ang); ux,uy=math.cos(a),-math.sin(a); nx,ny=-uy,ux
    for k in range(2,int(L*2)+1):
        t=k/2; cx,cy=x0+ux*t,y0+uy*t
        for o in (-1,1):
            q=(math.floor(cx+nx*o*1.0),math.floor(cy+ny*o*1.0)); d.setdefault(q,edge)
    for k in range(2,int(L*2)+1):
        t=k/2; d[(math.floor(x0+ux*t),math.floor(y0+uy*t))]=core
    return d

def forrest():
    fr=[]; CAP='#C8312E'; CAPD='#9E2321'; ROAD='#B9B1A8'; GH='#EBB7A3'; BR='#A0A6AE'; BRD='#6E737B'
    bits=[(-2,-3),(-1,-4),(1,-3),(2,-2),(-2,-1),(2,-4)]
    for i in range(64):
        sprint=i>=20
        p=eyes(base(arms=False,legs=False),1,0,blink=(i in (8,9)))
        put(p,rect(2,5,12,5)+rect(3,4,11,4),CAP); put(p,[(13,5),(14,5),(15,5)],CAPD); put(p,[(7,3)],CAPD)
        legs={}
        if not sprint:
            st=(i//4)%2
            for k,x in enumerate((3,5,9,11)):
                y=13 if (k%2==st) else 14
                legs[(x,13)]=BODY; legs[(x,14)]=BODY
            for x in (2,4,8,10,6,12): 
                for y in (13,14): legs[(x,y)]=BR if x in (2,4,8,10) else BRD
            for x in (2,8): legs[(x,13)]=BRD
            hand(p,-1,10); hand(p,14,10)
            rot=4*math.sin(TAU*i/8); dy=0; sq=kf(i,[(14,1),(18,0.82),(20,1.15),(23,1)])
        else:
            ph=i%4; A=ph<2
            L1=[(2,13),(3,14),(8,13),(9,14)]; L2=[(5,13),(5,14),(11,13),(12,14)]
            legs.update({q:BODY for q in (L1 if A else L2)})
            for q in (L2 if A else L1): legs.setdefault((q[0]-1,q[1]),GH)
            for q in (L1 if A else L2): legs.setdefault((q[0]-2,q[1]),'#F3D3C6')
            if A: hand(p,-1,8); hand(p,14,11)
            else: hand(p,-1,11); hand(p,14,8)
            rot=-7; dy=-0.6 if ph in (1,3) else 0; sq=1 if i>=23 else kf(i,[(20,1.15),(23,1)])
        body=xform(merge(legs,p),0,dy,rot=rot,**squash(sq))
        bib=Image.new('RGBA',canvas().size,(0,0,0,0)); d=ImageDraw.Draw(bib)
        if True:
            bx,by=(8+OX)*S,(10+OY)*S+round(dy*S)+6
            bl=Image.new('RGBA',(4*S,2*S+6),(0,0,0,0)); dd=ImageDraw.Draw(bl)
            dd.rectangle([0,0,4*S-1,2*S+5],fill='#FFFFFF'); dd.rectangle([2,2,5,5],fill='#B8B8B8'); dd.rectangle([4*S-6,2,4*S-3,5],fill='#B8B8B8')
            tl=text_layer('15',2,2*S,4,'#C8312E',None).crop((0,0,4*S,2*S+6)); bl.alpha_composite(tl)
            bl=bl.rotate(-rot,expand=True,resample=Image.NEAREST)
            bib.alpha_composite(bl,(bx-(bl.width-4*S)//2,by-(bl.height-2*S-6)//2))
        fx={}
        if 20<=i<34:
            t=i-20
            for k,(vx,vy) in enumerate(bits):
                x=round(7+vx*t*0.7); y=round(13+vy*t*0.6+0.12*t*t)
                if y<17: fx[(x,y)]=BR if k%2 else BRD
            if t<3:
                for q in [(1,12),(13,12),(0,14),(14,14),(7,11)]: fx[q]='#FFF6C2'
        scroll=i*(1.6 if sprint else 0.3)
        road={}
        for x in range(-4,19):
            road[(x,15)]=ROAD
            if int(x+scroll)%6<2: road[(x,16)]='#8F877E'
        mv={}
        for bxp,w,h in [(0,3,4),(9,2,6),(16,4,3)]:
            x0=round(bxp-scroll*0.25)%27-5
            for x in range(x0,x0+w):
                for y in range(15-h,15): mv[(x,y)]='#E2B79A' if y>15-h else '#D49A78'
        lines={}
        if sprint:
            for k,y in enumerate((6,9,12,3)):
                x0=round(-4+((i*2+k*5)%10)-2)
                for x in range(x0,x0+3): lines[(x-2,y)]='#E0DAD3'
        fx_f=round(18-(i*0.45)%26); fy=round(-5+1.5*math.sin(TAU*i/24))
        feather={(fx_f,fy):'#FFFFFF',(fx_f+1,fy):'#FFFFFF',(fx_f+2,fy-1):'#FFFFFF',(fx_f+3,fy-1):'#F2F2F2',(fx_f+1,fy+1):'#E6E6E6',(fx_f+2,fy):'#E6E6E6',(fx_f-1,fy+1):'#B9B9B9',(fx_f+4,fy-2):'#B9B9B9'}
        fr.append((comp(mv,road,lines,feather,body,bib,fx),60 if sprint else 80))
    return fr

def harry():
    fr=[]; HT='#3E2E6B'; HTL='#5A4592'; GL='#6E6E78'; WD='#7A4A2A'; GO='#F2C94C'
    PK=['#FF6FA5','#FF9EC4','#FF4F8B','#FFB3D1']
    import random; rnd=random.Random(5)
    H=[(rnd.uniform(40,140),rnd.uniform(0.25,0.45),k*1.7) for k in range(12)]
    for i in range(60):
        p=eyes(base(arms=False),0 if i<8 else 1,-1 if 8<=i<24 else 0,blink=(i in (50,51)))
        put(p,rect(0,5,14,5),HT); put(p,rect(3,4,11,4),HT); put(p,rect(4,3,10,3),HT); put(p,rect(5,2,9,2),HT); put(p,rect(6,1,8,1),HT)
        put(p,[(8,0),(9,0),(10,-1)],HT); put(p,[(6,3),(5,4)],HTL); put(p,[(7,3)],GO)
        hand(p,-1,10)
        hk=[(0,(15,10),25),(8,(15,10),25),(12,(16,6),110),(16,(15,7),70),(20,(16,5),120),(24,(15,8),60)]
        def at(j):
            if j<=hk[0][0]: return hk[0][1],hk[0][2]
            for (a,pa,aa),(b,pb,ab) in zip(hk,hk[1:]):
                if a<=j<=b:
                    t=ease((j-a)/(b-a)); return (round(pa[0]+(pb[0]-pa[0])*t),round(pa[1]+(pb[1]-pa[1])*t)),aa+(ab-aa)*t
            return hk[-1][1],hk[-1][2]
        (hx,hy),ang=at(min(i,24))
        hand(p,hx,hy)
        wand=line_pts(hx+0.5,hy,ang,4); put(p,wand,WD)
        tip=line_pts(hx+0.5,hy,ang,5)[-1]
        if i>=10: p[tip]='#FFFFFF' if i%2 else '#FFF6C2'
        hop=-kf(i,[(26,0),(29,1.6),(32,0),(36,1.6),(39,0)]) if 26<=i<40 else 0
        sq=kf(i,[(24,1),(26,0.88),(29,1.08),(32,0.9),(34,1)])
        ch=xform(p,0,hop,**squash(sq))
        fx={}
        if 10<=i<26:
            for j in range(max(10,i-4),i):
                (ax,ay),aa=at(j); q=line_pts(ax+0.5,ay,aa,5)[-1]; fx[q]=GO if (i-j)%2 else '#FFF6C2'
        if i>=24:
            for k,(a,sp,off) in enumerate(H):
                t=((i-24)+off*6)%36
                if i-24<off*6 and i<60-0: 
                    if i-24<off*2: continue
                x=round(15+math.cos(math.radians(a))*t*sp*1.4); y=round(2-math.sin(math.radians(a))*t*sp+0.012*t*t*4-t*0.05)
                if -6<x<19 and -8<y<16: fx.update(heart(x,y,PK[k%4],PK[(k+1)%4]))
        fr.append((comp(shadow(-hop),ch,fx),60))
    return fr

def obsession():
    fr=[]; TW='#8A7A45'; LF='#8DB86A'; BX='#5B3A6E'; BXL='#C9A44C'; CO='#F2C94C'; COD='#B5701B'
    rain=[(-3,0),(4,9),(13,2),(16,14),(-1,17),(9,22),(6,-4)]
    for i in range(64):
        snapped=i>=22
        p=eyes(base(arms=False),0,-1 if i<22 else (-1 if (i//6)%2 else 0),blink=(i in (12,13)))
        fx={}
        if not snapped:
            bend=0 if i<12 else min(2,(i-12)//3)
            hand(p,1,3+0); hand(p,12,3)
            for x in range(3,12):
                y=3-(bend if 6<=x<=8 else (bend//2 if x in (5,9) else 0))
                p[(x,y)]=TW
            p[(4,2)]=LF; p[(10,2)]=LF; p[(6,2-bend)]=LF
        else:
            sp=min(2,(i-22)//2)
            hand(p,1-sp,4); hand(p,12+sp,4)
            for k in range(4):
                p[(3-sp+k,4-k//2)]=TW; p[(11+sp-k,4-k//2)]=TW
            p[(4-sp,3)]=LF; p[(10+sp,3)]=LF
        if 22<=i<27:
            r=i-21
            for d in ((0,-1),(1,0),(-1,0),(1,-1),(-1,-1),(0,1)):
                fx[(7+d[0]*r,2+d[1]*r)]='#FFF6C2'
        sq=kf(i,[(20,1),(22,0.85),(25,1.12),(28,1)])
        hop=-kf(i,[(32,0),(36,1.8),(40,0),(44,1.8),(48,0)]) if 32<=i<50 else 0
        ch=xform(p,0,hop+(-0.4 if sq>1.05 else 0),**squash(sq))
        box={}
        put(box,rect(-3,12,0,14),BX); put(box,[(-3,12),(0,12),(-2,13),(-1,13)],BXL)
        put(box,[(-4,11),(-3,10),(-2,10),(-1,11)],BX)
        coins={}; words=None
        if snapped:
            for k,(x,y0) in enumerate(rain):
                yy=((i-22)*0.6+y0)%28-10
                xx=x+round(math.sin(TAU*(i/16+k*0.3)))
                yy=round(yy)
                coins.update({(xx+a,yy+b):CO for a in range(3) for b in range(3)})
                coins.update({(xx,yy):COD,(xx+1,yy):COD,(xx+2,yy):COD,(xx+1,yy+1):COD,(xx+1,yy+2):COD})
            words=canvas()
            for k,(x0,y0) in enumerate([(50,20),(190,110),(90,200)]):
                yy=round(((i-22)*7+y0)%300)-40
                words.alpha_composite(text_layer('token',2,x0+20*math.sin(i/6+k),yy,'#D77757','#FFFFFF'))
        fr.append((comp(box,shadow(-hop),coins,ch,fx,words),60))
    fr[21]=(fr[21][0],300)
    return fr

_spider_v1=spider
def spider():
    fr=[]; RD='#D23A3A'; RW='#8E1F24'; BU='#2D5BB0'
    for i in range(52):
        wave=24<=i<44
        p=eyes(base(),0,0 if i<20 else 1 if i<24 else 0,blink=(i in (46,47)))
        for (x,y),c in list(p.items()):
            if c==BODY: p[(x,y)]=RD if y<=9 else BU
        put(p,[(7,6),(7,7),(5,6),(9,6),(3,7),(11,7),(2,8),(12,8)],RW)
        if wave:
            clear(p,rect(13,7,14,10)); put(p,mirror(UP if (i//3)%2 else DOWN),RD)
        q={(x,20-y):c for (x,y),c in p.items()}
        enter=kf(i,[(0,-22),(10,0)])
        sy=kf(i,[(9,1),(11,1.12),(14,0.92),(17,1)])
        rot=7*math.sin(TAU*(i-14)/28)*kf(i,[(14,0),(18,1),(44,1),(52,0.4)]) if i>=14 else 0
        ch=xform(q,0,enter,sy=sy,sx=1,rot=rot,piv=(7.5,-7))
        web=canvas(); d=ImageDraw.Draw(web)
        Px,Py=(7.5+OX)*S,(-7+OY)*S
        a=math.radians(rot); L=(7+7+enter)*S
        ex,ey=Px-math.sin(a)*L*-1*-1, Py+math.cos(a)*L
        ex=Px+math.sin(-a)*L*-1; 
        ex=Px-math.sin(a)*L if False else Px+math.sin(a)*-L*-1
        d.line([(Px,Py-20),(Px-math.sin(-a)*L, Py+math.cos(a)*L)],fill='#C9CBD3',width=3)
        fr.append((comp(web,ch),60))
    return fr

def starwars():
    fr=[]; CK='#5A3B26'; CK2='#7A5236'; SV='#C8CDD3'; SVD='#2A2A2A'; BC='#CFF3FF'; BE='#1E8BFF'
    DS='#9AA0A8'; DSD='#6E737B'
    def angf(j): return 90-kf(j,[(18,0),(22,-35),(26,15),(30,-40),(35,10),(40,0)])
    for i in range(60):
        p=eyes(base(arms=False),1 if i<6 else 0,-1 if 8<=i<14 else 0,blink=(i in (54,55)))
        put(p,[(1,y) for y in range(6,13)]+[(13,y) for y in range(6,13)],CK)
        put(p,rect(2,5,12,5)+[(1,5),(13,5)],CK); put(p,[(x,4) for x in range(3,12)],CK2)
        fl=(i//3)%2; put(p,[(1,13),(13,13),(0,13+fl),(14,13+fl)],CK)
        hand(p,-1,10)
        hx,hy=15,9
        hand(p,hx,hy)
        ang=angf(i) if 18<=i<40 else 90
        a=math.radians(ang); ux,uy=math.cos(a),-math.sin(a)
        hilt=[(math.floor(hx+0.5+ux*k*0.75),math.floor(hy+0.5+uy*k*0.75)) for k in (0,1,2,3)]
        fx={}
        L=0
        if i>=6: L=kf(i,[(6,0),(10,10)])
        if i>=50: L=kf(i,[(50,10),(54,0)])
        base_x,base_y=hx+0.5+ux*2.5,hy+0.5+uy*2.5
        if 18<=i<40:
            for q in line_pts(base_x,base_y,angf(i-1),10)[2:]: fx[(math.floor(q[0]),math.floor(q[1]))]='#BFE6FF'
        if L>=1:
            for q,c in thick(base_x,base_y,ang,L,BC,BE).items(): fx[q]=c
        for k,q in enumerate(hilt): fx[q]=SVD if k in (1,3) else SV
        if 6<=i<9:
            for d in ((0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                fx[(math.floor(base_x)+d[0],math.floor(base_y)+d[1])]='#FFFFFF' if d==(0,0) or i==6 else BE
        sq=kf(i,[(6,1),(8,0.9),(11,1.08),(14,1)])
        ch=xform(p,0,0,**squash(sq))
        st={}
        for k,(x,y) in enumerate([(4,-6),(8,-4),(-2,4),(17,-6),(12,-6),(-4,9),(17,3)]):
            if (i//4+k)%3: st[(x,y)]='#C9D3F2'
        cx,cy,r=-1,-4,3.6
        for x in range(-5,4):
            for y in range(-8,1):
                dd=math.hypot(x-cx,y-cy)
                if dd<r: st[(x,y)]=DS if (x+y)%5 else '#B3B8BF'
        for x in range(-5,3): 
            if math.hypot(x-cx,0)<r: st[(x,-4)]=DSD
        st.update({(-2,-6):DSD,(-3,-6):DSD,(-2,-5):'#4F535A'})
        fr.append((comp(st,shadow(0),ch,fx),60))
    return fr

def walkingdead():
    fr=[]; HT='#B08A5A'; HTD='#7A5C38'; BAND='#4A3828'; GUN='#6E737B'; GUD='#3E4248'; DIRT='#8B6A4A'
    ZS='#9DB58A'; ZSD='#7A9168'; ZH='#3A3A2E'; ZT='#6B7C8F'; ZTD='#4F5D6E'; ZP='#4E4A44'
    def zombie(step):
        z={}
        put(z,rect(0,3,4,6),ZS); put(z,[(0,3),(1,3),(3,3),(4,2),(2,2)],ZH); put(z,[(4,5),(4,6)],ZSD)
        put(z,[(0,4),(2,4)],'#2A2A22'); put(z,[(1,6)],'#5E6E52')
        put(z,rect(0,7,4,11),ZT); put(z,[(1,11),(3,11),(4,9)],ZTD)
        put(z,[(-1,8),(-2,8),(-3,8+(step%2)),(-1,9),(-2,9+((step+1)%2))],ZS)
        put(z,[(1,12),(1,13),(1,14)] if step%2 else [(0,12),(0,13),(0,14)],ZP)
        put(z,[(3,12),(3,13),(4,14)] if step%2 else [(3,12),(3,13),(3,14)],ZP)
        return z
    for i in range(64):
        run=i>=22
        look=-1 if i<10 else 1
        if run: look=-1
        p=eyes(base(arms=False,legs=not run),look,0,blink=(i in (5,6)))
        put(p,rect(-1,5,15,5),HT); put(p,rect(3,3,11,4),HT); put(p,rect(3,4,11,4),BAND); put(p,[(-1,5),(15,5)],HTD); put(p,[(7,3)],HTD)
        put(p,[(3,11)],'#F2C94C')
        if not run:
            hand(p,-1,10); hand(p,14,10); put(p,[(16,10),(17,10)],GUN); put(p,[(16,11)],GUD)
        else:
            ph=i%4; A=ph<2
            L1=[(3,13),(2,14),(9,13),(8,14)]; L2=[(5,13),(6,14),(11,13),(12,14)]
            put(p,L1 if A else L2,BODY)
            for q in (L2 if A else L1): p.setdefault((q[0]+1,q[1]),'#EBB7A3')
            if A: hand(p,-1,8); hand(p,14,11)
            else: hand(p,-1,11); hand(p,14,8)
        jump=-kf(i,[(14,0),(16,2.6),(19,0)]) if 14<=i<20 else 0
        sq=kf(i,[(13,1),(14,0.85),(16,1.15),(19,0.88),(21,1)])
        cx=kf(i,[(22,0),(60,-26)]); bob=-0.6 if run and i%4 in (1,3) else 0
        ch=xform(p,cx,jump+bob,rot=7 if run else 0,**squash(sq))
        fx={}
        if 15<=i<26: fx.update(bang(7,-3+round(jump)))
        if run and i%3: fx.update({(round(cx)+15,5):'#8FC7F0',(round(cx)+15,6):'#8FC7F0',(round(cx)+16,3):'#8FC7F0'})
        zx=kf(i,[(0,22),(14,15),(22,15),(64,-16)])
        zs=i//(4 if run else 6)
        zb=-0.5 if zs%2 else 0
        zd=zombie(zs)
        zl=xform(zd,zx,zb,rot=-5+3*math.sin(i*0.6),piv=(2,14))
        dirt={(x,15):DIRT for x in range(-4,19)}
        dust={}
        if run:
            for k in range(3):
                pp=((i/8)+k/3)%1; x=round(cx+13+pp*4); y=14-round(pp*2)
                if pp<0.8: dust[(x,y)]='#C9B79C'
        fr.append((comp(dirt,dust,zl,shadow(-jump,y=14,col='#6E5238') if not run else None,ch,fx),60))
    return fr

# ================= v3 (revisions 2026-10-22 noon) =================
def forrest():
    fr=[]; CAP='#C8312E'; CAPD='#9E2321'; ROAD='#B9B1A8'; GH='#EBB7A3'; BR='#A0A6AE'; BRD='#6E737B'
    bits=[(-2,-3),(-1,-4),(1,-3),(2,-2),(-2,-1),(2,-4),(0,-5)]
    acc=0.0; scroll=0.0; BRK=30
    for i in range(64):
        spd=kf(i,[(0,0.17),(22,0.3),(BRK,0.5)])
        acc+=spd; scroll+=spd*3.0
        A=int(acc)%2==0; broken=i>=BRK
        mode='xx' if 25<=i<BRK+3 else ('hap' if BRK+3<=i<52 else 'n')
        p=face(base(arms=False,legs=False),mode,1,0,blink=(i in (8,9,58,59)))
        put(p,rect(2,5,12,5)+rect(3,4,11,4),CAP); put(p,[(13,5),(14,5),(15,5)],CAPD); put(p,[(7,3)],CAPD)
        arms(p,UP if A else DOWN, DOWN if A else UP)
        L1=[(2,13),(3,14),(8,13),(9,14)]; L2=[(5,13),(5,14),(11,13),(12,14)]
        legs={}; lit=L1 if A else L2
        legs.update({q:BODY for q in lit})
        for q in (L2 if A else L1): legs.setdefault((q[0]-1,q[1]),GH)
        if not broken:
            for q in lit: legs.setdefault((q[0]+1,q[1]),BR)
            for q in lit:
                if q[1]==13: legs[(q[0]+1,13)]=BRD
        rot=-kf(i,[(0,2),(BRK,8)])
        dy=-0.6 if (acc%1)<0.5 and i>=16 else 0
        sq=kf(i,[(BRK-2,1),(BRK,0.84),(BRK+2,1.14),(BRK+5,1)])
        body=xform(merge(legs,p),0,dy,rot=rot,**squash(sq))
        fx={}
        if BRK<=i<BRK+16:
            t=i-BRK
            for k,(vx,vy) in enumerate(bits):
                x=round(7+vx*t*0.8); y=round(13+vy*t*0.7+0.14*t*t)
                if y<17:
                    fx[(x,y)]=BR if k%2 else BRD; fx[(x+1,y)]=BR
            if t<3:
                for q in [(1,12),(13,12),(0,14),(14,14),(7,11),(-1,13),(15,13)]: fx[q]='#FFF6C2'
        road={}
        for x in range(-4,19):
            road[(x,15)]=ROAD
            if int(x+scroll)%6<2: road[(x,16)]='#8F877E'
        mv={}
        for bxp,w,h in [(0,3,4),(9,2,6),(16,4,3)]:
            x0=round(bxp-scroll*0.25)%27-5
            for x in range(x0,x0+w):
                for y in range(15-h,15): mv[(x,y)]='#E2B79A' if y>15-h else '#D49A78'
        lines={}
        if broken:
            for k,y in enumerate((6,9,12,3)):
                x0=round(-4+((i*2+k*5)%10)-2)
                for x in range(x0,x0+3): lines[(x-2,y)]='#E0DAD3'
        fx_f=round(18-(i*0.45)%26); fy=round(-5+1.5*math.sin(TAU*i/24))
        feather={(fx_f,fy):'#FFFFFF',(fx_f+1,fy):'#FFFFFF',(fx_f+2,fy-1):'#FFFFFF',(fx_f+3,fy-1):'#F2F2F2',(fx_f+1,fy+1):'#E6E6E6',(fx_f+2,fy):'#E6E6E6',(fx_f-1,fy+1):'#B9B9B9',(fx_f+4,fy-2):'#B9B9B9'}
        fr.append((comp(mv,road,lines,feather,body,fx),70 if i<BRK else 55))
    return fr

def ov_xform(img,ax,ay,sx=1,sy=1):
    if sx==1 and sy==1: return img
    co=(1/sx,0,ax-ax/sx,0,1/sy,ay-ay/sy)
    return img.transform(img.size,Image.AFFINE,co,resample=Image.BILINEAR)
def harry_specs(cs,ax,ay,sx,sy,edx):
    """圆框眼镜 + 额头小闪电（细线叠加，跟着眼睛和挤压走）"""
    img=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); d=ImageDraw.Draw(img)
    P=lambda x,y:(ax+(x-7.5)*cs,ay+(y-15)*cs)
    FR='#2B2B33'; r=1.65
    for ex in (4,10):
        cx,cy=P(ex+0.5+edx,9.0)
        d.ellipse([cx-r*cs,cy-r*cs,cx+r*cs,cy+r*cs],outline=FR,width=3)
    d.line([P(6.0+edx,8.45),P(9.0+edx,8.45)],fill=FR,width=3)
    d.line([P(2.6,8.6),P(3.05+edx,8.7)],fill=FR,width=3)
    d.line([P(12.4,8.6),P(11.95+edx,8.7)],fill=FR,width=3)
    d.line([P(8.05,6.15),P(7.25,6.85),P(7.95,6.85),P(7.15,7.55)],fill='#9A2E1E',width=3,joint='curve')
    return ov_xform(img,ax,ay,sx,sy)

def harry():
    fr=[]; HT='#3E2E6B'; HTL='#5A4592'; HTD='#2A1F4A'; WD='#7A4A2A'; GO='#F2C94C'
    PK='#FF6FA5'; PK2='#FFB3D1'
    # 6 hearts, hand-placed: alternating sides, rising in staggered waves
    HS=[(10,12,0),(2,13,0.5),(13,11,1.0),(-1,12,1.5),(7,13,2.0),(4,11,2.6)]
    CS=10; AX=(7.5+OX)*S; AY=(15+OY)*S
    for i in range(60):
        wave=10<=i<26
        mode='n'
        edx=1 if i<26 else 0
        p=face(base(arms=False),mode,edx,0,blink=(i in (5,6)))
        put(p,rect(0,9,1,10),BODY)
        put(p,rect(-1,5,15,5),HT); put(p,[(-1,5),(15,5)],HTD)
        rows={4:(2,12),3:(3,11),2:(4,10),1:(4,9),0:(5,9),-1:(6,9),-2:(7,10),-3:(9,11),-4:(11,12)}
        for y,(a,b) in rows.items(): put(p,rect(a,y,b,y),HT)
        put(p,rect(2,4,12,4),HTD); put(p,[(4,3),(4,2),(5,1),(5,0),(6,-1)],HTL)
        put(p,[(7,1),(6,2),(8,2),(7,3)],GO); put(p,[(7,2)],'#FFF6C2'); put(p,[(10,-2)],GO)
        if wave:
            # 魔杖稳稳举在右上，只轻轻点两下，不乱甩
            hy=7-(1 if (i//3)%2 else 0); hx=15
            hand(p,hx,hy); wx,wy=hx+0.5,hy; ang=72
        else:
            if i<10: put(p,rect(13,9,14,10),BODY); wx,wy,ang=15,9,60
            else: put(p,rect(13,7,14,8),BODY); wx,wy,ang=15,7,75
        wand=line_pts(wx,wy,ang,4); put(p,wand,WD)
        tip=line_pts(wx,wy,ang,5)[-1]
        if i>=8: p[tip]='#FFF6C2'   # 杖尖恒亮，不闪烁断节
        hop=-kf(i,[(28,0),(31,1.4),(34,0),(38,1.4),(41,0)]) if 28<=i<42 else 0
        sq=kf(i,[(26,1),(28,0.88),(31,1.08),(34,0.9),(36,1)])
        sv=squash(sq)
        ch=render(p,CS,AX,AY+hop*CS,sx=sv['sx'],sy=sv['sy'])
        ch.alpha_composite(harry_specs(CS,AX,AY+hop*CS,sv['sx'],sv['sy'],edx))
        sparks=canvas()
        if wave:
            dd=ImageDraw.Draw(sparks)
            TX=AX+(tip[0]-7.5+0.5)*CS; TY=AY+(tip[1]-15+0.5)*CS
            ph=(i//2)%3
            for k,(ox,oy) in enumerate([(0,-8),(7,-3),(-6,-2)][:ph+1]):
                dd.rectangle([TX+ox-3,TY+oy-3,TX+ox+3,TY+oy+3],fill=GO)
                dd.rectangle([TX+ox-1,TY+oy-1,TX+ox+1,TY+oy+1],fill='#FFF6C2')
        hearts={}
        if i>=26:
            t=(i-26)*0.42
            for k,(x,y,st) in enumerate(HS):
                age=t-st
                if age<0: continue
                yy=y-int(age)
                sway=round(1.2*math.sin(age*0.9+k))
                if yy<-8: continue
                if age<1.2:
                    hearts[(x+1,yy+1)]='#FFFFFF'
                else:
                    hearts.update(heart(x+sway,yy,PK,PK2))
        fr.append((comp(hearts,shadow(-hop),ch,sparks),60))
    fr[-1]=(fr[-1][0],300)
    return fr

def obsession():
    fr=[]; TW='#2A2622'; TWL='#5A5048'; CO='#F2C94C'; COD='#B5701B'
    KR='#D9B07A'; KRL='#EAC994'; KRD='#A9814E'; RD='#C8312E'
    rain=[(-3,0),(4,9),(13,2),(16,14),(-1,17),(9,22),(6,-4)]
    boxtxt=text_layer('ONE WISH WILLOW',2,W*S//2,(15+OY)*S-6,RD,None)
    for i in range(64):
        snapped=i>=22; held=i<34
        mode='n' if i<22 else ('xx' if i<28 else 'hap')
        p=face(base(arms=not held),mode,0,-1 if i<22 else 0,blink=(i in (12,13)))
        fx={}
        if held and not snapped:
            bend=0 if i<12 else min(2,(i-12)//3)
            hand(p,1,3); hand(p,12,3)
            for x in range(3,12):
                y=3-(bend if 6<=x<=8 else (bend//2 if x in (5,9) else 0))
                p[(x,y)]=TW
            for x in (4,9): p[(x,3)]=TWL
            p[(6,2-bend)]=TW
        elif held:
            sp=min(2,(i-22)//2)
            hand(p,1-sp,4); hand(p,12+sp,4)
            for k in range(4):
                p[(3-sp+k,4-k//2)]=TW; p[(11+sp-k,4-k//2)]=TW
            p[(4-sp,4)]=TWL; p[(10+sp,4)]=TWL
        else:
            arms(p,UP if (i//4)%2 else MID, MID if (i//4)%2 else UP)
        if 22<=i<27:
            r=i-21
            for d in ((0,-1),(1,0),(-1,0),(1,-1),(-1,-1),(0,1)):
                fx[(7+d[0]*r,2+d[1]*r)]='#FFF6C2'
        sq=kf(i,[(20,1),(22,0.85),(25,1.12),(28,1)])
        hop=-kf(i,[(36,0),(40,1.8),(44,0),(48,1.8),(52,0)]) if 36<=i<54 else 0
        ch=xform(p,0,hop+(-0.4 if sq>1.05 else 0),**squash(sq))
        box={}  # 盒子去掉
        coins={}; words=None
        if snapped:
            for k,(x,y0) in enumerate(rain):
                yy=round(((i-22)*0.6+y0)%28-10)
                xx=x+round(math.sin(TAU*(i/16+k*0.3)))
                # 清晰硬币：深边 + 亮芯 + 中间一点高光
                coins.update({(xx,yy):COD,(xx+1,yy):COD,(xx+2,yy):COD,
                              (xx,yy+1):COD,(xx+2,yy+1):COD,
                              (xx,yy+2):COD,(xx+1,yy+2):COD,(xx+2,yy+2):COD})
                coins[(xx+1,yy+1)]=CO; coins[(xx+1,yy)]='#FFE9A8'
            words=canvas()
            for k,(x0,y0) in enumerate([(50,20),(190,110),(90,200)]):
                yy=round(((i-22)*7+y0)%260)-40
                words.alpha_composite(text_layer('token',2,x0+20*math.sin(i/6+k),yy,'#D77757','#FFFFFF'))
        fr.append((comp(coins,ch,fx,words),60))
    fr[21]=(fr[21][0],300)
    return fr

def walkingdead():
    fr=[]; HT='#6B4A32'; HTD='#4A321F'; CORD='#C9A24A'; STAR='#E8C25A'; GUN='#6E737B'; GUD='#3E4248'; DIRT='#8B6A4A'
    ZS='#9DB58A'; ZSD='#7A9168'; ZH='#3A3A2E'; ZT='#6B7C8F'; ZTD='#4F5D6E'; ZP='#4E4A44'
    def zombie(step):
        z={}
        put(z,rect(0,3,4,6),ZS); put(z,[(0,3),(1,3),(3,3),(4,2),(2,2)],ZH); put(z,[(4,5),(4,6)],ZSD)
        put(z,[(0,4),(2,4)],'#2A2A22'); put(z,[(1,6)],'#5E6E52')
        put(z,rect(0,7,4,11),ZT); put(z,[(1,11),(3,11),(4,9)],ZTD)
        put(z,[(-1,8),(-2,8),(-3,8+(step%2)),(-1,9),(-2,9+((step+1)%2))],ZS)
        put(z,[(1,12),(1,13),(1,14)] if step%2 else [(0,12),(0,13),(0,14)],ZP)
        put(z,[(3,12),(3,13),(4,14)] if step%2 else [(3,12),(3,13),(3,14)],ZP)
        return z
    for i in range(64):
        run=i>=22
        look=-1 if (i<10 or run) else 1
        mode='xx' if run else 'n'
        p=face(base(arms=False,legs=not run),mode,look,0,blink=(i in (5,6)))
        put(p,rect(-1,5,15,5),HT); put(p,[(-1,5),(15,5)],HTD)
        put(p,rect(3,3,11,4),HT); put(p,rect(4,2,10,2),HT)
        put(p,[(3,4),(4,4),(5,4),(9,4),(10,4),(11,4)],CORD)
        put(p,[(7,2),(6,3),(7,3),(8,3),(6,4),(8,4)],STAR)
        if not run:
            put(p,rect(0,9,1,10)+rect(13,9,14,10),BODY); put(p,[(15,9),(16,9),(17,9)],GUN); put(p,[(15,10)],GUD)
        else:
            ph=i%4; A=ph<2
            L1=[(3,13),(2,14),(9,13),(8,14)]; L2=[(5,13),(6,14),(11,13),(12,14)]
            put(p,L1 if A else L2,BODY)
            for q in (L2 if A else L1): p.setdefault((q[0]+1,q[1]),'#EBB7A3')
            arms(p,UP if A else DOWN, DOWN if A else UP)
        jump=-kf(i,[(14,0),(16,2.6),(19,0)]) if 14<=i<20 else 0
        sq=kf(i,[(13,1),(14,0.85),(16,1.15),(19,0.88),(21,1)])
        cx=kf(i,[(22,0),(60,-26)]); bob=-0.6 if run and i%4 in (1,3) else 0
        ch=xform(p,cx,jump+bob,rot=7 if run else 0,**squash(sq))
        fx={}
        if 15<=i<26: fx.update(bang(7,-4+round(jump)))
        if run and i%3: fx.update({(round(cx)+15,5):'#8FC7F0',(round(cx)+15,6):'#8FC7F0',(round(cx)+16,3):'#8FC7F0'})
        zx=kf(i,[(0,22),(14,15),(22,15),(64,-16)])
        zs=i//(4 if run else 6)
        zl=xform(zombie(zs),zx,-0.5 if zs%2 else 0,rot=-5+3*math.sin(i*0.6),piv=(2,14))
        dirt={(x,15):DIRT for x in range(-4,19)}
        dust={}
        if run:
            for k in range(3):
                pp=((i/8)+k/3)%1; x=round(cx+13+pp*4); y=14-round(pp*2)
                if pp<0.8: dust[(x,y)]='#C9B79C'
        fr.append((comp(dirt,dust,zl,shadow(-jump,y=14,col='#6E5238') if not run else None,ch,fx),60))
    return fr

def starwars():
    fr=[]; CS=7; AY=(15+OY)*S
    DS='#9AA0A8'; DSD='#6E737B'
    def crab(i,side,mode,dx):
        p=face(base(arms=False),mode,dx,0,blink=(i in ((40,41) if side else (46,47))))
        hood='#5A3B26' if side==0 else '#24242A'; hood2='#7A5236' if side==0 else '#3A3A42'; hoodd='#3A2516' if side==0 else '#121216'
        # 兜帽：头顶包过去，两侧垂到肩，露脸
        put(p,rect(3,3,11,3),hood); put(p,rect(2,4,12,4),hood)          # 帽顶
        put(p,[(1,5),(13,5)],hood); put(p,[(2,5),(12,5)],hood2)
        put(p,[(5,3),(9,3)],hood2); put(p,[(7,2),(6,3),(8,3)],hood2)    # 帽尖高光
        # 垂肩的披风：两侧从耳朵往下拉成梯形
        for y in range(6,14):
            w=1 if y<9 else 2
            for xx in range(w):
                p[(1-xx,y)]=hood if xx==0 else hoodd
                p[(13+xx,y)]=hood if xx==0 else hoodd
        put(p,[(0,13),(14,13),(-1,14),(15,14)],hoodd)                   # 下摆
        put(p,rect(0,9,1,10),BODY)
        return p
    LK=[(0,80),(10,80),(14,110),(18,70),(22,100),(26,115),(28,70),(32,30),(35,40),(38,70),(43,100),(47,108),(51,72),(64,72)]
    RK=[(0,80),(10,80),(14,35),(18,70),(22,112),(26,100),(28,70),(32,108),(35,96),(38,70),(43,35),(47,30),(51,72),(64,72)]
    clashes=[18,28,38]
    def draw_saber(img,hx,hy,ang,L,col):
        d=ImageDraw.Draw(img,'RGBA'); a=math.radians(ang); ux,uy=math.cos(a),-math.sin(a)
        bx,by=hx+ux*16,hy+uy*16
        if L>0:
            ex,ey=bx+ux*L,by+uy*L
            # 柔和外晕三层 + 亮芯 + 白热尖
            d.line([(bx,by),(ex,ey)],fill=col+(60,),width=18)
            d.line([(bx,by),(ex,ey)],fill=col+(130,),width=12)
            d.line([(bx,by),(ex,ey)],fill=col+(255,),width=7)
            d.line([(bx,by),(ex,ey)],fill=(255,255,255,235),width=3)
            d.ellipse([ex-5,ey-5,ex+5,ey+5],fill=(255,255,255,210))   # 尖端白热
            d.ellipse([bx-7,by-7,bx+7,by+7],fill=col+(90,))           # 根部辉光
        d.line([(hx-ux*2,hy-uy*2),(bx,by)],fill=(200,205,211,255),width=7)
        for t in (4,10):
            d.line([(hx+ux*t,hy+uy*t),(hx+ux*(t+2),hy+uy*(t+2))],fill=(42,42,42,255),width=7)
        return (bx,by,ux,uy)
    for i in range(64):
        L=kf(i,[(6,0),(10,104)])
        lunge=0
        for c in clashes:
            lunge=max(lunge,kf(i,[(c-3,0),(c,4),(c+3,0)]))
        lunge=max(lunge,kf(i,[(48,0),(51,4),(64,4)]))
        clash=any(abs(i-c)<=1 for c in clashes) or i>=50
        mode='xx' if clash else 'n'
        shake=(1 if i%2 else -1)*2 if i>=51 else 0
        lx=60+lunge+shake; rx=216-lunge-shake
        bob=lambda o: -3 if ((i+o)//4)%2 and not clash else 0
        pl=crab(i,0,mode,1); pr=crab(i,1,mode,1)
        img=canvas(); d=ImageDraw.Draw(img)
        bg={}
        for k,(x,y) in enumerate([(-3,-6),(3,-2),(12,-6),(17,-3),(-2,2),(16,4),(9,-1)]):
            if (i//4+k)%3: bg[(x,y)]='#C9D3F2'
        cx,cy,r=7,-5,2.6
        for x in range(2,13):
            for y in range(-8,1):
                if math.hypot(x-cx,y-cy)<r: bg[(x,y)]=DS if (x+2*y)%5 else '#B3B8BF'
        for x in range(2,13):
            if math.hypot(x-cx,0)<r: bg[(x,-5)]=DSD
        bg.update({(8,-7):DSD,(8,-6):'#4F535A'})
        img.alpha_composite(comp(bg))
        for ax_ in (lx,rx): d.rectangle([ax_-40,AY,ax_+40,AY+5],fill='#D9D2CB')
        img.alpha_composite(render(pl,CS,lx,AY+bob(0)))
        img.alpha_composite(render(pr,CS,rx,AY+bob(2),flip=True))
        hlx,hly=lx+(14+0.5-7.5)*CS+4, AY+bob(0)+(9+0.5-15)*CS
        hrx,hry=rx-(14+0.5-7.5)*CS-4, AY+bob(2)+(9+0.5-15)*CS
        aL=kf(i,LK); aR=180-kf(i,RK)
        sab=canvas()
        b1=draw_saber(sab,hlx,hly,aL,L,(30,139,255))
        b2=draw_saber(sab,hrx,hry,aR,L,(255,48,48))
        img.alpha_composite(sab)
        for hx,hy in ((hlx,hly),(hrx,hry)):
            d.rectangle([hx-7,hy-7,hx+6,hy+6],fill=BODY)
        if clash and L>40:
            (x1,y1,u1,v1),(x2,y2,u2,v2)=b1,b2
            den=u1*(-v2)-v1*(-u2)
            if abs(den)>1e-3:
                t=((x2-x1)*(-v2)-(y2-y1)*(-u2))/den
                px_,py_=x1+u1*t,y1+v1*t
                for k in range(8):
                    a=k*45+(i*23)%45; rr=8+(i*7+k*5)%12
                    qx,qy=px_+math.cos(math.radians(a))*rr,py_-math.sin(math.radians(a))*rr
                    d.rectangle([qx-3,qy-3,qx+2,qy+2],fill='#FFF6C2' if k%2 else '#FFFFFF')
                d.rectangle([px_-6,py_-6,px_+5,py_+5],fill='#FFFFFF')
        fr.append((img,60))
    return fr

# ================= v5 (2026-10-22) =================
# 侏罗克公园：底部跑过一群小美颌龙
_jurassic_v4=jurassic
COMPY=[(5,0),(6,0),(4,1),(5,1),(7,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,3)]
def compy(d,x,y,step,cs=9):
    G='#A7B84A'; GD='#6F7D2C'; BE='#E3E6A6'
    pts={q:G for q in COMPY}; pts[(6,1)]=G; pts[(6,0)]=K
    for q in ((2,3),(3,3),(4,3)): pts[q]=BE
    pts[(1,2)]=GD; pts[(0,1 if step else 2)]=GD
    for q in ([(2,4),(4,4)] if step else [(1,4),(3,4)]): pts[q]=GD
    for (cx,cy),c in pts.items():
        X=x+cx*cs; Y=y+cy*cs; d.rectangle([X,Y,X+cs-1,Y+cs-1],fill=c)
def jurassic():
    fr=[]; N=48; span=W*S+72
    herd=[(0,0),(85,1),(170,0),(250,1)]
    for i,(im,dur) in enumerate(_jurassic_v4()):
        lay=canvas(); d=ImageDraw.Draw(lay)
        for k,(off,ph) in enumerate(herd):
            x=round(i/N*span+off)%span-72
            step=((i+ph*2+k)//2)%2
            y=H*S-46-(4 if step else 0)
            compy(d,x,y,step)
        im=im.copy(); im.alpha_composite(lay); fr.append((im,dur))
    return fr

# 钢铁克：小克在山洞里焊初代机甲 Mark I
def mark1(lit=0.0):
    G1='#80858C'; G2='#5B6068'; G3='#B3B8BE'; DK='#3B3F45'
    a={}
    def R(x0,y0,x1,y1,c):
        for x in range(x0,x1+1):
            for y in range(y0,y1+1): a[(x,y)]=c
    R(12,-4,14,-4,G1); R(11,-3,15,0,G1); R(11,-3,11,0,G2); R(15,-3,15,0,G2); R(12,-4,12,-4,G3)
    R(12,1,14,1,DK)
    R(9,2,17,8,G1); R(8,2,10,4,G2); R(16,2,18,4,G2); R(8,2,10,2,G3); R(16,2,18,2,G3)
    R(9,7,17,8,G2); R(11,9,15,9,DK); R(10,10,16,10,G2)
    R(8,5,9,10,G1); R(17,5,18,10,G1); R(8,5,8,10,G2); R(18,5,18,10,G2)
    R(8,11,9,12,DK); R(17,11,18,12,DK)
    R(10,11,12,14,G1); R(14,11,16,14,G1); R(10,11,10,14,G2); R(16,11,16,14,G2); R(10,12,12,12,G2); R(14,12,16,12,G2)
    R(9,15,12,15,DK); R(14,15,17,15,DK)
    for q in [(10,6),(16,6),(9,3),(17,3),(11,13),(15,13),(13,7),(12,2),(14,2)]: a[q]=G3
    EY=mix('#2A2D33','#BFF3FF',lit) if lit else '#2A2D33'
    a[(12,-2)]=EY; a[(14,-2)]=EY
    rc=mix('#4A5058','#6FD8FF',lit) if lit else '#4A5058'; cc=mix('#5E646C','#FFFFFF',lit) if lit else '#5E646C'
    for q in [(12,3),(13,3),(14,3),(12,4),(14,4),(12,5),(13,5),(14,5)]: a[q]=rc
    a[(13,4)]=cc
    return a
def mix(c1,c2,t):
    t=max(0,min(1,t)); a=[int(c1[k:k+2],16) for k in (1,3,5)]; b=[int(c2[k:k+2],16) for k in (1,3,5)]
    return '#%02X%02X%02X'%tuple(round(a[j]+(b[j]-a[j])*t) for j in range(3))
def ironman():
    fr=[]; N=64; CS=9; AX=round((2.2+OX)*S); AY=(15+OY)*S
    import random
    for i in range(N):
        weld=i<36
        lit=kf(i,[(36,0),(40,1),(58,1),(63,0.15)]) if i>=36 else 0
        mode='xx' if weld else ('hap' if i>=44 else 'n')
        p=face(base(arms=False),mode,1 if 36<=i<44 else 0,-1 if 36<=i<44 else 0,blink=False)
        put(p,rect(0,9,1,10),BODY)
        if weld:
            hy=8+(1 if (i//4)%2 else 0); hand(p,15,hy)
        else: put(p,mirror(rect(0,9,1,10)),BODY)
        hop=-kf(i,[(44,0),(47,1.6),(50,0),(54,1.6),(57,0)]) if 44<=i<58 else 0
        sq=kf(i,[(43,1),(44,0.86),(47,1.08),(50,0.9),(52,1)]) if 42<=i<53 else 1
        sv=squash(sq)
        ch=render(p,CS,AX,AY+hop*CS,sx=sv['sx'],sy=sv['sy'])
        jolt=(0,-0.4)[i in (40,41)] if True else 0
        arm=xform(mark1(lit),0,jolt,rot=(0.8*math.sin(TAU*(i-44)/14) if 44<=i<58 else 0),piv=(13,15))
        fx=canvas(); d=ImageDraw.Draw(fx)
        if weld:
            hx=AX+(15+1-7.5)*CS; hy_=AY+(hy+0.5-15)*CS
            d.line([hx,hy_,hx+10,hy_-3],fill='#3B3F45',width=6)
            d.line([hx+10,hy_-3,hx+16,hy_-5],fill='#C9A24A',width=4)
            tx,ty=hx+17,hy_-5
            fl=(i%2)
            d.polygon([(tx,ty-4),(tx+11+fl*4,ty-1),(tx,ty+3)],fill='#7FD6FF')
            d.polygon([(tx,ty-1),(tx+5+fl*2,ty),(tx,ty+1)],fill='#FFFFFF')
            gx,gy=tx+12,ty
            gr=10+3*fl
            d.ellipse([gx-gr,gy-gr,gx+gr,gy+gr],fill=(255,240,200,110))
            d.rectangle([gx-3,gy-3,gx+3,gy+3],fill='#FFFFFF')
            rnd=random.Random(7)
            for k in range(48):
                born=rnd.randint(-10,35); age=i-born
                if age<0 or age>9: continue
                vx=rnd.uniform(-4.5,2.5); vy=rnd.uniform(-6,-0.5)
                qx=gx+vx*age*2.6; qy=gy+vy*age*2.6+0.6*age*age*2
                c=['#FFFFFF','#FFE08A','#FFB347','#FF8A3D'][min(3,age//3)]
                sz=5 if age<4 else (4 if age<7 else 3)
                d.rectangle([qx,qy,qx+sz,qy+sz],fill=c)
        if lit>0.05:
            RX=(13+OX+0.5)*S; RY=(4+OY+0.5+jolt)*S
            for k in range(2):
                t=((i-38)/10+k*0.5)%1
                rr=10+t*26; al=int(170*(1-t)*lit)
                d.ellipse([RX-rr,RY-rr,RX+rr,RY+rr],outline=(111,216,255,al),width=3)
            d.ellipse([RX-16,RY-16,RX+16,RY+16],fill=(111,216,255,int(70*lit)))
            for ex in (12,14):
                EX=(ex+OX+0.5)*S; EY=(-2+OY+0.5+jolt)*S
                d.ellipse([EX-9,EY-9,EX+9,EY+9],fill=(191,243,255,int(60*lit)))
        floor={(x,15):'#C9BFB3' for x in range(-4,19)}
        sh=shadow(-hop) if False else {}
        fr.append((comp(floor,arm,fx,ch),60))
    fr[-1]=(fr[-1][0],240)
    return fr

MORE=['forrest','spider','harry','starwars','walkingdead','truman','jurassic','obsession','ironman']
if __name__=='__main__':
    cm.OUT=sys.argv[1] if len(sys.argv)>1 and os.path.isdir(sys.argv[1]) else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','movies','v6')
    names=[a for a in sys.argv[1:] if a in MORE] or MORE
    for nm in names: cm.save(nm,globals()[nm]())
