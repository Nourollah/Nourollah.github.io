import numpy as np
rng=np.random.default_rng(7)
# ---------- data for fits ----------
xd=np.sort(rng.uniform(0.3,5.9,14)); yd=np.sin(xd)+rng.normal(0,0.13,xd.size)
def coords(x,y): return " ".join(f"({a:.5g},{b:.5g})" for a,b in zip(x,y))
pre=open('preamble.tex').read()

# fit_example
p=np.polyfit(xd,yd,5); xs=np.linspace(0,6.2,200)
tex=pre+r"""
\begin{document}
\begin{tikzpicture}
\begin{axis}[width=15cm,height=10cm,xmin=0,xmax=6.2,ymin=-1.6,ymax=1.7,
  xlabel={input $x$ (e.g.\ concentration)}, ylabel={output $y$ (e.g.\ absorbance)},
  axis lines=left, ticks=none, clip=false]
\addplot[teal, line width=2.4pt, smooth] coordinates {"""+coords(xs,np.polyval(p,xs))+r"""};
\addplot[only marks, mark=*, mark size=3.6pt, mark options={fill=ink, draw=white, line width=0.8pt}] coordinates {"""+coords(xd,yd)+r"""};
\node[font=\small\bfseries, text=ink, anchor=south] at (axis cs:1.55,1.42) {training data};
\draw[->, inksoft, thick] (axis cs:1.55,1.45) -- (axis cs:"""+f"{xd[np.argmax(yd)]-0.05:.3f},{yd.max()+0.1:.3f}"+r""");
\node[font=\small\bfseries, text=teal, anchor=west] at (axis cs:0.25,-1.25) {fitted model};
\draw[->, teal, thick] (axis cs:1.3,-1.1) -- (axis cs:"""+f"{4.35:.2f},{np.polyval(p,4.35)-0.08:.2f}"+r""");
\end{axis}
\end{tikzpicture}
\end{document}"""
open('fit_example.tex','w').write(tex)

# extrapolation
xs=np.linspace(-1.6,8.4,400)
cols=['teal','blue','plum']; degs=[3,4,5]; plots=""
for d,c in zip(degs,cols):
    pp=np.polyfit(xd,yd,d); y=np.polyval(pp,xs); m=(y>-2.4)&(y<2.6)
    # keep contiguous segments only
    plots+=r"\addplot[%s, line width=2.2pt, smooth, restrict y to domain=-2.4:2.6, unbounded coords=jump] coordinates {%s};"%(c,coords(xs,y))+"\n"
tex=pre+r"""
\begin{document}
\begin{tikzpicture}
\begin{axis}[width=15cm,height=10cm,xmin=-1.6,xmax=8.4,ymin=-2.4,ymax=2.6,
  axis lines=left, ticks=none, xlabel={input $x$}, ylabel={output $y$}, clip=true]
\fill[tealsoft] (axis cs:0.3,-2.4) rectangle (axis cs:5.9,2.6);
\draw[teal!60, dashed, thick] (axis cs:0.3,-2.4) -- (axis cs:0.3,2.6) (axis cs:5.9,-2.4) -- (axis cs:5.9,2.6);
"""+plots+r"""
\addplot[only marks, mark=*, mark size=3.4pt, mark options={fill=ink, draw=white, line width=0.8pt}] coordinates {"""+coords(xd,yd)+r"""};
\node[font=\small\bfseries, text=teal] at (axis cs:3.1,2.3) {inside the data: models agree};
\node[font=\small\bfseries, text=amber, align=center] at (axis cs:7.2,-1.7) {outside:\\models disagree};
\node[font=\small\bfseries, text=amber, align=center] at (axis cs:-0.6,-1.7) {outside};
\end{axis}
\end{tikzpicture}
\end{document}"""
open('extrapolation.tex','w').write(tex)

# cost_scaling (illustrative)
N=np.logspace(1,3,60)
meth=[("CCSD(T)",7,60,'amber'),("MP2",5,5,'plum'),("Hartree--Fock",4,0.5,'blue'),("DFT",3,1.0,'teal'),("semi-empirical (GFN2-xTB)",3,1e-2,'inksoft'),("force field",1,1e-5,'greyc')]
plots=""
for name,pw,t10,c in meth:
    t=t10*(N/10)**pw; m=t<1e9
    plots+=r"\addplot[%s, line width=2.2pt] coordinates {%s};"%(c,coords(N[m],t[m]))+"\n"
