// Simple numbering for non-book documents
#let equation-numbering = "(1)"
#let callout-numbering = "1"
#let subfloat-numbering(n-super, subfloat-idx) = {
  numbering("1a", n-super, subfloat-idx)
}

// Theorem configuration for theorion
// Simple numbering for non-book documents (no heading inheritance)
#let theorem-inherited-levels = 0

// Theorem numbering format (can be overridden by extensions for appendix support)
// This function returns the numbering pattern to use
#let theorem-numbering(loc) = "1.1"

// Default theorem render function
#let theorem-render(prefix: none, title: "", full-title: auto, body) = {
  if full-title != "" and full-title != auto and full-title != none {
    strong[#full-title.]
    h(0.5em)
  }
  body
}
// Some definitions presupposed by pandoc's typst output.
#let content-to-string(content) = {
  if content.has("text") {
    content.text
  } else if content.has("children") {
    content.children.map(content-to-string).join("")
  } else if content.has("body") {
    content-to-string(content.body)
  } else if content == [ ] {
    " "
  }
}

#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

// Some quarto-specific definitions.

#show raw.where(block: true): set block(
    fill: luma(230),
    width: 100%,
    inset: 8pt,
    radius: 2pt
  )

#let block_with_new_content(old_block, new_content) = {
  let fields = old_block.fields()
  let _ = fields.remove("body")
  if fields.at("below", default: none) != none {
    // TODO: this is a hack because below is a "synthesized element"
    // according to the experts in the typst discord...
    fields.below = fields.below.abs
  }
  block.with(..fields)(new_content)
}

#let empty(v) = {
  if type(v) == str {
    // two dollar signs here because we're technically inside
    // a Pandoc template :grimace:
    v.matches(regex("^\\s*$")).at(0, default: none) != none
  } else if type(v) == content {
    if v.at("text", default: none) != none {
      return empty(v.text)
    }
    for child in v.at("children", default: ()) {
      if not empty(child) {
        return false
      }
    }
    return true
  }

}

// Subfloats
// This is a technique that we adapted from https://github.com/tingerrr/subpar/
#let quartosubfloatcounter = counter("quartosubfloatcounter")

#let quarto_super(
  kind: str,
  caption: none,
  label: none,
  supplement: str,
  position: none,
  subcapnumbering: "(a)",
  body,
) = {
  context {
    let figcounter = counter(figure.where(kind: kind))
    let n-super = figcounter.get().first() + 1
    set figure.caption(position: position)
    [#figure(
      kind: kind,
      supplement: supplement,
      caption: caption,
      {
        show figure.where(kind: kind): set figure(numbering: _ => {
          let subfloat-idx = quartosubfloatcounter.get().first() + 1
          subfloat-numbering(n-super, subfloat-idx)
        })
        show figure.where(kind: kind): set figure.caption(position: position)

        show figure: it => {
          let num = numbering(subcapnumbering, n-super, quartosubfloatcounter.get().first() + 1)
          show figure.caption: it => block({
            num.slice(2) // I don't understand why the numbering contains output that it really shouldn't, but this fixes it shrug?
            [ ]
            it.body
          })

          quartosubfloatcounter.step()
          it
          counter(figure.where(kind: it.kind)).update(n => n - 1)
        }

        quartosubfloatcounter.update(0)
        body
      }
    )#label]
  }
}

