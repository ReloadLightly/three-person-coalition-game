# Replication protocol

> **Current milestone:** M3b — one-generation evolutionary integration  
> **Study status:** Implementation validation / exploratory evidence  
> **Research ladder:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)

This file is the scientific contract for **Stage 1 — recreate**. It distinguishes source-recovered mechanisms from reconstructed executable details.

> **Mechanisms must be source-anchored. Missing implementation details are reconstructed. Missing numerical values are estimated or swept. Known mechanisms are never deleted merely because their historical coding details are incomplete.**

## 1. Source hierarchy

| ID | Source | Role |
|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game* | Primary scientific specification |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V* | Conference replication target |
| **S3** | Akiyama & Kaneko, BIES 1995 | Earlier version cited by S2 |
| **S4** | Akiyama, *三人ゲームにおける協力の発生とその進化* (1995) | Detailed repeated-game order, 8-ary coding, initialization, mutation transfer, parameters |
| **S5** | Akiyama doctoral thesis (1998), Chapter 18 | Detailed fitness equations and mutation operators |

## 2. Provenance labels

| Label | Meaning |
|:---|:---|
| **Exact** | Directly recovered mechanism, implementation detail, or numerical value |
| **Reconstructed** | Mechanism sourced; executable detail inferred from source evidence |
| **Estimated** | Mechanism sourced; numerical value chosen because historical value is unavailable |
| **Recombined** | Mechanism imported from another cited study; Stage 2 only |
| **Novel** | Mechanism or theory proposed by us; Stage 3 only |

Stage 1 may contain Exact, Reconstructed, and Estimated components. It may not silently introduce Recombined or Novel mechanisms.

## 3. Historical model contract

### 3.1 Stage game — Exact

Three players choose `0` or `1`. Exactly two matching players receive `3` each and the excluded player receives `0`. Unanimous profiles give all three `0`.

### 3.2 Relational state — Exact

$$
\mathrm{state}=4L+2R+S.
$$

### 3.3 Finite-history strategy — Exact semantics

The chromosome is an 8-ary tree of state-sequence genes. History is read most-recent-first. The strategy plays `1` when the available history and at least one maximal gene stand in a reciprocal prefix relation; otherwise it plays `0`. The first action is stored separately.

M2's maximal-gene storage is **Reconstructed** while preserving the Exact action rule.

### 3.4 Repeated interaction and positional swap — Exact

Each fixed seating is repeated for `1000` rounds. The source then swaps two players (`A,B,C → A,C,B` in its example) and repeats another `1000` rounds. M3b evaluates both partner orientations with fresh histories.

### 3.5 Ecological fitness — Exact

For focal species `i` and partner species `j,k`, let `g_ijk` be focal average payoff after the historical two-seating interaction. Species score is

$$
s_i=\sum_j\sum_k g_{ijk}x_jx_k.
$$

Own-species partners are included. Population mean and relative fitness are

$$
\bar{s}=\sum_i x_i s_i,
\qquad
w_i=s_i-\bar{s}.
$$

### 3.6 Population growth and extinction — Exact mechanism/baseline

$$
x_i(t+1)-x_i(t)=d\,w_i\,x_i(t),
\qquad d=0.2.
$$

A below-average species falling below `KillLimit = 0.2` is removed.

### 3.7 Mutation — Exact mechanisms

Historical maximum depth: `4`.

| Operator | Rate | Source action | Executable provenance |
|:---|---:|:---|:---|
| `PointAdd` | `0.1` | add absent branch | candidate enumeration Reconstructed |
| `PointRemove` | `0.1` | remove terminal branch | Exact |
| `Dupli` | `0.001` | add all 8 children to terminal | Exact; neutral at creation |
| `RemoveRecursively` | `0.001` | remove branch + descendants | target-as-subtree-edge Reconstructed |

Current combined operator order `PointAdd → PointRemove → Dupli → RemoveRecursively` is **Reconstructed**.

### 3.8 Initial population — Exact mechanism/values; generator Reconstructed

Historical start:

- six species;
- equal population `1/6` each;
- random memory-1 tree coding.

The executable generator uses independent `p=0.5` root branches and a `p=0.5` first action. This is **Reconstructed**, supported by the generation-0 branch statistics but not by preserved historical source code.

