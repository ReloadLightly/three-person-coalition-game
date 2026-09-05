# Three-person coalition game

> A source-anchored reconstruction of Akiyama & Kaneko's iterated three-person coalition model, built from replication toward recombination and eventually invention.

> **Study status:** Protocol  
> **Standard:** Scientific Repository Standard v1.0.0  
> **Research manifesto:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)  
> **Current milestone:** M2 — finite-history strategies + deterministic interaction  
> **Primary claim:** The stage game, state representation, and source-defined finite-history decision mechanism are reconstructed; no evolutionary claim is yet evaluated  
> **Reproduction:** `python -m unittest discover -s tests -v`

## Abstract

This repository reconstructs the artificial-life model introduced by Eizo Akiyama and Kunihiko Kaneko for studying the evolution of coalition structure, communication, cooperation, exploitation, and role differentiation in an iterated three-person game. Three players repeatedly choose between two initially meaningless actions; a two-player subgroup earns a payoff only by excluding the third player; finite-history strategies subsequently evolve through population dynamics and mutation.

The project follows a three-stage research ladder: **recreate → recombine → invent**. Stage 1 reconstructs the historical experiment, inferring missing implementation details and estimating missing numerical values where necessary while preserving the sourced mechanisms. Stage 2 will combine the reconstructed system with mechanisms from later published work. Stage 3 may introduce genuinely novel mechanisms or theory derived from what Stages 1 and 2 teach us.

M2 remains deliberately small. It adds the historical finite-history strategy semantics and one fixed-position synchronous repeated interaction. It still does **not** implement species ecology, tournament fitness, mutation, extinction, or population evolution.

## 1. Research question

**Primary replication question.**

> Does a faithful reconstruction of Akiyama & Kaneko's three-person evolutionary game reproduce the reported emergence of class differentiation, temporal role differentiation, and later diversification of coalition/communication patterns?

A later extension may ask whether the mechanism illuminates coalition formation and flexible alignment in decentralized international systems. That is **not** part of the current replication claim.

## 2. Why this matters

The model is unusually interesting for computational international relations because coalition structure is endogenous. With three actors, more than one coalition is possible; actors can be included or excluded, coalitions can change, and communication strategies can evolve in response to the strategic ecology.

The attraction is not an analogy in which countries are relabeled artificial organisms. The stronger route is to first understand the minimal ALife mechanism, then deliberately recombine it with later mechanisms, and only after that decide whether a genuinely new computational-IR construction is warranted.

## 3. Research manifesto

This repository follows [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md):

1. **Stage 1 — Recreate.** Recover the original mechanism. Exact code if available; reconstruct implementation when the mechanism is described but code is unavailable; estimate or sweep numerical values when the mechanism is known but the historical value is missing.
2. **Stage 2 — Recombine.** Add mechanisms from other cited experiments when doing so creates a meaningful new scientific question.
3. **Stage 3 — Invent.** Introduce new concepts, mechanisms, or theories only after Stages 1 and 2 provide enough understanding to motivate them.

The provenance vocabulary is: **Exact**, **Reconstructed**, **Estimated**, **Recombined**, **Novel**.

## 4. Primary sources

1. **Journal/preprint specification** — Eizo Akiyama & Kunihiko Kaneko, *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3), 293–304 (1995). DOI: https://doi.org/10.1162/artl.1995.2.3.293. Public preprint: https://arxiv.org/abs/adap-org/9504002.
2. **ALife V proceedings version** — Eizo Akiyama & Kunihiko Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, in *Artificial Life V*.
3. **Earlier BIES version** — cited by the ALife V paper, BIES 1995, pp. 76–83.
4. **Contemporary Japanese exposition** — Akiyama, *三人ゲームにおける協力の発生とその進化*, 物性研究 65-1 (1995), which gives especially useful detail on the 8-ary strategy coding and simulation parameters.
5. **Doctoral thesis** — Akiyama, *『動的ゲーム』とゲームのダイナミクス：結託構造とコミュニケーションの進化* (University of Tokyo, 1998), which gives a detailed later exposition of the same model.

See [`REPLICATION_PROTOCOL.md`](REPLICATION_PROTOCOL.md) for the source-to-model contract.

## 5. Research objectives

| ID | Objective | Operational test | Decision rule |
|:---|:---|:---|:---|
| R1 | Reconstruct the stage game exactly | Exhaustive enumeration of all 8 profiles | Every payoff and state index matches the source contract |
| R2 | Reconstruct finite-history strategy semantics | Source examples + deterministic interaction checks | History/action semantics agree with the recovered algorithm |
| R3 | Reconstruct evolutionary population dynamics | Source mechanisms plus explicit reconstruction choices | No documented mechanism is omitted |
| R4 | Reproduce reported qualitative regimes | Frozen multi-run replication | Evidence supports, fails to support, or leaves each regime unresolved |
| R5 | Separate historical replication from later extensions | Explicit Stage 1/2/3 boundaries | Recombined and novel mechanisms are labeled as such |

## 6. Method

The historical model contains four layers:

1. **Stage game** — three players choose `0` or `1`.
2. **Interaction** — the game is repeated; finite-history strategies condition actions on prior relational states.
3. **Ecology** — players with the same strategy form species and receive scores from interactions.
4. **Evolution** — population shares change with relative score; species go extinct and strategies mutate.

### 6.1 M1 — stage game and state representation

For a focal player, actions are ordered `(left, right, self)`. The source defines

\[
\text{state}=4L+2R+S.
\]

If exactly two players choose the same action, the matching pair receives `3` each and the excluded player receives `0`; unanimous profiles give everyone `0`.

### 6.2 M2 — finite-history strategy

