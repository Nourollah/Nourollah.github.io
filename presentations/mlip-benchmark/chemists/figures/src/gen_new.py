import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
pre=open('preamble.tex').read()
def doc(b): return pre+"\n\\begin{document}\n"+b+"\n\\end{document}\n"
def co(pts): return " ".join(f"({x:.3f},{y:.3f})" for x,y in pts)

# ---------- generalisation_scatter ----------
rng=np.random.default_rng(193)
def sample(n):
    a=rng.normal([3.6,6.0],[1.3,1.2],(n,2)); b=rng.normal([6.2,3.8],[1.25,1.3],(n,2))
    return a,b
A,B=sample(22); TA,TB=sample(9)
X=np.vstack([A,B]); y=np.r_[np.zeros(len(A)),np.ones(len(B))]
def nn(P):
    d=((P[:,None,:]-X[None,:,:])**2).sum(-1); return y[d.argmin(1)]
lin=lambda P: (P[:,0]-P[:,1]>0).astype(float)   # boundary y=x
g=np.linspace(0,10,500); GX,GY=np.meshgrid(g,g)
Z=nn(np.c_[GX.ravel(),GY.ravel()]).reshape(GX.shape)
cs=plt.contour(GX,GY,Z,levels=[0.5]); segs=cs.allsegs[0]
segs=[s[::3] for s in segs if len(s)>20]
T=np.vstack([TA,TB]); ty=np.r_[np.zeros(len(TA)),np.ones(len(TB))]
wrong_nn=(nn(T)!=ty); wrong_lin=(lin(T)!=ty)
print("train err lin",(lin(X)!=y).sum(),"test wrong nn",wrong_nn.sum(),"test wrong lin",wrong_lin.sum())
def panel(xoff, boundary, wrong, title, sub, col):
    o=[]
    o.append(r"\begin{scope}[shift={(%.2f,0)}, scale=0.62]"%xoff)
    o.append(r"\draw[linec, line width=0.8pt] (0,0) rectangle (10,10);")
    o.append(boundary)
    for px,py in A: o.append(r"\fill[teal] (%.2f,%.2f) circle (0.17);"%(px,py))
    for px,py in B: o.append(r"\fill[plum] (%.2f,%.2f) +(-0.16,-0.16) rectangle +(0.16,0.16);"%(px,py))
    for (px,py),c,w in zip(T,ty,wrong):
        cc="teal" if c==0 else "plum"
        if c==0: o.append(r"\draw[%s, line width=1.3pt, fill=white] (%.2f,%.2f) circle (0.19);"%(cc,px,py))
        else: o.append(r"\draw[%s, line width=1.3pt, fill=white] (%.2f,%.2f) +(-0.18,-0.18) rectangle +(0.18,0.18);"%(cc,px,py))
        if w: o.append(r"\draw[amber, line width=2.2pt] (%.2f,%.2f) circle (0.42);"%(px,py))
    o.append(r"\end{scope}")
    o.append(r"\node[font=\bfseries, text=%s, anchor=south west] at (%.2f,6.35) {%s};"%(col,xoff,title))
    o.append(r"\node[font=\small, text=inksoft, anchor=north west, align=left] at (%.2f,-0.15) {%s};"%(xoff,sub))
    return "\n".join(o)
linb=r"\draw[ink, line width=2.2pt] (0.3,0.3) -- (9.7,9.7);"
nnb="\n".join(r"\draw[ink, line width=2pt] plot[smooth] coordinates {%s};"%co(s) for s in segs)
body=r"\begin{tikzpicture}"+"\n"+panel(0,linb,wrong_lin,"simple boundary",
  r"misses %d training points\\new points: %d wrong"%((lin(X)!=y).sum(),wrong_lin.sum()),"ink")+"\n"+panel(7.4,nnb,wrong_nn,"over-fitted boundary",
  r"every training point right\\new points: %d wrong"%wrong_nn.sum(),"amber")+r"""
\begin{scope}[shift={(0,-1.75)}]
\fill[teal] (0.15,0) circle (0.11); \fill[plum] (0.55,0) +(-0.1,-0.1) rectangle +(0.1,0.1);
\node[font=\footnotesize, text=inksoft, anchor=west] at (0.75,0) {training data};
\draw[teal, line width=1pt, fill=white] (3.4,0) circle (0.12); \draw[plum, line width=1pt, fill=white] (3.8,0) +(-0.11,-0.11) rectangle +(0.11,0.11);
\node[font=\footnotesize, text=inksoft, anchor=west] at (4.0,0) {new data};
\draw[amber, line width=1.6pt] (6.4,0) circle (0.2); \node[font=\footnotesize, text=inksoft, anchor=west] at (6.7,0) {wrongly classified};
\end{scope}
\end{tikzpicture}"""
open('generalisation_scatter.tex','w').write(doc(body))