### 3.9 Mutant birth — Exact share and order

At generation change, a mutant receives **10%** of its parent's population and the parent loses that 10%. Final normalization occurs after growth/extinction and mutation.

Identical mutants merge into the identical existing species because species are defined by strategy identity.

### 3.10 Species capacity — Exact value; cap behavior Reconstructed

Maximum species count is `9`. When already full, M3b blocks a novel mutant rather than inventing an unsupported replacement mechanism. This cap rule is **Reconstructed** and must be tested for sensitivity before M4.

## 4. Historical baseline

| Parameter | Value |
|:---|---:|
| rounds per seating | `1000` |
| seatings per matchup | `2` |
| growth constant `d` | `0.2` |
| `KillLimit` | `0.2` |
| maximum memory depth | `4` |
| initial species | `6` |
| initial population each | `1/6` |
| initial memory length | `1` |
| maximum species | `9` |
| mutant share | `0.10` |
| `PointAdd` | `0.1` |
| `PointRemove` | `0.1` |
| `Dupli` | `0.001` |
| `RemoveRecursively` | `0.001` |

## 5. Implementation map

| Milestone | Executable mechanism | Status |
|:---|:---|:---|
| **M1** | stage game + state index | Implemented |
| **M2** | finite-history strategy + synchronous repeated interaction | Implemented |
| **M3a** | explicit tree + mutation + ecological selection/extinction | Implemented |
| **M3b** | two-seating evaluation + initialization + mutant birth/merge/cap + one generation | **Implemented and executed once** |
| **M4** | frozen multi-seed historical replication | Not yet run |

## 6. M3b experiment boundary

The first evolutionary integration experiment runs **one generation only** with:

- initialization seed `7`;
- mutation seed `11`;
- historical `1000` rounds per seating;
- all historical baseline values above.

Reproduce:

```bash
python -m experiments.m3b_one_generation
```

Evidence: [`evidence/m3b_one_generation.json`](evidence/m3b_one_generation.json).

This evidence validates end-to-end generation mechanics; it is not a successful historical replication claim.

## 7. Scientific invariants protected by tests

The implementation now protects:

- all 8 stage-game profiles and symmetry;
- relational state indexing;
- source prefix-matching strategy semantics;
- finite-memory bounded interaction histories;
- prefix-closed explicit chromosome topology;
- `Dupli` phenotype neutrality;
- all four historical mutation operators;
- source-required two-seating matchup evaluation;
- population-weighted ecological fitness;
- relative growth and extinction;
- six distinct equal-population initial species;
- exact 10% parent-to-mutant population transfer;
- final normalization after mutation;
- explicit Reconstructed behavior at the species cap.

## 8. Remaining reconstruction ledger

| ID | Detail | Current treatment | Blocks |
|:---|:---|:---|:---|
| **A6** | multi-operator mutation order | explicit Reconstructed order | M4 freeze |
| **A7** | exact historical random-tree/first-action generator | Bernoulli `0.5` reconstruction | M4 sensitivity |
| **A10** | outer mutation scheduler | one pass per surviving species | M4 sensitivity |
| **A11** | behavior at nine-species cap | block novel mutant | M4 sensitivity |
| **A8** | original seeds/run count | new frozen multi-seed plan needed | M4 |
| **A9** | objective regime diagnostics | define before frozen historical replication | M4 |

## 9. Stage boundary

### Stage 1 — recreate

M0–M4 reconstruct the historical experiment using Exact, Reconstructed, and where necessary Estimated components.

### Stage 2 — recombine

Only after a citable Stage-1 replication may later published mechanisms be added, each labeled Recombined.

### Stage 3 — invent

Only after Stages 1 and 2 provide enough understanding may genuinely new mechanisms or theory be introduced, labeled Novel.

## Strongest defensible statement at M3b

> The repository now executes one complete source-anchored generation from historical-style initialization through two-seating interaction, ecological fitness, relative growth, extinction, mutation birth, and final normalization. Several low-level bookkeeping choices remain explicitly Reconstructed, so the one-generation run is implementation evidence rather than evidence that the historical long-run regimes have been reproduced.
