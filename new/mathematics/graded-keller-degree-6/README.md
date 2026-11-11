# No graded counterexample to the Jacobian conjecture of type (1, -r, -s) has degree 5 or 6

Status: **verified** (two computational routes, and a separate re-derivation by an independent referee);
a small extension of known results, see "What is new and what is not". No earlier record of the statement
found (2026-11-11). Produced with AI assistance; see the repository README. Not submitted anywhere.

## Background and sources

On 19 July 2026 Levent Alpöge announced a polynomial map of C^3 with constant Jacobian determinant -2
that is three-to-one, credited to an AI model:

    F(x,y,z) = ( (1+xy)^3 z + y^2 (1+xy)(4+3xy),  y + 3x(1+xy)^2 z + 3xy^2 (4+3xy),  2x - 3x^2 y - x^3 z ),

of component degrees 7, 6, 4. For the grading wt(x,y,z) = (1,-1,-2) its components are homogeneous of
weights -2, -1, 1.

T. Shaska, *Graded Keller maps and the Jacobian Conjecture*, arXiv:2607.20210 (v2, 25 July 2026), studies
Keller maps (constant nonzero Jacobian) whose components are homogeneous for a grading (1,-r,-s). The
weights of the components are then a permutation of the weights of the variables (his Corollary 2.3),
and with the components in the order of weights 1, -r, -s the map is

    F = ( x p(u,v),  M(u,v) / x^r,  N(u,v) / x^s ),      u = x^r y,  v = x^s z.

It is Keller exactly when (his Theorem 8.3; p, M, N are his Λ, B, A)

    p {M,N} + r M {p,N} - s N {p,M} = constant ≠ 0,        {f,g} = f_u g_v - f_v g_u.

If p is not constant, F is not injective (his Theorem 8.7): the points with p = 0 and x ≠ 0 are sent
into the plane X_1 = 0, which is already the bijective image of the plane x = 0. (Nothing is
contracted: a Keller map has finite fibres.) The Alpöge map is of this form, with its components in
reverse order and p = 2 - 3u - v. Shaska asks (Remark 8.13) "for which signatures (r, s) and bounds d"
such maps exist.

K. Kistner and T. Shaska, *Orbits and fields of definition for graded Keller maps*, arXiv:2608.02863
(v1, 3 August 2026), show that non-injective examples exist for every type (1,-r,-s) with r, s ≥ 1, and,
assuming their Hypothesis 8.4, that the Alpöge map is the only one, up to scalings and the substitutions
(u,v) -> (au+bv, cv), with deg N ≤ 4, deg M ≤ 3, deg p ≤ 1 (degrees in u, v). They write:

> For w = (1,−1,−2) it is settled by Thm 8.5: d = (4,3,1) is a coordinatewise minimal nonempty box,
> every lower stratum inside it being empty; Thm 8.5 does not exclude incomparable degree vectors.

The examples they give for other types have component degrees (15, 27, 3) for type (1,-1,-1) and
(15, 13, 3) for type (1,-1,-3).

J. Wang and D. Yan, *Quartic Keller Maps and Tameness in Three Variables*, arXiv:2610.36495 (v1,
27 October 2026), Theorem 1.1: a polynomial map of C^3 with constant nonzero Jacobian and all
components of degree at most 4 is a tame automorphism. Their introduction says that the earlier results
"leave open the invertibility of arbitrary Keller maps in dimension three of ordinary total degrees
four, five, and six"; their theorem settles degree four.

F. Santibáñez-Leal, *The Jacobian Conjecture after the Three-Dimensional Counterexample*, Zenodo,
doi:10.5281/zenodo.22834207 (v0.13, 18 September 2026), Theorem 4.3: within one family of maps built from
a seed polynomial, all of type (1,-1,-2), "the minimal degree vector over the family is (7, 6, 4),
attained exactly at the announced map", and "the existence of a counterexample of total degree 3 to 6
remains open". The same note reports sparse scans over the gradings (1,-1,-m), m ≤ 4, without a degree
bound.

## Result

Let r, s ≥ 1. Let F be a polynomial map of C^3 with constant nonzero Jacobian determinant whose
components are homogeneous for the grading wt(x,y,z) = (1,-r,-s); up to a permutation of the components
their weights are 1, -r, -s. **If every component of F has degree at most 6, then the component of
weight 1 is c·x with c constant** (p is constant). F is then injective, and a polynomial automorphism.

