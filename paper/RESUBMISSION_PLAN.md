# T-IT resubmission plan — IT-26-0996

Rejected 27-Jul-2026 by the area editor, without review, on two grounds: scope,
and precision. Both were correct. This plan fixes what was actually wrong
rather than reformatting around it.

## The diagnosis

**The submission is two papers stapled together, in the wrong order, and the
editor read the first one.**

| Sections | Content | Audience |
|---|---|---|
| §2–§6 (`sec:framework` … `sec:rate`) | GO-1…GO-4: preregistered empirical program, sealed gates, Llama-3.2-3B, 14 corpora | ML |
| §7–§9 + App A–C | Achievability/converse, single-letter theorem for the true divergence, output-reduction tilt, complete two-stage rate region, dispersion, separation, commission tax | Information theory |

The information-theoretic content is real and there is a lot of it — six
theorems and roughly a dozen propositions and corollaries. It is all behind the
empirical material. An area editor scanning the abstract sees preregistration
IDs and a refuted conjecture, and concludes the work is not for his readership.
He is not wrong about what he read.

**The abstract argues against its own novelty.** It states that the distortion
is classical (Dobrushin–Tsybakov, Wolf–Ziv), that it reduces to Shannon by
Berger's change of variables, and that "we do not claim Shannon was
incomplete." A reader then asks what the theorem is. The claimed contribution —
that the read subspace is recoverable from black-box queries — is an estimation
result, not an information-theoretic one. That mismatch, more than the
notation, is what triggered the scope call.

## Paper A — the T-IT resubmission (new manuscript, not an appeal)

Working title: **Rate–Distortion for Composite Distortion Measures: Coding
Theorems, Successive Refinement, and the Price of a Misidentified Observer.**

Body, in this order:

1. **Setup.** Probability space, source, distortion class, the operational
   question. No motivation longer than a page.
2. **Coding theorems** (App A → body): `thm:coding` achievability and converse;
   `cor:pointdep` point-dependent surrogate.
3. **The true nonlinear divergence** (App B → body): `thm:B1` single-letter
   theorem; `thm:B2` output reduction / the tilt is $\mathcal{C}$; `cor:B2a`
   quotient floor; `cor:B2b` order of operations; `thm:B3` high-resolution
   closed form and the finite-$D$ pinch.
4. **Successive refinement** (§9, keep): `thm:region` complete two-stage rate
   region; `thm:multiobs` refinability iff nesting; `thm:multiobs-loss` exact
   rate loss; `cor:kobs` the $k$-observer chain.
5. **Finite blocklength and separation** (§8, keep): `prop:dispersion`,
   `cor:dispersion`, `prop:separation`.
6. **Mismatch** (App C → body): `thm:commission` commission tax; the omission
   floor.
7. **The quadratic surrogate as a local expansion.** `prop:main` demoted from
   the paper's centrepiece to a lemma: $P_\mathcal{C}=J^\top G J$ is the
   second-order behaviour of the composite distortion near the diagonal. This
   is where the geometry belongs — as a property of a distortion measure, not
   as a new framework.
8. **One short numerical section.** Gaussian and one real-embedding
   illustration of the rate region. No preregistration language.

Cut entirely: GO-1…GO-5 labelling, "sealed gates", §`sec:negatives` (honest
negatives and method), §`sec:boundary` (the refuted quotient), all prereg IDs,
the Llama arms narrative. These are the ML paper's spine, not this one's.

## The precision fixes, concretely

These are the editor's actual charges. Each is a real defect.

### 1. Notation: one symbol, one meaning

Present usage collides three ways — `X` as "a representation" (Def. 1), `X` as
a set of key vectors (Ex. 1), `X` as a random vector (`X\sim\mathcal N(0,
\Sigma_x)`, l. 726), with `\mathcal{X}` as the alphabet (l. 1120). Adopt the
convention T-IT expects and hold it everywhere:

| Symbol | Meaning |
|---|---|
| $\mathcal{X}$ | source alphabet, a Polish space; $\mathcal{X}\subseteq\mathbb{R}^d$ in the Euclidean case |
| $X$ | the source random vector, $X:\Omega\to\mathcal{X}$, law $P_X$ |
| $x$ | a realisation, $x\in\mathcal{X}$ |
| $\hat X,\hat x$ | reconstruction, on $\hat{\mathcal{X}}$ |
| $\mathcal{C}$ | the consumer map, Borel $\mathcal{X}\to\mathcal{U}$ |

Add a notation table. "A representation" becomes either $\mathcal{X}$ or
$P_X$ — decide which and never use the informal word again.

### 2. The probability space, before the first expectation

Currently `\E[\dO]` appears in Definition 1 (l. 152) and the measure-theoretic
setting first appears at l. 1119 — a 967-line gap. Open §2 with it:

> Let $(\Omega,\mathcal{F},\Pr)$ be a probability space and let
> $X:\Omega\to\mathcal{X}$ be a random vector with law $P_X$ on a standard
> Borel space $\mathcal{X}$. All expectations are with respect to $P_X$ unless
> subscripted otherwise. The source is $\{X_t\}_{t\ge1}$ i.i.d. $\sim P_X$.

Then delete the phrase "expectation over the instance", which is not a
definition.

### 3. Definition 1, rewritten

