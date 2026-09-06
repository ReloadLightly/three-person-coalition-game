# Replication protocol

> **Current milestone:** M3a — evolutionary core implementation  
> **Study status:** Protocol / implementation validation  
> **Research ladder:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)

This file is the scientific contract for **Stage 1 — recreate**. It distinguishes what is source-recovered from what is reconstructed at the executable-detail level.

> **Mechanisms must be source-anchored. Missing implementation details are reconstructed. Missing numerical values are estimated or swept. Known mechanisms are never deleted merely because their historical coding details are incomplete.**

## 1. Source hierarchy

| ID | Source | Role |
|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game* | Primary scientific specification |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V* | Conference replication target |
| **S3** | Akiyama & Kaneko, BIES 1995 | Earlier version cited by S2 |
| **S4** | Akiyama, *三人ゲームにおける協力の発生とその進化* (1995) | Detailed 8-ary coding, mutation rates, parameters |
| **S5** | Akiyama doctoral thesis (1998), Chapter 18 | Detailed fitness equations and mutation operators |

Where sources disagree, the disagreement must be recorded before the historical baseline is frozen.

## 2. Provenance labels

| Label | Meaning |
|:---|:---|
| **Exact** | Directly recovered mechanism, implementation detail, or numerical value |
| **Reconstructed** | Mechanism sourced; executable detail inferred from source evidence |
| **Estimated** | Mechanism sourced; numerical value chosen because the exact historical value is unavailable |
| **Recombined** | Mechanism imported from another cited study; Stage 2 only |
| **Novel** | Mechanism or theory proposed by us; Stage 3 only |

Stage 1 may contain Exact, Reconstructed, and Estimated components. It may not silently introduce Recombined or Novel mechanisms.

## 3. Historical model contract

### 3.1 Stage game — Exact

Three players choose `0` or `1`. Exactly two matching players receive `3` each and the excluded player receives `0`. Unanimous profiles give all three `0`.

### 3.2 Relational state — Exact

From the focal player's perspective the state is

\[
4L + 2R + S,
\]

where the binary digits are left, right, and self.

### 3.3 Finite-history strategy — Exact semantics

The chromosome is an 8-ary tree of state-sequence genes. History is read most-recent-first. The strategy plays `1` when the available history and at least one maximal gene stand in a reciprocal prefix relation; otherwise it plays `0`. The first action is stored separately.

M2's maximal-gene representation is a **Reconstructed storage representation preserving the Exact action rule**.

### 3.4 Repeated interaction — Exact mechanism

The three actions are chosen synchronously from prior histories; relational states/payoffs are then computed and histories updated. Historical interaction length: `1000` rounds.

### 3.5 Ordered ecological fitness — Exact mechanism

For focal species `i`, left species `j`, and right species `k`, `g_ijk` is focal average payoff per round. Species score is

\[
s_i=\sum_j\sum_k g_{ijk}x_jx_k.
\]

Own-species partners are included and left/right slots remain ordered. The population mean and fitness are

\[
\bar{s}=\sum_i x_i s_i,
\qquad
w_i=s_i-\bar{s}.
\]

### 3.6 Population update — Exact mechanism and baseline

\[
x_i(t+1)-x_i(t)=d\,w_i\,x_i(t),
\]

followed by normalization. Historical baseline: `d = 0.2`.

### 3.7 Extinction — Exact mechanism and baseline

A below-average species that falls below `KillLimit` is removed. Historical baseline: `KillLimit = 0.2`.

The current implementation evaluates the threshold after the growth step and before survivor normalization. That **timing is Reconstructed** from the described update sequence.

### 3.8 Explicit chromosome + mutation — Exact mechanisms

Historical maximum depth: `4`.

| Operator | Rate | Source-recovered action | Executable provenance |
|:---|---:|:---|:---|
| `PointAdd` | `0.1` | add an absent branch | candidate-slot enumeration **Reconstructed** |
| `PointRemove` | `0.1` | remove a terminal branch | **Exact** |
| `Dupli` | `0.001` | add all 8 children to a terminal | **Exact**, behaviorally neutral at creation |
| `RemoveRecursively` | `0.001` | remove a branch and descendants | target-as-subtree-edge **Reconstructed** |

The current combined mutation-pass order is

`PointAdd → PointRemove → Dupli → RemoveRecursively`.

That order is **Reconstructed**, because the inspected sources recover the four operators and their local rates but do not unambiguously specify multi-operator global ordering. It must be included in later sensitivity analysis rather than treated as historical fact.

## 4. Historical baseline recovered

| Parameter | Value |
|:---|---:|
| Maximum rounds | `1000` |
| Growth constant `d` | `0.2` |
| `KillLimit` | `0.2` |
| Maximum memory/tree depth | `4` |
| Initial species count | `6` |
| Initial memory length | `1` |
| Maximum species count | `9` |
| `PointAdd` | `0.1` |
| `PointRemove` | `0.1` |
| `Dupli` | `0.001` |
| `RemoveRecursively` | `0.001` |

These are baseline values for historical reconstruction, not theoretically privileged constants.

## 5. Implementation map

| Milestone | Executable mechanism | Status |
|:---|:---|:---|
| **M1** | stage game + state index | Implemented |
| **M2** | finite-history strategy + synchronous repeated interaction | Implemented |
| **M3a** | explicit tree + four mutation operators + ordered ecological fitness + selection/extinction | Implemented |
| **M3b** | historical initialization + mutant-species insertion/turnover + one generation | Not yet implemented |
| **M4** | frozen multi-seed historical replication | Not yet run |

## 6. Scientific invariants protected by tests

The current code should protect at least these properties:

- all 8 stage-game profiles match the source payoff rule;
- binary action labels are symmetric;
- state parity encodes the focal action;
- reciprocal-prefix strategy examples match the source;
- the explicit chromosome is prefix-closed and depth-bounded;
- `Dupli` leaves the action phenotype unchanged at creation;
- every ordered species triple, including self-play, enters the fitness tensor;
- species score uses `x_j x_k` weighting;
- equal scores produce no selection change;
- below-average species below `KillLimit` are removed.

Tests exist to protect mechanisms and invariants, not to maximize test count.

## 7. Remaining reconstruction ledger

| ID | Detail | Treatment | Blocks |
|:---|:---|:---|:---|
| **A6** | multi-operator mutation order | current order explicitly **Reconstructed**; later sensitivity | M4 freeze, not M3a existence |
| **A7** | random memory-1 initialization distribution | recover if possible; otherwise explicit reconstruction + sensitivity | M3b |
| **A10** | rule for inserting/merging mutant chromosomes as species under max-species constraint | recover from S4/S5 or reconstruct transparently | M3b |
| **A8** | original seeds / independent-run count | new frozen multi-seed plan regardless | M4 |
| **A9** | objective regime diagnostics | define before frozen run | M4 |

The critical current gap is **species turnover bookkeeping**. We will not infer population-level historical results until that mechanism is implemented.

## 8. Stage boundary

### Stage 1 — recreate

M0–M4 reconstruct the historical experiment using Exact, Reconstructed, and where necessary Estimated components.

### Stage 2 — recombine

Only after a citable Stage-1 replication may later published mechanisms be added, each labeled Recombined.

### Stage 3 — invent

Only after Stages 1 and 2 provide enough understanding may genuinely new mechanisms or theory be introduced, labeled Novel.

## Strongest defensible statement at M3a

> The repository now executes the source-recovered causal core from stage interaction through ecological fitness, relative selection, extinction, and explicit 8-ary tree mutation. It does not yet execute the historical species-birth/turnover process and therefore makes no claim to reproduce the paper's evolutionary regimes.
