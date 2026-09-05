# M3 source reconstruction

> **Scope:** source reconstruction only  
> **Implementation status:** no M3 evolutionary code has been added  
> **Purpose:** recover the historical species-matching/fitness calculation and the four 8-ary-tree mutation operators before implementation

This document is deliberately bounded. It reconstructs only the two pieces needed immediately before M3 implementation:

1. how species are matched and scored, including left/right positional ordering;
2. what `PointAdd`, `PointRemove`, `Dupli`, and `RemoveRecursively` do to the 8-ary strategy chromosome.

The governing research rule is [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md): mechanisms are source-anchored; missing low-level implementation details are reconstructed rather than used as a reason to delete a mechanism.

## 1. Sources used for this step

The decisive sources are:

- **S1/S2:** Akiyama & Kaneko's 1995/1996 English descriptions of the three-person game and population update;
- **S4:** Akiyama, *三人ゲームにおける協力の発生とその進化* (1995), which gives the named mutation parameters and detailed tree description;
- **S5:** Akiyama's 1998 University of Tokyo doctoral thesis, Chapter 18, which explicitly describes the four mutation operators and the population-fitness equations.

The detailed S5 formulation is used where the shorter conference paper compresses implementation detail.

---

# 2. Species matching and positional scoring

## 2.1 Species are strategy classes — Exact

Individuals with the same strategy belong to the same species. Let the population fraction of species `i` be

\[
x_i,
\]

with total population normalized to 1.

The source states that individuals play against the whole population **including their own species**. Consequently, interactions such as `(i,i,i)`, `(i,i,j)`, and `(i,j,j)` are part of the fitness calculation rather than excluded special cases.

## 2.2 The basic scored object is an ordered species triple — Exact mechanism

For three individuals belonging to species `i`, `j`, and `k`, let

\[
g_{ijk}
\]

be the average payoff **per round** obtained by the focal individual from species `i` after the repeated three-person interaction.

Because the strategy representation distinguishes a focal player's left and right neighbours, the two partner slots are relationally distinct. For executable notation we use:

- focal/self species: `i`;
- left-position species: `j`;
- right-position species: `k`.

The historical sources define the left/right distinction exactly. The assignment of the letters `j` and `k` to left versus right is merely a naming convention; swapping those labels globally changes no aggregate fitness because both ordered pairs are included in the double sum below.

**Provenance:**

- ordered focal/partner structure: **Exact**;
- naming `j = left`, `k = right`: **Reconstructed convention with no effect on aggregate fitness**.

## 2.3 Positional permutations are not collapsed into an unordered pair — Exact implication

The species score is

\[
s_i = \sum_j \sum_k g_{ijk} x_j x_k.
\]

This is a sum over **ordered** partner slots. Therefore when `j != k`, the two relational arrangements

\[
(i; j_{left}, k_{right})
\]

and

\[
(i; k_{left}, j_{right})
\]

are separate terms. This matters because strategies can react differently to their left and right neighbours.

There is no need to invent an additional six-permutation averaging rule. Holding species `i` as the focal individual, the ordered double sum already includes both left/right arrangements of every partner-species pair. Cyclic relabeling of the three physical seats is represented when each species is, in turn, evaluated as the focal species in its own `s_i` calculation.

## 2.4 Population weighting — Exact

The weight of an ordered partner pair `(j,k)` is

\[
x_j x_k.
\]

Thus the ecology is equivalent to drawing the focal player's left and right partners independently from the current species-frequency distribution, while allowing own-species draws.

The total mean payoff of the population is

\[
\bar{s} = \sum_i x_i s_i.
\]

Fitness is then

\[
w_i = s_i - \bar{s}.
\]

The already recovered population update is

\[
x_i(t+1)-x_i(t)=d\,w_i\,x_i(t),
\]

followed by normalization, with historical baseline `d = 0.2`.

## 2.5 What `g_ijk` requires operationally — Exact mechanism

For each ordered triple `(i,j,k)`:

1. place the three strategies in the three relational slots;
2. run the deterministic repeated interaction using the historical strategy rule;
3. accumulate the focal species-`i` player's payoff;
4. divide by the number of rounds to obtain average payoff per round `g_ijk`.

The historical baseline interaction length is `1000` rounds.

This is the complete mechanism needed to construct the fitness tensor and species scores. M3 implementation should not replace it with random pair sampling, unordered triples, or a single representative matchup.

---

# 3. Mutation operates on the explicit 8-ary chromosome

M2 could represent a strategy by its maximal gene paths because only action selection mattered. M3 mutation requires the actual branch topology.

The historical chromosome is therefore an explicit rooted **8-ary tree** whose outgoing branches correspond to possible prior states `0...7`, with depth bounded by `MaxMemoryLength = 4` in the historical baseline.

The four mutation mechanisms below are recovered from S4/S5.

## 3.1 `PointAdd` — add one previously absent branch

**Source mechanism:** attach a branch at a location where no branch currently exists.

The source describes this as a local mutation applied with mutation rate `PointAdd` to branch positions at nodes.

Historical baseline:

\[
\texttt{PointAdd}=0.1.
\]

### Executable interpretation

