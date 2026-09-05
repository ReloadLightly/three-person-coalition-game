# Three-person coalition game

> A source-anchored reconstruction of Akiyama & Kaneko's iterated three-person coalition model, built from replication toward recombination and eventually invention.

> **Study status:** Protocol  
> **Standard:** Scientific Repository Standard v1.0.0  
> **Research manifesto:** [`RESEARCH_MANIFESTO.md`](RESEARCH_MANIFESTO.md)  
> **Current milestone:** M3 source reconstruction — species fitness + mutation recovered; **no M3 evolutionary code yet**  
> **Primary claim:** M1–M2 behavior is implemented; the source mechanism for species scoring and the four historical tree mutations is now reconstructed for M3  
> **Reproduction:** `python -m unittest discover -s tests -v`

## Abstract

This repository reconstructs the artificial-life model introduced by Eizo Akiyama and Kunihiko Kaneko for studying the evolution of coalition structure, communication, cooperation, exploitation, and role differentiation in an iterated three-person game. Three players repeatedly choose between two initially meaningless actions; a two-player subgroup earns a payoff only by excluding the third player; finite-history strategies subsequently evolve through population dynamics and mutation.

The project follows a three-stage research ladder: **recreate → recombine → invent**. Stage 1 reconstructs the historical experiment, inferring missing implementation details and estimating missing numerical values where necessary while preserving sourced mechanisms. Stage 2 will combine the reconstructed system with mechanisms from later published work. Stage 3 may introduce genuinely novel mechanisms or theory derived from what Stages 1 and 2 teach us.

M1 and M2 implemented the deterministic stage game, relational state representation, finite-history strategy semantics, and a fixed-position synchronous repeated interaction. The current bounded step adds **documentation only**: the historical species-fitness calculation and the four branch-level mutation operators have been reconstructed before any evolutionary code is written.

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
4. **Contemporary Japanese exposition** — Akiyama, *三人ゲームにおける協力の発生とその進化*, 物性研究 (1995), which gives especially useful detail on the 8-ary strategy coding, mutation rates, and simulation parameters.
5. **Doctoral thesis** — Akiyama, *『動的ゲーム』とゲームのダイナミクス：結託構造とコミュニケーションの進化* (University of Tokyo, 1998), Chapter 18, which explicitly describes the four mutation operators and population-fitness equations.

See [`REPLICATION_PROTOCOL.md`](REPLICATION_PROTOCOL.md) for the source-to-model contract and [`M3_SOURCE_RECONSTRUCTION.md`](M3_SOURCE_RECONSTRUCTION.md) for the current bounded reconstruction.

## 5. Research objectives

| ID | Objective | Operational test | Decision rule |
|:---|:---|:---|:---|
| R1 | Reconstruct the stage game exactly | Exhaustive enumeration of all 8 profiles | Every payoff and state index matches the source contract |
| R2 | Reconstruct finite-history strategy semantics | Source examples + deterministic interaction checks | History/action semantics agree with the recovered algorithm |
| R3 | Reconstruct evolutionary population dynamics | Source mechanisms plus explicit reconstruction choices | No documented mechanism is omitted |
| R4 | Reproduce reported qualitative regimes | Frozen multi-run replication | Evidence supports, fails to support, or leaves each regime unresolved |
| R5 | Separate historical replication from later extensions | Explicit Stage 1/2/3 boundaries | Recombined and novel mechanisms are labeled as such |

## 6. Method recovered so far

The historical model contains four layers:

1. **Stage game** — three players choose `0` or `1`.
2. **Interaction** — the game is repeated; finite-history strategies condition actions on prior relational states.
3. **Ecology** — players with the same strategy form species and receive scores from interactions with the current population.
4. **Evolution** — population shares change with relative score; species go extinct and strategies mutate.

### 6.1 M1 — stage game and state representation

For a focal player, actions are ordered `(left, right, self)` and

\[
\text{state}=4L+2R+S.
\]

If exactly two players choose the same action, the matching pair receives `3` each and the excluded player receives `0`; unanimous profiles give everyone `0`.

### 6.2 M2 — finite-history strategy

The strategy chromosome is an **8-ary tree** assembled from finite state sequences called genes. Later actions are selected by reciprocal prefix matching between the focal player's most-recent-first state history and the tree's maximal genes. The first-round action is stored separately because no history exists yet.

M2 uses maximal gene paths as an action-equivalent representation and implements a fixed-position synchronous repeated interaction.

### 6.3 M3 source reconstruction — species fitness

The thesis defines `g_ijk` as species `i`'s average payoff per round in the repeated three-person interaction with partner species `j` and `k`. Species `i`'s score is

\[
s_i = \sum_j\sum_k g_{ijk}x_jx_k.
\]

