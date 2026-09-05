# Research Manifesto

## Replication → recombination → invention

This manifesto governs how we build computational research experiments.

The purpose of replication is not to freeze creativity. It is to earn the right to become creative without losing scientific grounding.

We move across three stages.

---

# Stage 1 — Recreate the original experiment

The objective is to recover the **scientific mechanism**, not to fetishize byte-identical historical code.

We descend through the available evidence in this order.

## 1. Exact implementation available

Reproduce it as closely as practical.

When original code, equations, parameter files, or executable specifications exist, they define the strongest available reconstruction target.

## 2. Mechanism specified, exact implementation unavailable

Reconstruct how the mechanism must work from the strongest available evidence:

- the paper;
- equations;
- pseudocode;
- figures;
- examples;
- supplementary material;
- related papers by the authors;
- standard implementations of that mechanism from the relevant period or literature.

A missing historical implementation detail does **not** justify deleting a known mechanism.

## 3. Mechanism known, exact numerical value unavailable

Implement the mechanism anyway.

Choose a defensible parameter value, label it as reconstructed or estimated, and preferably explore a small scientifically meaningful range.

Therefore:

> **unknown parameter ≠ missing mechanism**

and

> **unknown implementation detail ≠ permission to delete the mechanism**

The thing that invalidates Stage 1 is inventing a **different causal mechanism** while pretending it is the original one.

If a paper specifies replicator-like selection but does not report the exact growth coefficient, we implement replicator-like selection and estimate or sweep the coefficient. We do not replace the mechanism with a different selection process merely because it is convenient.

Parameter uncertainty can itself become an experiment.

---

# Stage 2 — Recombine with sourced mechanisms

Once the original experiment works and we understand it, we ask:

> **What later idea would make this experiment scientifically more interesting?**

We may now introduce mechanisms from **other published experiments or theories**, provided each addition has a source and a scientific reason.

Examples include:

- partner choice;
- spatial or network structure;
- costly signalling;
- reputation;
- ecological resource variation;
- endogenous network formation;
- learning mechanisms;
- coevolutionary mechanisms;
- mechanisms developed in later artificial-life, evolutionary-computation, game-theoretic, or domain-specific work.

This stage is not historical replication. It is **scientific recombination**:

\[
\text{original mechanism}
+
\text{later sourced mechanism}
\rightarrow
\text{new experiment}
\]

This stage is essential. A successful replication should become a **trusted experimental organism**, not a museum piece. Once we understand the original mechanism, we can deliberately recombine it with other ideas and study what changes.

---

# Stage 3 — Invent

After Stages 1 and 2 produce enough understanding, we may create mechanisms, concepts, representations, or theories that do not already exist in the literature.

These may include:

- a new representation;
- a new interaction mechanism;
- a new evolutionary operator;
- a new form of adaptation;
- a new theoretical construct;
- a new domain mapping;
- a mechanism suggested by a gap exposed during earlier experiments.

At this point invention is not a methodological failure. It is the point.

But provenance changes explicitly:

> **Stage 1:** “We recreated this.”
>
> **Stage 2:** “We combined these known mechanisms.”
>
> **Stage 3:** “We propose this new mechanism because Stages 1–2 suggest it.”

The path from reconstruction to synthesis to invention is what makes novelty interpretable rather than arbitrary.

---

# What “do not invent” means

When we say **do not invent stuff**, we mean:

> **Do not fabricate unsupported concepts, mechanisms, theories, causal relationships, or empirical facts and smuggle them into Stage 1 as though they came from the source.**

It does **not** mean:

> refuse to implement a known mechanism because one coefficient, threshold, seed, branch condition, stopping value, or coding detail is missing.

When a mechanism is known but an implementation detail is missing, we reconstruct it.

When a mechanism is known but a parameter value is missing, we estimate, calibrate, or sweep it.

When a mechanism itself is absent from the source, we do not add it during Stage 1.

Later stages deliberately relax that restriction in a traceable way.

---

# Provenance vocabulary

Every important experimental component can be described using five lightweight labels.

| Label | Meaning |
|:---|:---|
| **Exact** | Directly recovered implementation or numerical value |
| **Reconstructed** | Mechanism sourced; implementation inferred from descriptions or related evidence |
| **Estimated** | Mechanism sourced; numerical value chosen because the exact historical value is unavailable |
| **Recombined** | Mechanism imported from another cited study |
| **Novel** | Mechanism, concept, or theory proposed by us |

These labels are sufficient to preserve epistemic provenance without building an engineering bureaucracy around it.

A future experiment might therefore contain:

- coalition payoff — **Exact**;
- population update — **Exact**;
- an incompletely specified mutation branch — **Reconstructed**;
- an unavailable initialization coefficient — **Estimated**;
- partner choice imported from a later study — **Recombined**;
- a new adaptive coalition-memory mechanism — **Novel**.

---

# The ladder in one sentence

> **Stage 1 gives us understanding. Stage 2 gives us synthesis. Stage 3 gives us research.**

The goal is never endless faithful replication.

**Faithful replication is the launchpad that gives us permission to become creative without losing scientific grounding.**
