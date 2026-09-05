# Replication protocol

> **Current bounded step:** M3 source reconstruction — species fitness + mutation  
> **Implementation status:** M1–M2 code only; no M3 evolutionary code yet  
> **Study status:** Protocol  
> **Research ladder:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)

This document is the scientific contract for Stage 1 of the project: recreate Akiyama & Kaneko's three-person coalition experiment closely enough to understand and reproduce its mechanism before recombination or invention.

> **Mechanisms must be source-anchored. Missing implementation details are reconstructed. Missing numerical values are estimated or swept. Known mechanisms are never deleted merely because their historical coding details are incomplete.**

## 1. Source hierarchy

| ID | Source | Role |
|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3):293–304; arXiv `adap-org/9504002` | Primary scientific specification |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V*, pp. 193–201 | Conference specification and replication target |
| **S3** | Akiyama & Kaneko, BIES 1995, pp. 76–83 | Earlier version cited by S2 |
| **S4** | Akiyama, *三人ゲームにおける協力の発生とその進化* (1995) | Contemporary detailed exposition; 8-ary coding, mutation rates, simulation parameters |
| **S5** | Akiyama (1998), *『動的ゲーム』とゲームのダイナミクス：結託構造とコミュニケーションの進化*, University of Tokyo doctoral thesis, Chapter 18 | Detailed exposition of mutation operators and population-fitness equations |

Where sources differ, the discrepancy must be recorded before a historical baseline is frozen.

## 2. Provenance labels

| Label | Meaning |
|:---|:---|
| **Exact** | Directly recovered mechanism, implementation detail, or numerical value |
| **Reconstructed** | Mechanism sourced; executable detail inferred from descriptions/examples |
| **Estimated** | Mechanism sourced; numerical value chosen because historical value is unavailable |
| **Recombined** | Mechanism imported from another cited study; Stage 2 only |
| **Novel** | Mechanism or theory proposed by us; Stage 3 only |

Stage 1 may contain **Exact**, **Reconstructed**, and **Estimated** components. It may not silently introduce **Recombined** or **Novel** mechanisms.

## 3. Core model recovered before M3

### 3.1 Stage game — Exact

Each of three players chooses `0` or `1`. If exactly two match, those two receive `3` and the excluded player receives `0`; unanimous profiles give all players `0`.

### 3.2 Relational state — Exact

From a focal player's perspective the state digits are `(left,right,self)`, hence

\[
\text{state}=4L+2R+S.
\]

### 3.3 Finite-history strategy — Exact semantics; reconstructed Python representation

The historical chromosome is an 8-ary tree of state-sequence genes. A player forms its prior-state history in most-recent-first order and plays `1` if that sequence and at least one maximal gene stand in a reciprocal prefix relation; otherwise it plays `0`. The first-round action is stored separately.

M2 represents the action-equivalent chromosome by maximal gene paths. M3 mutation requires explicit branch topology.

### 3.4 Repeated interaction — Exact mechanism

Actions are selected synchronously from prior histories, relational states/payoffs are computed, histories are updated, and the process repeats. Historical baseline: `1000` rounds.

## 4. Historical baseline parameters recovered

| Parameter | Historical baseline | Provenance |
|:---|---:|:---|
| Maximum rounds | `1000` | Exact |
| Growth constant `d` | `0.2` | Exact |
| `KillLimit` | `0.2` | Exact |
| Maximum memory length | `4` | Exact |
| Initial species count | `6` | Exact |
| Initial memory length | `1` | Exact |
| Maximum species count | `9` | Exact |
| `PointAdd` | `0.1` | Exact |
| `PointRemove` | `0.1` | Exact |
| `Dupli` | `0.001` | Exact |
| `RemoveRecursively` | `0.001` | Exact |

These values define the historical baseline, not theoretically privileged constants. Sensitivity analysis comes after baseline reproduction.

---

# 5. M3 source reconstruction: species matching and fitness

The detailed source reconstruction is recorded in [`M3_SOURCE_RECONSTRUCTION.md`](M3_SOURCE_RECONSTRUCTION.md).

## 5.1 Species — Exact

Individuals with identical strategies form a species. Let `x_i` be species `i`'s population fraction. Own-species interactions are included.

## 5.2 Interaction payoff tensor — Exact mechanism

For an ordered species triple, define

\[
g_{ijk}
\]

as the focal species-`i` individual's average payoff per round in the repeated three-person interaction with partner species `j` and `k`.

Because the strategy itself distinguishes left and right positions, the partner slots are ordered. For implementation we name `j = left`, `k = right`; this letter assignment is a **Reconstructed convention** while positional distinction is **Exact**.

## 5.3 Species score — Exact

\[
s_i=\sum_j\sum_k g_{ijk}x_jx_k.
\]