The current definition leaves four things unstated: the type of $X$, the
formalisation of $\mathcal{Q}$, the law of $\delta$, and — critically — the
smoothness of $D_Y$ that `prop:main`'s second-order expansion requires two
pages later. Replacement:

> **Definition 1 (Consumer and induced distortion).** A *consumer* is a Borel
> map $\mathcal{C}:\mathcal{X}\to\mathcal{U}$ into a Polish space
> $\mathcal{U}$, together with a *output divergence*
> $D_Y:\mathcal{U}\times\mathcal{U}\to[0,\infty]$ that is jointly Borel and
> satisfies $D_Y(u,u)=0$ for all $u$. The *induced distortion* is
> $$d_{\mathcal{C}}(x,\hat x):=D_Y\big(\mathcal{C}(x),\mathcal{C}(\hat x)\big),$$
> a nonnegative single-letter distortion measure on
> $\mathcal{X}\times\hat{\mathcal{X}}$, jointly Borel as a composition of
> Borel maps.
>
> When a local expansion is required (Prop. 3 onward) we assume additionally
> that $D_Y(u,\cdot)$ is twice continuously differentiable in a neighbourhood
> of the diagonal, with $G(u):=\nabla^2_{2}D_Y(u,u')\big|_{u'=u}\succeq0$, and
> that $\mathcal{C}$ is differentiable with Jacobian $J(x)$. **These
> assumptions are used only where stated.**

Note this definition no longer mentions codes: $\mathcal{Q}$ belongs with the
coding theorem, as $(n,R)$ encoder/decoder pairs, not in the object definition.

### 4. Vocabulary

Keep "consumer" — it is good and it is yours — but subordinate it on first use:
say that $d_{\mathcal{C}}$ is a composite distortion measure, of the
indirect/remote source-coding type (Dobrushin–Tsybakov 1962; Wolf–Ziv 1970),
and that "consumer" names the map inducing it. Then the IT reader has a
handhold in the first paragraph.

Replace: "isotropic corner" → "the special case $P_\mathcal{C}=I$"; "pullback
of the output metric" → state $J^\top G J$ and say it is the pullback, in that
order; "resolution budget" → "rate constraint" or "distortion budget",
whichever is meant. Check the submitted PDF for the last one — it is absent
from the current source.

### 5. Abstract: ~200 words, theorem-first

Current abstract is a single ~700-word paragraph containing preregistration
identifiers, `7.5e-9`, and `0.647`. Structure the replacement as: (i) the
distortion class in one sentence; (ii) the coding theorem; (iii) the two-stage
region and the nesting characterisation; (iv) the mismatch penalty; (v) one
sentence on what this specialises to. No numbers from experiments. No prereg.

## The novelty audit — do this before writing

The rewrite is worth nothing if the theorems are already known, and reviewers
will check. Resolve each of these in writing, with citations, before drafting:

1. **`thm:region` / nesting.** Compare against Equitz–Cover, *Successive
   refinement of information* (IT 1991) — successive refinability iff a Markov
   condition holds — and Rimoldi (IT 1994) for the general two-stage region. If
   the nesting characterisation is a Gaussian-vector specialisation of
   Equitz–Cover, the paper must say so and claim the specialisation, not the
   theorem.
2. **`thm:coding`.** Achievability and converse for a general Borel
   single-letter distortion is classical (Csiszár; Kostina–Verdú for
   finite-blocklength). Establish precisely what is new: presumably not
   existence but the *reduction* (`lem:tilt`, `thm:B2`).
3. **`thm:B2` output reduction.** This looks like the strongest candidate for
   genuine novelty — the tilt being $\mathcal{C}$ itself, reducing the problem
   to the output source. Check against the remote source-coding literature
   (Witsenhausen; Yamamoto) before claiming it.
4. **`thm:commission`.** Compare with mismatched-distortion and
   mismatched-codebook results (Lapidoth 1997 on mismatched decoding;
   Dembo–Weissman on mismatched rate–distortion).

If (1)–(4) all resolve as "known, or a modest specialisation", then the honest
conclusion is that this is not a T-IT paper and JSAIT or an ML venue is right.
Finding that out now is cheaper than a second rejection.

## Paper B — the empirical paper

Already started as `paper-IV-tmlr.pdf`. It takes GO-1…GO-4, the preregistration
apparatus, the sealed gates, the refuted quotient, and the Llama rematch. That
material is genuinely strong *for that audience* — a reconstruction-identical
code flipping its verdict when the consumer changes is a good empirical result,
and the preregistration discipline is a real virtue at an ML venue. It was
simply fatal at T-IT.

Cross-reference: Paper B cites Paper A for the coding theorems; Paper A cites
Paper B for the empirical validation and does not restate it.

## Order of work

1. Send the reply (`REPLY-DRAFT.md`). Cheap, and the answer may redirect
   everything.
2. Novelty audit (1)–(4) above. **Gate:** if nothing survives, stop and go to
   JSAIT or ML only.
3. Notation and measure-theoretic pass on the retained material.
4. Restructure into Paper A; rewrite the abstract last, once the body is fixed.
5. Internal referee pass against T-IT's own criteria: would a reader who has
   never heard the word "consumer" follow §1–§3?
6. Submit as a **new** manuscript, with a cover letter noting the prior
   submission number and what changed. Do not disguise the resubmission —
   editors check, and Vincent Tan will remember this one.
