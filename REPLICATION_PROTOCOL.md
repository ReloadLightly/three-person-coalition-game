# Replication protocol

> **Milestone:** M0 — source reconstruction  
> **Status:** Protocol  
> **Implementation permitted after M0:** deterministic stage game and state representation only

This document is the scientific contract for the faithful-replication phase. It records what is supported by the sources, what remains ambiguous, and what must not be invented merely to make the code run.

## 1. Source hierarchy

| ID | Source | Role | Current use |
|:---|:---|:---|:---|
| **S1** | Akiyama & Kaneko (1995), *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3):293–304; arXiv `adap-org/9504002` | Primary scientific specification | Highest authority for the original model when inspected directly |
| **S2** | Akiyama & Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, *Artificial Life V*, pp. 193–201 | Detailed conference specification and replication target | Directly inspected for M0 |
| **S3** | Akiyama & Kaneko, BIES 1995, pp. 76–83 | Earlier version cited by S2 | Not yet inspected; cannot currently resolve disagreements |

### Source rule

1. A mechanism may be marked **specified** only when a source defines it sufficiently for implementation.
2. A numerical value may be marked **fixed** only when a source provides it for the relevant experiment.
3. A plausible reconstruction is not a source fact.
4. If S1 and S2 disagree, the disagreement is recorded before either version is chosen.
5. Any reconstruction choice required for execution must be exposed as such and tested for sensitivity later.

## 2. Model skeleton supported by the sources

### 2.1 Players and actions

An interaction contains three players. In each round, every player chooses one of two actions:

\[
a_i \in \{0,1\}.
\]

The symbols `0` and `1` are intentionally symmetric: unlike `C` and `D` in the Prisoner's Dilemma, the source does not assign them intrinsic cooperative or defective meanings.

**Status:** specified.

### 2.2 Coalition payoff rule

For the three-player action profile:

- if exactly two players choose the same action, those two form a subgroup and each receives **3**;
- the excluded player receives **0**;
- if all three choose the same action, all three receive **0**.

Because there are three players and two actions, these cases exhaust all eight action profiles.

**Status:** specified.

### 2.3 Relational position

The source arranges the three players in a circle and distinguishes a focal player's **left** and **right** partners. The game rule itself retains left/right symmetry, but a strategy is allowed to distinguish these relational positions. The authors later report that removing this ability prevents the emergence of temporal differentiation in their simulations.

**Status:** specified at the conceptual level.

**Implementation detail still to fix:** exact canonical ordering of `(left, right, self)` when converting an action profile to the integer state used by the strategy representation.

### 2.4 Eight round states

Each round corresponds to one of eight states defined by the binary combination of the three players' hands. From a player's perspective, the history of these states provides the input to the strategy.

**Status:** specified conceptually; exact indexing convention must be reconstructed before M1 state encoding is frozen.

### 2.5 Iterated interaction

The three-player stage game is repeated until a fixed maximum round count. The later simulations reported in S2 use:

- **maximum rounds per interaction:** `1000`.

The entire repeated sequence among three players is called an interaction or communication.

**Status:** fixed for the reported S2 simulations.

### 2.6 Strategy memory

A strategy refers to a finite history of prior round states. Histories can therefore be represented as octonary strings because every round has eight possible states.

For the reported simulations S2 states:

- **maximum memory length:** `4`;
- **initial species:** `6`;
- **initial strategy memory length:** `1`;
- initial strategy trees are generated randomly.

**Status:** these experiment-level values are specified.

### 2.7 Strategy representation

The source describes a strategy as a list/tree over finite octonary history strings. A strategy determines whether the player's next hand is `0` or `1`; the initial hand is also encoded by the strategy.

The paper describes branch addition/removal as mutation of this tree representation.

**Status:** partially specified.

**Unresolved before M2:** exact executable semantics for matching a finite current history against the tree/list when multiple stored sequences could match; exact serialization; exact handling of histories shorter than the maximum memory.

### 2.8 Species

Players with the same strategy are treated as the same species. Evolution operates on species population fractions.

**Status:** specified.

### 2.9 Tournament scoring

Within a generation, a player/species participates in the iterated three-person game against possible pairs of other players, including players from its own species. Scores over these interactions determine the species score.

**Status:** concept specified; exact weighting/enumeration requires reconstruction.

### 2.10 Population update