At a node below `MaxMemoryLength`, each absent outgoing state branch is a candidate location. A successful `PointAdd` event creates that branch.

This can add a new maximal gene or extend the set of histories that trigger card `1`.

**Provenance:** mechanism **Exact**; treating each absent child slot as the natural branch candidate is **Reconstructed from the tree description**.

## 3.2 `PointRemove` — remove a terminal branch

**Source mechanism:** cut off a branch at the edge/end of the tree.

The source states that each terminal branch is subject to mutation rate `PointRemove`.

Historical baseline:

\[
\texttt{PointRemove}=0.1.
\]

### Executable interpretation

Only an existing branch whose child is terminal is a `PointRemove` candidate. Removing it deletes that terminal path without recursively deleting a larger subtree.

This is the local deletion counterpart to `PointAdd`.

**Provenance:** **Exact**.

## 3.3 `Dupli` — expand one terminal into all eight children

**Source mechanism:** attach **eight branches at once** to a terminal branch/leaf.

The source explicitly notes that this mutation does **not change the strategy's current behavior**.

Historical baseline:

\[
\texttt{Dupli}=0.001.
\]

### Why it is behaviorally neutral

Suppose a terminal gene `g` currently makes the strategy play `1` whenever the recent history matches `g` by the reciprocal-prefix rule. Replacing that terminal by all eight children

\[
g0,g1,\ldots,g7
\]

still covers every possible next state after prefix `g`. The phenotype is therefore unchanged at the moment of duplication, while the genotype gains eight separately mutable descendants.

This operator is consequently a **neutral structural expansion** that creates future evolutionary degrees of freedom without immediately changing action behavior.

**Provenance:** **Exact** mechanism and stated behavioral neutrality.

## 3.4 `RemoveRecursively` — delete a branch and its entire descendant subtree

**Source mechanism:** remove a branch together with all branches attached beyond it, recursively.

S5 states that this occurs at nodes with mutation rate `RemoveRecursively`.

Historical baseline:

\[
\texttt{RemoveRecursively}=0.001.
\]

### Executable interpretation

Every non-root subtree is attached to the rest of the chromosome by one incoming branch. A recursive-removal event cuts that incoming branch and deletes the complete descendant subtree rooted there.

Unlike `PointRemove`, this operator can remove many terminal genes in a single event and therefore produce a large phenotypic change.

**Provenance:** recursive subtree deletion **Exact**; representing the candidate location as the incoming edge to a non-root node is the direct **Reconstructed graph interpretation** of the source wording.

---

# 4. Mutation parameter set recovered for the historical baseline

| Operator | Historical rate | Structural effect | Immediate behavioral effect |
|:---|---:|:---|:---|
| `PointAdd` | `0.1` | add one absent child branch | may change behavior |
| `PointRemove` | `0.1` | remove one terminal branch | may change behavior |
| `Dupli` | `0.001` | replace a terminal with all 8 children | source says no immediate strategy change |
| `RemoveRecursively` | `0.001` | remove a branch plus its descendant subtree | may produce large behavior change |

The historical maximum tree depth is `MaxMemoryLength = 4`.

---

# 5. One remaining low-level mutation ambiguity

The sources recover the **four causal mutation mechanisms and their local rates**. They do not, in the material inspected for this step, unambiguously specify a global ordering when more than one operator fires on the same chromosome during one generation.

That is a low-level implementation issue, not a missing mechanism.

Before M3 code is frozen we will therefore use one of two routes:

1. recover an explicit operation order from archival source/code if available; or
2. choose a deterministic documented order as a **Reconstructed** implementation detail and test whether alternative orders materially change results.

We will **not** add a new global mutation gate merely because the shorter English paper summarizes mutation with a generic `0.1`. The detailed S4/S5 operator-specific rates are the historical baseline for the four-operator implementation unless stronger source evidence shows otherwise.

---

# 6. Resolution status after this bounded step

| Previous ambiguity | Status after reconstruction |
|:---|:---|
| A4 — species-triple weighting and positional permutations | **Resolved at mechanism level**: ordered `(j,k)` partner positions, weighted by `x_j x_k`, with `s_i = sum_jk g_ijk x_j x_k` |
| A5 — four mutation mechanisms | **Resolved at mechanism level**: exact structural actions recovered for all four operators |
| A6 — generic S2 mutation `0.1` versus detailed named rates | **Partly resolved**: detailed S4/S5 rates define the four-operator baseline; exact cross-version shorthand/operation ordering remains documented rather than guessed |

No evolutionary code is introduced by this document.

---

# 7. Stop condition

This source-reconstruction step is complete when we can answer, without inventing a mechanism:

- who plays whom? **All species combinations, including own-species partners.**
- are partner positions ordered? **Yes; left/right remain distinct.**
- how is a species score computed? **`s_i = sum_jk g_ijk x_j x_k`.**
- what is `g_ijk`? **Focal species `i`'s average per-round payoff in the deterministic repeated interaction with partner species `j,k`.**
- what do the four mutation operators do? **Recovered above.**

The next step, if authorized, is M3 implementation of exactly these mechanisms plus the already recovered population update/extinction rules — and nothing beyond them.
