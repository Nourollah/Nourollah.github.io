from molkit import draw
pre=open('preamble.tex').read()
rows=[([(4,None,None,"butane")],[(9,None,None,"nonane")]),
 ([(5,"OH",None,"pentan-1-ol"),(5,"CHO",None,"pentanal")],[(5,"COOH",None,"pentanoic acid")]),
 ([(5,"COOH",None,"pentanoic acid")],[(5,"COOH","COOH","pentanedioic acid")]),
 ([(5,"NH2","NH2","pentane-1,5-diamine"),(5,"COOH","COOH","pentanedioic acid")],[(5,"COOH","NH2","5-aminopentanoic acid")]),
 ([(5,"COOH",None,"pentanoic acid")],[(5,"OH",None,"pentan-1-ol"),(5,"CHO",None,"pentanal")])]
Ht=12.5; CEN=[0.150,0.320,0.480,0.641,0.831]; HTS=[0.133,0.173,0.113,0.173,0.173]; TW=(0,6.0); SW=(6.8,12.8)
o=[r"\begin{tikzpicture}", r"\useasboundingbox (-0.1,0.15) rectangle (12.9,%.2f);"%(-Ht)]
o.append(r"\node[font=\bfseries, text=teal] at (3.0,%.2f) {training}"%(-0.04*Ht)+r";")
o.append(r"\node[font=\bfseries, text=amber] at (9.8,%.2f) {test}"%(-0.04*Ht)+r";")
for r,(tr,te) in enumerate(rows):
    yc=-CEN[r]*Ht; hh=HTS[r]*Ht/2
    o.append(r"\fill[tealsoft, rounded corners=6pt] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(TW[0],yc-hh,TW[1],yc+hh))
    o.append(r"\draw[amber, dashed, line width=1.1pt, fill=ambersoft, rounded corners=6pt] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(SW[0],yc-hh,SW[1],yc+hh))
    o.append(r"\draw[->, inksoft, line width=1.5pt] (%.2f,%.2f) -- (%.2f,%.2f);"%(TW[1]+0.12,yc,SW[0]-0.12,yc))
    for panel,items,bg in ((TW,tr,"tealsoft"),(SW,te,"ambersoft")):
        m=len(items); wd=(panel[1]-panel[0])/m
        for j,(n,l,rr,lab) in enumerate(items):
            cx=panel[0]+wd*(j+0.5)
            o.append(draw(n,l,rr,cx,yc+0.17,bg,L=0.36 if n>7 else 0.4))
            o.append(r"\node[font=\scriptsize, text=inksoft] at (%.2f,%.2f) {%s};"%(cx,yc-0.52,lab))
o.append(r"\end{tikzpicture}")
open('gmd_examples_rows.tex','w').write(pre+"\n\\begin{document}\n"+"\n".join(o)+"\n\\end{document}\n")
