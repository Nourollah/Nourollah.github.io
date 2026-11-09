import math
GC={"OH":"plum","CHO":"blue","COOH":"amber","NH2":"teal"}
def build(n,left=None,right=None,L=0.42):
    dx=L*math.cos(math.radians(30)); dy=L/2
    C=[(i*dx, dy if i%2==0 else 0.0) for i in range(n)]
    bonds=[(C[i],C[i+1],1,"ink") for i in range(n-1)]; atoms=[]
    def grp(g,ci,side):
        c=C[ci]; up=c[1]>0.01; s=-1 if side=="L" else 1
        diag=(c[0]+s*dx, c[1]-dy if up else c[1]+dy)
        vert=(c[0], c[1]+L if up else c[1]-L)
        col=GC[g]
        if g=="OH": bonds.append((c,diag,1,col)); atoms.append((diag,"HO" if side=="L" else "OH",col))
        if g=="NH2": bonds.append((c,diag,1,col)); atoms.append((diag,"H$_2$N" if side=="L" else "NH$_2$",col))
        if g=="CHO": bonds.append((c,diag,2,col)); atoms.append((diag,"O",col))
        if g=="COOH":
            bonds.append((c,vert,2,col)); atoms.append((vert,"O",col))
            bonds.append((c,diag,1,col)); atoms.append((diag,"HO" if side=="L" else "OH",col))
    if left: grp(left,0,"L")
    if right: grp(right,n-1,"R")
    xs=[p[0] for b in bonds for p in b[:2]]+[a[0][0] for a in atoms]
    ys=[p[1] for b in bonds for p in b[:2]]+[a[0][1] for a in atoms]
    return bonds,atoms,(min(xs),max(xs),min(ys),max(ys))
def draw(n,left,right,cx,cy,bg,L=0.42,w="1.2pt"):
    bonds,atoms,(x0,x1,y0,y1)=build(n,left,right,L)
    ox=cx-(x0+x1)/2; oy=cy-(y0+y1)/2; o=[]
    for a,b,k,col in bonds:
        a=(a[0]+ox,a[1]+oy); b=(b[0]+ox,b[1]+oy)
        if k==1: o.append(r"\draw[%s, line width=%s] (%.3f,%.3f) -- (%.3f,%.3f);"%(col,w,*a,*b))
        else:
            vx,vy=b[0]-a[0],b[1]-a[1]; l=math.hypot(vx,vy); px,py=-vy/l*0.045,vx/l*0.045
            for s in (1,-1): o.append(r"\draw[%s, line width=%s] (%.3f,%.3f) -- (%.3f,%.3f);"%(col,w,a[0]+s*px,a[1]+s*py,b[0]+s*px,b[1]+s*py))
    for p,t,col in atoms:
        o.append(r"\node[font=\scriptsize\bfseries, text=%s, fill=%s, inner sep=0.6pt] at (%.3f,%.3f) {%s};"%(col,bg,p[0]+ox,p[1]+oy,t))
    return "\n".join(o)
