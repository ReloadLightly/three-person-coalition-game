# Replication protocol

> **Current milestone:** M2 — finite-history strategies + deterministic interaction  
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
| **S4** | Akiyama, *三人ゲームにおける協力の発生とその進化*, 物性研究 65-1 (1995) | Contemporary detailed exposition; strategy coding and simulation parameters |
| **S5** | Akiyama (1998), *『動的ゲーム』とゲームのダイナミクス：結託構造とコミュニケーションの進化*, University of Tokyo doctoral thesis, especially Chapter 18 | Detailed later exposition of the same three-person model |

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

## 3. Model skeleton

### 3.1 Players and actions — Exact

Each interaction contains three players. In each round every player chooses one of two symmetric actions:

\[
a_i \in \{0,1\}.
\]

The historical white card corresponds to `1`; black corresponds to `0`. These symbols do **not** intrinsically mean cooperation and defection.

### 3.2 Coalition payoff — Exact

- If exactly two players choose the same action, those two form the subgroup and each receives `3`.
- The excluded player receives `0`.
- If all three choose the same action, all three receive `0`.

### 3.3 Relational position — Exact

Players are placed around a circle. From each focal player's perspective the other actors are distinguished as **left** and **right**. For global counter-clockwise order `(player1, player2, player3)`, the left neighbour of player `i` is `i+1` and the right neighbour is `i-1`, modulo three.

### 3.4 State indexing — Exact; resolved in M1

The source defines the state digits as `(left, right, self)`, so

\[
\text{state}=4L+2R+S.
\]

The worked examples confirm the interpretation, including `(0,1,1) -> 3` and `(1,0,1) -> 5` from a rotated perspective.

### 3.5 Iterated interaction — Exact mechanism

The stage game is synchronous and repeated for a fixed number of rounds. Every player's next action depends only on states from earlier rounds, so all three next actions are selected before the current round state is appended to history.

Historical baseline:

- maximum rounds per interaction: `1000`.

The full historical tournament later swaps relational positions and evaluates species combinations. M2 implements only one fixed-position repeated interaction; tournament scheduling belongs to M3.

### 3.6 Finite-history strategy coding — Exact semantics; reconstructed Python representation

S4/S5 describe the strategy chromosome as an **8-ary tree** assembled from one or more finite state sequences called **genes**. A gene is therefore a path such as `12`, `150`, `157`, or `43` through the eight possible prior states.

The source explicitly states the following decision algorithm:

1. Construct `B` from the focal player's prior states in **most-recent-first** order: one round ago, two rounds ago, three rounds ago, and so on. For example, if those states are `5`, `5`, `4`, then `B = 554`.
2. Extract the tree's non-completely-overlapping genes `A1...An`.
3. Compare `B` against every gene from the start of each sequence. If either sequence completely contains the other from the root — equivalently, if one is a prefix of the other — play **white/card 1**. Otherwise play **black/card 0**.

The source gives an explicit example: `B = 3546` and gene `A = 35` produce white/card `1`.

The reciprocal prefix rule is important: it defines behavior even when the interaction history is still shorter than the strategy's nominal memory length.

The source further states that when genes completely overlap from the root, the **shorter gene is replaced by the longer one**. Thus the action-relevant chromosome can be represented by its maximal root-to-terminal gene paths.

M2 stores those maximal paths directly rather than materializing an explicit node object for every 8-ary branch. This is a **Reconstructed representation preserving Exact action semantics**. M3 will revisit explicit tree topology only where branch-level mutation requires it.

### 3.7 Initial action — Exact mechanism

Each strategy separately contains the information needed to choose its card in the first round, before any history exists.

M2 therefore stores `initial_action` independently of the gene paths. The source supports the separation, although the exact historical in-memory serialization is not available and is irrelevant to the decision semantics.

### 3.8 Species and population ecology — Exact mechanism

Players with the same strategy form a species. Species scores determine changes in population fraction.

Historical baseline from S4:

- maximum number of species: `9`.

### 3.9 Population update — Exact mechanism and baseline value

\[
x_i(t+1)-x_i(t)=d\,[s_i-\bar{s}]\,x_i(t),
\]

followed by normalization.

Historical baseline:

- `d = 0.2`.

### 3.10 Extinction — Exact mechanism and baseline value

A below-average species whose population falls below `KillLimit` is removed.

Historical baseline:

- `KillLimit = 0.2`.

### 3.11 Mutation — Exact mechanism; operator details partly unresolved

S4 reports:

- `PointAdd = 0.1`;
- `PointRemove = 0.1`;
- `Dupli = 0.001`;
- `RemoveRecursively = 0.001`.

The mutation mechanism is known, but exact branch/operator sampling still belongs to M3 reconstruction.

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

