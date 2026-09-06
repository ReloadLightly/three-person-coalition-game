# M3b source reconstruction — initialization, seat swapping, and mutant birth

> **Status:** implemented as a one-generation integration milestone  
> **Scope:** Stage 1 — recreate  
> **Claim boundary:** this document supports one historical-style generation transition, not the paper's long-run evolutionary results

M3a reconstructed the ecological score, relative-fitness population dynamics, extinction, and the four 8-ary-tree mutation operators. M3b closes the next generation-level gap: how a historical population is initialized, how a three-species matchup is positionally evaluated, and how mutation transfers population from parent to mutant.

The governing rule is [RESEARCH_MANIFESTO.md](RESEARCH_MANIFESTO.md): source-defined mechanisms are preserved; missing low-level code is reconstructed explicitly rather than silently replaced or omitted.

## 1. Sources decisive for M3b

The most useful detailed source is Akiyama's 1995 Japanese exposition, *三人ゲームにおける協力の発生とその進化* (物性研究 65-1), together with the 1995/1996 English papers and Akiyama's later doctoral thesis.

Primary public source:

- https://repository.kulib.kyoto-u.ac.jp/dspace/bitstream/2433/95610/1/KJ00004737253.pdf

## 2. Two positional seatings per matchup — Exact

The detailed source states that the three-person game is first repeated for `max-round` in one clockwise player order. After that interaction ends, two players exchange positions — the source gives the example `A,B,C → A,C,B` — and the trio repeats another `max-round` interaction.

Therefore a focal strategy must be evaluated against both partner orientations, with fresh histories for the second interaction.

For focal `i` and partner strategies `j,k`, M3b evaluates

$$
g_{ijk}
=
\frac{G(i,j,k)+G(i,k,j)}{2},
$$

where each `G` is itself the focal player's average payoff across `1000` rounds in one fixed seating.

**Provenance:** **Exact mechanism**.

### Correction to M3a

M3a evaluated only one fixed seating inside each tensor entry. Because the ecological double sum already contains both `(j,k)` and `(k,j)` with equal population weights, this did not necessarily change aggregate `s_i`; nevertheless, the individual historical matchup was not represented faithfully. M3b corrects the tensor entry itself.

## 3. Historical initial population — Exact mechanism and population values

The detailed source states that the simulation begins with:

- **six species**;
- each species given the **same population `1.0 / 6`**;
- each species using a **randomly generated tree-coding within memory length 1**.

These parts are **Exact**.

## 4. Random memory-1 generator — Reconstructed executable detail

The source does not preserve the original PRNG or a line-by-line random-tree generator.

Generation-0 branch statistics provide an unusually strong clue: the paper reports an average of `2048` represented branches out of `4096` possible expanded length-4 histories. Its own random-comparison column corresponds to a 50/50 branch probability.

M3b therefore reconstructs a random memory-1 strategy as follows:

1. for each of the eight root states `0...7`, include the corresponding one-state gene independently with probability `0.5`;
2. draw the separately stored first action from Bernoulli `0.5`;
3. resample exact duplicates until six distinct species exist, because identical strategies define one species.

The mechanism **random memory-1 initialization** is Exact. The Bernoulli implementation and first-action distribution are **Reconstructed**.

## 5. Mutant population transfer — Exact

The source explicitly states that when mutation occurs at a generation transition:

- the mutant receives **10% of the population of its parent species**;
- the parent species loses the same **10%**;
- after growth/extinction and mutation have been processed, the population is normalized so total population equals 1.

Historical mutant share:

$$
m=0.10.
$$

For parent mass `p`, a novel admitted mutant therefore receives `0.1p` while the parent retains `0.9p` before final normalization.

**Provenance:** **Exact mechanism and value**.

## 6. One mutation proposal per surviving species — Reconstructed bookkeeping

The four local mutation operators and their per-branch/node rates are source-recovered. The inspected material does not preserve the exact outer loop by which mutant proposals are scheduled across species.

M3b uses the narrowest executable reconstruction:

> Each species that survives selection/extinction receives one local `Chromosome.mutate(...)` pass during the generation transition. Newly created mutants do not mutate again in that same generation.

All proposals are generated from the post-selection population snapshot, and each 10% transfer is calculated from the parent's pre-mutation mass. This avoids arbitrary dependence of transfer size on species iteration order.

**Provenance:** **Reconstructed**.

## 7. Identical mutant strategies merge — Exact implication

The model defines a species by strategy identity. Therefore if a mutant chromosome is identical to an already represented chromosome, it is not a new species; its transferred population is added to the existing species.

**Provenance:** species identity is **Exact**; merging is the direct executable implication.

## 8. Maximum species count = 9 — Exact value; at-cap rule Reconstructed

The historical baseline explicitly sets the maximum number of species to `9`.

The inspected source does not specify what the original program did when a novel mutant was proposed while all nine species slots were occupied.

M3b adopts the conservative rule:

> If a novel mutant is proposed at the cap, the mutant is not inserted and no parent population is transferred.

This preserves the source-defined capacity without inventing an unsupported replacement tournament.

**Provenance:** maximum `9` is **Exact**; `block_novel_mutant_when_full` is **Reconstructed** and must be sensitivity-tested before a confirmatory long-run replication.

## 9. Generation order now implemented

The M3b one-generation pipeline is:

1. evaluate all species matchups, including the source-required second seating;
2. compute population-weighted species scores;
3. apply relative-fitness growth with `d = 0.2`;
4. remove below-average species that fall below `KillLimit = 0.2`;
5. generate mutant proposals from surviving species;
6. transfer 10% parent population to admitted/merged mutants;
7. normalize total population to 1.

The source explicitly places normalization after the mutation transfer. M3b therefore exposes an unnormalized `selection_step(...)` instead of normalizing too early.

## 10. One bounded experiment

The first M3b experiment executes **exactly one generation**, then stops.

Configuration:

| Item | Value | Provenance |
|:---|---:|:---|
| initial species | `6` | Exact |
| initial population each | `1/6` | Exact |
| initial memory length | `1` | Exact |
| initial root-branch probability | `0.5` | Reconstructed |
| initial first-action probability | `0.5` | Reconstructed |
| rounds per seating | `1000` | Exact |
| seatings per matchup | `2` | Exact |
| growth constant | `0.2` | Exact |
| KillLimit | `0.2` | Exact |
| mutant share | `0.10` | Exact |
| maximum species | `9` | Exact |
| initial RNG seed | `7` | new reproducibility choice |
| mutation RNG seed | `11` | new reproducibility choice |

Raw evidence is written to [`evidence/m3b_one_generation.json`](evidence/m3b_one_generation.json).

## 11. What this experiment can establish

It can establish that the reconstructed system now executes the entire causal chain of **one** generation:

$$
\text{interaction}
\rightarrow
\text{fitness}
\rightarrow
\text{growth/extinction}
\rightarrow
\text{mutation birth}
\rightarrow
\text{normalization}.
$$

It cannot establish that the historical evolutionary trajectory or reported social regimes have been reproduced.

## 12. Remaining Stage-1 uncertainty before long-run replication

The scientifically important unresolved reconstruction choices are now narrow:

- exact historical outer mutation scheduler;
- exact behavior at the nine-species cap;
- exact original initial-action/random-tree PRNG;
- multi-operator order within one chromosome mutation pass;
- historical random seeds/run count;
- objective regime diagnostics for class differentiation, temporal differentiation, period-`3n` societies, and later diversity.

The first three are suitable for a short exploratory sensitivity study before the M4 historical replication is frozen.