So a graded counterexample of type (1,-r,-s) has a component of degree at least 7, and the Alpöge map
attains 7. The gradings (-1, r, s) are the same class.

## What is new and what is not

- Degree at most 4 is a special case of the theorem of Wang and Yan, which needs no grading. Only
  degrees 5 and 6 matter.
- For type (1,-1,-2) with deg p ≤ 1 the statement follows from Theorem 8.5 of Kistner and Shaska, which
  is conditional on their Hypothesis 8.4: the supports allowed by degree 6 lie inside their box, and no
  member of the orbit of the Alpöge map under their group has degree at most 6 (checked in `check.py`).
- For type (1,-1,-1) it follows from a bound that Kistner and Shaska quote from a companion preprint,
  deg N + deg M + deg p ≥ 14. We could not find that preprint.
- Santibáñez-Leal has the same conclusion inside one family of type (1,-1,-2).
- New here: the statement without Hypothesis 8.4; type (1,-1,-2) with deg p = 2 (degree vectors that are
  incomparable with (4,3,1)); and the other 22 types that have to be computed.

The new content is small: a finite computation that closes degrees 5 and 6 for one class of maps.

## Why

The monomial u^j v^k has degree (r+1)j + (s+1)k in x, y, z. Degree at most 6 leaves few monomials.
Take r ≤ s (otherwise swap y and z, and the two components).

- u can occur in p only if r ≤ 4, and v only if s ≤ 4. For r ≥ 5, p is constant.
- v can occur in M only if s ≤ r + 5. If p and M are polynomials in u alone, the condition reads
  (p M' + r M p') N_v = constant, and p M' + r M p' has degree deg p + deg M - 1 ≥ 1 when p is not
  constant: no solution.
- This leaves 24 types: r ≤ 4 and r ≤ s ≤ r + 5. For each, the unknown coefficients of p, M, N satisfy
  explicit cubic equations. For r < s, N has no term in u alone and the constant term of the equation is
  p(0) times the coefficient of u in M times the coefficient of v in N; scaling the three components
  makes these three numbers 1, and scaling y or z makes one further chosen coefficient of p equal to 1.
  For r = s, a linear change of (F_2, F_3) makes the linear part of (M,N) the identity, and a
  simultaneous linear change of (y,z) and (F_2,F_3) puts the quadratic part of p in the form uv, u^2 or
  0, and in the last case the linear part in the form u. The assumption "p is not constant" then splits
  into finitely many branches, and in every branch the equations generate the unit ideal over Q. The
  largest systems have 24 unknowns (type (1,-1,-1)) and 20 (type (1,-1,-2)).

If p is constant, (M,N) is a plane Keller map of degree at most 6 in (u,v), hence a plane automorphism
(Moh 1983: the plane conjecture holds up to degree 100). So F is injective on x ≠ 0. On x = 0 it is
(y,z) -> (m y, n z + c y^(s/r)) with m n ≠ 0 (c = 0 unless r divides s; for r = s an invertible linear
map), a bijection onto the plane X_1 = 0, which the points with x ≠ 0 do not meet. An injective
polynomial map of C^n is an automorphism.

## Check

    python check.py        (needs sympy and python-flint; a few minutes)

It verifies the Alpöge map (determinant, three-point fibre, degrees, weights), the reduced equation
against the 3x3 determinant with unknown coefficients for five types, the list of 24 types, and the
emptiness of every branch by two routes:

- route A: equations from the reduced condition in (u,v); FLINT's Buchberger routine (through
  python-flint) with splitting on factors, a branch being closed only by a nonzero constant in the ideal;
- route B: equations from the 3x3 Jacobian determinant in x, y, z; sympy's own Buchberger routine. For
  types (1,-1,-1) and (1,-1,-2) each branch is first split on five top coefficients (c = 0, or c ≠ 0
  encoded by t c = 1).

The two routes are parts of one script. They share the function that lists the allowed monomials, the
list of branches and the normal forms above; they differ in how the equations are obtained and in the
Gröbner engine.

Control, in the same script: type (1,-1,-2) with component degrees at most (4, 6, 7) for the weights
(1, -1, -2). The branches p = 1+u and p = 1+v are empty. The branch p = 1+u+v, which is empty at degree
6, is not: its solution set is one point, the Alpöge map in normal form, with multiplicity two (the
Gröbner basis is linear in all coefficients but one, c, the coefficient of u^3 v in N, and contains
(27c + 8)^2). So with these degree bounds the Alpöge map is the only graded Keller map of type
(1,-1,-2) with p not constant, up to scalings of the variables and of the components, without
Hypothesis 8.4; the double point agrees with the non-reduced structure in Theorem 8.5 of Kistner and
Shaska. This control was proposed and first run by the referee. Output is in `check.log`.