These values define the historical baseline, not theoretically privileged constants. Sensitivity analysis comes after baseline reproduction.

## 5. Completed M1 contract

M1 established the exact one-round payoff mechanism and state representation:

- all eight action profiles;
- binary-label symmetry;
- player-renaming symmetry;
- total payoff `6` for non-unanimous profiles and `0` for unanimous profiles;
- state parity `state % 2 == self_action`;
- source indexing examples.

Implementation: `three_person_coalition_game/game.py`.

## 6. M2 contract

M2 adds only the deterministic strategy/interaction layer required before any ecology or evolution.

### 6.1 Strategy object

A strategy contains:

- `initial_action in {0,1}`;
- zero or more maximal genes, each a non-empty sequence of states `0...7`.

The current representation is intentionally minimal. It is the action-equivalent terminal-path representation of the historical 8-ary chromosome, not a generic GP tree.

### 6.2 Decision rule

For non-empty chronological history `H`:

\[
B = \operatorname{reverse}(H).
\]

Then

\[
a(H)=
\begin{cases}
1 & \text{if } \exists g:\; g \preceq B \;\text{or}\; B \preceq g\\
0 & \text{otherwise,}
\end{cases}
\]

where `x <= y` denotes a root-prefix relation. With empty history, use `initial_action`.

### 6.3 Gene overlap rule

If one gene is a strict root-prefix of another, retain the longer gene. Exact duplicates collapse to one path. Shared partial prefixes such as `150` and `157` remain distinct.

### 6.4 Fixed-position interaction

M2 also implements a synchronous fixed-position repeated interaction:

1. each strategy chooses from its own prior focal-state history;
2. the three actions are committed simultaneously;
3. each player receives its relationally indexed state and payoff;
4. those states are appended to the three histories;
5. repeat.

No species, fitness, mutation, extinction, population update, or tournament scheduling enters M2.

### 6.5 M2 validation targets

The tests protect source semantics rather than test count:

- separately encoded first action;
- memory-1 decision behavior;
- source example `B=3546`, gene `35` -> card `1`;
- reciprocal prefix matching for short transient histories;
- non-match -> card `0`;
- shorter overlapping gene replaced by longer gene;
- source gene set `12,150,157,43` is representable;
- fixed-position perspective mapping from the source's unambiguous first round;
- synchronous repeated interaction under simple deterministic strategies;
- invalid actions, states, player counts, and round counts rejected.

## 7. Reported phenomena to reproduce later

These remain replication targets, not findings:

- **P1 — class differentiation**;
- **P2 — temporal differentiation**;
- **P3 — period-`3n` societies**;
- **P4 — regime replacement**;
- **P5 — diversification and complexification**;
- **P6 — relational dependence**.

## 8. Remaining reconstruction ledger

| ID | Unresolved detail | Treatment | Blocks |
|:---|:---|:---|:---|
| A4 | Exact weighting/scheduling of species triples and positional permutations | Recover from S4/S5; otherwise explicit reconstruction convention + sensitivity | M3 baseline freeze |
| A5 | Exact mutation operator and branch/location sampling | Reconstruct from S4/S5 mutation description | M3 |
| A6 | Relationship between S2 mutation `0.1` and S4 named operators | Compare source formulations | M3 baseline freeze |
| A7 | Random-tree initialization distribution | Recover if possible; otherwise explicit reconstruction distribution + sensitivity | M3 baseline freeze |
| A8 | Original random seeds / exact independent-run count | Search archival sources; new multi-seed plan declared regardless | M4 |
| A9 | Objective criteria for labeling regimes | Define measurable diagnostics before frozen replication | M4 |

### Resolved in M2

- **A2 — finite-history matching semantics:** reciprocal root-prefix matching recovered from S4/S5.
- **A3 — initial-hand mechanism:** source explicitly stores first-round action separately from finite-history strategy. Exact byte-level serialization is unnecessary for semantic replication.

None of the remaining uncertainties licenses removing a documented mechanism.

## 9. Stage ladder for this repository

### Stage 1 — recreate

M0–M4 reconstruct the historical experiment using Exact, Reconstructed, and where necessary Estimated components.

### Stage 2 — recombine

After a citable replication release, later published mechanisms may be added when they create a meaningful new experiment. Every imported mechanism is cited and labeled **Recombined**.

### Stage 3 — invent

Only after the reconstructed and recombined systems are understood do we introduce wholly new mechanisms or theories, labeled **Novel**.

## 10. Strongest defensible statement at M2

> The source now specifies enough of the finite-history strategy mechanism to reproduce its decision semantics: strategies consist of a separate first action and an 8-ary gene tree, while later actions are determined by reciprocal prefix matching between recent-first state history and maximal gene paths. The repository implements this mechanism and fixed-position deterministic interaction, but no evolutionary or population-level claim is yet evaluated.
