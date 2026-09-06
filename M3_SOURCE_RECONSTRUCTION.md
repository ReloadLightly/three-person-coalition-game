# M3 source reconstruction

> **Status:** completed pre-implementation evidence record  
> **Historical boundary:** this reconstruction was frozen before `chromosome.py` and `ecology.py` were added  
> **Current implementation:** see [README.md](README.md) and [REPLICATION_PROTOCOL.md](REPLICATION_PROTOCOL.md)

This document records the bounded source work that immediately preceded M3a. Its purpose was to recover two mechanisms **before writing evolutionary code**:

1. how species are matched and scored, including left/right positional order;
2. what `PointAdd`, `PointRemove`, `Dupli`, and `RemoveRecursively` do to the historical 8-ary chromosome.

The governing rule is [RESEARCH_MANIFESTO.md](RESEARCH_MANIFESTO.md): mechanisms are source-anchored; unavailable low-level coding details are reconstructed rather than used as a reason to delete a known mechanism.

## 1. Sources

The decisive evidence came from:

- Akiyama & Kaneko's 1995/1996 English descriptions of the three-person model;
- Akiyama's 1995 Japanese exposition, which gives the named mutation parameters and detailed tree representation;
- Akiyama's 1998 doctoral thesis, Chapter 18, which gives the population-fitness equations and explicit descriptions of the four mutation operators.

## 2. Species matching and fitness

Individuals with identical strategies form a species with population fraction `x_i`. Own-species opponents are included.

For focal species `i`, left species `j`, and right species `k`, define

\[
g_{ijk}
\]

as the focal individual's average payoff per round in the deterministic repeated interaction.

The two partner positions remain ordered because left/right are inputs to the strategy. The executable notation `j = left`, `k = right` is only a naming convention; positional distinction itself is source-defined.

Species score is

\[
s_i=\sum_j\sum_k g_{ijk}x_jx_k.
\]

Thus `(j,k)` and `(k,j)` are separate terms when the species differ, and combinations such as `(i,i,i)`, `(i,i,j)`, and `(i,j,j)` are included.

Population mean and relative fitness are

\[
\bar{s}=\sum_i x_i s_i,
\qquad
w_i=s_i-\bar{s}.
\]

The already recovered population update is

\[
x_i(t+1)-x_i(t)=d\,w_i\,x_i(t),
\]

with historical baseline `d = 0.2`, followed by normalization. The historical interaction length is `1000` rounds.

### Reconstruction decision

No random-pair approximation, unordered-triple shortcut, or extra six-permutation averaging rule is introduced. The ordered double sum is the historical ecological mechanism.

## 3. Explicit 8-ary chromosome

M2 could use maximal gene paths because only action selection mattered. M3 mutation requires branch topology.

The historical chromosome is therefore treated as a rooted 8-ary tree with outgoing branches labeled by prior states `0...7`, bounded by historical `MaxMemoryLength = 4`.

## 4. Four historical mutation mechanisms

| Operator | Historical rate | Source-recovered structural action | Immediate phenotype |
|:---|---:|:---|:---|
| `PointAdd` | `0.1` | add a branch where one is absent | may change |
| `PointRemove` | `0.1` | remove a terminal branch | may change |
| `Dupli` | `0.001` | attach all eight children to a terminal | source says unchanged |
| `RemoveRecursively` | `0.001` | remove a branch and its entire descendant subtree | may change strongly |

### `PointAdd`

The mechanism is source-defined. Treating each absent child state below maximum depth as a candidate slot is a **Reconstructed** executable interpretation of an 8-ary branch addition.

### `PointRemove`

Only terminal branches are local removal candidates. This is distinct from recursive subtree deletion.

### `Dupli`

A terminal gene `g` is expanded into

\[
g0,g1,\ldots,g7.
\]

Because every possible next state remains covered, the action phenotype is unchanged at creation. The operator therefore introduces neutral structural degrees of freedom that later mutation can differentiate.

### `RemoveRecursively`

Cutting one branch removes the complete descendant subtree attached beyond it. Representing the target as the incoming edge to a non-root subtree is the direct **Reconstructed** graph interpretation.

## 5. Remaining low-level ambiguity found during reconstruction

The sources recover all four causal operators and their local rates but do not unambiguously specify a global ordering when several operator types fire on one chromosome in the same generation.

This is **not** a missing mechanism. The M3a implementation therefore documents its current order as Reconstructed:

`PointAdd → PointRemove → Dupli → RemoveRecursively`.

Alternative orders belong in later sensitivity analysis.

## 6. Resolution achieved by this source step

| Question | Resolution |
|:---|:---|
| Who plays whom? | all ordered population combinations, including self-species partners |
| Are left/right positions distinct? | yes |
| How is species score computed? | `s_i = Σ_jk g_ijk x_j x_k` |
| What is `g_ijk`? | focal average payoff per round in the ordered repeated interaction |
| What does `PointAdd` do? | add an absent branch |
| What does `PointRemove` do? | remove a terminal branch |
| What does `Dupli` do? | attach all eight children, phenotypically neutral at creation |
| What does `RemoveRecursively` do? | delete a branch and its full descendant subtree |

## 7. Boundary preserved

This reconstruction did **not** establish the historical bookkeeping by which mutant chromosomes become, merge with, or replace species under the maximum-species constraint. That mechanism remains the central target for **M3b**, together with the exact/reconstructed random initialization distribution.

The source step therefore did exactly what it was supposed to do: recover the causal core needed for M3a without pretending that a full historical evolutionary run was already specified.
