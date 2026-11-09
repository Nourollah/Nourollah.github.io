import math
pre=open('preamble.tex').read()
L=0.62; dx=L*math.cos(math.radians(30)); dy=L/2
def chain(x0,y0,n,start_up=False):
    pts=[]
    for i in range(n):
        up=(i%2==1)!=start_up
        pts.append((x0+i*dx, y0+(dy if up else 0)))
    return pts
def line(a,b,w="1.3pt",col="ink"): return r"\draw[%s, line width=%s] (%.3f,%.3f) -- (%.3f,%.3f);"%(col,w,*a,*b)
def dbl(a,b,col="ink"):
    vx,vy=b[0]-a[0],b[1]-a[1]; l=math.hypot(vx,vy); px,py=-vy/l*0.055,vx/l*0.055
    return line((a[0]+px,a[1]+py),(b[0]+px,b[1]+py),col=col)+line((a[0]-px,a[1]-py),(b[0]-px,b[1]-py),col=col)
def atom(p,t,col,bg,anchor="center"): return r"\node[font=\small\bfseries, text=%s, fill=%s, inner sep=1pt, anchor=%s] at (%.3f,%.3f) {%s};"%(col,bg,anchor,p[0],p[1],t)
def skel(pts): return "\n".join(line(pts[i],pts[i+1]) for i in range(len(pts)-1))
def mol(kind,x,y,bg):
    o=[]
    c=chain(x,y,5,start_up=True)   # C1 up
    o.append(skel(c))
    C1=c[0]; left=(C1[0]-dx,C1[1]-dy)
    if kind=="ol":
        o.append(line(C1,left)); o.append(atom(left,"HO","plum",bg))
    if kind=="al":
        o.append(dbl(C1,left,"blue")); o.append(atom(left,"O","blue",bg))
    if kind in("ac","di"):
        up=(C1[0],C1[1]+L)
        o.append(dbl(C1,up,"amber")); o.append(atom(up,"O","amber",bg))
        o.append(line(C1,left)); o.append(atom(left,"HO","amber",bg))
    if kind=="di":
        C5=c[-1]  # C5 is up (i=4 -> up? start_up True: i%2==1 -> up false... compute)
        if C5[1]>y+0.1: up5=(C5[0],C5[1]+L); right=(C5[0]+dx,C5[1]-dy)
        else: up5=(C5[0],C5[1]-L); right=(C5[0]+dx,C5[1]+dy)
        o.append(dbl(C5,up5,"amber")); o.append(atom(up5,"O","amber",bg))
        o.append(line(C5,right)); o.append(atom(right,"OH","amber",bg))
    return "\n".join(o)
def label(x,y,name,form): return r"\node[align=center, anchor=north] at (%.2f,%.2f) {{\small\bfseries\color{ink}%s}\\[-1pt]{\footnotesize\color{inksoft}%s}};"%(x,y,name,form)
b=[r"\begin{tikzpicture}"]
b.append(r"\node[font=\bfseries, text=teal] at (6.4,3.75) {training};")
b.append(r"\node[font=\bfseries, text=amber] at (13.55,3.75) {test: a new molecule};")
rows=[("Fusion","both groups on one carbon",1.85,[("ol",5.05,"pentan-1-ol","\\ce{C5H11OH}"),("al",8.1,"pentanal","\\ce{C4H9CHO}")],("ac",12.75,"pentanoic acid","\\ce{C4H9COOH}")),
      ("Duplication","the group appears twice",-1.6,[("ac",5.75,"pentanoic acid","\\ce{C4H9COOH}")],("di",12.45,"pentanedioic acid","\\ce{HOOC(CH2)3COOH}"))]
for name,desc,y,train,test in rows:
    b.append(r"\node[anchor=west, align=left, text width=2.9cm] at (0,%.2f) {\textbf{\textcolor{ink}{%s}}\\[1pt]{\small\color{inksoft}%s}};"%(y,name,desc))
    b.append(r"\fill[tealsoft, rounded corners=8pt] (3.15,%.2f) rectangle (9.65,%.2f);"%(y-1.45,y+1.45))
    b.append(r"\draw[amber, dashed, line width=1.2pt, fill=ambersoft, rounded corners=8pt] (10.55,%.2f) rectangle (16.55,%.2f);"%(y-1.45,y+1.45))
    b.append(r"\draw[->, inksoft, line width=1.7pt] (9.8,%.2f) -- (10.4,%.2f);"%(y,y))
    for k,cx,n,f in train:
        b.append(mol(k,cx-1.0,y-0.05,"tealsoft")); b.append(label(cx+0.25,y-0.55,n,f))
    k,cx,n,f=test
    b.append(mol(k,cx-1.0,y-0.05,"ambersoft")); b.append(label(cx+(0.25 if k!="di" else 0.55),y-0.55,n,f))
b.append(r"\node[font=\footnotesize, text=inksoft, anchor=west] at (3.3,-3.45) {\textcolor{plum}{\textbf{hydroxyl}}\quad \textcolor{blue}{\textbf{carbonyl}}\quad \textcolor{amber}{\textbf{carboxylic acid}}\quad every group in the test molecule is seen in training};")
b.append(r"\end{tikzpicture}")
open('scaffold_fd.tex','w').write(pre+"\n\\begin{document}\n"+"\n".join(b)+"\n\\end{document}\n")
