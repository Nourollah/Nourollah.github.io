import math
pre=open('preamble.tex').read()
V=[(math.cos(math.radians(a)),math.sin(math.radians(a))) for a in [0,60,120,180,240,300]]
ring="--".join("(%.3f,%.3f)"%v for v in V)+"--cycle"
inner=[]
for i in [1,3,5]:
    a,b=V[i],V[(i+1)%6]; s=0.78
    inner.append(r"\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(a[0]*s,a[1]*s,b[0]*s,b[1]*s))
N=(2.0,0.0); C=(2.5,0.866); O=(2.0,1.732); Me=(3.5,0.866); Oh=(-2.0,0.0)
def L(a,b): return r"\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(*a,*b)
# double bond C=O offset perpendicular
vx,vy=O[0]-C[0],O[1]-C[1]; l=math.hypot(vx,vy); px,py=-vy/l*0.07,vx/l*0.07
body=r"""\begin{tikzpicture}[scale=1.5]
\fill[plum, fill opacity=0.16, rounded corners=12pt] (-2.55,-0.42) rectangle (-1.55,0.42);
\fill[teal, fill opacity=0.16] (0,0) circle (1.3);
\fill[blue, fill opacity=0.16, rounded corners=12pt] (1.62,-0.75) rectangle (2.95,2.1);
\fill[greyc, fill opacity=0.22] (3.5,0.866) circle (0.38);
\draw[ink, line width=1.6pt] """+ring+";\n"+"\n".join(inner)+"\n"+L(V[0],(N[0]-0.18,N[1]))+L((N[0]+0.1,N[1]+0.17),C)+L(C,Me)+\
L((C[0]+px,C[1]+py),(O[0]+px*1+0.08,O[1]+py-0.14))+L((C[0]-px,C[1]-py),(O[0]-px+0.08,O[1]-py-0.14))+L(V[3],(Oh[0]+0.22,0))+r"""
\node[font=\large\bfseries, text=nit, inner sep=1pt] at (%.3f,%.3f) {N};
\node[font=\bfseries, text=nit] at (%.3f,%.3f) {H};
\node[font=\large\bfseries, text=oxy, inner sep=1pt] at (%.3f,%.3f) {O};
\node[font=\large\bfseries, text=oxy, inner sep=1pt, anchor=east] at (%.3f,%.3f) {HO};
\node[font=\small\bfseries, text=plum] at (-2.05,0.75) {hydroxyl (phenol)};
\node[font=\small\bfseries, text=teal] at (0,-1.6) {aromatic ring};
\node[font=\small\bfseries, text=blue] at (2.28,-1.05) {amide};
\node[font=\small\bfseries, text=inksoft] at (3.55,1.5) {methyl};
\node[font=\normalsize\bfseries, text=ink, anchor=west] at (-2.55,-2.2) {paracetamol};
\end{tikzpicture}"""%(N[0],N[1],N[0],N[1]-0.42,O[0],O[1],Oh[0]+0.27,Oh[1])
open('molecule_parts.tex','w').write(pre+"\n\\begin{document}\n"+body+"\n\\end{document}\n")
