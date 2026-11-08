import math
pre=open('preamble.tex').read()
def doc(b): return pre+"\n\\begin{document}\n"+b+"\n\\end{document}\n"

# ---------------- pipeline ----------------
steps=[("SMILES","e.g.\\ CCCCCC(=O)O (hexanoic acid)","inksoft"),
       ("3D structure","RDKit conformer","inksoft"),
       ("Molecular dynamics","300 K, vacuum (FlashMD); about 2000 snapshots","teal"),
       ("DFT labels","ORCA, PBE/def2-TZVP + D3BJ: energy and forces","blue")]
b=[r"\begin{tikzpicture}[box/.style={draw=#1, line width=1.3pt, rounded corners=6pt, fill=#1!8, minimum width=10.8cm, minimum height=1.25cm, align=left, inner xsep=10pt}]"]
y=0
for k,(t,d,c) in enumerate(steps):
    b.append(r"\node[box=%s, anchor=west] (s%d) at (0,%.2f) {\textbf{\textcolor{%s}{%s}}\\[1pt]{\small\textcolor{inksoft}{%s}}};"%(c,k,y,c,t,d))
    b.append(r"\node[circle, fill=%s, text=white, font=\bfseries, minimum size=0.75cm] at (-0.65,%.2f) {%d};"%(c,y,k+1))
    if k: b.append(r"\draw[->, inksoft, line width=1.6pt] (s%d.south) -- (s%d.north);"%(k-1,k))
    y-=1.85
# small icons on right side of boxes
b.append(r"\begin{scope}[shift={(9.6,%.2f)}, scale=0.32] \draw[ink, line width=1.2pt] (0,0)--(0.87,0.5)--(1.73,0)--(2.6,0.5)--(3.46,0); \draw[ink, line width=1.2pt] (3.46,0)--(3.46,-0.9); \fill[oxy] (3.46,-1.0) circle (0.28); \end{scope}"%(-1.85*1))
b.append(r"\begin{scope}[shift={(9.3,%.2f)}] \draw[teal, line width=1.1pt] plot[smooth, domain=0:1.6, samples=40] (\x,{0.18*sin(\x*700)+0.07*sin(\x*2300)}); \end{scope}"%(-1.85*2))
b.append(r"\node[font=\small\bfseries, text=blue] at (10.1,%.2f) {$E$, $\mathbf{F}$};"%(-1.85*3))
# split step
ys=y
b.append(r"\node[draw=teal, line width=1.4pt, rounded corners=6pt, fill=teal!10, minimum width=5.15cm, minimum height=1.25cm, align=center, anchor=west, font=\small] (tr) at (0,%.2f) {\textbf{\textcolor{teal}{training molecules}}\\\textcolor{inksoft}{e.g.\ alcohols, aldehydes}};"%ys)
b.append(r"\node[draw=amber, line width=1.4pt, dashed, rounded corners=6pt, fill=amber!8, minimum width=5.15cm, minimum height=1.25cm, align=center, anchor=east, font=\small] (te) at (10.8,%.2f) {\textbf{\textcolor{amber}{unseen test molecules}}\\\textcolor{inksoft}{e.g.\ carboxylic acids}};"%ys)
b.append(r"\node[circle, fill=amber, text=white, font=\bfseries, minimum size=0.75cm] at (-0.65,%.2f) {5};"%ys)
b.append(r"\draw[->, inksoft, line width=1.6pt] (s3.south) -- ++(0,-0.3) -| (tr.north);")
b.append(r"\draw[->, inksoft, line width=1.6pt] (s3.south) -- ++(0,-0.3) -| (te.north);")
b.append(r"\node[font=\small\bfseries, text=ink, anchor=west, fill=white, inner sep=2pt] at (3.6,%.2f) {split by molecule};"%(ys+0.98))
b.append(r"\end{tikzpicture}")
open('gmd_pipeline.tex','w').write(doc("\n".join(b)))

# ---------------- families ----------------
fam=[("alkane","",""),("alcohol","","\\ce{OH}"),("aldehyde","","\\ce{CHO}"),("carboxylic acid","","\\ce{COOH}"),
     ("dicarboxylic acid","\\ce{HOOC}","\\ce{COOH}"),("diamine","\\ce{H2N}","\\ce{NH2}"),("amino acid","\\ce{H2N}","\\ce{COOH}")]
gc={"\\ce{OH}":"plum","\\ce{CHO}":"blue","\\ce{COOH}":"amber","\\ce{HOOC}":"amber","\\ce{H2N}":"teal","\\ce{NH2}":"teal"}
b=[r"\begin{tikzpicture}"]
for k,(name,L,R) in enumerate(fam):
    y=-k*1.05
    pts=[(1.9+0.55*i, y+(0.16 if i%2 else -0.16)) for i in range(6)]
    b.append(r"\draw[inksoft, line width=1.8pt] "+" -- ".join("(%.2f,%.2f)"%p for p in pts)+";")
    if L: b.append(r"\node[draw=%s, fill=%s!12, line width=1.2pt, rounded corners=4pt, font=\small\bfseries, text=%s, anchor=east, inner sep=3pt] at (%.2f,%.2f) {%s};"%(gc[L],gc[L],gc[L],pts[0][0]-0.08,pts[0][1],L)); 
    if R: b.append(r"\node[draw=%s, fill=%s!12, line width=1.2pt, rounded corners=4pt, font=\small\bfseries, text=%s, anchor=west, inner sep=3pt] at (%.2f,%.2f) {%s};"%(gc[R],gc[R],gc[R],pts[-1][0]+0.08,pts[-1][1],R))
    b.append(r"\node[font=\small, text=ink, anchor=west] at (6.6,%.2f) {%s};"%(y,name))
b.append(r"\node[font=\footnotesize, text=greyc, anchor=west] at (0.7,%.2f) {same carbon backbone, different groups at the ends (H, C, N, O only)};"%(-7*1.05+0.25))
b.append(r"\end{tikzpicture}")
open('gmd_families.tex','w').write(doc("\n".join(b)))
