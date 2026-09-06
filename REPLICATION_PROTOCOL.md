# Replication protocol

> **Current milestone:** M3d — species-capacity sensitivity  
> **Study status:** Exploratory sensitivity  
> **Research ladder:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)

This file is the scientific contract for **Stage 1 — recreate**. It distinguishes source-recovered mechanisms from reconstructed executable details and records what must be resolved before the historical replication is frozen.

> **Mechanisms must be source-anchored. Missing implementation details are reconstructed. Missing numerical values are estimated or swept. Known mechanisms are never deleted merely because their historical coding details are incomplete.**

## 1. Source hierarchy

| ID | Source | Role |
|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game* | Primary scientific specification |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V* | Conference replication target |
| **S3** | Akiyama & Kaneko, BIES 1995 | Earlier version cited by S2 |
| **S4** | Akiyama, *三人ゲームにおける協力の発生とその進化* (1995) | Detailed repeated-game order, initialization, mutation transfer, parameters, capacity rationale |
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

Each fixed seating is repeated for `1000` rounds. The source then swaps two players (`A,B,C → A,C,B` in its example) and repeats another `1000` rounds with fresh histories.

### 3.5 Ecological fitness — Exact

For focal species `i` and partner species `j,k`, species score is

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

The executable generator uses independent `p=0.5` root branches and a `p=0.5` first action. This is **Reconstructed**.

### 3.9 Mutant birth — Exact share and order

At generation change, an admitted mutant receives **10%** of its parent's population and the parent loses that 10%. Final normalization occurs after growth/extinction and mutation.

Identical mutants merge because species are defined by strategy identity.

### 3.10 Species capacity — Exact historical value; full-cap code unrecovered

The historical simulation sets maximum species to `9`.

The 1995 Japanese exposition additionally says:

- larger maximum species should increase strategy variation and reduce local-peak trapping;
- larger species sets become computationally expensive in the three-person game.

The inspected source still does **not** state what the original program did when a novel mutant was proposed while every species slot was occupied.

Current executable rule: block a novel mutant when full and leave the parent's mass unchanged for that proposal. This rule remains **Reconstructed**.

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

## 5. Implementation and experiment map

| Milestone | Scientific role | Status |
|:---|:---|:---|
| **M1** | stage game + state index | Implemented |
| **M2** | finite-history strategy + synchronous repeated interaction | Implemented |
| **M3a** | explicit tree + mutation + ecological selection/extinction | Implemented |
| **M3b** | initialization + mutant birth/merge/cap + one generation | Implemented and executed |
| **M3c** | three 25-generation exploratory trajectories | Completed |
| **M3d** | species-capacity sensitivity | **Completed** |
| **M3e** | outer mutation-scheduler reconstruction/sensitivity | Next |
| **M4** | frozen historical replication with objective regime diagnostics | Not yet run |

## 6. Exact computational acceleration

Cycle skipping and deterministic matchup caching preserve the exact 1000-round historical interaction while eliminating repeated computation. These are computational equivalences, not model changes.

## 7. M3c diagnostic result

M3c used three fixed seed pairs `(7,11)`, `(17,23)`, `(29,31)` for 25 generations at historical capacity `9`.

Across the three runs:

- 61 novel mutants were admitted;
- 504 novel mutants were blocked at full capacity;
- the cap was first reached by generation 3–4 in every trajectory.

This established that the full-cap rule is not a marginal edge case.

## 8. M3d capacity-sensitivity contract

M3d keeps all reconstructed bookkeeping fixed and varies only species capacity:

- historical baseline `9`;
- sensitivity variants `12` and `18`.

The same starting seed pairs are reused for every capacity condition. Post-divergence random mutation histories are not claimed to be identical because different populations consume different random events.

This is a **capacity sensitivity test**, not a candidate redefinition of the historical baseline.

Reproduce:

```bash
python -m experiments.m3d_capacity_sensitivity
```

Evidence: [`evidence/m3d_capacity_sensitivity.json`](evidence/m3d_capacity_sensitivity.json).

## 9. M3d result

| Cap | Seeds | Cap reached | Extinctions | New | Blocked | Final mean | Final depth |
|---:|:---|---:|---:|---:|---:|---:|---:|
| `9` | `7/11` | 4 | 12 | 15 | 184 | 1.5141 | 2 |
| `9` | `17/23` | 3 | 4 | 7 | 187 | 0.0000 | 3 |
| `9` | `29/31` | 4 | 36 | 39 | 133 | 0.8209 | 3 |
| `12` | `7/11` | 4 | 39 | 43 | 196 | 0.6993 | 4 |
| `12` | `17/23` | 3 | 4 | 10 | 247 | 0.0000 | 3 |
| `12` | `29/31` | 5 | 35 | 41 | 199 | 1.0326 | 3 |
| `18` | `7/11` | 5 | 56 | 68 | 268 | 0.7262 | 4 |
| `18` | `17/23` | 7 | 71 | 83 | 226 | 1.1611 | 4 |
| `18` | `29/31` | 6 | 69 | 81 | 234 | 1.3882 | 3 |

M3d therefore establishes:

1. larger capacity permits substantially more realized mutant variation;
2. species capacity materially changes ecological trajectories;
3. the `17/23` zero-payoff trajectory at capacity `9` and `12` is no longer present at capacity `18`;
4. even capacity `18` still saturates quickly and blocks hundreds of proposals.

Capacity is thus consequential, but increasing it alone does not remove the validity problem.

## 10. Remaining reconstruction ledger after M3d

| ID | Detail | Current treatment | Priority / blocks |
|:---|:---|:---|:---|
| **A10** | exact outer mutation scheduler | one pass per surviving species | **M3e / M4 freeze** |
| **A11** | exact behavior when species capacity is full | current rule blocks novel mutant; capacity sensitivity now quantified | M4 freeze |
| **A7** | exact historical random-tree/first-action generator | Bernoulli `0.5` reconstruction | M4 sensitivity |
| **A6** | multi-operator mutation order | explicit Reconstructed order | M4 sensitivity |
| **A8** | original seeds / independent-run count | new frozen multi-seed plan needed | M4 |
| **A9** | objective regime diagnostics | define before frozen historical replication | M4 |

The priority changes after M3d: persistent saturation even at capacity `18` makes **A10 — the outer mutation scheduler — the next bounded validity target**.

## 11. Next bounded step — M3e

Attempt to recover the historical outer mutation scheduler from S4/S5 and related source material.

If it remains unavailable, compare only a tiny set of defensible scheduler reconstructions while holding all source-defined mechanisms and starting seeds fixed. The goal is to determine whether the current one-pass-per-surviving-species rule is generating unrealistically aggressive species turnover.

## 12. Stage boundary

### Stage 1 — recreate

M0–M4 reconstruct the historical experiment using Exact, Reconstructed, and where necessary Estimated components.

### Stage 2 — recombine

Only after a citable Stage-1 replication may later published mechanisms be added, each labeled Recombined.

### Stage 3 — invent

Only after Stages 1 and 2 provide enough understanding may genuinely new mechanisms or theory be introduced, labeled Novel.

## Strongest defensible statement at M3d

> The reconstructed Akiyama–Kaneko ecology is materially sensitive to species capacity. Raising the capacity from the historical 9 to 12 or 18 increases realized mutant variation and changes some qualitative trajectories, yet even capacity 18 saturates rapidly. The next unresolved implementation detail with the greatest plausible leverage is therefore the outer mutation scheduler, not the existence of the source-defined evolutionary mechanisms.
