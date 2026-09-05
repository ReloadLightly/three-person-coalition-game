# Three-person coalition game

> A source-anchored replication of Akiyama & Kaneko's iterated three-person coalition model, built slowly enough that every implemented mechanism can be traced to the original study.

> **Study status:** Protocol  
> **Standard:** Scientific Repository Standard v1.0.0  
> **Current milestone:** M0 — source reconstruction  
> **Primary claim:** Not yet evaluated  
> **Reproduction:** Not yet available

## Abstract

This repository aims to faithfully reconstruct the artificial-life model introduced by Eizo Akiyama and Kunihiko Kaneko for studying the evolution of coalition structure, communication, cooperation, exploitation, and role differentiation in an iterated three-person game. The original model is deliberately minimal: three players repeatedly choose between two initially meaningless actions; a two-player subgroup can earn a payoff only by excluding the third player; finite-memory strategies evolve through selection and mutation. The reported simulations move through qualitatively different social regimes, including persistent class differentiation, temporal rotation of the excluded role, and later diversification of communication patterns.

The project begins with a **replication-first** objective. M0 contains no simulator and reports no findings. It reconstructs the paper's scientific contract, distinguishes source-supported mechanisms from numerical parameter choices, and fixes the source hierarchy that will govern later implementation. A geopolitical or international-relations interpretation is intentionally deferred until the original mechanism has been independently reproduced.

## 1. Research question

**Primary replication question.**

> Does a faithful reimplementation of Akiyama & Kaneko's deterministic three-person coalition model reproduce the reported emergence of class differentiation, temporal role differentiation, and later diversification of coalition/communication patterns?

A later extension may ask whether the mechanism illuminates coalition formation and flexible alignment in decentralized international systems. That is **not** part of the current replication claim.

## 2. Why this matters

The model is unusually interesting for computational international relations because coalition structure is endogenous. With three actors, more than one coalition is possible; actors can be included or excluded, coalitions can change, and communication strategies can evolve in response to the strategic ecology.

The attraction is not an analogy in which countries are relabeled artificial organisms. The scientific opportunity is narrower: first understand a minimal mechanism that generates changing coalition structures from decentralized strategic interaction, then test whether a carefully specified IR extension preserves or breaks that mechanism.

## 3. Contributions

At the current **Protocol** stage, this repository makes only two contributions:

1. **Replication protocol.** A source-to-model reconstruction of the original experiment that distinguishes mechanism fidelity from parameter uncertainty.
2. **Artifact design.** A deliberately small executable-paper structure in which later code, experiments, evidence, and claims will remain traceable to the sources.

There are no empirical or methodological novelty claims yet.

## 4. Primary sources

The source hierarchy is fixed for the replication phase:

1. **Journal/preprint specification** — Eizo Akiyama & Kunihiko Kaneko, *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3), 293–304 (1995). DOI: https://doi.org/10.1162/artl.1995.2.3.293. Public preprint: https://arxiv.org/abs/adap-org/9504002.
2. **ALife V proceedings version** — Eizo Akiyama & Kunihiko Kaneko, *Evolution of Communication and Strategies in an Iterated Three-Person Game*, in *Artificial Life V: Proceedings of the Fifth International Workshop on the Synthesis and Simulation of Living Systems*.
3. **Earlier BIES version** — cited by the ALife V paper as *Evolution of cooperation, differentiation, complexity, and diversity in an iterated three-person game*, BIES 1995, pp. 76–83. This source has not yet been independently inspected in this repository.
4. **Contemporary Japanese detailed exposition** — *三人ゲームにおける協力の発生とその進化*, 物性研究 65-1 (1995-10), used in M0 to recover several explicit simulation parameter values.

Where sources differ, the discrepancy must be documented before implementation changes.

## 5. Research objectives

**Table 1 — Replication objectives and decision rules**

| ID | Objective | Operational test | Decision rule |
|:---|:---|:---|:---|
| R1 | Reconstruct the stage game exactly | Exhaustive enumeration of all 8 action profiles | Every payoff matches the source-defined coalition rule |
| R2 | Reconstruct finite-history strategy semantics | Hand-worked trajectories from source examples | State/history/action transitions agree exactly |
| R3 | Reconstruct evolutionary population dynamics | Source-derived mechanisms plus explicit parameterization | No source mechanism is omitted; source values are used when recovered, while uncertain values remain explicit tunable parameters |
| R4 | Reproduce reported qualitative regimes | Frozen multi-run replication | Evidence supports, fails to support, or leaves each regime unresolved |
| R5 | Separate replication from IR extension | Release boundary before any geopolitical remapping | No IR-specific variable enters the faithful replication |