// callout rendering
// this is a figure show rule because callouts are crossreferenceable
#show figure: it => {
  if type(it.kind) != str {
    return it
  }
  let kind_match = it.kind.matches(regex("^quarto-callout-(.*)")).at(0, default: none)
  if kind_match == none {
    return it
  }
  let kind = kind_match.captures.at(0, default: "other")
  kind = upper(kind.first()) + kind.slice(1)
  // now we pull apart the callout and reassemble it with the crossref name and counter

  // when we cleanup pandoc's emitted code to avoid spaces this will have to change
  let old_callout = it.body.children.at(1).body.children.at(1)
  let old_title_block = old_callout.body.children.at(0)
  let children = old_title_block.body.body.children
  let old_title = if children.len() == 1 {
    children.at(0)  // no icon: title at index 0
  } else {
    children.at(1)  // with icon: title at index 1
  }

  // TODO use custom separator if available
  // Use the figure's counter display which handles chapter-based numbering
  // (when numbering is a function that includes the heading counter)
  let callout_num = it.counter.display(it.numbering)
  let new_title = if empty(old_title) {
    [#kind #callout_num]
  } else {
    [#kind #callout_num: #old_title]
  }

  let new_title_block = block_with_new_content(
    old_title_block,
    block_with_new_content(
      old_title_block.body,
      if children.len() == 1 {
        new_title  // no icon: just the title
      } else {
        children.at(0) + new_title  // with icon: preserve icon block + new title
      }))

  align(left, block_with_new_content(old_callout,
    block(below: 0pt, new_title_block) +
    old_callout.body.children.at(1)))
}

// 2023-10-09: #fa-icon("fa-info") is not working, so we'll eval "#fa-info()" instead
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: false, 
    fill: background_color, 
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"), 
    width: 100%, 
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%, 
      below: 0pt, 
      block(
        fill: background_color,
        width: 100%,
        inset: 8pt)[#if icon != none [#text(icon_color, weight: 900)[#icon] ]#title]) +
      if(body != []){
        block(
          inset: 1pt, 
          width: 100%, 
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}




#let article(
  title: none,
  subtitle: none,
  authors: none,
  keywords: (),
  date: none,
  abstract-title: none,
  abstract: none,
  thanks: none,
  cols: 1,
  lang: "en",
  region: "US",
  font: none,
  fontsize: 11pt,
  title-size: 1.5em,
  subtitle-size: 1.25em,
  heading-family: none,
  heading-weight: "bold",
  heading-style: "normal",
  heading-color: black,
  heading-line-height: 0.65em,
  mathfont: none,
  codefont: none,
  linestretch: 1,
  sectionnumbering: none,
  linkcolor: none,
  citecolor: none,
  filecolor: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
) = {
  // Set document metadata for PDF accessibility
  set document(title: title, keywords: keywords)
  set document(
    author: authors.map(author => content-to-string(author.name)).join(", ", last: " & "),
  ) if authors != none and authors != ()
  set par(
    justify: true,
    leading: linestretch * 0.65em
  )
  set text(lang: lang,
           region: region,
           size: fontsize)
  set text(font: font) if font != none
  show math.equation: set text(font: mathfont) if mathfont != none
  show raw: set text(font: codefont) if codefont != none

  set heading(numbering: sectionnumbering)

  show link: set text(fill: rgb(content-to-string(linkcolor))) if linkcolor != none
  show ref: set text(fill: rgb(content-to-string(citecolor))) if citecolor != none
  show link: this => {
    if filecolor != none and type(this.dest) == label {
      text(this, fill: rgb(content-to-string(filecolor)))
    } else {
      text(this)
    }
   }

  let has-title-block = title != none or (authors != none and authors != ()) or date != none or abstract != none
  if has-title-block {
    place(
      top,
      float: true,
      scope: "parent",
      clearance: 4mm,
      block(below: 1em, width: 100%)[

        #if title != none {
          align(center, block(inset: 2em)[
            #set par(leading: heading-line-height) if heading-line-height != none
            #set text(font: heading-family) if heading-family != none
            #set text(weight: heading-weight)
            #set text(style: heading-style) if heading-style != "normal"
            #set text(fill: heading-color) if heading-color != black

            #text(size: title-size)[#title #if thanks != none {
              footnote(thanks, numbering: "*")
              counter(footnote).update(n => n - 1)
            }]
            #(if subtitle != none {
              parbreak()
              text(size: subtitle-size)[#subtitle]
            })
          ])
        }

        #if authors != none and authors != () {
          let count = authors.len()
          let ncols = calc.min(count, 3)
          grid(
            columns: (1fr,) * ncols,
            row-gutter: 1.5em,
            ..authors.map(author =>
                align(center)[
                  #author.name \
                  #author.affiliation \
                  #author.email
                ]
            )
          )
        }

        #if date != none {
          align(center)[#block(inset: 1em)[
            #date
          ]]
        }

        #if abstract != none {
          block(inset: 2em)[
          #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
          ]
        }
      ]
    )
  }

  if toc {
    let title = if toc_title == none {
      auto
    } else {
      toc_title
    }
    block(above: 0em, below: 2em)[
    #outline(
      title: toc_title,
      depth: toc_depth,
      indent: toc_indent
    );
    ]
  }

  doc
}

