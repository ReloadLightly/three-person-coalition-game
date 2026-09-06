# Replication protocol

> **Current milestone:** M3c — 25-generation exploratory trajectories  
> **Study status:** Exploratory  
> **Research ladder:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)

This file is the scientific contract for **Stage 1 — recreate**. It distinguishes source-recovered mechanisms from reconstructed executable details and records the experiment boundary before the historical replication is frozen.

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

Each fixed seating is repeated for `1000` rounds. The source then swaps two players (`A,B,C → A,C,B` in its example) and repeats another `1000` rounds with fresh histories.

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

The executable generator uses independent `p=0.5` root branches and a `p=0.5` first action. This is **Reconstructed**, supported by generation-0 branch statistics but not preserved source code.

### 3.9 Mutant birth — Exact share and order

At generation change, an admitted mutant receives **10%** of its parent's population and the parent loses that 10%. Final normalization occurs after growth/extinction and mutation.

Identical mutants merge because species are defined by strategy identity.

### 3.10 Species capacity — Exact value; cap behavior Reconstructed

Maximum species count is `9`. The current implementation blocks a novel mutant when all nine slots are occupied and leaves the parent's mass unchanged for that rejected proposal.

The value `9` is **Exact**. The full-cap bookkeeping rule is **Reconstructed**.

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
| **M3c** | three 25-generation exploratory trajectories + diagnostics | **Completed** |
| **M3d** | resolve/sensitivity-test full-cap bookkeeping | Next |
| **M4** | frozen historical replication with objective regime diagnostics | Not yet run |

## 6. Exact computational acceleration used in M3c

M3c preserves the historical interaction length and evaluates the same deterministic strategies while eliminating redundant computation.

### 6.1 Cycle skipping

A deterministic finite-memory three-player interaction has a finite joint history state. If that exact joint state recurs, all subsequent actions and payoffs repeat. Complete future copies of that deterministic cycle can therefore be skipped exactly.

This is not an approximation and introduces no new parameter.

### 6.2 Matchup payoff caching

For fixed strategies, `g_ijk` is deterministic and independent of current species frequencies. Once a strategy triple has been evaluated, the same payoff can be reused in later generations.

Caching is likewise computational only. The accelerated evaluator is tested against explicit round-by-round two-seating execution.

## 7. M3c exploratory experiment contract

M3c uses exactly three fixed seed pairs:

- `(initial=7, mutation=11)`;
- `(initial=17, mutation=23)`;
- `(initial=29, mutation=31)`.

Each trajectory runs for `25` generations with `1000` rounds per seating and all historical baseline values. The following are recorded each generation:

- species count and complete frequency vector;
- dominant species share;
- Shannon entropy of species frequencies;
- ecological mean/min/max scores;
- extinction count;
- mutation outcomes: unchanged / new / merged / blocked at cap;
- chromosome mean/max node count;
- maximum evolved memory depth.

The purpose is diagnostic: determine whether the reconstructed ecology runs across generations and whether unresolved reconstruction choices are actually exercised strongly enough to threaten a later replication claim.

## 8. M3c diagnostic result

| Seeds | Cap first reached | Extinctions | New | Merged | Blocked | Final mean score | Final max depth |
|:---|---:|---:|---:|---:|---:|---:|---:|
| `7 / 11` | `4` | `12` | `15` | `0` | `184` | `1.5141` | `2` |
| `17 / 23` | `3` | `4` | `7` | `2` | `187` | `0.0000` | `3` |
| `29 / 31` | `4` | `36` | `39` | `0` | `133` | `0.8209` | `3` |

Across all three short trajectories:

- `504` novel mutant proposals are blocked at the current full-cap rule;
- `61` novel mutants are admitted;
- `2` mutants merge with an existing species.

Therefore the full-cap bookkeeping is **not** a marginal low-level detail in the current reconstruction. It becomes active by generation 3–4 in every pilot and suppresses substantially more novel proposals than are admitted.

The `17/23` trajectory reaches ecological mean score `0` by generation 2 and remains there through generation 25. This is an exploratory seeded observation, not evidence that the historical model generically collapses.

Evidence:

- [`evidence/m3c_25_generation_summary.json`](evidence/m3c_25_generation_summary.json)
- [`evidence/m3c_seed_7_diagnostics.csv`](evidence/m3c_seed_7_diagnostics.csv)
- [`evidence/m3c_seed_17_diagnostics.csv`](evidence/m3c_seed_17_diagnostics.csv)
- [`evidence/m3c_seed_29_diagnostics.csv`](evidence/m3c_seed_29_diagnostics.csv)

## 9. Remaining reconstruction ledger after M3c

| ID | Detail | Current treatment | Priority / blocks |
|:---|:---|:---|:---|
| **A11** | exact behavior when nine species are already present | current rule blocks novel mutant; M3c shows this is highly consequential | **M3d / M4 freeze** |
| **A10** | exact outer mutation scheduler | one pass per surviving species | M3d sensitivity / M4 freeze |
| **A7** | exact historical random-tree/first-action generator | Bernoulli `0.5` reconstruction | M4 sensitivity |
| **A6** | multi-operator mutation order | explicit Reconstructed order | M4 sensitivity |
| **A8** | original seeds / independent-run count | new frozen multi-seed plan needed | M4 |
| **A9** | objective regime diagnostics | define before frozen historical replication | M4 |

M3c changes the priority ordering: **A11 is now the immediate validity threat** because the experiment demonstrates that it governs hundreds of mutation proposals in only 75 total generations.

## 10. Next bounded step — M3d

Before M4, attempt once more to recover the historical full-cap behavior from detailed source material or archival code.

If it remains unavailable, compare only a small set of defensible cap bookkeeping reconstructions under matched seeds, mutation streams, historical parameters, and diagnostics. The purpose is not to select the reconstruction that visually resembles the historical paper. It is to measure whether the conclusions we eventually want to test are robust to this unavoidable missing implementation detail.

## 11. Stage boundary

### Stage 1 — recreate

M0–M4 reconstruct the historical experiment using Exact, Reconstructed, and where necessary Estimated components.

### Stage 2 — recombine

Only after a citable Stage-1 replication may later published mechanisms be added, each labeled Recombined.

### Stage 3 — invent

Only after Stages 1 and 2 provide enough understanding may genuinely new mechanisms or theory be introduced, labeled Novel.

## Strongest defensible statement at M3c

> The reconstructed Akiyama–Kaneko ecology now executes across multiple generations with historical-scale deterministic interactions, selection, extinction, mutation, and species birth. Three 25-generation pilots show genuine turnover and increasing chromosome depth, but they also show that the current Reconstructed nine-species cap rule becomes active almost immediately and blocks most novel mutant proposals. That bookkeeping choice must therefore be resolved or sensitivity-tested before a historical replication can be frozen.
