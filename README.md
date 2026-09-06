# Three-person coalition game

**Reconstructing Akiyama & Kaneko's artificial-life ecology, one source-anchored mechanism at a time.**

[Method](#6-method) · [Experiment](#7-experimental-design) · [Evidence](#8-results) · [Reproduce](#11-reproduction) · [Research manifesto](RESEARCH_MANIFESTO.md)

**Table 1 — Study at a glance**

| Field | Current state |
|:---|:---|
| Study status | **Exploratory sensitivity** |
| Milestone | **M3d** — species-capacity sensitivity completed |
| Supported claim | Species capacity materially changes the short evolutionary trajectory; historical long-run regimes are **not yet reproduced** |
| Verification | `python -m unittest discover -s tests -v` |
| M3d experiment | `python -m experiments.m3d_capacity_sensitivity` |

## Abstract

This repository reconstructs the artificial-life model developed by Eizo Akiyama and Kunihiko Kaneko to study coalition structure, communication, exploitation, cooperation, and role differentiation in an iterated three-person game. Three players repeatedly choose between two symmetric actions. When exactly two actions match, those players receive a payoff and the third receives none. Strategies use finite histories of relational states and are encoded by an 8-ary chromosome. Strategy classes form species whose population shares change through ecological fitness, extinction, and mutation.

M1–M3b reconstructed the stage game, finite-history strategy, two-seating repeated interaction, explicit chromosome, ecological fitness, relative selection, extinction, initialization, mutation, and mutant birth. M3c then ran three 25-generation exploratory trajectories and discovered that the historical maximum of nine species becomes active almost immediately: the current Reconstructed full-cap rule blocked 504 novel mutants across only 75 generations.

**M3d tests that validity threat directly.** The historical capacity `9` is compared with larger sensitivity values `12` and `18`, using the same starting seed pairs and keeping every other reconstructed bookkeeping choice fixed. The 1995 source explicitly says larger species capacity should increase strategy variation but is computationally expensive. The experiment confirms that capacity materially changes the ecology — including whether one seeded trajectory remains trapped at zero payoff — while also showing that even capacity `18` saturates quickly.

## 1. Research question

**Does a faithful reconstruction reproduce the reported transition from class differentiation to temporal role differentiation and, later, diversified coalition/communication regimes?**

M3d asks a narrower validity question first:

> **How strongly does the reconstructed evolutionary trajectory depend on species capacity, given that the historical source fixes capacity at nine but does not preserve the full-cap program logic?**

## 2. Why this matters

The model is unusually attractive for artificial-life approaches to international relations because **coalition structure is endogenous**. Coalition membership, exclusion, role allocation, and communication emerge from decentralized interaction rather than being hard-coded as a permanent alliance graph.

But before using the model for anything new, the historical artificial ecology has to be trustworthy. M3c showed that one unresolved bookkeeping detail was exercised constantly; M3d therefore tests that detail before any attempt at confirmatory replication.

## 3. Contributions at the current stage

1. **Source reconstruction.** Original papers, Akiyama's detailed Japanese exposition, and his thesis are translated into an executable mechanism with provenance labels.
2. **Multi-generation executable ecology.** Historical-style interaction, selection, extinction, mutation, and species birth run across generations.
3. **Capacity-sensitivity evidence.** The historical capacity `9` is compared against larger source-motivated sensitivity variants without changing the underlying mutation or selection mechanisms.
4. **Explicit uncertainty.** The historical value `9` remains Exact while the at-cap bookkeeping remains Reconstructed.
5. **Executable-paper structure.** Question, method, evidence, interpretation, limitations, and reproduction remain visible in the repository itself.

## 4. Primary sources

- **Akiyama & Kaneko (1995)** — *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*, *Artificial Life* 2(3), 293–304.
- **Akiyama & Kaneko (Artificial Life V)** — *Evolution of Communication and Strategies in an Iterated Three-Person Game*.
- **Akiyama (1995)** — *三人ゲームにおける協力の発生とその進化*, the detailed contemporary Japanese exposition used for repeated-game order, initialization, mutation transfer, and simulation parameters.
- **Akiyama (1998)** — doctoral thesis, especially the chapter describing the dynamic three-person game, population fitness, and mutation operators.

The 1995 Japanese exposition explicitly sets maximum species to `9`, argues that a larger maximum should increase strategy variation, and explains that larger species sets are expensive in a three-person game. It does **not** state what the original program did when a novel mutant was proposed while all species slots were occupied.

See [REPLICATION_PROTOCOL.md](REPLICATION_PROTOCOL.md), [M3_SOURCE_RECONSTRUCTION.md](M3_SOURCE_RECONSTRUCTION.md), [M3B_SOURCE_RECONSTRUCTION.md](M3B_SOURCE_RECONSTRUCTION.md), and [M3D_CAPACITY_SENSITIVITY.md](M3D_CAPACITY_SENSITIVITY.md).

## 5. Research objectives

**Table 2 — Replication objectives**

| ID | Objective | Operational test | Current status |
|:---|:---|:---|:---|
| R1 | Reconstruct stage game | Exhaust all 8 action profiles | **Implemented** |
| R2 | Reconstruct finite-history strategy | Source examples + deterministic trajectories | **Implemented** |
| R3 | Reconstruct evolutionary population dynamics | Source equations + mutation + species turnover | **Implemented; sensitivity testing active** |
| R4 | Reproduce historical evolutionary regimes | Frozen multi-seed experiment with objective diagnostics | Not yet run |
| R5 | Separate replication from later extension | Explicit Stage 1/2/3 provenance | Active |

## 6. Method

```mermaid
flowchart LR
    A["Stage game<br/>0 / 1"] --> B["Relational state<br/>4L + 2R + S"]
    B --> C["Finite-history strategy<br/>8-ary chromosome"]
    C --> D["Two seatings per trio<br/>A,B,C ↔ A,C,B"]
    D --> E["Ecological fitness<br/>gᵢⱼₖ → sᵢ"]
    E --> F["Growth + extinction<br/>d, KillLimit"]
    F --> G["Tree mutation<br/>4 operators"]
    G --> H["Mutant birth<br/>10% parent mass"]
    H --> I["Species capacity<br/>historical max = 9"]
    I --> J["Normalize<br/>next generation"]
    J --> D
```

### 6.1 Stage game and relational state

$$
\mathrm{state}=4L+2R+S.
$$

Exactly two matching actions earn `3` each; the excluded player earns `0`. Unanimous profiles yield `0` for all three.

### 6.2 Finite-history strategy

The strategy is an 8-ary tree of finite state sequences. History is read most-recent-first. Card `1` is selected when the available history and at least one maximal gene are reciprocal-prefix compatible; otherwise the strategy selects `0`. The first action is stored separately.

### 6.3 Historical interaction and ecological fitness

Each three-strategy matchup is played for `1000` rounds, then the partner positions are exchanged and a second fresh `1000`-round interaction is played.

For focal species `i` and partner species `j,k`,

$$
s_i=\sum_j\sum_k g_{ijk}x_jx_k,
$$

with own-species partners included. Population mean and relative fitness are

$$
\bar{s}=\sum_i x_i s_i,
\qquad
w_i=s_i-\bar{s}.
$$

Population growth is

$$
x_i(t+1)-x_i(t)=d\,w_i\,x_i(t),
\qquad d=0.2.
$$

A below-average species that falls below `KillLimit = 0.2` is removed.

### 6.4 Mutation and mutant birth

The historical chromosome mutates through `PointAdd`, `PointRemove`, `Dupli`, and `RemoveRecursively`. An admitted mutant receives

$$
0.10\,x_{parent}
$$

of its parent's post-selection population, and the parent loses exactly that amount. Final normalization follows mutation transfer.

### 6.5 Exact computational acceleration

Cycle skipping and deterministic matchup caching eliminate repeated computation without changing the 1000-round historical interaction or any model parameter. The accelerated evaluator is checked against explicit round-by-round execution.

## 7. Experimental design

### M3d — capacity sensitivity at matched starting seeds

M3d first revisited the source. The full-cap code path remains unavailable. Instead of inventing replacement logic, the experiment holds the current conservative `block_novel_mutant_when_full` rule fixed and varies only the species-capacity parameter.

**Table 3 — M3d configuration**

| Component | Values | Provenance |
|:---|:---|:---|
| generations | `25` | exploratory design |
| seed pairs `(initial, mutation)` | `(7,11)`, `(17,23)`, `(29,31)` | matched starting seeds |
| maximum species | `9`, `12`, `18` | `9` **Exact**; `12/18` sensitivity variants |
| rounds per seating | `1000` | **Exact** |
| seatings per matchup | `2` | **Exact** |
| growth constant | `0.2` | **Exact** |
| `KillLimit` | `0.2` | **Exact** |
| mutant share | `0.10` | **Exact** |
| full-cap behavior | block novel mutant | **Reconstructed**, held fixed |
| outer mutation scheduler | one local pass per surviving species | **Reconstructed**, held fixed |
| random memory-1 initialization | Bernoulli `0.5` branches/action | **Reconstructed**, held fixed |

Each capacity condition restarts from the same initial and mutation seeds. Once the capacity conditions admit different mutants, their random streams naturally diverge because the populations diverge; this is therefore a **matched-start sensitivity design**, not identical post-divergence mutation histories.

## 8. Results

### 8.1 Run-level capacity sensitivity

**Table 4 — M3d trajectory summary**

| Cap | Seeds | Cap reached | Extinctions | New | Blocked | Final mean score | Final dominant share | Final depth |
|---:|:---|---:|---:|---:|---:|---:|---:|---:|
| `9` | `7/11` | 4 | 12 | 15 | 184 | 1.5141 | 0.3118 | 2 |
| `9` | `17/23` | 3 | 4 | 7 | 187 | 0.0000 | 0.3715 | 3 |
| `9` | `29/31` | 4 | 36 | 39 | 133 | 0.8209 | 0.4348 | 3 |
| `12` | `7/11` | 4 | 39 | 43 | 196 | 0.6993 | 0.5070 | 4 |
| `12` | `17/23` | 3 | 4 | 10 | 247 | 0.0000 | 0.3575 | 3 |
| `12` | `29/31` | 5 | 35 | 41 | 199 | 1.0326 | 0.3919 | 3 |
| `18` | `7/11` | 5 | 56 | 68 | 268 | 0.7262 | 0.4319 | 4 |
| `18` | `17/23` | 7 | 71 | 83 | 226 | 1.1611 | 0.4029 | 4 |
| `18` | `29/31` | 6 | 69 | 81 | 234 | 1.3882 | 0.2869 | 3 |

### 8.2 Aggregate variation increases with capacity

**Table 5 — Aggregate M3d diagnostics**

| Cap | Admitted new mutants | Blocked mutants | Mean final score | Mean extinctions |
|---:|---:|---:|---:|---:|
| `9` | `61` | `504` | `0.7783` | `17.3` |
| `12` | `94` | `642` | `0.5773` | `26.0` |
| `18` | `232` | `728` | `1.0918` | `65.3` |

The source's qualitative expectation is visible: larger species capacity permits substantially more realized strategy variation.

But larger capacity does **not** make the constraint disappear. All three capacity-18 runs still reach the cap by generation 5–7 and together block 728 proposals.

### 8.3 One qualitative trajectory changes

The `17/23` reconstruction is especially informative:

- cap `9` → final mean score `0.0000`;
- cap `12` → final mean score `0.0000`;
- cap `18` → final mean score `1.1611`, with evolved memory depth `4`.

So species capacity can change not just mutation counts but the qualitative ecological outcome of a matched starting condition.

### 8.4 Evidence artifacts

- [`evidence/m3d_capacity_sensitivity.json`](evidence/m3d_capacity_sensitivity.json) — complete run-level results;
- `evidence/m3d_capacity_sensitivity.csv` — generated generation-level diagnostics when the experiment is rerun.

### 8.5 Historical evolutionary result

**Not yet evaluated.** Class differentiation, temporal differentiation, period-`3n` societies, regime replacement, and later diversity remain the Stage-1 replication targets.

## 9. Interpretation

M3d answers the immediate validity question: **species capacity is scientifically consequential** in the current reconstruction.

The historical value `9` cannot simply be treated as an innocuous computational constant. It limits realized mutation strongly enough to alter payoff trajectories, extinction, chromosome depth, and — for one starting condition — whether the ecology escapes a zero-payoff state.

At the same time, raising the cap to `18` still produces rapid saturation. That points upstream to the next unresolved implementation choice: the **outer mutation scheduler**. If every surviving species is currently generating a local mutation pass each generation more aggressively than the historical implementation did, increasing capacity alone can never solve the problem.

## 10. Limitations and threats to validity

The priority ordering after M3d is now:

1. **outer mutation scheduler** — Reconstructed and now the strongest candidate explanation for persistent cap saturation;
2. **exact full-cap bookkeeping** — still unrecovered, although capacity sensitivity is now quantified;
3. **random memory-1 initialization / first-action generator** — Reconstructed;
4. **combined mutation-operator order** — Reconstructed;
5. **historical seeds / run count** — unresolved;
6. **objective diagnostics for class vs temporal differentiation and later diversity** — must be frozen before M4.

M3d deliberately does not choose a capacity or bookkeeping rule because it produces the most paper-like trajectory.

## 11. Reproduction

No external dependency is required.

```bash
git clone https://github.com/ReloadLightly/three-person-coalition-game.git
cd three-person-coalition-game
python -m unittest discover -s tests -v
python -m experiments.m3d_capacity_sensitivity
```

The M3d command regenerates the JSON summary and generation-level CSV from the fixed seed pairs.

## 12. Repository map

**Table 6 — Scientific artifact map**

| Path | Scientific role |
|:---|:---|
| `README.md` | Compact executable paper |
| `RESEARCH_MANIFESTO.md` | recreate → recombine → invent |
| `REPLICATION_PROTOCOL.md` | current source-to-model and experiment contract |
| `M3_SOURCE_RECONSTRUCTION.md` | pre-M3a ecological/mutation reconstruction |
| `M3B_SOURCE_RECONSTRUCTION.md` | initialization, positional swap, mutant-birth reconstruction |
| `M3D_CAPACITY_SENSITIVITY.md` | source finding + M3d sensitivity design and interpretation |
| `three_person_coalition_game/` | executable historical reconstruction |
| `experiments/m3c_25_generations.py` | short trajectory pilot |
| `experiments/m3d_capacity_sensitivity.py` | species-capacity sensitivity experiment |
| `evidence/m3c_*` | M3c trajectory evidence |
| `evidence/m3d_capacity_sensitivity.json` | M3d run-level evidence |
| `tests/` | source examples and scientific invariants |

## 13. Citation

Akiyama, E., & Kaneko, K. (1995). *Evolution of Cooperation, Differentiation, Complexity, and Diversity in an Iterated Three-Person Game*. *Artificial Life*, 2(3), 293–304.

A project-specific `CITATION.cff` will be added when the historical replication reaches a citable release.

## 14. Next bounded step

**M3e — recover or sensitivity-test the outer mutation scheduler before M4.**

The question is now whether the historical program generated mutation proposals as aggressively as our current one-pass-per-surviving-species reconstruction. We should resolve that from the sources if possible; if not, compare only a tiny set of defensible scheduling reconstructions under the same historical mechanisms and matched starting seeds.
