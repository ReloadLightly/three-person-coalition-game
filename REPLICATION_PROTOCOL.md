# Replication protocol

> **Milestone:** M0 — source reconstruction  
> **Status:** Protocol  
> **Implementation permitted after M0:** deterministic stage game and state representation only

This document is the scientific contract for the faithful-replication phase. It records which **concepts and mechanisms** are supported by the sources, which numerical values are historically recovered, and which numerical values may remain explicit reconstruction parameters. Faithfulness applies first to the mechanism. A missing historical constant never licenses deleting a documented mechanism.

## 1. Source hierarchy

| ID | Source | Role | Current use |
|:---|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3):293–304; arXiv `adap-org/9504002` | Primary scientific specification | Highest authority for the original model when inspected directly |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V*, pp. 193–201 | Detailed conference specification and replication target | Directly inspected for M0 |
| **S3** | Akiyama & Kaneko, BIES 1995, pp. 76–83 | Earlier version cited by S2 | Not yet independently inspected |
| **S4** | *三人ゲームにおける協力の発生とその進化*, 物性研究 65-1 (1995-10) | Contemporary detailed Japanese exposition | Used to recover explicit simulation parameter values |

### Fidelity rule

1. **Concepts, mechanisms, and theoretical structure must be source-anchored.** We do not invent a new selection mechanism, coalition rule, strategy representation, mutation mechanism, or explanatory theory and call it a replication.
2. **A documented mechanism must be implemented even when its exact historical numerical value is unknown.** Omitting the mechanism would change the model more fundamentally than choosing a provisional value.
3. **A numerical value has one of two statuses:**
   - **historical baseline** — directly recovered from a source for the relevant experiment;
   - **reconstruction parameter** — explicitly chosen because the mechanism is known but the exact historical value is not yet recovered.
4. Reconstruction parameters are never presented as source facts. They remain configurable and are subjected to sensitivity analysis.
5. Source-recovered numerical values are the baseline for faithful replication, but they are not treated as theoretically privileged constants. Parameter variation is scientifically interesting and belongs in later robustness experiments.
6. If sources disagree on a mechanism or parameter, the discrepancy is documented before the replication baseline is frozen.

## 2. Model skeleton supported by the sources

### 2.1 Players and actions

An interaction contains three players. In each round, every player chooses one of two actions:

\[
a_i \in \{0,1\}.
\]

The symbols `0` and `1` are intentionally symmetric: unlike `C` and `D` in the Prisoner's Dilemma, the source does not assign them intrinsic cooperative or defective meanings.

**Status:** mechanism specified.

### 2.2 Coalition payoff rule

For the three-player action profile:

- if exactly two players choose the same action, those two form a subgroup and each receives **3**;
- the excluded player receives **0**;
- if all three choose the same action, all three receive **0**.

Because there are three players and two actions, these cases exhaust all eight action profiles.

**Status:** mechanism and payoff values specified.

### 2.3 Relational position

The source arranges the three players in a circle and distinguishes a focal player's **left** and **right** partners. The game rule itself retains left/right symmetry, but a strategy is allowed to distinguish these relational positions. The authors later report that removing this ability prevents the emergence of temporal differentiation in their simulations.

**Status:** mechanism specified at the conceptual level.

**Implementation detail still to fix:** exact canonical ordering of `(left, right, self)` when converting an action profile to the integer state used by the strategy representation.

### 2.4 Eight round states

Each round corresponds to one of eight states defined by the binary combination of the three players' hands. From a player's perspective, the history of these states provides the input to the strategy.

**Status:** mechanism specified conceptually; exact indexing convention must be reconstructed before M1 state encoding is frozen.

### 2.5 Iterated interaction

The three-player stage game is repeated until a fixed maximum round count.

Historical baseline recovered from S2/S4:

- **maximum rounds per interaction:** `1000`.

The entire repeated sequence among three players is called an interaction or communication.

**Status:** mechanism specified; baseline value recovered.

### 2.6 Strategy memory

A strategy refers to a finite history of prior round states. Histories can therefore be represented as octonary strings because every round has eight possible states.

Historical baseline recovered from S2/S4:

- **maximum memory length:** `4`;
- **initial species:** `6`;
- **initial strategy memory length:** `1`;
- initial strategy trees are generated randomly.

**Status:** mechanism specified; these experiment-level values are recovered.

### 2.7 Strategy representation

The source describes a strategy as a list/tree over finite octonary history strings. A strategy determines whether the player's next hand is `0` or `1`; the initial hand is also encoded by the strategy.

The paper describes mutation of this tree representation.

**Status:** mechanism specified; exact executable semantics remain partly unresolved.

**Unresolved before M2:** exact matching semantics when multiple stored sequences could match; exact serialization; exact handling of histories shorter than the maximum memory; exact initial-hand genotype encoding.

### 2.8 Species

Players with the same strategy are treated as the same species. Evolution operates on species population fractions.

Historical baseline recovered from S4:

- **maximum number of species:** `9`.

**Status:** mechanism specified; baseline capacity recovered.