Own-species partners are included. Because left and right are distinct strategy inputs, the two partner positions are ordered: `(j,k)` and `(k,j)` are separate terms when the species differ. The population mean is

\[
\bar{s}=\sum_i x_i s_i,
\]

and fitness is `w_i = s_i - \bar{s}` before the already recovered replicator-like population update.

No random-pair approximation or unordered-triple shortcut belongs in the faithful baseline.

### 6.4 M3 source reconstruction — four historical mutations

The detailed sources recover four distinct 8-ary-tree mutations:

| Operator | Rate | Historical structural action |
|:---|---:|:---|
| `PointAdd` | `0.1` | add one absent branch at a node |
| `PointRemove` | `0.1` | remove a terminal branch |
| `Dupli` | `0.001` | attach all eight children to a terminal; source states this is behaviorally neutral when created |
| `RemoveRecursively` | `0.001` | remove a branch together with its entire descendant subtree |

The historical maximum memory/tree depth is `4`.

The precise source reconstruction, including provenance boundaries, is in [`M3_SOURCE_RECONSTRUCTION.md`](M3_SOURCE_RECONSTRUCTION.md).

## 7. Validation

The executable repository still contains the **18 focused M1–M2 tests**. No tests have been added merely for this source-documentation step because no M3 code has been introduced.

Reproduce the existing implementation with:

```bash
python -m unittest discover -s tests -v
```

## 8. Results

### 8.1 Implementation result

The repository currently implements:

- the complete deterministic stage game;
- the relational state index;
- finite-history source-style strategy decisions;
- a fixed-position synchronous repeated interaction.

These are implementation-validation results, not evidence for the paper's evolutionary findings.

### 8.2 Source-reconstruction result

The M3 fitness mechanism and four mutation mechanisms are now sufficiently specified to begin a small evolutionary implementation without inventing their causal structure.

One low-level issue remains explicit rather than hidden: the inspected detailed sources do not clearly specify a global operator ordering when multiple mutation events occur on the same tree in one generation. If archival code does not resolve this, operation order will be labeled **Reconstructed** and checked for sensitivity rather than turned into a new mechanism.

### 8.3 Evolutionary results

No population-level result is reported yet.

Class differentiation, temporal differentiation, period-`3n` societies, regime replacement, and later diversification remain replication targets.

## 9. Interpretation

The source-reconstruction step clarifies an important point: historical fitness is genuinely ecological. A strategy is not scored against a fixed benchmark; its payoff is integrated over the **current population distribution** through `x_j x_k`, including relationally distinct left/right partner arrangements. Mutation likewise changes the evolving communication code itself rather than merely perturbing a scalar parameter.

No claim about international politics follows from this reconstruction.

## 10. Limitations and threats to validity

The main remaining Stage-1 reconstruction issues are random-tree initialization, low-level mutation event ordering/sampling, original seeds/run count, and objective regime-classification criteria. None licenses removal of a documented mechanism.

Important historical parameter values already recovered include `d = 0.2`, `KillLimit = 0.2`, interaction length `1000`, maximum memory `4`, maximum species count `9`, and the four named mutation rates above.

A successful historical replication would establish behavior of this artificial ecology, not validate a model of real states or alliances.

## 11. Reproduction

No external dependency is required for the current M1–M2 implementation.

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
| `M3_SOURCE_RECONSTRUCTION.md` | Bounded M3 species-fitness and mutation reconstruction |
| `three_person_coalition_game/game.py` | M1 stage-game mechanism |
| `three_person_coalition_game/strategy.py` | M2 finite-history decision mechanism |
| `three_person_coalition_game/interaction.py` | M2 fixed-position synchronous interaction |
| `tests/` | M1–M2 source examples and scientific invariants |
| `SCIENTIFIC_REPOSITORY_STANDARD.md` | Governing repository standard |

## 13. Citation

Akiyama, E., & Kaneko, K. (1995). *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*. Artificial Life, 2(3), 293–304. https://doi.org/10.1162/artl.1995.2.3.293

A project-specific `CITATION.cff` will be added when the repository has a citable replication release.

## 14. License and responsible use

A repository license has not yet been selected. No downstream deployment or policy claim is supported by the current artifact.

---

## Current bounded step

**M3 source reconstruction is complete at the mechanism level. No M3 evolutionary code has been written.**

### Explicit non-goals of this step

- no species class implementation;
- no fitness tensor code;
- no mutation code;
- no extinction/population update code;
- no experiments;
- no plots;
- no IR extension.

### Next step

If authorized, the next bounded step is **M3 implementation** of the recovered species-fitness calculation, explicit 8-ary tree mutations, population update, and extinction mechanism — without adding any mechanism beyond the historical model.
