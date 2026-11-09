pre=open('preamble.tex').read()
o=[r"\begin{tikzpicture}"]
o.append(r"\node[font=\bfseries, text=ink, anchor=west] at (-1.9,3.3) {augmented chain extension};")
o.append(r"\node[font=\small, text=inksoft, anchor=west] at (-1.9,2.8) {chain length $n$ (carbon atoms)};")
cw=0.5
for n in range(2,16):
    x=(n-2)*cw
    o.append(r"\node[font=\scriptsize, text=inksoft] at (%.2f,2.35) {%d};"%(x+cw/2,n))
    alc_train = n in (2,3) or n>=9
    acid_train = 4<=n<=8
    for row,(lab,tr) in enumerate((("alcohols",alc_train),("acids",acid_train))):
        y=1.6-row*0.75
        if tr: o.append(r"\fill[teal!55] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x+0.03,y-0.3,x+cw-0.03,y+0.3))
        else: o.append(r"\draw[amber, line width=1pt, fill=ambersoft] (%.2f,%.2f) rectangle (%.2f,%.2f);"%(x+0.04,y-0.29,x+cw-0.04,y+0.29))
o.append(r"\node[font=\small\bfseries, text=plum, anchor=east] at (-0.1,1.6) {alcohols};")
o.append(r"\node[font=\small\bfseries, text=amber, anchor=east] at (-0.1,0.85) {carboxylic acids};")
o.append(r"\fill[teal!55] (0,-0.05) rectangle (0.35,0.2); \node[font=\footnotesize, text=inksoft, anchor=west] at (0.4,0.08) {training};")
o.append(r"\draw[amber, line width=1pt, fill=ambersoft] (2.0,-0.05) rectangle (2.35,0.2); \node[font=\footnotesize, text=inksoft, anchor=west] at (2.4,0.08) {test};")
o.append(r"\node[font=\small, text=ink, anchor=west, align=left] at (-1.9,-0.75) {every length and every group is seen in training;\\only the (length, group) pairing is new};")
o.append(r"\draw[linec, line width=1pt] (7.6,-1.3) -- (7.6,3.5);")
# right panel
X=8.2
def tile(name,x,y,col,txt,dashed=False):
    return r"\node[draw=%s, fill=%s!12, line width=1.3pt, rounded corners=5pt, minimum height=0.75cm, minimum width=1.1cm, font=\small\bfseries, text=%s%s] (%s) at (%.2f,%.2f) {%s};"%(col,col,col,", dashed" if dashed else "",name,x,y,txt)
o.append(r"\node[font=\bfseries, text=ink, anchor=west] at (%.2f,3.3) {augmented fusion};"%X)
o.append(r"\node[font=\small, text=teal, anchor=west] at (%.2f,2.6) {added to training: a worked example};"%X)
o.append(tile("a1",X+0.75,1.75,"blue","C=O")+r"\node[font=\bfseries, text=inksoft] at (%.2f,1.75) {+};"%(X+1.6)+tile("a2",X+2.45,1.75,"teal","NH$_2$"))
o.append(r"\draw[->, inksoft, line width=1.5pt] (%.2f,1.75) -- (%.2f,1.75);"%(X+3.1,X+3.8))
o.append(tile("a3",X+4.75,1.75,"teal","CONH$_2$")+r"\node[font=\footnotesize, text=inksoft] at (%.2f,1.1) {amide};"%(X+4.75))
o.append(r"\node[font=\small, text=amber, anchor=west] at (%.2f,0.35) {test: the same operation, other parts};"%X)
o.append(tile("b1",X+0.75,-0.5,"blue","C=O")+r"\node[font=\bfseries, text=inksoft] at (%.2f,-0.5) {+};"%(X+1.6)+tile("b2",X+2.45,-0.5,"plum","OH"))
o.append(r"\draw[->, inksoft, line width=1.5pt] (%.2f,-0.5) -- (%.2f,-0.5);"%(X+3.1,X+3.8))
o.append(tile("b3",X+4.75,-0.5,"amber","COOH",True)+r"\node[font=\footnotesize, text=inksoft] at (%.2f,-1.15) {carboxylic acid};"%(X+4.75))
o.append(r"\end{tikzpicture}")
open('augmented.tex','w').write(pre+"\n\\begin{document}\n"+"\n".join(o)+"\n\\end{document}\n")
