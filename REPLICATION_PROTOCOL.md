# Replication protocol

> **Current milestone:** M1 — deterministic stage game + state representation  
> **Study status:** Protocol  
> **Research ladder:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)

This document is the scientific contract for Stage 1 of the project: recreate Akiyama & Kaneko's three-person coalition experiment closely enough to understand and reproduce its mechanism before recombination or invention.

The governing rule is simple:

> **Mechanisms must be source-anchored. Missing implementation details are reconstructed. Missing numerical values are estimated or swept. Known mechanisms are never deleted merely because their historical coding details are incomplete.**

## 1. Source hierarchy

| ID | Source | Role |
|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3):293–304; arXiv `adap-org/9504002` | Primary scientific specification |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V*, pp. 193–201 | Detailed conference specification and replication target |
| **S3** | Akiyama & Kaneko, BIES 1995, pp. 76–83 | Earlier version cited by S2 |
| **S4** | *三人ゲームにおける協力の発生とその進化*, 物性研究 65-1 (1995-10) | Contemporary Japanese exposition used to recover additional parameter values |

Where sources differ, the discrepancy must be recorded before a historical baseline is frozen.

## 2. Provenance labels

Important components are assigned one of the manifesto labels:

| Label | Meaning |
|:---|:---|
| **Exact** | Directly recovered mechanism, implementation detail, or numerical value |
| **Reconstructed** | Mechanism sourced; executable detail inferred from descriptions/examples |
| **Estimated** | Mechanism sourced; numerical value chosen because historical value is unavailable |
| **Recombined** | Mechanism imported from another cited study; Stage 2 only |
| **Novel** | Mechanism or theory proposed by us; Stage 3 only |

Stage 1 may contain **Exact**, **Reconstructed**, and **Estimated** components. It may not silently introduce **Recombined** or **Novel** mechanisms.

## 3. Model skeleton

### 3.1 Players and actions — Exact

Each interaction contains three players. In each round every player chooses one of two symmetric actions:

\[
a_i \in \{0,1\}.
\]

The symbols `0` and `1` do not intrinsically mean cooperation or defection.

### 3.2 Coalition payoff — Exact

- If exactly two players choose the same action, those two form the subgroup and each receives `3`.
- The excluded player receives `0`.
- If all three choose the same action, all three receive `0`.

These rules exhaust all eight action profiles.

### 3.3 Relational position — Exact

From a focal player's perspective the other actors are distinguished as **left** and **right**. The game rule itself is left/right symmetric, but strategies may condition on this relational information.

### 3.4 State indexing — Exact, resolved in M1

S2 states that the three binary digits correspond respectively to **left player, right player, self** and that the eight states are their binary representation. Therefore

\[
\text{state} = 4L + 2R + S.
\]

The source's worked example confirms this interpretation:

- `(left,right,self) = (0,1,1)` is state `3` (`011₂`);
- from the right player's perspective the same physical round is `(1,0,1)`, state `5` (`101₂`).

The source also notes that even-numbered states correspond to the focal player choosing `0`, while odd-numbered states correspond to choosing `1`, which follows directly because `self` is the least-significant bit.

This resolves former ambiguity **A1**.

### 3.5 Iterated interaction — Exact mechanism; baseline value recovered

The stage game is repeated for a fixed maximum number of rounds.

Historical baseline:

- maximum rounds per interaction: `1000`.

### 3.6 Finite-memory strategies — Exact mechanism; executable detail partly unresolved

Strategies map finite histories of the eight round states to the next action. Histories can therefore be represented as octonary strings/tree paths.

Historical baseline:

- maximum memory length: `4`;
- initial species count: `6`;
- initial memory length: `1`;
- initial strategies generated randomly.

### 3.7 Species and population ecology — Exact mechanism

Players with the same strategy form a species. Species scores determine changes in population fraction.

Historical baseline from S4:

- maximum number of species: `9`.

### 3.8 Population update — Exact mechanism and baseline value

The source gives the replicator-like update

\[
x_i(t+1)-x_i(t)=d\,[s_i-\bar{s}]\,x_i(t),
\]

followed by normalization.

Historical baseline from S4:

- growth constant `d = 0.2`.

### 3.9 Extinction — Exact mechanism and baseline value

A below-average species whose population falls below `KillLimit` is removed.

Historical baseline from S4:

- `KillLimit = 0.2`.

The extinction mechanism must be present even if later experiments deliberately vary the threshold.

### 3.10 Mutation — Exact mechanism; operator details partly unresolved

Mutation changes the finite-history strategy representation. S4 reports:

- `PointAdd = 0.1`;
- `PointRemove = 0.1`;
- `Dupli = 0.001`;
- `RemoveRecursively = 0.001`.