## 6. Method

The original system contains four conceptual layers:

1. **Stage game** — three players choose action `0` or `1`.
2. **Interaction** — the stage game is repeated; strategies condition actions on finite histories of prior three-player states.
3. **Ecology** — players sharing a strategy form a species; species receive scores from interactions with other strategy combinations.
4. **Evolution** — population shares change with relative score and strategies mutate.

The replication rule is strict about **mechanisms**, not dogmatic about numerical constants. A mechanism documented by the source must be implemented even when its exact historical parameter value is unknown. When a value is source-recovered, it becomes the historical baseline; when it is not, the implementation uses an explicitly labeled reconstruction value and later tests sensitivity to that choice. Missing a number is never a reason to delete the mechanism.

M0 does not yet implement these layers. See [`REPLICATION_PROTOCOL.md`](REPLICATION_PROTOCOL.md).

## 7. Evidence protocol

The replication will follow this order:

1. source reconstruction;
2. deterministic game checks;
3. deterministic strategy checks;
4. evolutionary-mechanism reconstruction;
5. minimal exploratory calibration and parameter sensitivity where needed;
6. frozen replication runs;
7. robustness analysis;
8. only then, a separately labeled IR extension.

Exploratory observations will not be promoted into confirmatory findings.

## 8. Results

No results are reported at M0.

The repository contains no simulator, no experiment run, and no evidence bundle yet.

## 9. Interpretation

The model is promising for later IR work because it allows coalition structure and role allocation to emerge rather than prescribing a permanent alliance pattern. That observation motivates the project but is not itself an empirical result about international politics.

## 10. Limitations and threats to validity

The immediate replication risks concern exact executable semantics more than the existence of the model's mechanisms. Several details still require reconstruction, including state indexing, strategy-tree matching, tournament weighting, and exact mutation operator semantics.

Two parameter values that were initially unresolved from the ALife V proceedings have now been recovered from a contemporary Japanese exposition of the model: **growth constant `d = 0.2`** and **`KillLimit = 0.2`**. The same source also reports `max-round = 1000`, `MaxMemoryLength = 4`, maximum species count `9`, and mutation-related settings `PointAdd = 0.1`, `PointRemove = 0.1`, `Dupli = 0.001`, and `RemoveRecursively = 0.001`. These are historical baseline values, not sacred constants: robustness experiments should deliberately vary them after faithful baseline reproduction.

A second risk is conceptual overreach. Even a successful replication would establish behavior of this artificial ecology, not a validated model of states, alliances, or geopolitics.

## 11. Reproduction

Not yet available. M0 deliberately contains no executable model.

## 12. Repository map

| Path | Scientific role |
|:---|:---|
| `README.md` | Compact paper and current scientific status |
| `REPLICATION_PROTOCOL.md` | Source-to-model contract, parameter provenance, ambiguity ledger, and milestone gates |
| `SCIENTIFIC_REPOSITORY_STANDARD.md` | Pinned governing standard for repository development |

No empty implementation directories are created at M0.

## 13. Citation

The scientific model being replicated should be cited to the original authors:

Akiyama, E., & Kaneko, K. (1995). *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*. Artificial Life, 2(3), 293–304. https://doi.org/10.1162/artl.1995.2.3.293

A project-specific `CITATION.cff` will be added when the repository has a citable implementation or release.

## 14. License and responsible use

A repository license has not yet been selected at M0. No downstream deployment or policy claim is supported by the current artifact.

---

## Current milestone: M0

M0 is complete when the source hierarchy, formal model skeleton, known parameters, explicitly reconstructable parameters, replication targets, and M1 boundary are inspectable and internally consistent.

### Explicit non-goals for M0

- no Python package;
- no simulator;
- no evolutionary loop;
- no figures presented as results;
- no CI or infrastructure layer;
- no Japan/China/US relabeling;
- no claim that the model already explains international relations.

### Next milestone

**M1 will implement only the deterministic three-person stage game and its state representation.**

If M1 cannot be explained line by line from the source contract, it is not ready to merge.
