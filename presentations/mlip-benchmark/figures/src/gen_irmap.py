import numpy as np, math
pre=open('preamble.tex').read()
w=np.linspace(4000,500,1400)
bands=[(2984,22,28),(2940,14,22),(1742,92,14),(1447,22,16),(1373,40,12),(1240,98,20),(1047,70,16),(938,18,10),(847,15,10),(634,20,12)]
A=sum(a*(g**2/((w-c)**2+g**2)) for c,a,g in bands); T=100-np.clip(A,0,96)
co=" ".join(f"({a:.1f},{b:.2f})" for a,b in zip(w,T))
# molecule (ethyl acetate) coords in cm, origin shifted
s=1.3; ox,oy=7.6,6.9
P={"Cm":(0,0),"Cc":(0.866,0.5),"Od":(0.866,1.5),"Oe":(1.732,0),"Ca":(2.598,0.5),"Cb":(3.464,0)}
P={k:(ox+s*v[0],oy+s*v[1]) for k,v in P.items()}
def L(a,b,col="ink"): return r"\draw[%s, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(col,*P[a],*P[b])
o=[r"\begin{tikzpicture}"]
o.append(r"""\begin{axis}[name=ax, at={(0,0)}, width=19cm,height=6.2cm,x dir=reverse,xmin=500,xmax=4000,ymin=0,ymax=112,
  axis lines=left, xlabel={wavenumber (cm$^{-1}$)}, ylabel={transmittance (\%)},
  xtick={4000,3000,2000,1500,1000,500}, ytick={0,50,100}, clip=false]""")
for (lo,hi,col,name) in [(2880,3060,"teal","CH"),(1700,1785,"amber","CO"),(1000,1290,"plum","COC")]:
    o.append(r"\fill[%s, fill opacity=0.15] (axis cs:%d,0) rectangle (axis cs:%d,104);"%(col,hi,lo))
    o.append(r"\coordinate (b%s) at (axis cs:%.0f,104);"%(name,(lo+hi)/2))
o.append(r"\addplot[ink, line width=1.5pt] coordinates {"+co+"};")
o.append(r"\node[font=\small\bfseries, text=teal] at (axis cs:2970,60) {C--H};")
o.append(r"\node[font=\small\bfseries, text=amber, anchor=east] at (axis cs:1800,20) {C=O};")
o.append(r"\node[font=\small\bfseries, text=plum] at (axis cs:820,20) {C--O--C};")
o.append(r"\end{axis}")
# molecule highlights
o.append(r"\fill[teal, fill opacity=0.18] (%.3f,%.3f) circle (0.32);"%P["Cm"])
o.append(r"\fill[teal, fill opacity=0.18] (%.3f,%.3f) circle (0.32);"%P["Ca"])
o.append(r"\fill[teal, fill opacity=0.18] (%.3f,%.3f) circle (0.32);"%P["Cb"])
cx=(P["Cc"][0]+P["Od"][0])/2
o.append(r"\fill[amber, fill opacity=0.2, rounded corners=6pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"%(P["Cc"][0]-0.3,P["Cc"][1]+0.05,P["Cc"][0]+0.3,P["Od"][1]+0.32))
o.append(r"\fill[plum, fill opacity=0.18] (%.3f,%.3f) circle (0.36);"%P["Oe"])
for a,b in [("Cm","Cc"),("Cc","Oe"),("Oe","Ca"),("Ca","Cb")]: o.append(L(a,b))
vx,vy=0,1; o.append(r"\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(P["Cc"][0]-0.07,P["Cc"][1],P["Od"][0]-0.07,P["Od"][1]-0.15))
o.append(r"\draw[ink, line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(P["Cc"][0]+0.07,P["Cc"][1]+0.04,P["Od"][0]+0.07,P["Od"][1]-0.15))
o.append(r"\node[font=\bfseries, text=oxy, fill=white, inner sep=1pt] at (%.3f,%.3f) {O};"%P["Od"])
o.append(r"\node[font=\bfseries, text=oxy, fill=white, inner sep=1pt] at (%.3f,%.3f) {O};"%P["Oe"])
o.append(r"\node[font=\bfseries, text=ink, anchor=west] at (%.3f,%.3f) {ethyl acetate};"%(P["Cb"][0]+0.5,P["Cb"][1]+0.25))
# connectors
o.append(r"\draw[teal, dashed, line width=1.2pt, ->] (%.3f,%.3f) to[out=-150, in=90] (bCH);"%(P["Cm"][0]-0.3,P["Cm"][1]-0.1))
o.append(r"\draw[amber, dashed, line width=1.2pt, ->] (%.3f,%.3f) to[out=0, in=90] (bCO);"%(P["Od"][0]+0.35,P["Od"][1]))
o.append(r"\draw[plum, dashed, line width=1.2pt, ->] (%.3f,%.3f) to[out=-60, in=90] (bCOC);"%(P["Oe"][0]+0.2,P["Oe"][1]-0.3))
o.append(r"\node[font=\scriptsize, text=greyc, anchor=north east] at ([yshift=-0.75cm]ax.south east) {schematic; peak positions approximate};")
o.append(r"\end{tikzpicture}")
open('ir_mapped.tex','w').write(pre+"\n\\begin{document}\n"+"\n".join(o)+"\n\\end{document}\n")
