# Reframing draft for the T-IT manuscript (2026-10-01)

Goal (owner): make this a foundational paper, the first exactly solved instance of the principle the broader programme rests on, while keeping T-IT's classical vocabulary (the earlier synthesis was rejected partly on terminology). The principle is stated in classical terms only: the cost of a description is a property of who observes what, not of the source and side information alone. Every claim below is tied to a result already in tit-cr-context-r2.tex; nothing new is asserted.

House style kept: no em-dashes; colons and semicolons avoided in new prose.

---

## 1. New opening paragraph of the Introduction (replaces lines 79-92)

A stored description of data has no single cost. The decoder that reconstructs from it pays its rate. A party that keeps the description and holds side information pays something else, the conditional entropy of the description given what it holds, which is the least rate at which that party can re-encode it. This paper proves, in the simplest setting where the question can be answered exactly, that these two costs are set by different parts of the encoding configuration and cannot in general be minimized together. Three facts carry the result. The second cost is not determined by the joint law of the reproduced variable and the side information, because it depends on what the encoder observes (Corollary~\ref{cor:notmarginal}). The two costs are minimized by different descriptions exactly when the encoder's extra observation is partially informative, and the gap between the two optima grows without bound as the side information becomes clean (Theorem~\ref{thm:region}(b), Corollary~\ref{cor:misalign}). And for jointly Gaussian sources the whole picture is explicit, the minimal conditional content in closed form and the rate--content region with its frontier. The doubly symmetric binary source is solved through a tilt equation.

## 2. Replacement for the "endpoint excesses are small" sentence (lines 192-196)

Current text leads with the gap being small (0.11 bits rate, 0.08 bits content) and mentions the unbounded regime second. Replacement leads with the structure and states the size as a property of the regime:

The size of the misalignment is a property of the regime. It grows without bound toward the clean-context boundary, where the content-optimal description pins the reproduction to the context and its rate diverges, for instance by $1.54$ bits at $(\rho^2,\tau^2,D)=(0.5,10^{-3},0.5)$. Over a moderate parameter box it stays below $0.12$ bits of rate and $0.08$ bits of content (Section~\ref{sec:region}).

(Numbers are the paper's own: 1.537 bits at (0.5, 1e-3, 0.5), 0.1138 and 0.0770 bits over the box, lines 1959-1963.)

## 3. Hardness paragraph (new, after the paragraph that ends "...credited to Armstrong's source-side sufficiency \cite{armstrong2026} as a distortion-preserving specialization."; or as a short subsection "Why the evaluation is not routine")

The functional is known, so it is fair to ask whether its Gaussian evaluation is routine. Four features keep it from being so. First, the distortion constrains $Y$ alone, yet the optimal channel loads on the context, with coefficient $b=(g^\star-1)\rho/(g^\star k)$ nonzero for every $\rho\ne0$ (Theorem~\ref{thm:function}(a)). Under the Markov chain the content is $I(T;\hY)-I(\hY;S)$ (Section~\ref{sec:intro}), so loading the description on the context, which the side information observes, lowers its content even though it does nothing for the distortion. The reverse water-filling on $Y$ that solves the classical and Gray problems therefore does not apply, and the optimization runs over the joint regression of the reproduction on $(Y,V)$ against the conditional covariance of $(Y,V)$ given $S$. Second, the region is not traced by one water level. Its frontier is the solution of a coupled stationarity system in two noise fractions, and the existence and uniqueness of that solution at every weight is a separate result (Proposition~\ref{prop:uniq}), proved through a convexity lemma in transformed coordinates (Lemma~\ref{lem:mxconvex}). Third, at the clean-context boundary $\tau^2=0$ the conditional covariance of $(Y,V)$ given $S$ is singular, the exhaustion lemma behind the converse (Lemma~\ref{lem:gauss}) no longer applies, and the persistence of the tradeoff there needs its own argument (Propositions~\ref{prop:marg} and~\ref{rem:cleanboundary}). Fourth, the operational meaning of the second coordinate is the conditional entropy of a discrete index given a continuous side information, which does not follow from the finite-alphabet theorem by a standard limit. Appendix~\ref{app:gaussian} proves the Gaussian operational theorem directly through a quantized conditioner, and the same obstruction is why the finite-blocklength dispersion of the content coordinate remains open (Section~\ref{sec:discussion}).

## 4. Discussion: state the principle the paper establishes (append to the first paragraph of Section~\ref{sec:discussion}, after "...not of the source and side-information pair alone.")

Stated generally, the paper establishes in an exactly solvable case that the cost of a description is relative to the party that pays it. One description carries one rate but as many conditional contents as there are parties holding different side information, and the encoder's observations, not the source alone, decide how those costs trade off. The closed form and the region make the principle quantitative, and the open problems below are its natural next instances.

## 5. Abstract (optional, one sentence added at the start)

Prepend: "A stored description has a rate, paid by the decoder, and a conditional content, paid by any party that keeps it while holding side information, and the two are set by different parts of the encoding configuration."

Keep the rest. Word count would rise from 242 to about 270; T-IT has no hard abstract limit, but trim one later sentence if needed (for instance "The closed form recovers the classical, Gray, and Steinberg formulas as limits." could move to the introduction).

## 6. Cover letter (one sentence, where the programme can be named without touching the paper's vocabulary)

"The paper is the first exactly solved instance of a broader question, how the information cost of a description depends on which party observes what, and it is written to stand on its own in classical rate--distortion terms."

---

## What this does not change

No theorem, proof, number or citation changes. The vocabulary stays classical (no "observer", "consumer", "programme" in the paper). The 0.11 and 0.08 bit figures stay in Section V, now framed as one regime rather than the headline.

## Open choices for the owner

1. Section 3 as a paragraph in Related Work, or as its own short subsection "Why the evaluation is not routine" (more visible to a skeptical referee).
2. Whether to add the abstract sentence (section 5).
3. Whether the cover-letter sentence names the programme as "Observation Theory" explicitly. Given the earlier rejection, I would leave the name out of the paper and use at most the neutral phrasing above in the letter.