#set table(
  inset: 6pt,
  stroke: none
)
#import "@preview/fontawesome:0.5.0": *
#let brand-color = (:)
#let brand-color-background = (:)
#let brand-logo = (:)

#set page(
  paper: "us-letter",
  margin: (x: 1.25in, y: 1.25in),
  numbering: "1",
  columns: 1,
)

#show: doc => article(
  title: [Explainable Graph Neural Network for Computational Chemistry],
  subtitle: [Annual Review 2025 · Cardiff University],
  authors: (
    ( name: [Amir Masoud Nourollah],
      affiliation: [],
      email: [] ),
    ),
  date: [Invalid Date],
  toc_title: [Table of contents],
  toc_depth: 3,
  doc,
)

= Overview
<overview>
#block[
#block[
]
#block[

+ #strong[The Current State of MLIPs] \
  #text(size: 0.85em)[Neural potentials, the black-box problem, and systemic extrapolation failure]

+ #strong[The Data-Evaluation Paradox] \
  #text(size: 0.85em)[Why standard benchmarks cannot measure generalisation]

+ #strong[GMD-26: A Framework for Systematic Evaluation] \
  #text(size: 0.85em)[Our benchmark, four tasks, and key results]

+ #strong[The DeepSet-MoE] \
  #text(size: 0.85em)[Proposed architecture for interpretable generalisation]

+ #strong[Conclusion & Future Outlook] \
  #text(size: 0.85em)[Key findings and next steps]

]
]
= Neural Network Architectures in Chemistry
<neural-network-architectures-in-chemistry>
Neural networks in chemistry can be categorised by their resolution and computational cost:

- #strong[Quantum Chemistry Methods] #emph[\(e.g., PauliNet)]
- #strong[Semi-Empirical Methods] #emph[\(e.g., NN-xTB)]
- #strong[Coarse-Grained Methods] #emph[\(e.g., CGNet)]
- #strong[Force Field Methods] #emph[\(e.g., SchNet)]

#block[
#block[
#callout(
body: 
[
Force field methods, or #strong[Machine-Learned Interatomic Potentials (MLIPs)], are currently the most widely adopted approach. They offer an optimal trade-off between #strong[computational complexity] and #strong[predictive accuracy].

]
, 
title: 
[
Note
]
, 
background_color: 
rgb("#dae6fb")
, 
icon_color: 
rgb("#0758E5")
, 
icon: 
none
, 
body_background_color: 
white
)
]
]
= Impact of MLIPs in Computational Chemistry
<impact-of-mlips-in-computational-chemistry>
#block[
#block[
#block[
#strong[Bridging the Gap]

- MLIPs maintain #emph[ab initio] accuracy while matching the #strong[efficiency] of classical force fields.
- #strong[Scaling Advantage:] DFT scales cubically ($O \( N^3 \)$), whereas MLIPs scale linearly ($O \( N \)$), preventing cost explosion for large systems.

]
]
#block[
#block[
#strong[Computational Breakthroughs]

+ #strong[Drastic Acceleration:] Achieving speedups of #strong[$10^5 times$] compared to standard DFT.
+ #strong[Overcoming Intractability:] Simulations requiring #strong[decades] of DFT compute time can be completed in days.
+ #strong[Resource Efficiency:] High-fidelity MD is now feasible on consumer GPUs rather than massive HPC clusters.

]
]
]
= The Ambiguity of Learned Representations
<the-ambiguity-of-learned-representations>
The shift from fixed descriptors to #strong[learnable representations] has traded transparency for accuracy, creating a fundamental "Black Box" problem:

#block[
#block[
#block[
#strong[\1. The Latent Space "Black Box"]

- Unlike descriptor-based models (using clear physical quantities), end-to-end architectures map atoms to #strong[abstract latent vectors].
- These high-dimensional representations are opaque; it is effectively impossible to #strong[disentangle] which physical features the model has learned.

]
]
#block[
#block[
#strong[\2. The Mapping Problem]

- Even in large-scale #strong[Foundation Models], the mapping between data and representation remains hidden.
- It is unclear if the model has constructed a continuous, valid #strong[Chemical Space], or merely memorised disjointed training manifolds.

]
]
]
= The Consequence: Systemic Extrapolation Failure
<the-consequence-systemic-extrapolation-failure>
Because the learned representation is opaque, we cannot define its validity domain. This leads to critical failures that standard metrics fail to detect:

