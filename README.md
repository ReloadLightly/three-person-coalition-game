# Three-person coalition game

> A source-anchored reconstruction of Akiyama & Kaneko's iterated three-person coalition model, built from replication toward recombination and eventually invention.

> **Study status:** Protocol  
> **Standard:** Scientific Repository Standard v1.0.0  
> **Research manifesto:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)  
> **Current milestone:** M1 — deterministic stage game + state representation  
> **Primary claim:** The one-round coalition payoff and state-indexing mechanism are reproduced; no evolutionary claim is yet evaluated  
> **Reproduction:** `python -m unittest discover -s tests -v`

## Abstract

This repository reconstructs the artificial-life model introduced by Eizo Akiyama and Kunihiko Kaneko for studying the evolution of coalition structure, communication, cooperation, exploitation, and role differentiation in an iterated three-person game. The original model is deliberately minimal: three players repeatedly choose between two initially meaningless actions; a two-player subgroup can earn a payoff only by excluding the third player; finite-memory strategies evolve through population dynamics and mutation.

The project follows a three-stage research ladder: **recreate → recombine → invent**. Stage 1 reconstructs the historical experiment, inferring missing implementation details and estimating missing numerical values when necessary while preserving the sourced mechanisms. Stage 2 will deliberately combine the reconstructed system with mechanisms from later published work. Stage 3 may introduce genuinely novel mechanisms or theory derived from what the earlier stages teach us.

M1 is intentionally tiny. It implements only one deterministic round of the original game plus the source-defined binary state representation. It does not yet implement repeated interaction, strategy trees, species, mutation, or population evolution.

## 1. Research question

**Primary replication question.**

> Does a faithful reconstruction of Akiyama & Kaneko's three-person evolutionary game reproduce the reported emergence of class differentiation, temporal role differentiation, and later diversification of coalition/communication patterns?

A later extension may ask whether the mechanism illuminates coalition formation and flexible alignment in decentralized international systems. That is **not** part of the current replication claim.

## 2. Why this matters

The model is unusually interesting for computational international relations because coalition structure is endogenous. With three actors, more than one coalition is possible; actors can be included or excluded, coalitions can change, and communication strategies can evolve in response to the strategic ecology.

The attraction is not an analogy in which countries are relabeled artificial organisms. The scientific opportunity is narrower and stronger: first understand a minimal mechanism that generates changing coalition structures from decentralized interaction, then test what happens when that mechanism is recombined with later ideas, and only after that consider genuinely new theoretical constructions.

## 3. Research manifesto

This repository follows [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md):

1. **Stage 1 — Recreate.** Recover the original mechanism. Exact code if available; reconstruct implementation when the mechanism is described but code is unavailable; estimate or sweep numerical values when the mechanism is known but the historical value is missing.
2. **Stage 2 — Recombine.** Add mechanisms from other cited experiments when doing so creates a meaningful new scientific question.
3. **Stage 3 — Invent.** Introduce new concepts, mechanisms, or theories only after Stages 1 and 2 provide enough understanding to motivate them.

The provenance vocabulary is: **Exact**, **Reconstructed**, **Estimated**, **Recombined**, **Novel**.

## 4. Primary sources

1. **Journal/preprint specification** — Eizo Akiyama & Kunihiko Kaneko, *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3), 293–304 (1995). DOI: https://doi.org/10.1162/artl.1995.2.3.293. Public preprint: https://arxiv.org/abs/adap-org/9504002.
2. **ALife V proceedings version** — Eizo Akiyama & Kunihiko Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, in *Artificial Life V: Proceedings of the Fifth International Workshop on the Synthesis and Simulation of Living Systems*.
3. **Earlier BIES version** — cited by the ALife V paper as *Evolution of cooperation, differentiation, complexity, and diversity in an iterated three-person game*, BIES 1995, pp. 76–83.
4. **Contemporary Japanese exposition** — *三人ゲームにおける協力の発生とその進化*, 物性研究 65-1 (1995-10), used to recover additional simulation parameters.

See [`REPLICATION_PROTOCOL.md`](REPLICATION_PROTOCOL.md) for the source-to-model contract.

## 5. Research objectives

| ID | Objective | Operational test | Decision rule |
|:---|:---|:---|:---|
| R1 | Reconstruct the stage game exactly | Exhaustive enumeration of all 8 profiles | Every payoff and state index matches the source contract |
| R2 | Reconstruct finite-history strategy semantics | Hand-worked source trajectories | State/history/action transitions agree |
| R3 | Reconstruct evolutionary population dynamics | Source mechanisms plus explicit reconstruction choices | No documented mechanism is omitted |
| R4 | Reproduce reported qualitative regimes | Frozen multi-run replication | Evidence supports, fails to support, or leaves each regime unresolved |
| R5 | Separate historical replication from later extensions | Explicit Stage 1/2/3 boundaries | Recombined and novel mechanisms are labeled as such |