S2 gives a replicator-like update in which the change in species fraction is proportional to the species' excess score over the population mean. Written in equivalent notation:

\[
x_i(t+1)-x_i(t) = \delta\,[s_i-\bar{s}]\,x_i(t),
\]

followed by normalization of the population fractions.

Where:

- `x_i(t)` is the population fraction of species `i`;
- `s_i` is its score;
- `\bar{s}` is the population-average score;
- `\delta` is described as a growth constant.

**Status:** equation specified; numerical `delta` not yet resolved from the inspected S2 text.

### 2.11 Extinction

A species whose score is below the average and whose population falls below a lower bound (`KillLimit` in the source) is eliminated.

**Status:** rule specified; numerical `KillLimit` unresolved in the currently inspected source material.

### 2.12 Mutation

When the population is updated, the paper reports a strategy mutation rate of:

- **mutation ratio:** `0.1` in later examples.

Mutation changes the strategy tree by adding or removing a branch.

**Status:** rate specified for later examples; exact operator semantics are only partially specified.

## 3. Exhaustive stage-game contract

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

## 4. Reported qualitative phenomena to reproduce later

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

## 5. Ambiguity ledger

No item in this table may be silently filled with a convenient default.

| ID | Unresolved detail | Why it matters | Resolution path | Blocks |
|:---|:---|:---|:---|:---|
| A1 | Exact binary-to-state indexing from each focal player's perspective | Strategy histories depend on state identity | Compare S1/S2 tables and worked examples | M1 state encoding |
| A2 | Exact octonary tree/list matching semantics | Different matching rules define different strategies | Reconstruct from S1 text/examples; inspect S3 if necessary | M2 |
| A3 | Initial-hand encoding in the strategy genotype | Changes transient dynamics | Recover exact representation from source | M2 |
| A4 | Exact scoring weights for species triples / same-species combinations | Changes fitness and selection pressure | Recover tournament definition mathematically from S1 | M3 |
| A5 | Numerical growth constant `delta` | Changes population dynamics and extinction timing | Search S1/S3 and any author code/material | M3 |
| A6 | Numerical `KillLimit` | Changes diversity and persistence | Search S1/S3 and any author code/material | M3 |
| A7 | Exact mutation operation and location sampling | Changes accessible strategy space | Reconstruct tree mutation procedure from source | M3 |
| A8 | Whether mutation probability `0.1` is per species, per reproduction/update, or another unit | Changes effective mutation rate | Resolve exact wording in S1/S3 | M3 |
| A9 | Random-tree initialization distribution | Can affect early evolutionary path | Recover generator or define explicit reconstruction sensitivity study | M3 |
| A10 | Number of independent runs / original random seeds | Determines what constitutes faithful statistical reproduction | Search source and archival material | M4 |
| A11 | Exact criteria used by authors to label regimes/periods | Needed to avoid subjective replication claims | Derive measurable definitions before frozen run | M4 |

## 6. What M0 deliberately does not infer

The following tempting choices are prohibited at this stage:

- setting `delta = 1` because it is convenient;
- choosing an arbitrary extinction threshold;
- treating species triples as uniformly weighted without source support;
- implementing a generic genetic-programming tree and calling it the original strategy representation;
- interpreting `0` as cooperation and `1` as defection;
- mapping the three players to named countries;
- treating one visually similar trajectory as a successful replication.

## 7. Milestone gates

### M0 — Source reconstruction

**Permitted work:** documents only.

**Complete when:**

- source hierarchy is fixed;
- stage-game rule is explicit;
- known experiment parameters are separated from unresolved parameters;
- reported phenomena are recorded as replication targets rather than findings;
- ambiguity ledger exists;
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

Starts only after the population update, tournament weighting, extinction, and mutation semantics are source-anchored or explicitly designated reconstruction choices.

### M4 — Frozen replication

Starts only after exploratory reconstruction choices and regime metrics are frozen.

### M5 — IR extension

Starts only after a citable faithful-replication release exists. Any IR mapping must be a separate experimental layer and must not modify the evidence for the historical replication.

## 8. M0 strongest defensible statement

> The available source material specifies a minimal deterministic three-player coalition game and enough of its evolutionary architecture to define a replication program, but several implementation-critical details remain unresolved and therefore should not yet be guessed in code.

That is the only scientific claim this repository is intended to support at M0.