# ---------- steep_wall (regression with hard slope) ----------
D,a,re=4.5,2.6,1.0
E=lambda r: D*(1-np.exp(-a*(r-re)))**2-D
rng=np.random.default_rng(5)
rs=np.sort(np.clip(rng.normal(1.05,0.12,40),0.82,1.6))
rs=np.r_[rs, rng.uniform(1.4,2.25,7)]; rs.sort()
Es=E(rs)
p=np.polyfit(rs,Es,3)
rr=np.linspace(0.6,2.3,300)
Et=E(rr)
r0=0.9; h=1e-4; s0=(E(r0+h)-E(r0-h))/(2*h)
Em=np.where(rr>=r0, E(rr), E(r0)+s0*(rr-r0)*0.55)
clip=lambda v: np.clip(v,-5.2,9.0)
body=r"""\begin{tikzpicture}
\begin{axis}[width=15cm,height=10cm,xmin=0.6,xmax=2.35,ymin=-5.4,ymax=6.4, axis lines=left,
 xlabel={bond length $r$ (\AA)}, ylabel={energy}, ytick=\empty, xtick={0.8,1.2,1.6,2.0,2.4}, clip=true]
\fill[ambersoft] (axis cs:0.6,-5.4) rectangle (axis cs:0.84,6.4);
\addplot[ink, line width=2.4pt] coordinates {"""+co(zip(rr,clip(Et)))+r"""};
\addplot[amber, line width=2.2pt, dashed] coordinates {"""+co(zip(rr,clip(Em)))+r"""};
\addplot[only marks, mark=*, mark size=2.8pt, mark options={fill=teal, draw=white, line width=0.6pt}] coordinates {"""+co(zip(rs,Es))+r"""};
\addplot[only marks, mark=|, mark size=5pt, teal, line width=1pt] coordinates {"""+co(zip(rs,np.full(len(rs),-5.1)))+r"""};
\node[font=\small\bfseries, text=amber, align=left, anchor=west] at (axis cs:0.86,5.6) {steep wall: few samples,\\[-1pt]model goes wrong};
\node[font=\small\bfseries, text=ink, anchor=west] at (axis cs:0.715,2.4) {true energy};
\node[font=\small\bfseries, text=amber, anchor=north] at (axis cs:0.7,-3.35) {model};
\node[font=\small\bfseries, text=teal, anchor=west] at (axis cs:1.2,-4.3) {training data};
\node[font=\footnotesize, text=teal, anchor=south west] at (axis cs:1.62,-5.15) {where the samples are};
\end{axis}
\end{tikzpicture}"""
open('steep_wall.tex','w').write(doc(body))

# ---------- reaction_ts ----------
x=np.linspace(-2.2,2.2,400)
def Et(x): return 6*np.exp(-x**2/0.18) - 5.0*np.exp(-(x+1.15)**2/0.35) - 6.5*np.exp(-(x-1.2)**2/0.35)
Etrue=Et(x)
Emod=Etrue-2.6*np.exp(-x**2/0.09)
# sample histogram: Boltzmann-ish density
w=np.exp(-(Etrue-Etrue.min())/1.1); w/=w.max()
bins=np.linspace(-2.2,2.2,45); cen=(bins[:-1]+bins[1:])/2
h=np.interp(cen,x,w); 
bars="\n".join(r"\fill[teal!55] (axis cs:%.3f,-9.2) rectangle (axis cs:%.3f,%.3f);"%(c-0.042,c+0.042,-9.2+3.0*v) for c,v in zip(cen,h))
ts=Et(0.0); tm=Emod[np.argmin(abs(x))]; rmin=Etrue[x<0].min()
body=r"""\begin{tikzpicture}
\begin{axis}[width=15cm,height=10.5cm,xmin=-2.2,xmax=2.2,ymin=-9.4,ymax=8.0, axis lines=left,
 xlabel={reaction coordinate}, ylabel={energy}, ytick=\empty, xtick=\empty, clip=false]
"""+bars+r"""
\node[font=\footnotesize, text=teal] at (axis cs:-0.1,-8.4) {how often MD visits each point};
\addplot[ink, line width=2.4pt] coordinates {"""+co(zip(x,Etrue))+r"""};
\addplot[amber, line width=2.2pt, dashed] coordinates {"""+co(zip(x,Emod))+r"""};
\node[font=\small\bfseries, text=ink] at (axis cs:-1.15,-5.6+0.4) {};
\node[font=\small\bfseries, text=ink, anchor=north] at (axis cs:-1.15,%.2f) {reactant};
\node[font=\small\bfseries, text=ink, anchor=west] at (axis cs:1.5,%.2f) {product};
\node[font=\small\bfseries, text=ink, anchor=south] at (axis cs:0,%.2f) {transition state};
\draw[ink!40, dashed] (axis cs:-1.15,%.2f) -- (axis cs:0.3,%.2f);
\draw[<->, ink, line width=1.3pt] (axis cs:-0.09,%.2f) -- (axis cs:-0.09,%.2f);
\draw[<->, amber, line width=1.3pt] (axis cs:0.09,%.2f) -- (axis cs:0.09,%.2f);
\draw[<->, ink, line width=1.3pt] (axis cs:-2.05,5.9) -- (axis cs:-2.05,7.3); \node[font=\small\bfseries, text=ink, anchor=west] at (axis cs:-2.0,6.6) {true barrier};
\draw[<->, amber, line width=1.3pt] (axis cs:-2.05,3.9) -- (axis cs:-2.05,5.1); \node[font=\small\bfseries, text=amber, anchor=west] at (axis cs:-2.0,4.5) {model barrier};
\node[font=\small\bfseries, text=ink, anchor=west] (tl) at (axis cs:0.72,6.3) {true energy};
\draw[->, ink, line width=1.1pt] (tl.west) -- (axis cs:0.2,4.62);
\node[font=\small\bfseries, text=amber, anchor=west] (ml) at (axis cs:0.72,4.6) {model};
\draw[->, amber, line width=1.1pt] (ml.west) -- (axis cs:0.155,2.98);
\end{axis}
\end{tikzpicture}"""%(rmin-0.3, Etrue[x>0].min()+0.2, ts+0.3, rmin,rmin, rmin,ts, rmin,tm)
open('reaction_ts.tex','w').write(doc(body))
