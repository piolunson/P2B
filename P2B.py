"""
pay 2 brick — Kivy edition
65 ciphers + 10 hashes
Responsive: landscape = side-by-side, portrait = top/bottom
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.clock import Clock

import math, base64, hashlib, zlib, random as _rnd

# ── THEME ─────────────────────────────────────────────────────────────────────

DARK = dict(
    bg=(0.06,0.06,0.08,1), panel=(0.09,0.09,0.12,1),
    accent=(0.90,0.22,0.27,1), accent2=(0.75,0.18,0.22,1),
    fg=(0.91,0.91,0.94,1), sub=(0.53,0.53,0.67,1),
    border=(0.16,0.16,0.23,1), input=(0.12,0.12,0.16,1),
    btn=(0.14,0.14,0.20,1), btn2=(0.18,0.18,0.26,1),
)
LIGHT = dict(
    bg=(0.94,0.94,0.96,1), panel=(1.00,1.00,1.00,1),
    accent=(0.90,0.22,0.27,1), accent2=(0.75,0.18,0.22,1),
    fg=(0.07,0.07,0.13,1), sub=(0.33,0.33,0.47,1),
    border=(0.80,0.80,0.87,1), input=(0.93,0.93,0.97,1),
    btn=(0.87,0.87,0.92,1), btn2=(0.80,0.80,0.88,1),
)
STATE = {"dark": True}
def T(): return DARK if STATE["dark"] else LIGHT

# ── HELPERS ───────────────────────────────────────────────────────────────────

def _si(k, d=3):
    try: return int(k)
    except: return d

def _ash(c, s):
    if c.isalpha():
        b = ord('A') if c.isupper() else ord('a')
        return chr((ord(c)-b+s)%26+b)
    return c

def _modinv(a, m):
    for x in range(1,m):
        if (a*x)%m==1: return x
    return 1

# ── 65 CIPHERS ────────────────────────────────────────────────────────────────

def reverse_e(t,k): return t[::-1]
def reverse_d(t,k): return t[::-1]

_R13=str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                   "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm")
def rot13_e(t,k): return t.translate(_R13)
def rot13_d(t,k): return t.translate(_R13)
def rot5_e(t,k): return "".join(chr((ord(c)-48+5)%10+48) if c.isdigit() else c for c in t)
def rot5_d(t,k): return rot5_e(t,k)
def rot47_e(t,k): return "".join(chr((ord(c)-33+47)%94+33) if 33<=ord(c)<=126 else c for c in t)
def rot47_d(t,k): return rot47_e(t,k)
def rot18_e(t,k): return rot13_e(rot5_e(t,k),k)
def rot18_d(t,k): return rot18_e(t,k)

def atbash_e(t,k):
    res=[]
    for c in t:
        if c.isalpha(): b=ord('A') if c.isupper() else ord('a'); res.append(chr(b+25-(ord(c)-b)))
        else: res.append(c)
    return "".join(res)
def atbash_d(t,k): return atbash_e(t,k)

_L={'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7','l':'1','g':'9','b':'8'}
_LR={v:k for k,v in _L.items()}
def leet_e(t,k): return "".join(_L.get(c.lower(),c) for c in t)
def leet_d(t,k): return "".join(_LR.get(c,c) for c in t)
def swapcase_e(t,k): return t.swapcase()
def swapcase_d(t,k): return t.swapcase()

def caesar_e(t,k): s=_si(k,3); return "".join(_ash(c,s) for c in t)
def caesar_d(t,k): s=_si(k,3); return "".join(_ash(c,-s) for c in t)
def caesarall_e(t,k): s=_si(k,3); return "".join(chr((ord(c)+s)%256) for c in t)
def caesarall_d(t,k): s=_si(k,3); return "".join(chr((ord(c)-s)%256) for c in t)
def caesarnum_e(t,k): s=_si(k,5); return "".join(str((int(c)+s)%10) if c.isdigit() else c for c in t)
def caesarnum_d(t,k): s=_si(k,5); return "".join(str((int(c)-s)%10) if c.isdigit() else c for c in t)

def affine_e(t,k):
    p=(k or "5,8").split(',')
    try: a,b=int(p[0]),int(p[1])
    except: a,b=5,8
    res=[]
    for c in t:
        if c.isalpha(): base=ord('A') if c.isupper() else ord('a'); res.append(chr((a*(ord(c)-base)+b)%26+base))
        else: res.append(c)
    return "".join(res)
def affine_d(t,k):
    p=(k or "5,8").split(',')
    try: a,b=int(p[0]),int(p[1])
    except: a,b=5,8
    ai=_modinv(a,26); res=[]
    for c in t:
        if c.isalpha(): base=ord('A') if c.isupper() else ord('a'); res.append(chr((ai*(ord(c)-base-b))%26+base))
        else: res.append(c)
    return "".join(res)

def _vig(t,k,dec=False):
    k=(k or "key").lower(); res,ki=[],0
    for c in t:
        if c.isalpha():
            sh=ord(k[ki%len(k)])-ord('a')
            if dec: sh=-sh
            res.append(_ash(c,sh)); ki+=1
        else: res.append(c)
    return "".join(res)
def vigenere_e(t,k): return _vig(t,k,False)
def vigenere_d(t,k): return _vig(t,k,True)

def beaufort_e(t,k):
    k=(k or "key").lower(); res,ki=[],0
    for c in t:
        if c.isalpha():
            base=ord('A') if c.isupper() else ord('a'); kv=ord(k[ki%len(k)])-ord('a')
            res.append(chr((kv-(ord(c)-base))%26+base)); ki+=1
        else: res.append(c)
    return "".join(res)
def beaufort_d(t,k): return beaufort_e(t,k)

def autokey_e(t,k):
    k=(k or "key").lower(); letters=[c.lower() for c in t if c.isalpha()]
    ks=list(k)+letters; res,ki=[],0
    for c in t:
        if c.isalpha(): sh=ord(ks[ki])-ord('a'); ki+=1; res.append(_ash(c,sh))
        else: res.append(c)
    return "".join(res)
def autokey_d(t,k):
    k=(k or "key").lower(); ks=list(k); res,ki=[],0
    for c in t:
        if c.isalpha():
            sh=ord(ks[ki])-ord('a'); ki+=1; dc=_ash(c,-sh); ks.append(dc.lower()); res.append(dc)
        else: res.append(c)
    return "".join(res)

def gronsfeld_e(t,k):
    k=''.join(c for c in (k or "1234") if c.isdigit()) or "1234"; res,ki=[],0
    for c in t:
        if c.isalpha(): res.append(_ash(c,int(k[ki%len(k)]))); ki+=1
        else: res.append(c)
    return "".join(res)
def gronsfeld_d(t,k):
    k=''.join(c for c in (k or "1234") if c.isdigit()) or "1234"; res,ki=[],0
    for c in t:
        if c.isalpha(): res.append(_ash(c,-int(k[ki%len(k)]))); ki+=1
        else: res.append(c)
    return "".join(res)

def runningkey_e(t,k):
    k=(k or "thequickbrownfoxjumpsoverthelazydog")*max(1,len(t)//10+1)
    return vigenere_e(t,k)
def runningkey_d(t,k):
    k=(k or "thequickbrownfoxjumpsoverthelazydog")*max(1,len(t)//10+1)
    return vigenere_d(t,k)

def trithemius_e(t,k):
    res=[]; i=0
    for c in t:
        if c.isalpha(): res.append(_ash(c,i)); i+=1
        else: res.append(c)
    return "".join(res)
def trithemius_d(t,k):
    res=[]; i=0
    for c in t:
        if c.isalpha(): res.append(_ash(c,-i)); i+=1
        else: res.append(c)
    return "".join(res)

def keyedrot_e(t,k):
    s=sum(ord(c) for c in (k or "a"))%26
    return "".join(_ash(c,s) for c in t)
def keyedrot_d(t,k):
    s=sum(ord(c) for c in (k or "a"))%26
    return "".join(_ash(c,-s) for c in t)

def porta_e(t,k):
    k=(k or "key").lower(); ROWS=["acegikmoqs","bdfhjlnprt","uwyxzvqomk","egikmoqsuw","bdfhjlnprt","acegikmoqs"]
    res,ki=[],0
    for c in t:
        if c.isalpha():
            kv=(ord(k[ki%len(k)])-ord('a'))//2; row=ROWS[kv%6]; low=c.lower()
            if low in row: mapped=chr(ord('a')+(row.index(low)+13)%26)
            else: mapped=chr(ord('a')+(ord(low)-ord('a')+13)%26)
            res.append(mapped.upper() if c.isupper() else mapped); ki+=1
        else: res.append(c)
    return "".join(res)
def porta_d(t,k): return porta_e(t,k)

def keyword_e(t,k):
    k=(k or "key").upper(); seen=[]; alpha=[]
    for c in k:
        if c.isalpha() and c not in seen: seen.append(c); alpha.append(c)
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in seen: alpha.append(c)
    tbl={chr(65+i):alpha[i] for i in range(26)}
    res=[]
    for c in t:
        if c.isalpha(): m=tbl[c.upper()]; res.append(m if c.isupper() else m.lower())
        else: res.append(c)
    return "".join(res)
def keyword_d(t,k):
    k=(k or "key").upper(); seen=[]; alpha=[]
    for c in k:
        if c.isalpha() and c not in seen: seen.append(c); alpha.append(c)
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in seen: alpha.append(c)
    tbl={alpha[i]:chr(65+i) for i in range(26)}
    res=[]
    for c in t:
        if c.isalpha(): m=tbl.get(c.upper(),c.upper()); res.append(m if c.isupper() else m.lower())
        else: res.append(c)
    return "".join(res)

def simpsub_e(t,k):
    k=(k or "ZYXWVUTSRQPONMLKJIHGFEDCBA").upper().ljust(26,"A")[:26]; res=[]
    for c in t:
        if c.isalpha(): m=k[ord(c.upper())-65]; res.append(m if c.isupper() else m.lower())
        else: res.append(c)
    return "".join(res)
def simpsub_d(t,k):
    k=(k or "ZYXWVUTSRQPONMLKJIHGFEDCBA").upper().ljust(26,"A")[:26]
    rev={k[i]:chr(65+i) for i in range(26)}; res=[]
    for c in t:
        if c.isalpha(): m=rev.get(c.upper(),c.upper()); res.append(m if c.isupper() else m.lower())
        else: res.append(c)
    return "".join(res)

_HOMO={chr(65+i):list(range(i*3,i*3+3)) for i in range(26)}
_HOMO_R={v:chr(65+ki) for ki,vals in enumerate(_HOMO.values()) for v in vals}
def homophonic_e(t,k): return " ".join(str(_rnd.choice(_HOMO[c.upper()])) if c.isalpha() else c for c in t)
def homophonic_d(t,k):
    res=[]
    for w in t.split():
        try: res.append(_HOMO_R.get(int(w),'?'))
        except: res.append(w)
    return "".join(res)

def chaocipher_e(t,k):
    L=list((k.upper()+"ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:26]) if k and len(k)>=26 else list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    R=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); res=[]
    for c in t:
        if c.isalpha():
            up=c.upper(); idx=R.index(up) if up in R else 0
            res.append(L[idx] if c.isupper() else L[idx].lower())
            L=L[idx:]+L[:idx]; L.insert(1,L.pop(13%len(L)))
            R=R[idx:]+R[:idx]; R.insert(0,R.pop(13%len(R)))
        else: res.append(c)
    return "".join(res)
def chaocipher_d(t,k):
    L=list((k.upper()+"ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:26]) if k and len(k)>=26 else list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    R=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); res=[]
    for c in t:
        if c.isalpha():
            up=c.upper(); idx=L.index(up) if up in L else 0
            res.append(R[idx] if c.isupper() else R[idx].lower())
            L=L[idx:]+L[:idx]; L.insert(1,L.pop(13%len(L)))
            R=R[idx:]+R[:idx]; R.insert(0,R.pop(13%len(R)))
        else: res.append(c)
    return "".join(res)

def railfence_e(t,k):
    rails=max(2,_si(k,3)); fence=[[] for _ in range(rails)]; r,d=0,1
    for c in t:
        fence[r].append(c)
        if r==0: d=1
        elif r==rails-1: d=-1
        r+=d
    return "".join("".join(row) for row in fence)
def railfence_d(t,k):
    rails=max(2,_si(k,3)); n=len(t); pattern=[]; r,d=0,1
    for _ in range(n):
        pattern.append(r)
        if r==0: d=1
        elif r==rails-1: d=-1
        r+=d
    counts=[pattern.count(i) for i in range(rails)]; idx=0; rows=[]
    for c in counts: rows.append(list(t[idx:idx+c])); idx+=c
    ptrs=[0]*rails; res=[]
    for r in pattern: res.append(rows[r][ptrs[r]]); ptrs[r]+=1
    return "".join(res)

def columnar_e(t,k):
    k=k or "key"; cols=len(k); rows=math.ceil(len(t)/cols)
    padded=t.ljust(rows*cols,'_'); order=sorted(range(cols),key=lambda i:k[i])
    return "".join(padded[r*cols+c] for c in order for r in range(rows))
def columnar_d(t,k):
    k=k or "key"; cols=len(k); rows=math.ceil(len(t)/cols)
    chunk=len(t)//cols; extra=len(t)%cols
    order=sorted(range(cols),key=lambda i:k[i])
    col_lens=[chunk+(1 if order.index(i)<extra else 0) for i in range(cols)]
    idx=0; col_data={}
    for c in order: l=col_lens[c]; col_data[c]=list(t[idx:idx+l]); idx+=l
    res=[]; ptrs={c:0 for c in range(cols)}
    for r in range(rows):
        for c in range(cols):
            if ptrs[c]<len(col_data.get(c,[])): res.append(col_data[c][ptrs[c]]); ptrs[c]+=1
    return "".join(res).rstrip('_')
def doubletrans_e(t,k): return columnar_e(columnar_e(t,k),k)
def doubletrans_d(t,k): return columnar_d(columnar_d(t,k),k)

def revwords_e(t,k): return " ".join(w[::-1] for w in t.split())
def revwords_d(t,k): return revwords_e(t,k)
def revorder_e(t,k): return " ".join(reversed(t.split()))
def revorder_d(t,k): return revorder_e(t,k)
def revlines_e(t,k): return "\n".join(line[::-1] for line in t.splitlines())
def revlines_d(t,k): return revlines_e(t,k)
def mirror_e(t,k): return t+t[::-1]
def mirror_d(t,k): return t[:len(t)//2] if len(t)%2==0 else t[:(len(t)+1)//2]
def wordscramble_e(t,k):
    def sc(w):
        if len(w)<=3: return w
        mid=list(w[1:-1]); _rnd.shuffle(mid); return w[0]+"".join(mid)+w[-1]
    return " ".join(sc(w) for w in t.split())
def wordscramble_d(t,k): return t

def _pf_tbl(k):
    k=(k or "key").upper().replace('J','I'); seen=[]; tbl=[]
    for c in k+"ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in seen and c!='J': seen.append(c); tbl.append(c)
    return tbl
def _pf_pos(tbl,c): idx=tbl.index(c); return idx//5,idx%5
def _pf_pair(tbl,a,b,enc):
    ra,ca=_pf_pos(tbl,a); rb,cb=_pf_pos(tbl,b); d=1 if enc else -1
    if ra==rb: return tbl[ra*5+(ca+d)%5]+tbl[rb*5+(cb+d)%5]
    if ca==cb: return tbl[((ra+d)%5)*5+ca]+tbl[((rb+d)%5)*5+cb]
    return tbl[ra*5+cb]+tbl[rb*5+ca]
def _pf_proc(t,k,enc):
    tbl=_pf_tbl(k); letters=[c for c in t.upper().replace('J','I') if c.isalpha()]
    pairs=[]; i=0
    while i<len(letters):
        a=letters[i]; b=letters[i+1] if i+1<len(letters) else 'X'
        if a==b: pairs.append((a,'X')); i+=1
        else: pairs.append((a,b)); i+=2
    return " ".join(_pf_pair(tbl,a,b,enc) for a,b in pairs)
def playfair_e(t,k): return _pf_proc(t,k,True)
def playfair_d(t,k): return _pf_proc(t,k,False)

def foursquare_e(t,k):
    parts=k.split(',') if ',' in (k or "") else [k or "key",(k or "key")[::-1]]
    t1=_pf_tbl(parts[0]); t2=_pf_tbl(parts[1] if len(parts)>1 else (k or "key"))
    std=_pf_tbl(""); letters=[c for c in t.upper() if c.isalpha() and c!='J']
    if len(letters)%2: letters.append('X')
    res=[]
    for i in range(0,len(letters),2):
        a,b=letters[i],letters[i+1]; ra,ca=_pf_pos(std,a); rb,cb=_pf_pos(std,b)
        res.append(t1[ra*5+cb]+t2[rb*5+ca])
    return " ".join(res)
def foursquare_d(t,k):
    parts=k.split(',') if ',' in (k or "") else [k or "key",(k or "key")[::-1]]
    t1=_pf_tbl(parts[0]); t2=_pf_tbl(parts[1] if len(parts)>1 else (k or "key"))
    std=_pf_tbl(""); letters=[c for c in t.upper() if c.isalpha() and c!='J']
    if len(letters)%2: letters.append('X')
    res=[]
    for i in range(0,len(letters),2):
        a,b=letters[i],letters[i+1]; ra,ca=_pf_pos(t1,a); rb,cb=_pf_pos(t2,b)
        res.append(std[ra*5+cb]+std[rb*5+ca])
    return " ".join(res)

def _bifid_tbl(k):
    k=(k or "key").upper().replace('J','I'); seen=[]; tbl=[]
    for c in k+"ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in seen and c!='J': seen.append(c); tbl.append(c)
    return tbl
def bifid_e(t,k):
    tbl=_bifid_tbl(k); letters=[c.upper().replace('J','I') for c in t if c.isalpha()]
    rows=[tbl.index(c)//5 for c in letters]; cols=[tbl.index(c)%5 for c in letters]
    n=len(letters); combined=rows+cols
    return "".join(tbl[combined[i]*5+combined[i+n]] for i in range(n))
def bifid_d(t,k):
    tbl=_bifid_tbl(k); letters=[c.upper().replace('J','I') for c in t if c.isalpha()]
    n=len(letters); combined=[]
    for c in letters: idx=tbl.index(c); combined.append(idx//5); combined.append(idx%5)
    rows=combined[:n]; cols=combined[n:]
    return "".join(tbl[rows[i]*5+cols[i]] for i in range(n))

_POLY="ABCDEFGHIKLMNOPQRSTUVWXYZ"
def polybius_e(t,k):
    res=[]
    for c in t.upper():
        if c=='J': c='I'
        if c in _POLY: idx=_POLY.index(c); res.append(f"{idx//5+1}{idx%5+1}")
        else: res.append(c)
    return " ".join(res)
def polybius_d(t,k):
    res=[]
    for code in t.split():
        if len(code)==2 and code.isdigit():
            try: res.append(_POLY[(int(code[0])-1)*5+(int(code[1])-1)])
            except: res.append('?')
        else: res.append(code)
    return "".join(res)

_BACON={c:''.join('B' if b=='1' else 'A' for b in format(i,'05b')) for i,c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
_BACON_R={v:k for k,v in _BACON.items()}
def bacon_e(t,k): return " ".join(_BACON.get(c.upper(),'?') for c in t if c.isalpha())
def bacon_d(t,k): return "".join(_BACON_R.get(c.upper(),'?') for c in t.split())

def _hill2(t,mat,inv=False):
    def mm(m,v): return [(m[0]*v[0]+m[1]*v[1])%26,(m[2]*v[0]+m[3]*v[1])%26]
    def inv2(m):
        det=(m[0]*m[3]-m[1]*m[2])%26; di=_modinv(det,26)
        return [(m[3]*di)%26,(-m[1]*di)%26,(-m[2]*di)%26,(m[0]*di)%26]
    letters=[c.upper() for c in t if c.isalpha()]
    if len(letters)%2: letters.append('X')
    if inv: mat=inv2(mat)
    res=[]
    for i in range(0,len(letters),2):
        v=[ord(letters[i])-65,ord(letters[i+1])-65]; ev=mm(mat,v)
        res.append(chr(ev[0]+65)+chr(ev[1]+65))
    return "".join(res)
def hill_e(t,k):
    p=(k or "3,3,2,5").split(',')
    try: mat=[int(x)%26 for x in p[:4]]
    except: mat=[3,3,2,5]
    while len(mat)<4: mat.append(0)
    return _hill2(t,mat,False)
def hill_d(t,k):
    p=(k or "3,3,2,5").split(',')
    try: mat=[int(x)%26 for x in p[:4]]
    except: mat=[3,3,2,5]
    while len(mat)<4: mat.append(0)
    return _hill2(t,mat,True)

def otp_e(t,k):
    if not k: return "[Key required: comma-separated integers e.g. 3,1,4,1,5]"
    try:
        shifts=[int(x) for x in k.split(',')]; res=[]; ki=0
        for c in t:
            if c.isalpha(): res.append(_ash(c,shifts[ki%len(shifts)])); ki+=1
            else: res.append(c)
        return "".join(res)
    except: return "[Error: key must be comma-separated integers]"
def otp_d(t,k):
    if not k: return "[Key required]"
    try:
        shifts=[int(x) for x in k.split(',')]; res=[]; ki=0
        for c in t:
            if c.isalpha(): res.append(_ash(c,-shifts[ki%len(shifts)])); ki+=1
            else: res.append(c)
        return "".join(res)
    except: return "[Error]"

_ER=["EKMFLGDQVZNTOWYHXUSPAIBRCJ","AJDKSIRUXBLHWTMCQGZNPYFVOE","BDFHJLCPRTXVZNYEIWGAKMUSQO"]
_EN=[16,4,21]
def enigma_e(t,k):
    pos=[_si(x,0)%26 for x in (k or "0,0,0").split(',')][:3]
    while len(pos)<3: pos.append(0)
    res=[]
    for c in t:
        if c.isalpha():
            up=c.upper(); pos[2]=(pos[2]+1)%26
            if pos[2]==_EN[2]: pos[1]=(pos[1]+1)%26
            if pos[1]==_EN[1]: pos[0]=(pos[0]+1)%26
            x=ord(up)-65
            for i in range(2,-1,-1): x=(_ER[i].index(chr((x+pos[i])%26+65))-pos[i])%26
            res.append(chr(x+65) if c.isupper() else chr(x+97))
        else: res.append(c)
    return "".join(res)
def enigma_d(t,k): return enigma_e(t,k)

def xor_e(t,k):
    try: kv=int(k or "42")%256; return " ".join(format(ord(c)^kv,'02X') for c in t)
    except: k=k or "a"; return " ".join(format(ord(t[i])^ord(k[i%len(k)]),'02X') for i in range(len(t)))
def xor_d(t,k):
    try:
        parts=t.split(); ints=[int(x,16) for x in parts]
        try: kv=int(k or "42")%256; return "".join(chr(v^kv) for v in ints)
        except: k=k or "a"; return "".join(chr(ints[i]^ord(k[i%len(k)])) for i in range(len(ints)))
    except: return "[Error: invalid XOR data]"
def xorhex_e(t,k):
    try: kv=int(k or "FF",16)%256; return " ".join(format(ord(c)^kv,'02X') for c in t)
    except: return "[Error: key must be hex byte e.g. FF]"
def xorhex_d(t,k):
    try: kv=int(k or "FF",16)%256; return "".join(chr(int(x,16)^kv) for x in t.split())
    except: return "[Error]"

def b64_e(t,k): return base64.b64encode(t.encode()).decode()
def b64_d(t,k):
    try: return base64.b64decode(t.encode()).decode(errors='replace')
    except: return "[Error: invalid Base64]"
def b32_e(t,k): return base64.b32encode(t.encode()).decode()
def b32_d(t,k):
    try: pad=t+(8-len(t)%8)%8*'='; return base64.b32decode(pad.upper()).decode(errors='replace')
    except: return "[Error: invalid Base32]"
def b16_e(t,k): return t.encode().hex().upper()
def b16_d(t,k):
    try: return bytes.fromhex(t).decode(errors='replace')
    except: return "[Error: invalid Hex]"
_B58='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58_e(t,k):
    n=int.from_bytes(t.encode(),'big')
    if n==0: return '1'
    res=[]
    while n: n,r=divmod(n,58); res.append(_B58[r])
    return ''.join(reversed(res))
def b58_d(t,k):
    n=sum(_B58.index(c)*58**i for i,c in enumerate(reversed(t)))
    if n==0: return ''
    length=(n.bit_length()+7)//8
    try: return n.to_bytes(length,'big').decode(errors='replace')
    except: return "[Error]"
def b85_e(t,k):
    try: return base64.b85encode(t.encode()).decode()
    except: return "[Error]"
def b85_d(t,k):
    try: return base64.b85decode(t.encode()).decode(errors='replace')
    except: return "[Error: invalid Base85]"
def ascii_e(t,k): return " ".join(str(ord(c)) for c in t)
def ascii_d(t,k):
    try: return "".join(chr(int(x)) for x in t.split())
    except: return "[Error]"
def binary_e(t,k): return " ".join(format(ord(c),'08b') for c in t)
def binary_d(t,k):
    try: return "".join(chr(int(x,2)) for x in t.split())
    except: return "[Error]"
def octal_e(t,k): return " ".join(format(ord(c),'o') for c in t)
def octal_d(t,k):
    try: return "".join(chr(int(x,8)) for x in t.split())
    except: return "[Error]"
def url_e(t,k): return "".join(c if c.isalnum() or c in '-_.~' else '%'+format(ord(c),'02X') for c in t)
def url_d(t,k):
    import urllib.parse
    try: return urllib.parse.unquote(t)
    except: return "[Error]"
def html_e(t,k): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')
def html_d(t,k): return t.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#39;',"'")
def unicode_e(t,k): return t.encode('unicode_escape').decode()
def unicode_d(t,k):
    try: return t.encode().decode('unicode_escape')
    except: return "[Error]"

_MO={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'}
_MOR={v:k for k,v in _MO.items()}
def morse_e(t,k): return " ".join(_MO.get(c.upper(),'?') for c in t if not c.isspace())
def morse_d(t,k): return "".join(_MOR.get(w,'?') for w in t.split())

_BR={'a':'⠁','b':'⠃','c':'⠉','d':'⠙','e':'⠑','f':'⠋','g':'⠛','h':'⠓','i':'⠊','j':'⠚','k':'⠅','l':'⠇','m':'⠍','n':'⠝','o':'⠕','p':'⠏','q':'⠟','r':'⠗','s':'⠎','t':'⠞','u':'⠥','v':'⠧','w':'⠺','x':'⠭','y':'⠽','z':'⠵',' ':'⠀'}
_BRR={v:k for k,v in _BR.items()}
def braille_e(t,k): return "".join(_BR.get(c.lower(),'?') for c in t)
def braille_d(t,k): return "".join(_BRR.get(c,'?') for c in t)

_TP="ABCDEFGHIKLMNOPQRSTUVWXYZ"
def tap_e(t,k):
    res=[]
    for c in t.upper():
        if c=='J': c='I'
        if c in _TP: idx=_TP.index(c); res.append(f"{idx//5+1} {idx%5+1}")
        else: res.append(c)
    return "  ".join(res)
def tap_d(t,k):
    res=[]
    for p in t.strip().split("  "):
        nums=p.strip().split()
        if len(nums)==2:
            try: res.append(_TP[(int(nums[0])-1)*5+(int(nums[1])-1)])
            except: res.append('?')
        else: res.append(p)
    return "".join(res)

def pigpen_e(t,k):
    pos="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return " ".join(str(pos.index(c.upper())+1) if c.upper() in pos else c for c in t)
def pigpen_d(t,k):
    pos="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; res=[]
    for w in t.split():
        try: res.append(pos[int(w)-1])
        except: res.append(w)
    return "".join(res)

def null_e(t,k):
    msg=[c for c in t if c.isalpha()]; f=["the","a","and","of","in","is","to","on"]
    result=[]
    for c in msg: result.append(c.upper()); result.extend(_rnd.sample(f,2))
    return " ".join(result)
def null_d(t,k): return "".join(w[0] for w in t.split() if w[0].isupper()).lower()

def piglatin_e(t,k):
    V="aeiouAEIOU"
    def pw(w):
        if not w or not w[0].isalpha(): return w
        if w[0] in V: return w+"ay"
        for i,c in enumerate(w):
            if c in V: return w[i:]+w[:i]+"ay"
        return w+"ay"
    return " ".join(pw(w) for w in t.split())
def piglatin_d(t,k):
    def dw(w):
        if w.endswith("ay") and len(w)>2:
            w=w[:-2]
            for i in range(len(w)-1,-1,-1):
                if w[i] in "aeiouAEIOU": return w[i+1:]+w[:i+1]
        return w
    return " ".join(dw(w) for w in t.split())

_FL={'a':'ɐ','b':'q','c':'ɔ','d':'p','e':'ǝ','f':'ɟ','g':'ƃ','h':'ɥ','i':'ᴉ','j':'ɾ','k':'ʞ','l':'l','m':'ɯ','n':'u','o':'o','p':'d','q':'b','r':'ɹ','s':'s','t':'ʇ','u':'n','v':'ʌ','w':'ʍ','x':'x','y':'ʎ','z':'z'}
_FLR={v:k for k,v in _FL.items()}
def flip_e(t,k): return "".join(_FL.get(c.lower(),c) for c in reversed(t))
def flip_d(t,k): return "".join(_FLR.get(c,c) for c in reversed(t))
def fullwidth_e(t,k): return "".join(chr(ord(c)+0xFEE0) if 0x21<=ord(c)<=0x7E else c for c in t)
def fullwidth_d(t,k): return "".join(chr(ord(c)-0xFEE0) if 0xFF01<=ord(c)<=0xFF5E else c for c in t)
def spoiler_e(t,k): return "||"+"||||".join(t)+"||"
def spoiler_d(t,k): return t.replace("||","")

_ZU=['\u030d','\u030e','\u0304','\u0305','\u033f','\u0311','\u0306','\u0310','\u0352','\u0357']
_ZD=['\u0316','\u0317','\u0318','\u0319','\u031c','\u031d','\u031e','\u031f','\u0320','\u0324']
def zalgo_e(t,k):
    level=max(1,min(10,_si(k,3))); res=[]
    for c in t:
        res.append(c)
        for _ in range(level): res.append(_rnd.choice(_ZU+_ZD))
    return "".join(res)
def zalgo_d(t,k):
    import unicodedata
    return "".join(c for c in t if unicodedata.category(c)!='Mn')
def zlibcomp_e(t,k): return base64.b64encode(zlib.compress(t.encode())).decode()
def zlibcomp_d(t,k):
    try: return zlib.decompress(base64.b64decode(t.encode())).decode()
    except: return "[Error: invalid compressed data]"
def crc32_e(t,k): return format(zlib.crc32(t.encode())&0xFFFFFFFF,'08X')
def crc32_d(t,k): return "[CRC32 is one-way]"

# ── 10 HASHES ─────────────────────────────────────────────────────────────────
def hash_md5(t,k):      return hashlib.md5(t.encode()).hexdigest()
def hash_sha1(t,k):     return hashlib.sha1(t.encode()).hexdigest()
def hash_sha224(t,k):   return hashlib.sha224(t.encode()).hexdigest()
def hash_sha256(t,k):   return hashlib.sha256(t.encode()).hexdigest()
def hash_sha384(t,k):   return hashlib.sha384(t.encode()).hexdigest()
def hash_sha512(t,k):   return hashlib.sha512(t.encode()).hexdigest()
def hash_sha3_256(t,k): return hashlib.sha3_256(t.encode()).hexdigest()
def hash_sha3_512(t,k): return hashlib.sha3_512(t.encode()).hexdigest()
def hash_blake2b(t,k):  return hashlib.blake2b(t.encode()).hexdigest()
def hash_blake2s(t,k):  return hashlib.blake2s(t.encode()).hexdigest()

# ── REGISTRIES ────────────────────────────────────────────────────────────────
CIPHERS = {
    "01 Reverse":(False,reverse_e,reverse_d),"02 ROT-13":(False,rot13_e,rot13_d),
    "03 ROT-5":(False,rot5_e,rot5_d),"04 ROT-18":(False,rot18_e,rot18_d),
    "05 ROT-47":(False,rot47_e,rot47_d),"06 Atbash":(False,atbash_e,atbash_d),
    "07 Leet Speak":(False,leet_e,leet_d),"08 Swap Case":(False,swapcase_e,swapcase_d),
    "09 Caesar":(True,caesar_e,caesar_d),"10 Caesar All-ASCII":(True,caesarall_e,caesarall_d),
    "11 Caesar Numbers":(True,caesarnum_e,caesarnum_d),"12 Affine":(True,affine_e,affine_d),
    "13 Vigenere":(True,vigenere_e,vigenere_d),"14 Beaufort":(True,beaufort_e,beaufort_d),
    "15 Autokey":(True,autokey_e,autokey_d),"16 Gronsfeld":(True,gronsfeld_e,gronsfeld_d),
    "17 Running Key":(True,runningkey_e,runningkey_d),"18 Trithemius":(False,trithemius_e,trithemius_d),
    "19 Keyed ROT":(True,keyedrot_e,keyedrot_d),"20 Porta":(True,porta_e,porta_d),
    "21 Keyword Cipher":(True,keyword_e,keyword_d),"22 Simple Substitution":(True,simpsub_e,simpsub_d),
    "23 Homophonic":(False,homophonic_e,homophonic_d),"24 Chaocipher":(True,chaocipher_e,chaocipher_d),
    "25 Rail Fence":(True,railfence_e,railfence_d),"26 Columnar Transposition":(True,columnar_e,columnar_d),
    "27 Double Transposition":(True,doubletrans_e,doubletrans_d),"28 Reverse Words":(False,revwords_e,revwords_d),
    "29 Reverse Word Order":(False,revorder_e,revorder_d),"30 Reverse Each Line":(False,revlines_e,revlines_d),
    "31 Mirror":(False,mirror_e,mirror_d),"32 Word Scramble":(False,wordscramble_e,wordscramble_d),
    "33 Playfair":(True,playfair_e,playfair_d),"34 Four-Square":(True,foursquare_e,foursquare_d),
    "35 Bifid":(True,bifid_e,bifid_d),"36 Polybius Square":(False,polybius_e,polybius_d),
    "37 Bacon Cipher":(False,bacon_e,bacon_d),"38 Hill 2x2":(True,hill_e,hill_d),
    "39 One-Time Pad":(True,otp_e,otp_d),"40 Enigma (3-rotor)":(True,enigma_e,enigma_d),
    "41 XOR decimal":(True,xor_e,xor_d),"42 XOR hex":(True,xorhex_e,xorhex_d),
    "43 Base64":(False,b64_e,b64_d),"44 Base32":(False,b32_e,b32_d),
    "45 Base16 / Hex":(False,b16_e,b16_d),"46 Base58":(False,b58_e,b58_d),
    "47 Base85":(False,b85_e,b85_d),"48 ASCII Codes":(False,ascii_e,ascii_d),
    "49 Binary":(False,binary_e,binary_d),"50 Octal":(False,octal_e,octal_d),
    "51 URL Encode":(False,url_e,url_d),"52 HTML Entities":(False,html_e,html_d),
    "53 Unicode Escape":(False,unicode_e,unicode_d),"54 Morse Code":(False,morse_e,morse_d),
    "55 Braille":(False,braille_e,braille_d),"56 Tap Code":(False,tap_e,tap_d),
    "57 Pigpen":(False,pigpen_e,pigpen_d),"58 Null Cipher":(False,null_e,null_d),
    "59 Pig Latin":(False,piglatin_e,piglatin_d),"60 Flip Upside-Down":(False,flip_e,flip_d),
    "61 Full-Width":(False,fullwidth_e,fullwidth_d),"62 Discord Spoiler":(False,spoiler_e,spoiler_d),
    "63 Zalgo":(True,zalgo_e,zalgo_d),"64 Zlib+Base64":(False,zlibcomp_e,zlibcomp_d),
    "65 CRC32":(False,crc32_e,crc32_d),
}
HASHES = {
    "H01 MD5":hash_md5,"H02 SHA-1":hash_sha1,"H03 SHA-224":hash_sha224,
    "H04 SHA-256":hash_sha256,"H05 SHA-384":hash_sha384,"H06 SHA-512":hash_sha512,
    "H07 SHA3-256":hash_sha3_256,"H08 SHA3-512":hash_sha3_512,
    "H09 BLAKE2b":hash_blake2b,"H10 BLAKE2s":hash_blake2s,
}
CIPHER_NAMES = list(CIPHERS.keys())
HASH_NAMES   = list(HASHES.keys())

# ═══════════════════════════════════════════════════════════════════════════════
#  CUSTOM WIDGETS
# ═══════════════════════════════════════════════════════════════════════════════

class StyledSpinnerOption(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        th = T()
        self.background_normal = ''
        self.background_color  = th["btn2"]
        self.color             = th["fg"]
        self.font_size         = sp(13)
        self.size_hint_y       = None
        self.height            = dp(44)


def lbl(text, size=sp(13), color=None, bold=False, halign='left'):
    th = T()
    l = Label(
        text=text, font_size=size,
        color=color or th["fg"],
        bold=bold, halign=halign, valign='middle',
        size_hint_y=None, height=dp(30),
    )
    l.bind(size=lambda i,v: setattr(i,'text_size',(v[0],None)))
    return l


def btn(text, bg=None, fg=None, h=dp(44), fs=sp(14)):
    th = T()
    b = Button(
        text=text, font_size=fs,
        color=fg or th["fg"],
        background_normal='',
        background_color=bg or th["accent"],
        size_hint_y=None, height=h,
    )
    return b


def inp(hint='', ml=False, h=dp(44)):
    th = T()
    return TextInput(
        hint_text=hint, multiline=ml,
        background_color=th["input"],
        foreground_color=th["fg"],
        hint_text_color=th["sub"],
        cursor_color=th["accent"],
        font_size=sp(14),
        size_hint_y=None, height=h,
        padding=[dp(8), dp(8)],
    )


def spinner(vals, cur):
    th = T()
    s = Spinner(
        text=cur, values=vals,
        font_size=sp(13),
        color=th["fg"],
        background_normal='',
        background_color=th["btn"],
        size_hint_y=None, height=dp(44),
        option_cls=StyledSpinnerOption,
    )
    return s

# ═══════════════════════════════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════════════════════════════

class Pay2BrickApp(App):

    def build(self):
        self.title      = "pay 2 brick"
        self._hash_mode = False
        self._enc_mode  = True

        Window.clearcolor = T()["bg"]
        Window.bind(on_resize=lambda *_: Clock.schedule_once(lambda dt: self._apply_layout(), 0.05))

        root = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(6))
        root.add_widget(self._mk_header())

        self._content = BoxLayout(spacing=dp(8))
        self._left_scroll, self._left_inner = self._mk_left()
        self._right = self._mk_right()
        self._content.add_widget(self._left_scroll)
        self._content.add_widget(self._right)
        root.add_widget(self._content)

        self._apply_layout()
        return root

    # ── header ────────────────────────────────────────────────────────────────
    def _mk_header(self):
        th = T()
        h = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))

        title = Label(
            text="[b][color=e63946]pay 2 brick[/color][/b]",
            markup=True, font_size=sp(21),
            size_hint_x=0.45, halign='left', valign='middle',
        )
        title.bind(size=lambda i,v: setattr(i,'text_size',(v[0],None)))

        sub = Label(
            text=f"[color=666688]{len(CIPHERS)} ciphers · {len(HASHES)} hashes[/color]",
            markup=True, font_size=sp(11),
            size_hint_x=0.35, halign='left', valign='middle',
        )
        sub.bind(size=lambda i,v: setattr(i,'text_size',(v[0],None)))

        self._theme_btn = btn("☀ Light", bg=th["btn"], h=dp(36), fs=sp(12))
        self._theme_btn.size_hint_x = None
        self._theme_btn.width = dp(88)
        self._theme_btn.bind(on_release=self._toggle_theme)

        h.add_widget(title)
        h.add_widget(sub)
        h.add_widget(Widget())
        h.add_widget(self._theme_btn)
        return h

    # ── left panel ────────────────────────────────────────────────────────────
    def _mk_left(self):
        th = T()
        scroll = ScrollView()
        inner  = BoxLayout(orientation='vertical', padding=dp(10),
                           spacing=dp(7), size_hint_y=None)
        inner.bind(minimum_height=inner.setter('height'))

        # Mode
        inner.add_widget(lbl("Mode", size=sp(11), color=th["sub"]))
        mrow = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        self._enc_btn = btn("Encode", bg=th["accent"])
        self._dec_btn = btn("Decode", bg=th["btn"])
        self._enc_btn.bind(on_release=lambda _: self._set_mode(True))
        self._dec_btn.bind(on_release=lambda _: self._set_mode(False))
        mrow.add_widget(self._enc_btn); mrow.add_widget(self._dec_btn)
        inner.add_widget(mrow)

        # Arrow
        self._arrow = lbl("▼", size=sp(20), color=th["sub"], halign='center')
        self._arrow.height = dp(26)
        inner.add_widget(self._arrow)

        # Cipher
        inner.add_widget(lbl("Cipher / Algorithm", size=sp(11), color=th["sub"]))
        self._cipher_sp = spinner(CIPHER_NAMES, CIPHER_NAMES[0])
        self._cipher_sp.bind(text=self._on_cipher_change)
        inner.add_widget(self._cipher_sp)

        # Key (hidden by default)
        self._key_lbl = lbl("▼  Key required", color=th["accent"])
        self._key_lbl.height = 0; self._key_lbl.opacity = 0
        self._key_inp = inp("Enter key here…")
        self._key_inp.height = 0; self._key_inp.opacity = 0
        inner.add_widget(self._key_lbl)
        inner.add_widget(self._key_inp)

        # Divider
        div = Widget(size_hint_y=None, height=dp(1))
        with div.canvas: Color(*th["border"]); Rectangle(pos=div.pos, size=div.size)
        div.bind(pos=lambda i,_: self._redraw_div(i), size=lambda i,_: self._redraw_div(i))
        self._div = div
        inner.add_widget(div)

        # Hash toggle
        hrow = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        hrow.add_widget(Label(text="⬤", font_size=sp(12), color=th["sub"],
                              size_hint_x=None, width=dp(22)))
        self._hash_btn = btn("HASH MODE", bg=th["btn"])
        self._hash_btn.bind(on_release=self._toggle_hash)
        hrow.add_widget(self._hash_btn)
        inner.add_widget(hrow)

        scroll.add_widget(inner)
        return scroll, inner

    def _redraw_div(self, w):
        w.canvas.clear()
        with w.canvas: Color(*T()["border"]); Rectangle(pos=w.pos, size=w.size)

    # ── right panel ───────────────────────────────────────────────────────────
    def _mk_right(self):
        th = T()
        p = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(7))

        p.add_widget(lbl("INPUT", size=sp(11), color=th["sub"], bold=True))

        self._in_box = TextInput(
            hint_text="Type or paste your text here…",
            multiline=True,
            background_color=th["input"], foreground_color=th["fg"],
            hint_text_color=th["sub"], cursor_color=th["accent"],
            font_size=sp(14), size_hint_y=1,
        )
        p.add_widget(self._in_box)

        start = btn("▶  START", h=dp(52), fs=sp(16))
        start.bold = True
        start.bind(on_release=self._run)
        p.add_widget(start)

        p.add_widget(lbl("OUTPUT", size=sp(11), color=th["sub"], bold=True))

        self._out_box = TextInput(
            hint_text="Result will appear here…",
            multiline=True, readonly=True,
            background_color=th["input"], foreground_color=th["fg"],
            hint_text_color=th["sub"], cursor_color=th["accent"],
            font_size=sp(14), size_hint_y=1,
        )
        p.add_widget(self._out_box)
        return p

    # ── responsive ────────────────────────────────────────────────────────────
    def _apply_layout(self):
        w, h = Window.size
        if w >= h:                          # LANDSCAPE — side by side
            self._content.orientation = 'horizontal'
            self._left_scroll.size_hint  = (None, 1)
            self._left_scroll.width      = dp(280)
            self._right.size_hint        = (1, 1)
        else:                               # PORTRAIT — stacked
            self._content.orientation = 'vertical'
            self._left_scroll.size_hint  = (1, None)
            self._left_scroll.height     = dp(300)
            self._right.size_hint        = (1, 1)

    # ── events ────────────────────────────────────────────────────────────────
    def _set_mode(self, encode):
        self._enc_mode = encode
        th = T()
        self._enc_btn.background_color = th["accent"] if encode else th["btn"]
        self._dec_btn.background_color = th["btn"] if encode else th["accent"]

    def _on_cipher_change(self, sp_, value):
        needs_key = CIPHERS.get(value, (False,None,None))[0]
        th = T()
        if needs_key:
            self._key_lbl.height  = dp(28); self._key_lbl.opacity  = 1
            self._key_inp.height  = dp(44); self._key_inp.opacity  = 1
            self._arrow.text      = "▼  key needed"
            self._arrow.color     = th["accent"]
        else:
            self._key_lbl.height  = 0; self._key_lbl.opacity  = 0
            self._key_inp.height  = 0; self._key_inp.opacity  = 0
            self._arrow.text      = "▼"
            self._arrow.color     = th["sub"]

    def _toggle_hash(self, *_):
        self._hash_mode = not self._hash_mode
        th = T()
        if self._hash_mode:
            self._hash_btn.background_color = th["accent"]
            self._hash_btn.text             = "CIPHER MODE"
            self._cipher_sp.values          = HASH_NAMES
            self._cipher_sp.text            = HASH_NAMES[0]
            self._enc_btn.disabled = True
            self._dec_btn.disabled = True
            self._key_lbl.height = 0; self._key_lbl.opacity = 0
            self._key_inp.height = 0; self._key_inp.opacity = 0
        else:
            self._hash_btn.background_color = th["btn"]
            self._hash_btn.text             = "HASH MODE"
            self._cipher_sp.values          = CIPHER_NAMES
            self._cipher_sp.text            = CIPHER_NAMES[0]
            self._enc_btn.disabled = False
            self._dec_btn.disabled = False
            self._on_cipher_change(None, CIPHER_NAMES[0])

    def _toggle_theme(self, *_):
        STATE["dark"] = not STATE["dark"]
        th = T()
        Window.clearcolor = th["bg"]
        self._theme_btn.text             = "☀ Light" if STATE["dark"] else "🌙 Dark"
        self._theme_btn.background_color = th["btn"]
        for box in [self._in_box, self._out_box]:
            box.background_color = th["input"]
            box.foreground_color = th["fg"]
            box.hint_text_color  = th["sub"]

    def _run(self, *_):
        text = self._in_box.text.strip()
        if not text:
            self._out_box.text = "[No input provided]"; return

        name = self._cipher_sp.text
        key  = self._key_inp.text.strip()

        try:
            if self._hash_mode and name in HASHES:
                result = HASHES[name](text, key)
            else:
                info = CIPHERS.get(name)
                if not info:
                    result = "[Unknown algorithm]"
                else:
                    _, enc_fn, dec_fn = info
                    if self._enc_mode:
                        result = enc_fn(text, key)
                    else:
                        result = dec_fn(text, key) if dec_fn else "[One-way — cannot decode]"
        except Exception as e:
            result = f"[Error: {e}]"

        self._out_box.text = result


if __name__ == "__main__":
    Pay2BrickApp().run()