The detailed contemporary sources describe each strategy as an **8-ary tree** assembled from finite state sequences called **genes**. Examples include `12`, `150`, `157`, and `43`.

To choose the next card, the source constructs a state-history sequence `B` in **most-recent-first** order. It compares `B` against every maximal gene from the root. If either the gene is a prefix of `B` or `B` is a prefix of the gene, the player chooses **white/card 1**. Otherwise it chooses **black/card 0**.

The source gives the explicit example:

```text
B = 3546
A = 35
=> white / card 1
```

This reciprocal prefix rule also explains how the strategy produces an action during the early transient when the available history is shorter than its nominal memory length.

The source separately stores the **first-round action**, because no prior state exists yet.

### 6.3 M2 representation choice

The historical chromosome is an 8-ary tree. For M2 action selection, the tree is represented by its **maximal gene paths**. This is behaviorally equivalent for the recovered decision rule and avoids introducing branch-level machinery before mutation requires it.

When one gene is a complete root-prefix of another, the source keeps the longer one. Partial sharing is preserved: `150` and `157`, for example, remain separate genes.

This representation is labeled **Reconstructed**; the decision rule itself is **Exact** from the source description.

### 6.4 Fixed-position repeated interaction

M2 additionally implements the smallest synchronous repeated-game loop:

1. each of the three strategies chooses from its own prior focal-state history;
2. all three current actions are committed simultaneously;
3. the source-defined focal state and payoff are computed for each player;
4. the three histories are updated;
5. repeat.

The historical tournament's position swapping and species scheduling are deliberately deferred to M3.

## 7. Validation

The repository now contains **18 focused tests** across M1 and M2.

M1 protects the exact payoff and state-indexing contract. M2 additionally checks:

- the separately encoded first action;
- memory-1 behavior;
- the source prefix example `3546` vs `35`;
- shorter transient history matching a longer gene;
- non-match → card `0`;
- longer-gene replacement under complete overlap;
- representation of the source gene set `12, 150, 157, 43`;
- the source's unambiguous first-round relational orientation;
- simple synchronous repeated interactions;
- invalid state/action/player/round inputs.

Reproduce with:

```bash
python -m unittest discover -s tests -v
```

## 8. Results

### 8.1 M1–M2 implementation result

The repository now reconstructs:

- the complete deterministic stage game;
- the relational state index;
- finite-history source-style strategy decisions;
- a fixed-position synchronous repeated interaction.

These are **implementation-validation results**, not evidence for the paper's evolutionary findings.

### 8.2 Evolutionary results

No population-level result is reported yet.

Class differentiation, temporal differentiation, period-`3n` societies, regime replacement, and later diversification remain replication targets.

## 9. Interpretation

M2 is the first point where the system acquires genuine behavioral memory. The action is not a label such as "cooperate" or "defect"; it is generated from a player's recent **relational history**. The 8-ary tree therefore acts as a compact evolving communication/response code over sequences of social states.

That is already conceptually much richer than an ordinary fixed payoff matrix, but it still supports no claim about international politics.

## 10. Limitations and threats to validity

The major remaining reconstruction risks are now downstream: exact tournament weighting and positional permutations, branch-level mutation semantics, random strategy initialization, and the eventual criteria for classifying social regimes.

Important historical parameter values have already been recovered, including `d = 0.2`, `KillLimit = 0.2`, maximum interaction length `1000`, maximum memory `4`, maximum species count `9`, and named mutation settings. Missing values will become explicit **Estimated** parameters and sensitivity experiments rather than excuses to remove mechanisms.

A successful historical replication would establish behavior of this artificial ecology, not validate a model of real states or alliances.

## 11. Reproduction

No external dependency is required at M2.

```bash
git clone https://github.com/ReloadLightly/three-person-coalition-game.git
cd three-person-coalition-game
python -m unittest discover -s tests -v
```

## 12. Repository map

| Path | Scientific role |
|:---|:---|
| `README.md` | Compact paper and current study status |
| `RESEARCH_MANIFESTO.md` | Research ladder: recreate → recombine → invent |
| `REPLICATION_PROTOCOL.md` | Source-to-model contract and reconstruction ledger |
| `three_person_coalition_game/game.py` | M1 stage-game mechanism |
| `three_person_coalition_game/strategy.py` | M2 finite-history decision mechanism |
| `three_person_coalition_game/interaction.py` | M2 fixed-position synchronous interaction |
| `tests/test_game.py` | M1 source examples and invariants |
| `tests/test_strategy.py` | M2 strategy semantics |
| `tests/test_interaction.py` | M2 relational/repeated-interaction checks |
| `SCIENTIFIC_REPOSITORY_STANDARD.md` | Governing repository standard |

## 13. Citation

Akiyama, E., & Kaneko, K. (1995). *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*. Artificial Life, 2(3), 293–304. https://doi.org/10.1162/artl.1995.2.3.293

A project-specific `CITATION.cff` will be added when the repository has a citable replication release.

## 14. License and responsible use

A repository license has not yet been selected. No downstream deployment or policy claim is supported by the current artifact.

---

## Current milestone: M2

**M2 is implemented:** finite-history strategy semantics and a fixed-position deterministic repeated interaction now sit on top of the validated M1 stage game.

### Explicit non-goals retained at M2

- no species ecology;
- no tournament fitness;
- no mutation implementation;
- no extinction;
- no population evolution;
- no result plots;
- no geopolitical relabeling.

### Next milestone

**M3 — evolutionary ecology.**

Before implementation, we will reconstruct the historical species-triple scheduling/weighting and branch-level mutation semantics from the detailed sources. If some low-level coding details remain unavailable, we will infer the mechanism and expose uncertain values or choices explicitly rather than omitting the mechanism.
