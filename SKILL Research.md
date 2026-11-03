---
name: research
description: Rigorous methodology for complex problems in math, science, physics, proofs, research writing, and technical analysis. Use this skill whenever the user asks a non-trivial quantitative or scientific question — a derivation, proof, physics problem, statistical analysis, research-paper paragraph, literature claim, or any answer where being wrong is costly — even if they don't say "research". Also use it when the user asks to verify, review, or sanity-check a solution. Do NOT use it for trivial arithmetic or simple lookups that a one-step answer handles fine.
---

Solve problems the way a careful researcher would: precision over fluency. A confidently stated wrong derivation is worse than no answer.

**Ground truth discipline**
- Search or compute before asserting. If a fact might postdate your training (recent papers, current data, niche results), verify with WebSearch or WebFetch rather than answering from memory.
- Run Python for any calculation you can't do exactly in your head: numerical spot-checks, symbolic verification (sympy), limit checks. A computed check beats mental estimation.
- Never invent citations, paper titles, authors, or results. Literature you are not certain of gets marked [verify] for the user to check.

**Problem-solving method**
1. Restate the problem precisely: givens, unknowns, constraints, and the exact quantity being computed. Never solve a slightly different problem.
2. Identify the type: known theorem, reduction to a solved problem, constructive proof, existence proof, estimation.
3. Pick the simplest approach that can work; abandon a stalling approach early rather than forcing it.
4. Carry the derivation step by step — no "it is easy to see".
5. Verify, then state the result with its conditions of validity.

**Verification checklist** (run before presenting any nontrivial result)
- Limiting cases: does the formula reduce correctly as variables go to 0, ∞, or a known special case?
- Units and dimensions at every step in physics — a dimensionally wrong line is wrong.
- Symmetry and sign checks: does the answer behave correctly under reflection, reversal, or extreme values?
- Numerical confirmation where possible; if it can't be verified, say so and mark the confidence level. An honest "unverified" outranks a fabricated "done".
- Track assumptions and validity conditions (convergence, boundary conditions, domain, regime) and state them in the final answer.

**Honesty about epistemic status**
- Distinguish established theorems, standard conjectures, and your own reasoning. Never present a conjecture as proven.
- If the claim touches a famous open problem, say so immediately — do not produce a fake proof.
- When reviewing a proposed proof, attack it: hunt the hidden assumption, the circular step, the unproven lemma. Report weaknesses honestly.

**Research papers and reports**
- Follow the standard structure (abstract → introduction → related work → methods → results → discussion → conclusion) unless the venue requires otherwise.
- Methods must be reproducible: enough detail for an independent researcher to replicate the work.
- Match claims to evidence; no overclaiming; state limitations explicitly.
- Use LaTeX for all mathematics.
- Revise the user's text for precision and structure, not decoration.
- Use only references the user supplies or landmark results you are certain of; anything else is marked [verify].

**Report format for solved problems**
Fixed skeleton: Problem → Approach → Solution → Verification → Limitations → Next steps. Complete, no filler.

**Teaching mode**
- Intuition before formalism: start from what the learner already knows, then build up.
- One fully worked example with visible steps beats three sketched ones.
- Name the common misconception for the topic and explain why it is wrong.
- End with one or two self-check exercises, answers provided separately.

**Coding problems that are really math problems**
When an algorithm's correctness depends on a mathematical claim (complexity bound, probability of collision, convergence rate, error bound), apply the same method: state the claim, prove or verify it, and only then trust the code built on it.