Re-derivation by an independent referee (own code, not part of this folder): monomials listed directly
by weight and degree, equations from the determinant, no scaling of y, z and no normal form for p
("p not constant" encoded coefficient by coefficient). All 157 types tried with r ≤ 6 and s ≤ 40, among
them every type we treat by the one-variable argument, type (1,-1,-2) and its mirror (1,-2,-1), came
out empty; 15 of them also with sympy. Type (1,-1,-1) did not finish in that formulation. With scalings
only, 11 of its 13 cases were closed and 2 were stopped after 25 minutes; with the normal form for the
quadratic part of p, re-derived by the referee, its three branches are empty.

## Limits

- Only gradings with one weight 1 and two negative weights, or the mirror (-1, r, s). Not covered: a zero
  weight, a positive weight of 2 or more, and maps with no grading. For general maps of C^3 the known
  bound is that a counterexample has degree at least 5 (Wang 1980 for degree 2, Vistoli 1999 for degree
  3, Wang and Yan 2026, a preprint, for degree 4). Degrees 5 and 6 remain open outside the class
  treated here.
- Degree 7 is classified only in the control above. Other degree vectors with a component of degree 7,
  and the other types, were not examined.
- Type (1,-1,-1) rests on the normal form of a binary quadratic form under GL2, and the split into
  branches is a hand argument shared by both routes.
- The computed statement is "p is constant". The conclusion "automorphism" uses in addition Moh's
  theorem and the fact that an injective polynomial map is an automorphism.
- The emptiness statements are unit ideals over Q, so "p is constant" holds over every field of
  characteristic zero. Nothing is claimed in positive characteristic.
- No explicit certificate (a combination of the equations equal to 1) was produced. Route A and the
  referee's solver both rest on FLINT's Buchberger routine; route B rests on sympy's (which uses
  python-flint for rational arithmetic when it is installed).
- That routine is described by its authors as naive. Stopped by a limit, it returned bases that did not
  generate the input ideal, so the script uses such bases only as elements of the ideal (the referee
  confirmed on examples that they are). The referee also saw it crash with a stack overflow on Windows
  on one large system; that is a crash, not a wrong answer, and did not occur in `check.py`.
- We read the statements of the cited theorems of Kistner and Shaska and of Wang and Yan, not their
  proofs.

## Novelty check (2026-11-11)

Read by us: the English Wikipedia article "Jacobian conjecture" and its 2026 references; T. Tao's post
of 21 July 2026 and its comment pages (a comment of 3 August asks whether the Alpöge map is minimal; no
answer); of arXiv 2607.20210 and 2608.02863 the abstracts, the sections on degree bounds and the
concluding questions, the rest searched by keyword; 2608.00222 (Gao), 2609.17795 (van den Essen),
2607.22198 (Meng, Yang), 2608.12543 (abstract); of arXiv 2610.36495 the abstract, the introduction and
Theorem 1.1; of Zenodo 22834207 (v0.13) the abstract, Theorem 4.3, the open problems and the paragraph
on other gradings; the certification page at simgen.dev; the README
of the repository dasjoms/jacobian-conjecture-counterexample-exploration; two third-party claim
registers; in-depth web searches for a minimal-degree statement. The referee found the last two
papers, which our first search had missed, and in addition read arXiv 2610.24889 (de Bondt; no bound),
several project pages and six notes of the dasjoms repository, and ran nine further searches. Nothing
found states the bound for graded maps or settles degrees 5 and 6 in dimension three.

Not reached: the companion preprint of Kistner and Shaska, "Differential obstructions and minimal models
for balanced graded Keller maps" (not online); MathOverflow; posts on X; three Zenodo records on family
constructions (21551408, 21506477, 21479195).

## Credit

The counterexample: L. Alpöge (announcement of 19 July 2026). The graded framework, the reduced equation
and the questions: T. Shaska; K. Kistner and T. Shaska. Degree at most 4: J. Wang and D. Yan. Minimality
of (7,6,4) inside the seed family: F. Santibáñez-Leal. This page adds the computation for degrees 5 and 6
in the graded class. The referee's review supplied the control with degrees (4, 6, 7), the two missing
references and several corrections.
