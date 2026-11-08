pre=open('preamble.tex').read()
def doc(body): return pre+"\n\\begin{document}\n"+body+"\n\\end{document}\n"
F={}

# ---------------- molecule_as_data ----------------
atoms=[("C",1.1879,-0.3829,0.0),("C",0.0,0.5526,0.0),("O",-1.1867,-0.2472,0.0),("H",-1.9237,0.3850,0.0),
       ("H",2.0985,0.2306,0.0),("H",1.1184,-1.0093,0.8869),("H",1.1184,-1.0093,-0.8869),("H",0.0563,1.1972,0.8770),("H",0.0563,1.1972,-0.8770)]
bonds=[(0,1),(1,2),(2,3),(0,4),(0,5),(0,6),(1,7),(1,8)]
sc=1.55
P=[(sc*(x+0.42*z), sc*(y+0.30*z)) for _,x,y,z in atoms]
col={"C":"carb","O":"oxy","H":"hyd"}; rad={"C":0.36,"O":0.34,"H":0.22}
xyz="\\\\[-1pt]".join([r"\texttt{9}",r"\texttt{\color{greyc}ethanol}"]+[r"\texttt{%s\ \ %7.3f %7.3f %7.3f}"%(e,x,y,z) for e,x,y,z in atoms]).replace(" ","~")
xyz=xyz.replace("\\texttt{","\\texttt{").replace("~"," ") 
rows=[r"\texttt{9}",r"\texttt{\textcolor{greyc}{ethanol}}"]+[r"\texttt{%s%s%s%s}"%(e, *[("~"*(9-len(f"{v:.3f}")))+f"{v:.3f}" for v in (x,y,z)]) for e,x,y,z in atoms]
xyz=r"\\[1pt]".join(rows)
order=sorted(range(len(atoms)), key=lambda i: atoms[i][3])  # back to front
draw=[]
for i,j in bonds:
    draw.append(r"\draw[inksoft!80, line width=3.2pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[i],*P[j]))
for i in order:
    e=atoms[i][0]; x,y=P[i]
    draw.append(r"\shade[ball color=%s, draw=ink!60, line width=0.4pt] (%.3f,%.3f) circle (%.2f);"%(col[e],x,y,rad[e]))
    if e!="H": draw.append(r"\node[font=\footnotesize\bfseries, text=white] at (%.3f,%.3f) {%s};"%(x,y,e))
forces=[(2,(-0.55,-0.75)),(4,(0.8,0.25)),(7,(0.25,0.85)),(5,(0.5,-0.6))]
for i,(dx,dy) in forces:
    x,y=P[i]; draw.append(r"\draw[amber, line width=1.8pt, -{Stealth[length=8pt]}] (%.3f,%.3f) -- ++(%.2f,%.2f);"%(x,y,dx,dy))
ox,oy=P[2]
body=r"""\begin{tikzpicture}
\node[draw=linec, fill=white, rounded corners=4pt, inner sep=9pt, align=left, font=\small, text=ink] (xyz) at (-8.4,0) {"""+xyz+r"""};
\node[font=\small\bfseries, text=teal, anchor=south west] at (xyz.north west) {input: elements + positions};
\draw[->, teal, line width=1.6pt] ($(xyz.east)+(0.2,0)$) -- ($(xyz.east)+(1.0,0)$);
\begin{scope}
\draw[teal, dashed, line width=1.2pt, fill=tealsoft, fill opacity=0.55] (%.3f,%.3f) circle (2.15);
"""%(ox,oy)+"\n".join(draw)+r"""
\node[font=\small, text=teal, align=center] at (%.3f,%.3f) {neighbourhood\\of O (cut-off)};
\node[font=\small\bfseries, text=amber, align=left, anchor=west] at (2.4,-2.3) {force $\mathbf{F}_i$\\[-1pt]{\mdseries on each atom}};
\end{scope}
\node[font=\small\bfseries, text=ink, anchor=south] at (0,3.3) {output: energy $E$ and forces $\mathbf{F}_i=-\partial E/\partial \mathbf{r}_i$};
\end{tikzpicture}"""%(ox-0.4,oy-2.7)
F['molecule_as_data']=doc(body)

# ---------------- methods_ladder ----------------
rungs=[("force fields","fitted classical functions"),("semi-empirical","PM6, GFN2-xTB"),("Hartree--Fock","mean-field, no correlation"),("DFT","B3LYP, \\(\\omega\\)B97X-D, \\dots"),("MP2","perturbative correlation"),("CCSD(T)","the ``gold standard''")]
body=[r"\begin{tikzpicture}",r"\draw[ink!70, line width=2.4pt] (0,-0.4) -- (0,7.0); \draw[ink!70, line width=2.4pt] (5.2,-0.4) -- (5.2,7.0);"]
for k,(n,d) in enumerate(rungs):
    y=k*1.3+0.2
    c=["greyc","inksoft","blue","teal","plum","amber"][k]
    body.append(r"\draw[ink!70, line width=2.4pt] (0,%.2f) -- (5.2,%.2f);"%(y,y))
    body.append(r"\node[fill=white, draw=%s, line width=1.3pt, rounded corners=5pt, minimum width=3.9cm, minimum height=0.82cm, font=\bfseries, text=%s] (r%d) at (2.6,%.2f) {%s};"%(c,c,k,y,n))
    body.append(r"\node[font=\small, text=inksoft, anchor=west] at (5.6,%.2f) {%s};"%(y,d))
body.append(r"\draw[teal, line width=2pt, ->] (-1.1,-0.2) -- (-1.1,6.9) node[midway, rotate=90, above, font=\bfseries, text=teal] {typically more accurate};")
body.append(r"\draw[amber, line width=2pt, ->] (-2.1,-0.2) -- (-2.1,6.9) node[midway, rotate=90, above, font=\bfseries, text=amber] {more time and resources};")
body.append(r"% To mark the GMD reference level, uncomment and set the rung (r0 ... r5):")
body.append(r"% \node[fill=teal, text=white, font=\small\bfseries, rounded corners=3pt, anchor=east] at ($(r3.west)+(-0.15,0)$) {GMD data};")
body.append(r"\end{tikzpicture}")
F['methods_ladder']=doc("\n".join(body))

# ---------------- ml_where ----------------
body=r"""\begin{tikzpicture}
\draw[->, ink, line width=1.4pt] (0,0) -- (12.2,0); \node[font=\small, text=ink] at (6,-0.55) {cost per calculation};
\draw[->, ink, line width=1.4pt] (0,0) -- (0,8.2);
\node[font=\small, text=ink, rotate=90] at (-0.9,4.0) {typical error};
\node[font=\footnotesize, text=greyc, anchor=north west] at (0,-0.05) {cheap};
\node[font=\footnotesize, text=greyc, anchor=north east] at (12,-0.05) {expensive};
\node[font=\footnotesize, text=greyc, anchor=east] at (-0.1,0.3) {small};
\node[font=\footnotesize, text=greyc, anchor=east] at (-0.1,7.8) {large};
\fill[greyc, fill opacity=0.18] (1.6,6.6) ellipse (1.3 and 0.9); \node[font=\small\bfseries, text=inksoft] at (1.6,6.6) {force fields};
\fill[inksoft, fill opacity=0.15] (3.9,4.9) ellipse (1.5 and 0.95); \node[font=\small\bfseries, text=inksoft, align=center] at (3.9,4.9) {semi-empirical\\[-2pt]{\footnotesize\mdseries PM6, GFN2-xTB}};
\fill[blue, fill opacity=0.14] (6.8,4.1) ellipse (1.1 and 0.75); \node[font=\small\bfseries, text=blue] at (6.8,4.1) {HF};
\fill[teal, fill opacity=0.18] (7.7,2.4) ellipse (1.5 and 0.85); \node[font=\small\bfseries, text=teal] at (7.7,2.4) {DFT};
\fill[plum, fill opacity=0.15] (9.4,1.6) ellipse (1.0 and 0.6); \node[font=\small\bfseries, text=plum] at (9.4,1.6) {MP2};
\fill[amber, fill opacity=0.15] (10.9,0.8) ellipse (1.05 and 0.55); \node[font=\small\bfseries, text=amber] at (10.9,0.8) {CCSD(T)};
\node[circle, draw=amber, line width=2.2pt, dashed, minimum size=1.55cm, font=\fontsize{34}{34}\selectfont\bfseries, text=amber, fill=white] at (2.4,2.2) {?};
\node[font=\small\bfseries, text=amber] at (2.4,1.05) {machine learning};
\end{tikzpicture}"""
F['ml_where']=doc(body)

# ---------------- fragment-based schematics ----------------
fragA=r"\ring"; fragB=r"\ce{C=O}"; fragC=r"\ce{NH2}"
def frag(name,pos,col,content): return r"\frag{%s}{%s}{%s}{%s}"%(name,pos,col,content)

# scaffold_split
body=r"""\begin{tikzpicture}
\node[font=\bfseries, text=teal, anchor=west] at (-0.6,3.05) {training: the model sees these molecules};
"""+frag("a1","0.6,1.8","teal",fragA)+frag("b1","2.4,1.8","blue",fragB)+r"\bond{a1}{b1}"+"\n"+\
frag("b2","5.2,1.8","blue",fragB)+frag("c2","7.0,1.8","plum",fragC)+r"\bond{b2}{c2}"+"\n"+\
frag("a3","9.8,1.8","teal",fragA)+frag("a4","11.6,1.8","teal",fragA)+r"\bond{a3}{a4}"+r"""
\draw[linec, line width=1pt] (-0.6,0.5) -- (12.6,0.5);
\node[font=\bfseries, text=amber, anchor=west] at (-0.6,-0.15) {test: same parts, joined in a new way};
"""+frag("a5","4.0,-1.45","teal",fragA)+frag("c5","5.8,-1.45","plum",fragC)+r"\bond{a5}{c5}"+r"""
\node[draw=amber, line width=1.8pt, dashed, rounded corners=9pt, fit=(a5)(c5), inner sep=7pt] (box) {};
\node[font=\small, text=inksoft, anchor=west, align=left] at (7.2,-1.45) {every part is familiar\\only the connection is new};
\end{tikzpicture}"""
F['scaffold_split']=doc(body)

# overview_teaser
body=r"""\begin{tikzpicture}
\node[font=\bfseries, text=ink] at (1.5,3.4) {known molecules};
"""+frag("a1","0.6,2.2","teal",fragA)+frag("b1","2.4,2.2","blue",fragB)+r"\bond{a1}{b1}"+"\n"+\
frag("b2","0.6,0.4","blue",fragB)+frag("c2","2.4,0.4","plum",fragC)+r"\bond{b2}{c2}"+r"""
\draw[->, inksoft, line width=1.8pt] (3.6,1.3) -- (4.7,1.3);
\node[font=\bfseries, text=ink] at (6.15,3.4) {known parts};
"""+frag("a","5.5,2.2","teal",fragA)+frag("b","6.8,2.2","blue",fragB)+frag("c","6.15,0.4","plum",fragC)+r"""
\draw[->, inksoft, line width=1.8pt] (7.6,1.3) -- (8.7,1.3);
\node[font=\bfseries, text=amber] at (11.0,3.4) {a new molecule};
"""+frag("a3","9.7,1.3","teal",fragA)+frag("c3","11.3,1.3","plum",fragC)+frag("b3","12.9,1.3","blue",fragB)+r"\bond{a3}{c3}\bond{c3}{b3}"+r"""
\node[draw=amber, line width=1.8pt, dashed, rounded corners=9pt, fit=(a3)(b3), inner sep=8pt] (nb) {};
\node[circle, fill=amber, text=white, font=\Large\bfseries, minimum size=0.95cm] at ($(nb.north east)+(-0.1,0.05)$) {?};
\end{tikzpicture}"""
F['overview_teaser']=doc(body)

# chemist_vs_model
import math, random
random.seed(3)
pts=[(0,0),(1.0,0.55),(1.95,0.05),(1.0,1.65),(-0.95,0.6),(-1.9,0.05),(-0.95,-0.55),(1.0,-0.6),(2.9,0.5),(0.1,2.4),(-2.8,0.55),(-0.9,-1.6),(2.0,-1.0)]
S=1.0; cx,cy=10.6,1.35
P2=[(cx+S*x,cy+S*y) for x,y in pts]
dots="\n".join(r"\fill[%s] (%.2f,%.2f) circle (%.2f);"%("carb" if k<8 else "greyc",x,y,0.24 if k<8 else 0.15) for k,(x,y) in enumerate(P2))
dl=[]
for k,lab,pos in [(1,"1.39","above left"),(6,"1.43","below right"),(3,"2.42","right")]:
    x,y=P2[k]
    dl.append(r"\draw[teal, line width=1.1pt, dashed] (%.2f,%.2f) -- (%.2f,%.2f) node[pos=0.55, %s, font=\footnotesize, text=teal, inner sep=2pt] {%s\,\AA};"%(P2[0][0],P2[0][1],x,y,pos,lab))
body=r"""\begin{tikzpicture}
\node[font=\bfseries, text=ink] at (2.6,4.45) {a chemist sees parts};
\node[draw=teal, fill=teal!12, line width=1.4pt, rounded corners=6pt, minimum width=2.2cm, minimum height=1.1cm, text=teal, font=\bfseries\small, align=center] (r) at (2.6,1.4) {aromatic\\ring};
\node[draw=blue, fill=blue!12, line width=1.4pt, rounded corners=6pt, minimum width=1.9cm, minimum height=1.1cm, text=blue, font=\bfseries\small] (am) at (5.1,1.4) {amide};
\node[draw=plum, fill=plum!12, line width=1.4pt, rounded corners=6pt, minimum width=1.9cm, minimum height=1.1cm, text=plum, font=\bfseries\small] (oh) at (0.1,1.4) {hydroxyl};
\node[draw=greyc, fill=greyc!15, line width=1.4pt, rounded corners=6pt, minimum width=1.6cm, minimum height=1.1cm, text=inksoft, font=\bfseries\small] (me) at (5.1,3.0) {methyl};
\bond{oh}{r}\bond{r}{am}\bond{am}{me}
\node[font=\small, text=inksoft, align=center] at (2.6,-0.6) {each part brings known behaviour};
\draw[linec, line width=1pt] (7.0,-1.0) -- (7.0,4.6);
\node[font=\bfseries, text=ink] at (10.4,4.45) {a model sees atoms and distances};
"""+"\n".join(dl)+"\n"+dots+r"""
\node[circle, fill=amber, text=white, font=\Large\bfseries, minimum size=0.9cm] at (13.6,3.7) {?};
\node[font=\small, text=inksoft, align=center] at (10.4,-0.6) {are the parts in there anywhere?};
\end{tikzpicture}"""
F['chemist_vs_model']=doc(body)

# ood_map
body=r"""\begin{tikzpicture}
\draw[linec, line width=1pt, rounded corners=10pt] (-6.2,-4.0) rectangle (6.2,4.0);
\node[font=\small, text=greyc, anchor=north] at (0,3.9) {chemical space (schematic)};
\fill[teal, fill opacity=0.2] plot[smooth cycle, tension=0.8] coordinates {(-3.3,0.9) (-2.2,1.9) (-0.9,1.3) (-0.8,-0.2) (-2.0,-1.1) (-3.4,-0.5)};
\fill[teal, fill opacity=0.2] plot[smooth cycle, tension=0.8] coordinates {(0.9,0.6) (2.1,1.6) (3.3,1.0) (3.2,-0.6) (2.0,-1.2) (0.8,-0.5)};
\node[font=\bfseries, text=teal] at (-2.1,0.25) {training};
\node[font=\bfseries, text=teal] at (2.05,0.2) {training};
\foreach \x/\y/\lx/\ly/\t/\a in {-1.7/1.6/-3.8/3.1/high energy\\[-2pt]distorted geometries/south, 2.4/1.5/3.9/3.1/high-temperature\\[-2pt]MD/south, -2.8/-0.9/-4.2/-3.1/elements never\\[-2pt]seen in training/north, 2.6/-1.0/4.0/-3.1/a different\\[-2pt]property/north}{
  \draw[->, inksoft, line width=1.5pt] (\x,\y) -- (\lx,\ly);
  \node[font=\small, text=inksoft, align=center, anchor=\a] at (\lx,\ly) {\t};
}
\draw[->, inksoft, line width=1.5pt] (-3.35,0.2) -- (-4.25,0.2);
\node[font=\small, text=inksoft, align=center, anchor=east] at (-4.3,0.2) {rare events\\[-2pt]transition\\[-2pt]states};
\node[circle, fill=amber, minimum size=0.42cm, inner sep=0] (n) at (-0.05,0.25) {};
\draw[->, amber, line width=1.7pt] (0.0,-2.4) -- (n.south);
\node[font=\small\bfseries, text=amber, align=center, anchor=north] at (0.0,-2.4) {a new combination\\[-2pt]of known parts};
\end{tikzpicture}"""
F['ood_map']=doc(body)

# universal_models
mols=[("water","\\ce{H2O}"),("ethanol","\\ce{C2H5OH}"),("benzene","\\ce{C6H6}"),("glycine","\\ce{NH2CH2COOH}"),("pyridine","\\ce{C5H5N}"),("acetone","\\ce{(CH3)2CO}")]
body=[r"\begin{tikzpicture}"]
for k,(n,f) in enumerate(mols):
    y=4.0-k*1.15; c=["teal","blue","plum","teal","blue","plum"][k]
    body.append(r"\node[draw=%s, fill=%s!10, line width=1.2pt, rounded corners=5pt, minimum width=3.6cm, minimum height=0.8cm, font=\small, text=ink, anchor=east] (m%d) at (3.4,%.2f) {\textbf{%s}\ \ %s};"%(c,c,k,y,n,f))
    body.append(r"\draw[->, inksoft!80, line width=1.3pt] (m%d.east) to[out=0, in=180] (6.2,1.1);"%k)
body.append(r"\node[draw=ink, fill=ink, text=white, rounded corners=8pt, minimum width=3.2cm, minimum height=2.2cm, font=\bfseries, align=center] (u) at (7.8,1.1) {one universal\\model};")
body.append(r"\node[font=\footnotesize, text=inksoft, align=center] at (7.8,-0.6) {trained on millions\\of reference calculations};")
body.append(r"\draw[->, amber, line width=2pt] (u.east) -- ++(1.3,0);")
body.append(r"\node[draw=amber, line width=1.8pt, dashed, rounded corners=8pt, minimum width=2.6cm, minimum height=1.4cm, font=\bfseries, text=amber, align=center, anchor=west] at ($(u.east)+(1.45,0)$) {your new\\molecule?};")
body.append(r"\end{tikzpicture}")
F['universal_models']=doc("\n".join(body))

# molecule_parts: paracetamol skeletal
import math
R=1.0
V=[(R*math.cos(math.radians(a)),R*math.sin(math.radians(a))) for a in [0,60,120,180,240,300]]
ring="--".join("(%.3f,%.3f)"%v for v in V)+"--cycle"
inner=[]
for i in [1,3,5]:
    a,b=V[i],V[(i+1)%6]; s=0.78
    inner.append(r"\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(a[0]*s,a[1]*s,b[0]*s,b[1]*s))
N=(1.866,0.5); C=(2.732,0.0); O=(2.732,-1.0); Me=(3.598,0.5); Oh=(-1.866,0.5)
body=r"""\begin{tikzpicture}[scale=1.55]
\fill[plum, fill opacity=0.16, rounded corners=12pt] (-2.75,0.05) rectangle (-1.25,1.0);
\fill[teal, fill opacity=0.16] (0,0) circle (1.28);
\fill[blue, fill opacity=0.16, rounded corners=12pt] (1.4,-1.45) rectangle (3.15,1.02);
\fill[greyc, fill opacity=0.22] (3.62,0.55) circle (0.42);
\draw[ink, line width=1.6pt] """+ring+";\n"+"\n".join(inner)+r"""
\draw[ink, line width=1.6pt] (1,0) -- (%.3f,%.3f);
\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);
\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);
\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);
\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);
\draw[ink, line width=1.6pt] (-1,0) -- (%.3f,%.3f);
\node[fill=white, inner sep=1.5pt, font=\large\bfseries, text=nit] at (%.3f,%.3f) {N};
\node[font=\bfseries, text=nit, anchor=south] at (%.3f,%.3f) {H};
\node[fill=white, inner sep=1.5pt, font=\large\bfseries, text=oxy] at (%.3f,%.3f) {O};
\node[fill=white, inner sep=1.5pt, font=\large\bfseries, text=oxy] at (%.3f,%.3f) {HO};
\node[font=\small\bfseries, text=plum] at (-2.0,1.35) {hydroxyl (phenol)};
\node[font=\small\bfseries, text=teal] at (0,-1.6) {aromatic ring};
\node[font=\small\bfseries, text=blue] at (2.27,-1.75) {amide};
\node[font=\small\bfseries, text=inksoft] at (3.62,1.2) {methyl};
\node[font=\normalsize\bfseries, text=ink, anchor=west] at (-2.75,-2.25) {paracetamol};
\end{tikzpicture}"""%(N[0]-0.12,N[1]-0.07, N[0]+0.12,N[1]-0.07, C[0],C[1], C[0],C[1],Me[0],Me[1],
   C[0]-0.1,C[1]+0.05, O[0]-0.1,O[1]+0.2, C[0]+0.1,C[1]-0.06, O[0]+0.1,O[1]+0.2,
   Oh[0]+0.15,Oh[1]-0.09, N[0],N[1], N[0],N[1]+0.18, O[0],O[1], Oh[0]-0.12,Oh[1])
F['molecule_parts']=doc(body)

for k,v in F.items(): open(k+'.tex','w').write(v)
print(list(F))