S2 also describes branch addition/removal and reports a mutation ratio of `0.1` in later examples. The exact relationship among these formulations still requires reconstruction before M3.

## 4. Historical baseline currently recovered

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

These values define the initial historical baseline. They are not theoretically sacred constants. After the baseline is reproduced, sensitivity to values such as `d`, `KillLimit`, mutation rates, memory length, and species capacity becomes a scientific question.

## 5. M1 contract

M1 implements only one round of the game and its state number.

### 5.1 Exhaustive payoff table

| Left | Right | Self | Payoffs `(L,R,S)` | State |
|---:|---:|---:|:---|---:|
| 0 | 0 | 0 | `(0,0,0)` | 0 |
| 0 | 0 | 1 | `(3,3,0)` | 1 |
| 0 | 1 | 0 | `(3,0,3)` | 2 |
| 0 | 1 | 1 | `(0,3,3)` | 3 |
| 1 | 0 | 0 | `(0,3,3)` | 4 |
| 1 | 0 | 1 | `(3,0,3)` | 5 |
| 1 | 1 | 0 | `(3,3,0)` | 6 |
| 1 | 1 | 1 | `(0,0,0)` | 7 |

### 5.2 Scientific invariants

M1 must establish:

1. **Binary-label symmetry** — complementing all actions (`0 ↔ 1`) does not change payoffs.
2. **Player-renaming symmetry** — consistently permuting players only permutes the payoff vector.
3. **Total payoff** — every non-unanimous profile distributes exactly `6`; unanimous profiles distribute `0`.
4. **State parity** — `state % 2 == self_action` because self is the least-significant bit.
5. **No semantic smuggling** — neither action is labeled cooperation or defection.

### 5.3 M1 implementation boundary

Permitted:

- immutable representation of one action profile;
- state index `4L + 2R + S`;
- deterministic payoff function;
- tests for source examples and scientific invariants.

Not permitted yet:

- repeated interactions;
- strategy trees;
- species;
- mutation;
- population evolution;
- plots;
- geopolitical extension.

## 6. Reported phenomena to reproduce later

These remain targets, not findings of this repository:

- **P1 — class differentiation:** persistent 2-against-1 exploitation;
- **P2 — temporal differentiation:** rotation of the excluded role, giving equal long-run payoff in the ideal case;
- **P3 — period-`3n` societies:** periodic role differentiation including period 6;
- **P4 — regime replacement:** mutants destabilize previously dominant communication patterns;
- **P5 — diversification and complexification:** multiple communication periods coexist at later stages;
- **P6 — relational dependence:** without left/right distinction the authors report class differentiation but not temporal differentiation.

## 7. Remaining reconstruction ledger

| ID | Unresolved detail | Treatment | Blocks |
|:---|:---|:---|:---|
| A2 | Exact finite-history tree/list matching semantics | Reconstruct from source examples and related papers | M2 |
| A3 | Initial-hand encoding in genotype | Reconstruct from source | M2 |
| A4 | Exact weighting of species triples / same-species combinations | Recover if possible; otherwise explicit reconstruction convention + sensitivity | M3 baseline freeze |
| A5 | Exact mutation operator/location sampling | Reconstruct from source descriptions | M3 |
| A6 | Relationship between S2 mutation `0.1` and S4 named operators | Compare source formulations | M3 baseline freeze |
| A7 | Random-tree initialization distribution | Recover if possible; otherwise explicit reconstruction distribution + sensitivity | M3 baseline freeze |
| A8 | Original random seeds / exact independent-run count | Search archival sources; new multi-seed plan will be declared regardless | M4 |
| A9 | Exact objective criteria for labeling regimes | Define measurable diagnostics before frozen replication | M4 |

None of these uncertainties licenses removing a documented mechanism.

## 8. Stage ladder for this repository

### Stage 1 — recreate

M0–M4 reconstruct the historical experiment using Exact, Reconstructed, and where necessary Estimated components.

### Stage 2 — recombine

After a citable replication release, later published mechanisms may be added when they create a meaningful new experiment. Every imported mechanism must be cited and labeled **Recombined**.

### Stage 3 — invent

Only after the reconstructed and recombined systems are understood do we introduce wholly new mechanisms or theories. These are explicitly labeled **Novel**.

## 9. Strongest defensible statement at M1

> The source-defined one-round coalition mechanism and binary state representation are sufficiently specified to implement exactly: the state number is the binary integer `(left,right,self)`, and the payoff rule rewards the unique matching pair when the profile is non-unanimous. No claim about evolutionary dynamics is yet supported by this repository.