Thus `(j,k)` and `(k,j)` are separate contributions when `j != k`. Partner combinations such as `j=i`, `k=i`, and `j=k` are permitted because individuals play the whole population including their own species.

No additional unordered-triple or six-permutation averaging rule is introduced.

## 5.4 Population mean and fitness — Exact

\[
\bar{s}=\sum_i x_i s_i,
\]

\[
w_i=s_i-\bar{s}.
\]

The recovered population update is

\[
x_i(t+1)-x_i(t)=d\,w_i\,x_i(t),
\]

followed by normalization.

Historical baseline: `d = 0.2`.

## 5.5 Extinction — Exact mechanism

A species with below-average score whose population falls below `KillLimit` is removed. Historical baseline: `KillLimit = 0.2`.

---

# 6. M3 source reconstruction: four tree mutations

M3 must mutate the explicit historical 8-ary chromosome, not a generic GP or neural representation.

## 6.1 `PointAdd` — Exact mechanism

Add a branch at a location where a branch is currently absent.

Historical rate: `0.1`.

Executable branch-slot enumeration is a **Reconstructed** detail derived directly from the 8-ary tree representation: absent outgoing state branches below `MaxMemoryLength` are candidate locations.

## 6.2 `PointRemove` — Exact

Remove an existing terminal branch at the edge of the tree.

Historical rate: `0.1`.

This is a local deletion; it does not recursively delete a larger internal subtree.

## 6.3 `Dupli` — Exact

At a terminal branch/leaf, attach all eight possible child branches simultaneously.

Historical rate: `0.001`.

The source explicitly states that this operation **does not change the strategy itself at the moment of duplication**. It is therefore a neutral genotype expansion that creates future separately mutable branches.

## 6.4 `RemoveRecursively` — Exact mechanism

Remove a branch together with all of its descendants recursively.

Historical rate: `0.001`.

Representing the mutation target as the incoming edge to a non-root subtree is the direct **Reconstructed graph interpretation** of the source wording.

## 6.5 Tree depth — Exact baseline

All branch growth remains bounded by

\[
\texttt{MaxMemoryLength}=4.
\]

---

# 7. Remaining reconstruction ledger

| ID | Detail | Status / treatment | Blocks |
|:---|:---|:---|:---|
| A4 | Species-triple weighting and positional arrangements | **Resolved at mechanism level**: ordered partner slots and `s_i = Σ_jk g_ijk x_j x_k` | no longer blocks M3 |
| A5 | Four mutation mechanisms | **Resolved at mechanism level**: all four structural operations recovered | no longer blocks M3 |
| A6 | S2 generic mutation `0.1` versus S4/S5 named four-operator rates and exact multi-event order | **Partly resolved**: detailed S4/S5 rates define the four-operator baseline; global event ordering remains a low-level reconstruction detail | M3 freeze, not mechanism existence |
| A7 | Random memory-1 tree initialization distribution | Recover if possible; otherwise explicit reconstruction distribution + sensitivity | M3 baseline freeze |
| A8 | Original random seeds / exact independent-run count | Search archival sources; declare new multi-seed plan regardless | M4 |
| A9 | Objective criteria for labeling regimes | Define measurable diagnostics before frozen replication | M4 |

### Important boundary

A6 does **not** justify omitting any mutation operator. If operation order cannot be recovered, we will choose a deterministic documented order, label it **Reconstructed**, and test sensitivity to alternative orders.

Likewise A7 does not justify omitting random initialization: the initialization mechanism is known, so an unrecovered distribution becomes a reconstruction choice.

---

# 8. Completed milestone status

### M1 — complete

Stage game + relational state representation.

### M2 — complete at implementation level

Finite-history strategy semantics + fixed-position deterministic repeated interaction.

### M3 source reconstruction — complete at mechanism level

Recovered before code:

- ordered species matching and population weighting;
- `g_ijk`, `s_i`, population mean, and fitness construction;
- all four named tree mutation mechanisms and rates.

**No M3 evolutionary code has been added in this bounded step.**

---

# 9. Next authorized implementation boundary

If M3 implementation begins, it is limited to the already sourced mechanisms:

1. explicit 8-ary chromosome topology;
2. ordered species-triple interaction scores `g_ijk`;
3. population-weighted species scores `s_i`;
4. the four historical mutation operators;
5. replicator-like population update and normalization;
6. extinction with `KillLimit`.

No later ALife mechanism, geopolitical interpretation, additional optimizer, or novel theory enters M3.

## Strongest defensible statement now

> The source record now specifies the causal machinery required for the next evolutionary layer: each species is evaluated against ordered pairs drawn from the current population distribution, and the 8-ary chromosome evolves through four identifiable branch operators (`PointAdd`, `PointRemove`, `Dupli`, `RemoveRecursively`). One low-level question about multi-operator event ordering remains explicit, but the evolutionary mechanisms themselves no longer need to be guessed or omitted.