### 2.9 Tournament scoring

Within a generation, a player/species participates in the iterated three-person game against possible pairs of other players, including players from its own species. Scores over these interactions determine the species score.

**Status:** mechanism specified; exact weighting/enumeration still requires reconstruction. If exact historical weighting remains unavailable, M3 must implement the documented tournament mechanism with an explicit weighting convention and test sensitivity rather than omit tournament fitness.

### 2.10 Population update

S2 gives a replicator-like update in which the change in species fraction is proportional to the species' excess score over the population mean:

\[
x_i(t+1)-x_i(t) = d\,[s_i-\bar{s}]\,x_i(t),
\]

followed by normalization of the population fractions.

Where:

- `x_i(t)` is the population fraction of species `i`;
- `s_i` is its score;
- `\bar{s}` is the population-average score;
- `d` is the growth constant.

Historical baseline recovered from S4:

- **growth constant:** `d = 0.2`.

**Status:** mechanism and historical baseline recovered.

### 2.11 Extinction

A species whose score is below the population average and whose population falls below a lower bound (`KillLimit`) is eliminated.

Historical baseline recovered from S4:

- **`KillLimit = 0.2`**.

S4 also notes the substantive role of this parameter: lower `KillLimit` permits more strategy variation/species persistence, while computational limits motivated a relatively small maximum species count.

**Status:** mechanism and historical baseline recovered.

### 2.12 Mutation

Mutation changes the strategy tree. S4 reports the following historical simulation settings:

- **`PointAdd = 0.1`**;
- **`PointRemove = 0.1`**;
- **`Dupli = 0.001`**;
- **`RemoveRecursively = 0.001`**.

S2 separately describes a mutation ratio of `0.1` in later examples and states that mutation adds or removes branches.

**Status:** mutation as a mechanism is specified; several historical parameter values are recovered. Exact executable operator semantics and the relationship between S2's generic `0.1` statement and S4's named mutation operations still require reconstruction before M3.

## 3. Historical baseline currently recovered

**Table 1 — Baseline parameter set from the contemporary sources**

| Parameter | Historical baseline | Status |
|:---|---:|:---|
| Maximum rounds | `1000` | Recovered |
| Growth constant `d` | `0.2` | Recovered |
| `KillLimit` | `0.2` | Recovered |
| Maximum memory length | `4` | Recovered |
| Initial species count | `6` | Recovered |
| Initial memory length | `1` | Recovered |
| Maximum species count | `9` | Recovered |
| `PointAdd` | `0.1` | Recovered |
| `PointRemove` | `0.1` | Recovered |
| `Dupli` | `0.001` | Recovered |
| `RemoveRecursively` | `0.001` | Recovered |

These values define the initial historical-replication baseline unless a higher-authority source contradicts them. Later robustness experiments should deliberately vary scientifically meaningful parameters, especially `d`, `KillLimit`, mutation rates, memory length, and species capacity.

## 4. Exhaustive stage-game contract

M1 must reproduce this table exactly before any repeated-game logic is introduced.

| Left | Right | Self | Coalition outcome | Payoffs `(L,R,S)` |
|---:|---:|---:|:---|:---|
| 0 | 0 | 0 | no subgroup | `(0,0,0)` |
| 0 | 0 | 1 | left + right | `(3,3,0)` |
| 0 | 1 | 0 | left + self | `(3,0,3)` |
| 0 | 1 | 1 | right + self | `(0,3,3)` |
| 1 | 0 | 0 | right + self | `(0,3,3)` |
| 1 | 0 | 1 | left + self | `(3,0,3)` |
| 1 | 1 | 0 | left + right | `(3,3,0)` |
| 1 | 1 | 1 | no subgroup | `(0,0,0)` |

### Scientific invariants for M1

1. **Binary-label symmetry:** complementing all three actions (`0 ↔ 1`) leaves payoffs unchanged.
2. **Player-renaming symmetry:** consistently permuting players permutes payoffs but does not change the coalition rule.
3. **Total payoff:** every non-unanimous profile has total payoff `6`; every unanimous profile has total payoff `0`.
4. **No semantic smuggling:** neither `0` nor `1` is labeled cooperation or defection in the faithful replication.

These are scientific invariants, not test-count targets.

## 5. Reported qualitative phenomena to reproduce later

These are **replication targets**, not current findings of this repository.

### P1 — Class differentiation

Early evolution can produce a biased 2-against-1 structure in which one player/species is repeatedly excluded while the other two obtain the coalition payoff.

### P2 — Temporal differentiation

Later strategies can rotate the excluded role through time. In the ideal equal rotation described by the source, each player is excluded in turn and obtains an average payoff of `2`.

### P3 — Period-`3n` cooperative societies

The source reports societies with periodic role differentiation whose period is a multiple of three, including a period-6 example in which players exchange exclusion symmetrically.

### P4 — Breakdown and replacement of dominant periodic regimes

Mutants can exploit or destabilize a currently dominant communication pattern, leading to transitions among different periodic societies.