labels=r"""
\node[text=amber, font=\small\bfseries, anchor=west] at (axis cs:30,3e8) {CCSD(T) $\sim N^7$};
\node[text=plum, font=\small\bfseries, anchor=west] at (axis cs:300,6e7) {MP2 $\sim N^5$};
\node[text=blue, font=\small\bfseries, anchor=west] at (axis cs:1050,5e8) {HF $\sim N^4$};
\node[text=teal, font=\small\bfseries, anchor=west] at (axis cs:1050,1e6) {DFT $\sim N^3$};
\node[text=inksoft, font=\small\bfseries, anchor=west] at (axis cs:1050,1e4) {semi-empirical};
\node[text=greyc, font=\small\bfseries, anchor=west] at (axis cs:1050,1e-3) {classical};
\node[text=greyc, font=\small\bfseries, anchor=west] at (axis cs:1050,1.2e-4) {force field};
"""
tex=pre+r"""
\begin{document}
\begin{tikzpicture}
\begin{axis}[width=13cm,height=10cm,xmode=log,ymode=log,xmin=10,xmax=1000,ymin=1e-6,ymax=1e9,
  axis lines=left, xlabel={number of atoms $N$}, ylabel={time per energy + forces (s)},
  ytick={1e-6,1e-3,1,1e3,1e6,1e9}, clip=false]
\fill[ambersoft] (axis cs:10,1e-6) rectangle (axis cs:1000,0.086);
\draw[amber, dashed, thick] (axis cs:10,0.086) -- (axis cs:1000,0.086);
\node[text=amber, font=\footnotesize, anchor=south east, align=right] at (axis cs:980,0.1) {budget for $10^6$ MD steps in one day};
"""+plots+labels+r"""
\node[font=\scriptsize, text=greyc, anchor=north east] at (rel axis cs:1,-0.11) {illustrative scaling; prefactors schematic};
\end{axis}
\end{tikzpicture}
\end{document}"""
open('cost_scaling.tex','w').write(tex)

# IR spectrum (schematic ethyl acetate)
w=np.linspace(4000,500,1400)
bands=[(2984,22,28),(2940,14,22),(1742,92,14),(1447,22,16),(1373,40,12),(1240,98,20),(1047,70,16),(938,18,10),(847,15,10),(634,20,12)]
A=sum(a*(g**2/((w-c)**2+g**2)) for c,a,g in bands)
T=100-np.clip(A,0,96)
tex=pre+r"""
\begin{document}
\begin{tikzpicture}
\begin{axis}[width=15.5cm,height=9.5cm,x dir=reverse,xmin=500,xmax=4000,ymin=0,ymax=118,
  axis lines=left, xlabel={wavenumber (cm$^{-1}$)}, ylabel={transmittance (\%)},
  xtick={4000,3000,2000,1500,1000,500}, ytick={0,50,100}, clip=false]
\fill[linec!45] (axis cs:1500,0) rectangle (axis cs:500,104);
\node[font=\footnotesize, text=inksoft] at (axis cs:1000,110) {fingerprint region};
\addplot[ink, line width=1.6pt] coordinates {"""+coords(w,T)+r"""};
\node[text=teal, font=\small\bfseries, align=center] at (axis cs:2960,58) {C--H stretch\\[-1pt]{\footnotesize\mdseries $\sim$2980}};
\draw[teal,->,thick] (axis cs:2960,66) -- (axis cs:2975,75);
\node[text=amber, font=\small\bfseries, align=center, anchor=east] at (axis cs:1840,14) {C=O stretch\\[-1pt]{\footnotesize\mdseries $\sim$1740}};
\draw[amber,->,thick] (axis cs:1830,14) -- (axis cs:1752,10);
\node[text=plum, font=\small\bfseries, align=center] at (axis cs:760,16) {C--O--C stretch\\[-1pt]{\footnotesize\mdseries $\sim$1240, 1050}};
\draw[plum,->,thick] (axis cs:900,10) -- (axis cs:1225,4);
\draw[plum,->,thick] (axis cs:900,20) -- (axis cs:1035,29);
\node[font=\small\bfseries, text=ink, anchor=west] at (axis cs:3950,20) {ethyl acetate, \ce{CH3COOCH2CH3}};
\node[font=\scriptsize, text=greyc, anchor=west] at (axis cs:3950,11) {schematic; peak positions approximate};
\end{axis}
\end{tikzpicture}
\end{document}"""
open('ir_spectrum.tex','w').write(tex)
print("ok")
