# Scientific README visual system

> **Version:** 1.0 · **Reference implementation:** `three-person-coalition-game`  
> A presentation companion to `SCIENTIFIC_REPOSITORY_STANDARD.md`, not a replacement for it or the research manifesto.

## 1. One family, one scientific identity per repository

Use the same page hierarchy, palette, and banner proportions across the portfolio. Change the repository name, scientific subtitle, and motif. The motif must depict the research object, not generic technology decoration.

The reference banner is [`assets/hero.svg`](assets/hero.svg). It depicts one legal three-player round and an eight-branch memory tree. It does not depict an observed evolutionary outcome.

## 2. Reusable hero recipe

Copy the SVG and edit its plain-text labels and motif; no generator, service, or build dependency is required.

| Field | Reference value | Reuse rule |
|:---|:---|:---|
| Repository label | `three-person-coalition-game` | Exact repository name |
| Display title | Three-person / coalition game | Human-readable title; at most two lines |
| Subtitle | Coalition structure in an artificial-life ecology. | One factual scientific sentence |
| Source line | Akiyama & Kaneko reconstruction | Credit the underlying work, or state the study type |
| Motif | Matching pair, excluded player, 8-ary memory | Depict the new repository's mechanism |
| Footer | Recreate → recombine → invent | Shared research identity |

**Layout:** SVG `viewBox="0 0 1200 400"`, displayed at up to 960 px. Use 48-unit margins. Keep title text to the left of the divider at x=690; place the main motif on the right. Keep the footer below y=312. Wrap long titles deliberately rather than shrinking them until unreadable.

Keep changing status, milestones, result counts, and reproduction commands in native README text, not the graphic. This prevents a stale banner from contradicting the scientific record and keeps commands selectable.

Possible motifs include a graph for a network experiment, resource/organism interactions for an artificial ecosystem, and contrasting network topologies for a neuroevolution study. Such examples are design suggestions, not new scientific claims or automatic changes to other repositories.

## 3. Visual tokens

**Table 1 — Shared palette**

| Role | Value | Use |
|:---|:---|:---|
| Paper | `#FFFFFF` | Background |
| Ink | `#111827` | Main text |
| Slate | `#475569` | Supporting text and outlines |
| Muted | `#94A3B8` | Secondary marks |
| Rule | `#E2E8F0` | Dividers and borders |
| Accent | `#0072B2` | One focal mechanism |

*Reading:* Use the accent to convey emphasis, not as decoration. Labels and line styles must preserve meaning without color.

Use GitHub-native typography in Markdown and `DejaVu Sans, Arial, sans-serif` in SVG. Use regular and bold only. No external fonts, scripts, embedded web content, gradients, or shadows. Prefer one clear motif over a dashboard of tiny labels.

## 4. Preserve the paper structure

The banner precedes the H1, one-sentence thesis, a short navigation line, and the study-status block. Then follow the adopted scientific order:

**Abstract → research question → motivation → contributions → related work → objectives → method → experimental design → results → interpretation → limitations → reproduction → repository map → citation → license/responsible use.**

Milestone history is supplementary, not the organizing logic of the paper. A presentation pass must preserve the current stage, uncertainties, negative findings, and claim boundaries. It must not silently turn a code component into an empirical result.

## 5. Tables stay native and inspectable

Use Markdown tables for selectable, searchable content. Do not use screenshots of tables or raw LaTeX `tabular` environments as a README substitute.

Four useful table families are study metadata, research objectives, mechanism/provenance, and evidence/results. Add a milestone ledger only when it contributes information not already stated elsewhere.

Give scientific tables a numbered title and one-sentence reading. Prefer two to four columns, with six as an upper guideline. Left-align text, right-align numbers, put units and metric direction in headers when applicable, and use consistent numerical precision. Show missing values as `—`, not unexplained blanks. Include sample sizes and uncertainty when stochastic results exist; never manufacture them for implementation checks.

## 6. Equations use native GitHub math

Use `$...$` inline and a separate `$$` block for displayed equations:

```markdown
The population share is $x_i$.

$$
s_i = \sum_j \sum_k g_{ijk} x_j x_k.
$$
```

Define symbols in prose, keep notation consistent with the model, and link the associated method to its protocol or implementation. Use a few load-bearing equations, not a wall of mathematics. Do not place display equations in table cells or code fences in the actual README.

GitHub also supports fenced `math` blocks. Rendering behavior is documented in [GitHub's mathematical-expression guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions).

## 7. Diagrams explain mechanisms; plots report evidence

Use one compact Mermaid mechanism diagram where useful. Label nodes by scientific role rather than software classes. In this repository, solid arrows connect implemented components and dashed arrows identify the unimplemented species-turnover integration. The caption must state that distinction.

Use short labels, explicit `<br/>` line breaks, and restrained styling. GitHub's supported Markdown syntax is documented in its [diagram guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

A banner or mechanism diagram may appear before results exist if clearly labeled as an illustration. Result plots may only present recorded evidence. No placeholder curve, decorative trajectory, or fabricated number may be made to look like an experimental finding.

## 8. Check before publishing

Render the hero at its intended README width and inspect text wrapping, overlap, clipping, and contrast. Keep an SVG title/description plus meaningful image alt text. Check relative paths, table structure, balanced math delimiters, and code fences.

Limit the design diff to the README and presentation assets. Verify the pushed commit and its changed-file list. Do not claim the model was tested merely because a visual rendered, and do not add CI or experiment infrastructure for a presentation change.