### P5 — Diversification and complexification

At later stages, multiple communication periods may coexist. The source interprets this as co-evolution of diversity and strategy/interaction complexity.

### P6 — Dependence on relational information

When strategies cannot distinguish left from right, the authors report class differentiation but not temporal differentiation.

## 6. Ambiguity ledger

The purpose of this ledger is to prevent **conceptual/mechanistic invention**, not to freeze the project whenever a tunable number is uncertain.

| ID | Unresolved detail | Why it matters | Resolution path | Blocks |
|:---|:---|:---|:---|:---|
| A1 | Exact binary-to-state indexing from each focal player's perspective | Strategy histories depend on state identity | Compare S1/S2 tables and worked examples | M1 state encoding |
| A2 | Exact octonary tree/list matching semantics | Different matching rules define different strategies | Reconstruct from S1 text/examples; inspect S3 if useful | M2 |
| A3 | Initial-hand encoding in the strategy genotype | Changes transient dynamics | Recover representation from source | M2 |
| A4 | Exact scoring weights for species triples / same-species combinations | Changes fitness landscape | Recover tournament definition; if still ambiguous, expose weighting as a reconstruction parameter and test sensitivity | M3 baseline freeze |
| A5 | Exact mutation operation and location sampling | Changes accessible strategy space | Reconstruct tree mutation procedure from source | M3 |
| A6 | Relationship between S2's generic mutation ratio `0.1` and S4's named mutation operators | Affects historical baseline interpretation | Compare source formulations | M3 baseline freeze |
| A7 | Random-tree initialization distribution | Can affect early evolutionary path | Recover generator or define explicit reconstruction distribution plus sensitivity study | M3 baseline freeze |
| A8 | Number of independent runs / original random seeds | Affects comparison with reported qualitative behavior | Search source/archival material; use a new declared multi-seed plan regardless | M4 |
| A9 | Exact criteria used by authors to label regimes/periods | Needed to avoid subjective replication claims | Define measurable regime diagnostics before frozen run | M4 |

### Resolved during M0

- numerical growth constant: `d = 0.2`;
- extinction threshold: `KillLimit = 0.2`;
- maximum species count: `9`;
- named mutation settings: `PointAdd = 0.1`, `PointRemove = 0.1`, `Dupli = 0.001`, `RemoveRecursively = 0.001`.

## 7. What must not be invented

The prohibition is about changing the **scientific mechanism** while pretending to replicate the paper. We must not:

- invent a different coalition payoff mechanism;
- replace the finite-history strategy system with a generic neural network or unrelated GP representation and call it faithful;
- remove extinction because its threshold is inconvenient;
- remove the growth/selection update because its coefficient is uncertain;
- replace the source mutation mechanism with an unrelated optimizer without labeling it an extension;
- interpret `0` as cooperation and `1` as defection;
- map the three players to named countries inside the faithful replication;
- treat one visually similar trajectory as a successful replication.

What **is** legitimate is to estimate, select, calibrate, or sweep a numerical parameter when its mechanism is source-supported but its exact value is unavailable—provided the value is labeled as a reconstruction choice rather than historical fact.

## 8. Milestone gates

### M0 — Source reconstruction

**Permitted work:** documents only.

**Complete when:**

- source hierarchy is fixed;
- stage-game rule is explicit;
- mechanism fidelity is distinguished from parameter-value uncertainty;
- recovered historical baseline values are recorded;
- reported phenomena are recorded as replication targets rather than findings;
- remaining mechanistic ambiguities are explicit;
- M1 scope is narrow and testable.

### M1 — Stage game + state representation

**Permitted work:**

- immutable representation of one three-player action profile;
- payoff function;
- source-faithful state indexing once A1 is resolved;
- only tests needed to establish the four stage-game invariants and source examples.

**Explicitly forbidden in M1:**

- repeated interactions;
- strategy trees;
- species;
- mutation;
- population evolution;
- plots;
- geopolitical extension.

### M2 — Finite-history strategies

Starts only after M1 is independently checked and A2/A3 are resolved.

### M3 — Evolutionary ecology

Implements **all documented evolutionary mechanisms**: tournament fitness, replicator-like growth, normalization, extinction, species turnover, and mutation. Historical baseline values are used where recovered; any remaining numerical uncertainty becomes explicit configuration plus sensitivity analysis, not a reason to omit a mechanism.

### M4 — Frozen replication

Starts only after exploratory reconstruction choices and regime metrics are frozen.

### M5 — IR extension

Starts only after a citable faithful-replication release exists. Any IR mapping must be a separate experimental layer and must not modify the evidence for the historical replication.

## 9. M0 strongest defensible statement

> The contemporary sources specify the mechanisms of the three-person coalition ecology and now provide a substantial historical baseline parameter set, including `d = 0.2` and `KillLimit = 0.2`. Remaining uncertainty concerns some executable semantics and sampling details; these must be reconstructed explicitly, while numerical uncertainty may be handled through transparent parameter choices and sensitivity analysis without deleting source-supported mechanisms.
