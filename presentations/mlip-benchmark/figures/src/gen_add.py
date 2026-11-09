import math
pre=open('preamble.tex').read()
L=0.75; dx=L*math.cos(math.radians(30)); dy=L/2
def pts(x0,y0):
    c=[(x0+i*dx, y0+(dy if i%2==0 else 0)) for i in range(5)]   # C1 up
    C1=c[0]; Ou=(C1[0],C1[1]+L); Oh=(C1[0]-dx,C1[1]-dy)
    return c,Ou,Oh
def line(a,b,col="ink",w="1.4pt"): return r"\draw[%s, line width=%s] (%.3f,%.3f) -- (%.3f,%.3f);"%(col,w,*a,*b)
def dbl(a,b,col):
    vx,vy=b[0]-a[0],b[1]-a[1]; l=math.hypot(vx,vy); px,py=-vy/l*0.06,vx/l*0.06
    return line((a[0]+px,a[1]+py),(b[0]+px,b[1]+py),col)+line((a[0]-px,a[1]-py),(b[0]-px,b[1]-py),col)
o=[r"\begin{tikzpicture}"]
# ---- left: group additivity
x0,y0=1.4,0.0
c,Ou,Oh=pts(x0,y0)
o.append(r"\node[font=\bfseries, text=ink, anchor=west] at (-0.2,2.55) {chemistry: group additivity};")
o.append(r"\fill[amber, fill opacity=0.18, rounded corners=7pt] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(Oh[0]-0.45,Oh[1]-0.35,c[0][0]+0.35,Ou[1]+0.35))
for i in (1,2,3): o.append(r"\fill[teal, fill opacity=0.18] (%.3f,%.3f) circle (0.3);"%c[i])
o.append(r"\fill[greyc, fill opacity=0.3] (%.3f,%.3f) circle (0.3);"%c[4])
for i in range(4): o.append(line(c[i],c[i+1]))
o.append(dbl(c[0],Ou,"amber")); o.append(line(c[0],Oh,"amber"))
o.append(r"\node[font=\small\bfseries, text=amber, fill=white, fill opacity=0, text opacity=1, inner sep=1pt] at (%.3f,%.3f) {O};"%Ou)
o.append(r"\node[font=\small\bfseries, text=amber, inner sep=1pt, anchor=east] at (%.3f,%.3f) {HO};"%(Oh[0]+0.12,Oh[1]))
o.append(r"\node[font=\footnotesize\bfseries, text=amber] at (%.2f,%.2f) {COOH};"%(c[0][0]-0.35,Oh[1]-0.6))
o.append(r"\node[font=\footnotesize\bfseries, text=teal] at (%.2f,%.2f) {CH$_2$\,$\times$\,3};"%(c[2][0],y0-0.62))
o.append(r"\node[font=\footnotesize\bfseries, text=inksoft] at (%.2f,%.2f) {CH$_3$};"%(c[4][0]+0.05,c[4][1]+0.6))
o.append(r"\node[font=\small, text=ink, anchor=west] at (-0.2,-1.55) {$\Delta H_\mathrm{f} \approx [\mathrm{CH_3}] + 3\,[\mathrm{CH_2}] + [\mathrm{COOH}]$};")
o.append(r"\node[font=\footnotesize, text=inksoft, anchor=west] at (-0.2,-2.15) {property = sum of group contributions};")
o.append(r"\draw[linec, line width=1pt] (5.9,-2.4) -- (5.9,2.8);")
# ---- right: MLIP
x0,y0=8.1,0.0
c,Ou,Oh=pts(x0,y0)
o.append(r"\node[font=\bfseries, text=ink, anchor=west] at (6.3,2.55) {machine learning: an MLIP};")
o.append(r"\draw[teal, dashed, line width=1.2pt, fill=tealsoft, fill opacity=0.6] (%.3f,%.3f) circle (1.05);"%c[2])
for i in range(4): o.append(line(c[i],c[i+1],"inksoft!70","1.2pt"))
o.append(line(c[0],Ou,"inksoft!70","1.2pt")); o.append(line(c[0],Oh,"inksoft!70","1.2pt"))
for p in c: o.append(r"\fill[carb] (%.3f,%.3f) circle (0.13);"%p)
for p in (Ou,Oh): o.append(r"\fill[oxy] (%.3f,%.3f) circle (0.13);"%p)
o.append(r"\fill[amber] (%.3f,%.3f) circle (0.17);"%c[2])
o.append(r"\node[font=\footnotesize\bfseries, text=amber] at (%.2f,%.2f) {atom $i$};"%(c[2][0]+0.05,c[2][1]-0.45))
o.append(r"\node[font=\footnotesize, text=teal, anchor=west] at (%.2f,%.2f) {neighbourhood};"%(c[2][0]+0.75,c[2][1]+1.05))
o.append(r"\node[font=\small, text=ink, anchor=west] at (6.3,-1.55) {$E = \sum_i \varepsilon(\text{neighbourhood of atom } i)$};")
o.append(r"\node[font=\footnotesize, text=inksoft, anchor=west] at (6.3,-2.15) {energy = sum of local atomic contributions};")
o.append(r"\end{tikzpicture}")
open('additivity.tex','w').write(pre+"\n\\begin{document}\n"+"\n".join(o)+"\n\\end{document}\n")