#block[
#block[
#block[
#strong[\1. The Extrapolation Catastrophe]

- #strong[Undefined Boundaries:] Models cannot signal when they leave the training domain. They "hallucinate" interactions for unseen chemical species.
- #strong[Physics Violation:] The opaque latent space often maps valid geometric distortions to unphysical energy surfaces, leading to unstable dynamics in OOD settings.

]
]
#block[
#block[
#strong[\2. The Evaluation Blind Spot]

- #strong[The Interpolation Trap:] Standard benchmarks (e.g., MD17, QM9) rely on ID splits. This rewards models for #strong[memorising] the local manifold rather than learning transferable principles.
- #strong[False Security:] High accuracy on these datasets masks the model's inability to generalise compositionally to larger or more complex systems.

]
]
]
= Landscape of Established Datasets
<landscape-of-established-datasets>
Existing benchmarks were designed for accuracy --- not for probing #strong[compositional generalisation].

The field has evolved from small, specific datasets to massive, heterogeneous aggregates:

#block[
#block[
#block[
#block[
#strong[\1. Single-System MD] \
#emph[MD17 · rMD17]
]
Trajectories of single small molecules (Ethanol, Aspirin).

- #strong[Focus:] Learning the force field of a #emph[specific] molecule.
- #strong[Limit:] Models overfit to "that aspirin" and fail to transfer.

]
]
#block[
#block[
#block[
#strong[\2. Static Equilibrium] \
#emph[QM9 · OE62]
]
Properties for thousands of stable organic molecules.

- #strong[Focus:] Predicting properties of relaxed geometries.
- #strong[Limit:] Lacks the distorted geometries needed for reaction dynamics.

]
]
#block[
#block[
#block[
#strong[\3. Massive Aggregates] \
#emph[OMat24 · MPtrj]
]
Huge, heterogeneous collections mixing equilibrium and non-equilibrium data.

- #strong[Focus:] Training general-purpose #strong[Foundation Models].
- #strong[Limit:] Unstructured coverage; difficult to audit for systematic OOD gaps.

]
]
]
#block[
#block[
#strong[Gap:] #emph[Despite the scale of Category 3, we still lack systematic benchmarks designed to specifically stress-test #strong[compositional extrapolation].]

]
]
= The Data-Evaluation Paradox
<the-data-evaluation-paradox>
While datasets have scaled massively to create "Universal" models, evaluation protocols remain fundamentally flawed:

#block[
#block[
#block[
#strong[\1. The Scale of Data]

Modern efforts aim for universal coverage using massive, heterogeneous aggregates:

- #strong[Organic:] ANI-1x (20M+ conformations).
- #strong[Materials:] MPtrj (Inorganic trajectories).
- #strong[Surfaces:] Open Catalyst (Millions of relaxations).

]
#block[
#block[
#set text(size: 0.95em , weight: "700"); → Assumption: "More data automatically yields better physical understanding."
]
]
]
#block[
#block[
#strong[\2. The Evaluation Deficit]

#strong[A. The In-Distribution Trap:]

- Random splits test #strong[memorisation] of the local manifold, not physical learning.

#strong[B. The "Ineffective" OOD Solution:]

- Existing benchmarks use #strong[arbitrary] splits rather than systematic variations.
- #strong[Opacity:] They cannot quantify #emph[where] in chemical space the model fails.

]
]
]
#block[
#block[
#strong[The Critical Gap:] #emph[We lack a metric to measure #strong[how far] a model can extrapolate. We define OOD loosely ("unseen"), rather than mathematically ("distance from training manifold").]

]
]
= Introducing GMD-26: A Framework for Generalisation
<introducing-gmd-26-a-framework-for-generalisation>
We introduce #strong[GMD-26] not merely as a dataset, but as a flexible #strong[Benchmarking Framework] designed to rigorously quantify generalisation.

#block[
#block[
#block[
#strong[\1. The Protocol (Domain-Agnostic)]

A systematic structure adaptable to diverse fields (e.g., Polymers, Proteins):

- #strong[4 Systematic Tasks:] Defined by specific compositional shifts rather than random splits.
- #strong[2 Subtasks:] Targeted probes for specific failure modes.
- #strong[Philosophy:] Testing #emph[physical principles] (transferable) vs.~#emph[memorisation].

]
]
#block[
#block[
#strong[\2. Reference Implementation]

