# M3d — species-capacity sensitivity

> **Status:** completed exploratory sensitivity step  
> **Stage:** Stage 1 — recreate  
> **Claim boundary:** diagnose sensitivity to species capacity; do not infer the historical full-cap code or claim historical regime replication

M3c exposed a concrete validity problem: the reconstructed ecology reached the historical maximum of nine species within 3–4 generations and then blocked hundreds of novel mutants. M3d asks whether that is merely a bookkeeping edge case or whether species capacity materially changes the evolutionary trajectory.

## 1. Source finding before the experiment

A final source check did **not** recover the original at-cap code path.

What the 1995 Japanese exposition does say is unusually informative:

- the historical simulation sets **maximum species = 9**;
- larger maximum species should increase strategy variation and reduce the risk of evolution getting stuck at a local peak;
- larger populations of species are computationally expensive because three-person matchups scale much more sharply than two-person games;
- the authors therefore treat maximum species partly as a computational constraint, not as a theoretically sacred constant.

Primary source:

- Akiyama, *三人ゲームにおける協力の発生とその進化* (1995): https://repository.kulib.kyoto-u.ac.jp/dspace/bitstream/2433/95610/1/KJ00004737253.pdf

The same source explains that mutation occurs at generation change and a mutant receives 10% of its parent species' population, but it does not state what happens if a novel mutant is proposed while every species slot is occupied.

Therefore M3d does **not** invent a replacement-at-cap mechanism.

## 2. Experimental question

> **If we keep all reconstructed bookkeeping fixed but relax only the species-capacity parameter, do the short evolutionary trajectories materially change?**

This is a sensitivity test, not a candidate historical reconstruction.

The historical value `9` remains the baseline. Values `12` and `18` are deliberately nonhistorical capacity variants motivated by the source's own statement that a larger maximum should permit more strategy variation.

## 3. Matched design

The same three starting seed pairs used in M3c are reused:

- `(7, 11)`;
- `(17, 23)`;
- `(29, 31)`.

Each capacity condition restarts from the same initial and mutation seeds. Once different capacity constraints admit different mutants, the random streams naturally diverge because the populations themselves diverge; the comparison is therefore **matched at initialization**, not a claim of identical mutation events after divergence.

| Component | Values |
|:---|:---|
| generations | `25` |
| max species | `9`, `12`, `18` |
| rounds per seating | `1000` |
| seatings per matchup | `2` |
| growth constant | `0.2` |
| `KillLimit` | `0.2` |
| mutant share | `0.10` |
| at-cap behavior | block novel mutant — held fixed |
| outer mutation scheduler | one local pass per surviving species — held fixed |
| initialization reconstruction | root branches `p=0.5`, first action `p=0.5` — held fixed |

The experiment is reproducible with:

```bash
python -m experiments.m3d_capacity_sensitivity
```

## 4. Results

### 4.1 Run-level summary

| Capacity | Seeds | Cap first reached | Extinctions | New mutants | Blocked | Final mean score | Final dominant share | Final depth |
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

Raw summary evidence: [`evidence/m3d_capacity_sensitivity.json`](evidence/m3d_capacity_sensitivity.json).

The experiment script also regenerates generation-level diagnostics at `evidence/m3d_capacity_sensitivity.csv`.

### 4.2 Capacity materially changes the ecology

The comparison is not numerically cosmetic.

At capacity `9`, the `17/23` trajectory enters the zero-payoff ecology observed in M3c and ends at mean score `0.0`.

At capacity `12`, that same seeded reconstruction still ends at `0.0`.

At capacity `18`, it no longer does: its final mean score is approximately `1.1611`, maximum memory reaches depth `4`, and 83 novel mutants are admitted during the 25 generations.

That is a **qualitative capacity dependence** in one matched starting condition.

### 4.3 Larger capacity increases realized variation

Across the three runs:

| Capacity | New mutants admitted | Mutants blocked | Mean final score | Mean extinctions |
|---:|---:|---:|---:|---:|
| `9` | 61 | 504 | 0.7783 | 17.3 |
| `12` | 94 | 642 | 0.5773 | 26.0 |
| `18` | 232 | 728 | 1.0918 | 65.3 |

The source's qualitative expectation is therefore visible in the reconstruction: larger capacity permits substantially more realized mutant variation.

But the important surprise is that even capacity `18` still saturates in every run and continues to block many proposals.

## 5. Interpretation

M3d establishes two things.

First, the species-capacity choice is **scientifically consequential**. It changes admitted mutation, extinction, chromosome depth, final mean payoff, and in one seed pair whether the ecology remains trapped at zero payoff.

Second, merely increasing capacity does **not** make the bookkeeping problem disappear. All three capacity-18 runs still reach the cap within 5–7 generations, and 728 proposals are blocked across those three runs.

This suggests that the next uncertainty is no longer only the value `9`. The interaction between capacity and the still-Reconstructed **outer mutation scheduler** is now the most plausible next target.

## 6. What M3d does not establish

M3d does not tell us:

- what the historical source code did at exactly nine occupied species slots;
- whether capacity `12` or `18` is "better";
- whether any condition reproduces class differentiation or temporal differentiation;
- which condition looks most like the published historical trajectory.

We deliberately do not select a reconstruction by visual resemblance to the target paper.

## 7. Stop condition

M3d is complete because the question that motivated it has a clear answer:

> **Yes. The short-run evolutionary behavior is materially sensitive to species capacity, and the cap remains heavily active even when doubled from 9 to 18.**

The next bounded scientific question should therefore move one level upstream: recover or sensitivity-test the **outer mutation scheduler** before M4 is frozen.