## 6. Method

The historical model contains four layers:

1. **Stage game** — three players choose `0` or `1`.
2. **Interaction** — the game is repeated; finite-memory strategies condition actions on prior three-player states.
3. **Ecology** — players with the same strategy form species and receive scores from interactions.
4. **Evolution** — population shares change with relative score; species go extinct and strategies mutate.

### 6.1 M1 implementation

M1 implements only the first layer.

For a focal player, the three actions are ordered `(left, right, self)`. The source defines the eight round states as the binary representation of those actions, hence

\[
\text{state} = 4L + 2R + S.
\]

If exactly two players choose the same action, the matching pair receives `(3,3)` and the excluded player receives `0`. If all three choose the same action, all receive `0`.

**M1 provenance:**

| Component | Status |
|:---|:---|
| Two symmetric actions `{0,1}` | **Exact** |
| Coalition payoff rule | **Exact** |
| `(left,right,self)` relational ordering | **Exact** |
| Binary state index `4L + 2R + S` | **Exact** |
| Python implementation | New reconstruction artifact implementing the exact mechanism |

## 7. M1 validation

The implementation is protected by six focused tests rather than broad infrastructure. They establish:

- all eight source-defined payoff profiles;
- the source indexing example `011₂ → state 3` and the rotated perspective `101₂ → state 5`;
- binary-label symmetry;
- player-renaming symmetry;
- total payoff `6` for non-unanimous profiles and `0` for unanimous profiles;
- rejection of non-binary actions.

Reproduce locally with:

```bash
python -m unittest discover -s tests -v
```

The current M1 test suite passes all six tests.

## 8. Results

### 8.1 M1 implementation result

The deterministic one-round model now reproduces the complete eight-profile payoff table and the source-defined binary state representation.

This is an **implementation-validation result**, not evidence about the evolutionary claims of the original paper.

### 8.2 Evolutionary results

No repeated-game or evolutionary result is reported yet.

Class differentiation, temporal differentiation, period-`3n` societies, regime replacement, and later diversification remain future replication targets.

## 9. Interpretation

M1 establishes the smallest trustworthy building block of the experiment. A state is not merely a payoff outcome: it is a **relationally indexed observation from one actor's perspective**, preserving which other actor is left and which is right. That distinction later matters because the authors report that removing left/right information prevents temporal role differentiation.

No claim about international politics follows from M1.

## 10. Limitations and threats to validity

The remaining reconstruction risks lie downstream of the stage game: exact finite-history tree semantics, initial-hand encoding, tournament weighting, mutation operator details, random-tree initialization, and later regime classification.

Several important numerical values have already been recovered, including `d = 0.2`, `KillLimit = 0.2`, maximum interaction length `1000`, maximum memory `4`, maximum species count `9`, and named mutation settings. Missing numerical values will not cause mechanisms to be omitted; they will become explicit **Estimated** parameters and sensitivity experiments if necessary.

A successful historical replication would establish behavior of this artificial ecology, not validate a model of real states or alliances.

## 11. Reproduction

No external dependency is required for M1.

```bash
git clone https://github.com/ReloadLightly/three-person-coalition-game.git
cd three-person-coalition-game
python -m unittest discover -s tests -v
```

## 12. Repository map

| Path | Scientific role |
|:---|:---|
| `README.md` | Compact paper and current study status |
| `RESEARCH_MANIFESTO.md` | Portfolio research ladder: recreate → recombine → invent |
| `REPLICATION_PROTOCOL.md` | Source-to-model contract, provenance, historical parameters, unresolved reconstruction details |
| `three_person_coalition_game/game.py` | M1 executable stage-game mechanism |
| `tests/test_game.py` | M1 source examples and scientific invariants |
| `SCIENTIFIC_REPOSITORY_STANDARD.md` | Governing repository standard |

## 13. Citation

Akiyama, E., & Kaneko, K. (1995). *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*. Artificial Life, 2(3), 293–304. https://doi.org/10.1162/artl.1995.2.3.293

A project-specific `CITATION.cff` will be added when the repository has a citable replication release.

## 14. License and responsible use

A repository license has not yet been selected. No downstream deployment or policy claim is supported by the current artifact.

---

## Current milestone: M1

**M1 is complete at the implementation level:** the deterministic stage game and state representation are implemented and validated.

### Explicit non-goals retained at M1

- no repeated interactions;
- no strategy-tree implementation;
- no species ecology;
- no mutation;
- no population evolution;
- no result plots;
- no geopolitical relabeling.

### Next milestone

**M2 — finite-history strategies.**

Before writing that code, we will reconstruct the strategy-tree matching semantics and initial-action encoding from the source evidence. We will infer executable details where the mechanism is clear rather than freezing the project over unavailable historical code.