Validation via #strong[Small Organic Molecules]:

- #strong[Tractable Systems:] Small molecules provide interpretable, clear failure modes.
- #strong[Multi-Trajectory Challenge:] Unlike MD17, we use #emph[multiple diverse trajectories]. This forces models to learn the potential surface, not just a single path.
- #strong[Fidelity Status:] Currently generated at #strong[GFN2-xTB] level; active upgrade to #strong[DFT] is underway to support Foundation Models.

]
]
]
#block[
#block[
#strong[Goal:] #emph[To establish a universal standard for auditing model robustness across any chemical domain.]

]
]
= GMD-26: The Four Systematic Generalisation Tasks
<gmd-26-the-four-systematic-generalisation-tasks>
#figure([
#box(image("GMD26.png", width: 93.0%))
], caption: figure.caption(
position: bottom, 
[
Visual schematic of the four GMD-26 tasks.
]), 
kind: "quarto-float-fig", 
supplement: "Figure", 
)


= Results: The "Duplication" Challenge
<results-the-duplication-challenge>
#strong[Task Definition:] Training on molecules with a #strong[single fragment A] (e.g., Mono-acid) and testing on molecules with #strong[two] of the same #strong[fragment A] (e.g., Di-acid).

#{set text(size: 0.72em); table(
  columns: 9,
  align: (left,auto,auto,auto,auto,auto,auto,auto,auto,),
  table.header(table.cell(align: left, rowspan: 2, stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[Model], table.cell(colspan: 2, stroke: (bottom: (paint: rgb("#ccc"), thickness: 0.75pt)))[Forces MAE], table.cell(colspan: 2, stroke: (bottom: (paint: rgb("#ccc"), thickness: 0.75pt)))[Cosine Sim.], table.cell(colspan: 2, stroke: (bottom: (paint: rgb("#ccc"), thickness: 0.75pt)))[F Mag. MAE], table.cell(colspan: 2, stroke: (bottom: (paint: rgb("#ccc"), thickness: 0.75pt)))[Energy MAE (eV)],
    table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[ID], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[OOD], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[ID], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[OOD], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[ID], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[OOD], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[ID], table.cell(stroke: (bottom: (paint: rgb("#8b1538"), thickness: 1.5pt)))[OOD],),
  table.hline(),
  table.cell(align: left)[SchNet], [0.0292], [0.1143], [0.9979], [0.9691], [0.0307], [0.1458], [0.0295], [29.32],
  table.cell(align: left)[PaiNN], [0.0020], [0.0600], [0.9999], [0.9768], [0.0022], [0.0713], [0.0181], [30.72],
  table.cell(align: left)[GemNet], [0.0009], [0.0224], [0.9999], [0.9978], [0.0010], [0.0223], [0.0129], [12.27],
  table.cell(align: left)[EquiFormerV2], [0.0018], [0.0538], [0.9999], [0.9746], [0.0019], [0.0603], [0.0984], [#set text(weight: "700" , fill: rgb("#8b1538")); 133.77],
  table.cell(align: left)[DimeNet#super[\++]], [0.0018], [0.2484], [0.9999], [0.9406], [0.0019], [0.3863], [0.0128], [34.86],
  table.cell(align: left)[#strong[MACE]], [0.0028], [#strong[0.0171]], [0.9999], [#strong[0.9978]], [0.0030], [#strong[0.0201]], [0.0018], [#set text(weight: "700" , fill: rgb("#8b1538")); #strong[40.97]],
  table.cell(align: left)[NequIP], [0.0256], [0.0460], [0.9984], [0.9922], [0.0269], [0.0501], [0.0198], [34.59],
  table.hline(),
  table.footer(table.cell(align: left, colspan: 9)[Detailed performance metrics on the Fragment Duplication task. Values in #text(weight: "700" , fill: rgb("#8b1538"))[red] indicate catastrophic OOD failure.],),
)}
= Results: The "Chain Extension" Challenge
<results-the-chain-extension-challenge>
#figure([
#box(image("length_generalisation_figure_main.png", width: 93.0%))
], caption: figure.caption(
position: bottom, 
[
Detailed comparison of predicted vs.~actual values. Note the divergence in the OOD regions (right side) compared to the tight correlation in ID regions (left side).
]), 
kind: "quarto-float-fig", 
supplement: "Figure", 
)


= Proposed Architecture: The DeepSet-MoE
<proposed-architecture-the-deepset-moe>
We implement the #strong[DeepSet] framework ($E = rho \( sum phi.alt \)$), modifying the pipeline to expose interpretability and challenge standard assumptions:

#block[
#block[
#block[
#block[
\1. Encoder ($phi.alt$)
]
#strong[Architecture:] Mixture of Experts (MoE) replacing the monolithic network.

Refined Routing Metrics:

- #strong[Metric A (Spatial):] Experts activated by #emph[pairwise distances] (replacing the previous dual-cutoff).
- #strong[Metric B (Identity):] Experts assigned by #emph[central atom type]. One expert processes all hierarchies.

]
]
#block[
#block[
#block[
\2. Aggregation ($sum$)
]
#strong[Role:] Pooling atomic states into a global representation.

