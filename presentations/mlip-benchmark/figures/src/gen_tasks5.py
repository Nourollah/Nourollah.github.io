from molkit import draw
pre=open('preamble.tex').read()
W=3.55
tasks=[("Chain extension","longer chains",[(4,None,None,"butane")],[(9,None,None,"nonane")]),
 ("Fusion","both groups on one carbon",[(5,"OH",None,"pentan-1-ol"),(5,"CHO",None,"pentanal")],[(5,"COOH",None,"pentanoic acid")]),
 ("Duplication","the group twice",[(5,"COOH",None,"pentanoic acid")],[(5,"COOH","COOH","pentanedioic acid")]),
 ("Combination","different groups at the ends",[(5,"NH2","NH2","pentane-1,5-diamine"),(5,"COOH","COOH","pentanedioic acid")],[(5,"COOH","NH2","5-aminopentanoic acid")]),
 ("Fission","each group on its own",[(5,"COOH",None,"pentanoic acid")],[(5,"OH",None,"pentan-1-ol"),(5,"CHO",None,"pentanal")])]
o=[r"\begin{tikzpicture}"]
TY=(3.0,6.2); SY=(-0.55,2.45)
o.append(r"\node[font=\bfseries, text=teal, rotate=90] at (-0.35,%.2f) {training};"%((TY[0]+TY[1])/2))
o.append(r"\node[font=\bfseries, text=amber, rotate=90] at (-0.35,%.2f) {test};"%((SY[0]+SY[1])/2))
for k,(name,desc,tr,te) in enumerate(tasks):
    x=k*W+W/2
    o.append(r"\node[font=\bfseries, text=ink] at (%.2f,7.1) {%s};"%(x,name))
    o.append(r"\node[font=\footnotesize, text=inksoft] at (%.2f,6.65) {%s};"%(x,desc))
    o.append(r"\fill[tealsoft, rounded corners=6pt] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x-W/2+0.1,TY[0],x+W/2-0.1,TY[1]))
    o.append(r"\draw[amber, dashed, line width=1.1pt, fill=ambersoft, rounded corners=6pt] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x-W/2+0.1,SY[0],x+W/2-0.1,SY[1]))
    o.append(r"\draw[->, inksoft, line width=1.5pt] (%.2f,%.2f) -- (%.2f,%.2f);"%(x,TY[0]-0.05,x,SY[1]+0.05))
    for panel,items,bg in ((TY,tr,"tealsoft"),(SY,te,"ambersoft")):
        m=len(items); h=(panel[1]-panel[0])/m
        for j,(n,l,r,lab) in enumerate(items):
            cy=panel[1]-h*(j+0.5)+0.18
            Lb=0.36 if n>7 else 0.42
            o.append(draw(n,l,r,x,cy,bg,L=Lb))
            o.append(r"\node[font=\scriptsize, text=inksoft] at (%.2f,%.2f) {%s};"%(x,cy-0.62,lab))
o.append(r"\node[font=\footnotesize, text=inksoft, anchor=west] at (0.1,-1.0) {\textcolor{plum}{\textbf{hydroxyl}}\quad\textcolor{blue}{\textbf{carbonyl}}\quad\textcolor{amber}{\textbf{carboxylic acid}}\quad\textcolor{teal}{\textbf{amine}}\qquad chain lengths illustrative};")
o.append(r"\end{tikzpicture}")
open('gmd_examples.tex','w').write(pre+"\n\\begin{document}\n"+"\n".join(o)+"\n\\end{document}\n")
