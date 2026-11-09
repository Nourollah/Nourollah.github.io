pre=open('preamble.tex').read()
def frag(n,pos,c,t): return r"\frag{%s}{%s}{%s}{%s}"%(n,pos,c,t)
b=r"""\begin{tikzpicture}[cmd/.style={draw=#1, fill=#1!10, line width=1.3pt, rounded corners=5pt, font=\ttfamily\bfseries, text=#1, minimum height=0.85cm, inner xsep=8pt}]
\node[font=\bfseries, text=ink, anchor=west] at (-0.3,4.1) {language (SCAN)};
\node[font=\small, text=teal, anchor=west] at (-0.3,3.35) {training};
\node[cmd=teal, anchor=west] at (-0.3,2.55) {jump};
\node[cmd=teal, anchor=west] at (1.75,2.55) {walk twice};
\node[font=\small, text=amber, anchor=west] at (-0.3,1.75) {test};
\node[cmd=amber, anchor=west, dashed] at (-0.3,0.7) {jump twice};
\draw[linec, line width=1pt] (5.2,-0.2) -- (5.2,4.4);
\node[font=\bfseries, text=ink, anchor=west] at (5.6,4.1) {molecules (GMD)};
\node[font=\small, text=teal, anchor=west] at (5.6,3.35) {training};
"""+frag("a1","6.25,2.55","teal",r"\ring")+frag("b1","7.75,2.55","blue",r"\ce{C=O}")+r"\bond{a1}{b1}"+frag("b2","9.55,2.55","blue",r"\ce{C=O}")+frag("c2","11.05,2.55","plum",r"\ce{NH2}")+r"\bond{b2}{c2}"+r"""
\node[font=\small, text=amber, anchor=west] at (5.6,1.75) {test};
"""+frag("a3","6.25,0.7","teal",r"\ring")+frag("c3","7.75,0.7","plum",r"\ce{NH2}")+r"\bond{a3}{c3}"+r"""
\node[draw=amber, line width=1.6pt, dashed, rounded corners=8pt, fit=(a3)(c3), inner sep=5pt] {};
\node[font=\small, text=inksoft, align=center] at (5.2,-0.75) {every part seen in training; only the composition is new};
\end{tikzpicture}"""
open('compositional_ml.tex','w').write(pre+"\n\\begin{document}\n"+b+"\n\\end{document}\n")