Current State:

- Standard Summation.

The Aggregation Hypothesis:

- #strong[Hypothesis:] Rigid summation #strong[obscures] distinct atomic contributions.
- #strong[Experiment:] Removing the Aggregation Head entirely.

]
]
#block[
#block[
#block[
\3. Decoder ($rho$)
]
#strong[Role:] Mapping latent state to Energy/Force.

Inference:

- Currently Identity (Direct).
- #strong[Goal:] Eliminate ambiguity by inferring directly from Encoder output.

]
]
]
= Summary: The Generalisation Crisis
<summary-the-generalisation-crisis>
#block[
#block[
#callout(
body: 
[
#strong[The Diagnosis]

We challenged the generalisation capabilities of established SOTA architectures by introducing #strong[GMD-26], a benchmark designed to test physical robustness rather than memorisation.

]
, 
title: 
[
Note
]
, 
background_color: 
rgb("#dae6fb")
, 
icon_color: 
rgb("#0758E5")
, 
icon: 
none
, 
body_background_color: 
white
)
]
]

#block[
#strong[Key Findings:]

]
#block[
- #strong[Universal Failure:] Every evaluated architecture --- from simple invariant models (SchNet) to equivariant transformers (EquiFormerV2) and high-order bodies (MACE) --- failed to generalise compositionally.

]
#block[
- #strong[The Magnitude of Error:] OOD errors were not merely higher; they were catastrophic (often #strong[orders of magnitude] larger than ID errors), proving that excellent performance on standard benchmarks masks a critical lack of physical understanding.

]
= Future Outlook: Toward Interpretable Generalisation
<future-outlook-toward-interpretable-generalisation>
To bridge this gap, we are moving away from monolithic "Black Box" networks toward a modular, chemically aligned architecture:

#block[
#block[
#block[
#strong[\1. The DeepSet-MoE Implementation]

- #strong[Specialised Encoding:] Replacing the single encoder with a #strong[Mixture of Experts] routed by optimised physical metrics.
- #strong[Goal:] To ensure distinct chemical environments are processed and learned by distinct, specialised parameters.

]
]
#block[
#block[
#strong[\2. The Aggregation Hypothesis]

- #strong[Current Bottleneck:] We suspect the rigid summation ($sum$) obscures the distinct share of atomic contributions.
- #strong[Next Step:] We are currently investigating alternative aggregation paradigms to identify a strategy that preserves distinct atomic contributions within the global prediction.

]
]
]

#block[
#block[
#strong[Final Conclusion:] #emph[We aim to establish DeepSet-MoE as an explainable architecture where OOD performance remains close to ID levels, prioritising this #strong[generalisation stability] over chasing the absolute lowest ID errors seen in SOTA models.]

]
]
= Thank You
<thank-you>
#block[
#block[
]
#block[

#block[
#strong[Amir Masoud Nourollah]

PhD Student · Cardiff NLP & Knowledge Representation and Reasoning Groups

#emph[Supervisors:] Prof.~Stefano Leoni · Prof.~Steven Schockaert

📧 #link("mailto:NourollahA@cardiff.ac.uk")[NourollahA\@cardiff.ac.uk] \
🌐 #link("https://nourollah.me")[nourollah.me]

#text(size: 0.8em)[Preprint available at #link("https://arxiv.org/abs/2605.08988")[arxiv.org/abs/2605.08988]]

]
]
]



