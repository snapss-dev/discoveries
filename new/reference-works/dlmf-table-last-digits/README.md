# NIST DLMF: six table entries are not the correctly rounded values (Tables 3.5.4, 3.5.5, 3.5.7, 7.13.3)

Status: **verified**; not in the DLMF errata list as read on 2026-11-11. Produced with AI assistance;
see the repository README. Nothing was reported to NIST.

## The source

The [NIST Digital Library of Mathematical Functions](https://dlmf.nist.gov/) prints numerical tables in
several chapters: Gauss quadrature nodes and weights in §3.5(v), extrema of the gamma function in §5.4,
zeros of the error and Fresnel functions in §7.13, zeros of the Airy functions in §9.9, Bernoulli and
Euler numbers in §24.2, combinatorial numbers in Chapter 26 and arithmetic functions in §27.2. The pages
were fetched on 2026-11-11; the errata page then listed Version 1.2.8 (September 15, 2026) as the latest.

## Result

47 tables holding 2195 printed values were recomputed. 2189 values are exact or correctly rounded. Six
are not:

| table | entry | printed | value to more digits | correctly rounded |
|---|---|---|---|---|
| 3.5.4, 40-point Gauss–Legendre | weight at x = 0.41377 92043 71605 00152 5 | 0.07061 16473 91286 77969 **6** | 0.07061 16473 91286 77969 5484 | ...77969 5 |
| 3.5.4, 40-point Gauss–Legendre | weight at x = 0.93281 28082 78676 53336 1 | 0.02793 70069 80023 40109 **9** | 0.02793 70069 80023 40109 8489 | ...40109 8 |
| 3.5.5, 80-point Gauss–Legendre | weight at x = 0.95459 07663 43634 90549 3 | 0.01162 41141 20797 82691 **7** | 0.01162 41141 20797 82691 6467 | ...82691 6 |
| 3.5.7, 10-point Gauss–Laguerre | weight at the first node, 0.13779 34705 40492 431 | 0.30844 11157 65020 14**1** | 0.30844 11157 65020 14154 7 | ...020 142 |
| 3.5.7, 10-point Gauss–Laguerre | weight at the fourth node, 3.40143 36978 54899 51 | 0.62087 45609 86777 47**5** × 10^-1 | 0.62087 45609 86777 47392 9 × 10^-1 | ...777 474 |
| 7.13.3, complex zeros of the Fresnel integral C(z) | y_5 | 0.19066 9732**4** | 0.19066 97323 4885 | ...9732 3 |

The printed digit differs from the correctly rounded one by one unit in each case. Measured against the
true value the errors are 0.52, 0.51, 0.53, 0.55, 1.07 and 0.51 units of the last printed place. Five of
the six are therefore rounding slips just beyond half a unit; the Gauss–Laguerre weight at the fourth
node is off by a full unit. None of them matters for any computation done with these tables.

All other entries of the same tables are correctly rounded (403 of the 408 Gauss entries in Tables
3.5.1 to 3.5.17, and 39 of 40 in Tables 7.13.1 to 7.13.4), which is why these six are read as slips and
not as a different rounding convention.

## Why this is worth recording

DLMF has treated wrong final digits as errata before. The errata entry for Version 1.0.18 (March 27,
2018) reads: "Table 5.4.1: The table of extrema for the Euler gamma function Γ had several entries in
the x_n column that were wrong in the last 2 or 3 digits. These have been corrected and 10 extra decimal
places have been included." The corrected Table 5.4.1 passes the check here (22 of 22 values).

## How it was computed

Two methods that share no code, for every value.

- Gauss rules. First: the monic orthogonal polynomial is obtained exactly from the rational moments of
  the weight function (a Hankel system solved over the rationals), its roots are isolated with certified
  ball arithmetic (Arb, through python-flint), and each weight is the exact moment functional applied to
  the quotient polynomial. For the 40- and 80-point Legendre rules Arb's certified Legendre roots and
  weights are used. Second: mpmath at 120 digits, with Newton iteration on the three-term recurrence
  (Legendre), polynomial root finding and the classical weight formulas (Laguerre, Hermite), and the
  Golub–Welsch construction from a Cholesky factor of the moment matrix at 250 digits (logarithmic
  weight).
- Zeros. mpmath root finding at 60 digits, and Newton iteration in Arb started from the printed value.
  For the zeros of the digamma function the root is enclosed by a certified sign change.
- Integer and rational tables. A library function and an independent recurrence or closed form.

## Check

    python check.py

reads `dlmf_tables.json` (the tables as extracted from the fetched pages) and recomputes everything in
about 25 seconds. Output in `check.log`; the last lines list the six entries.

## Limits

- Only the tables listed in `check.log` were recomputed. Not recomputed: Tables 3.5.18 to 3.5.21,
  3.10.1, 3.11.1, 24.2.1, 24.2.2, 26.4.1, 28.6.1 and 36.7.1, and every table in chapters whose pages
  were not fetched.
- The complex zeros in §7.13 and §9.9 were not enclosed rigorously: they rest on the agreement of two
  libraries to far more digits than are printed.
- DLMF does not state a rounding convention next to these tables. The claim is that the six entries
  differ from the nearest decimal, as the other entries of the same tables do not.
- The printed NIST Handbook of Mathematical Functions (2010) was not compared.

## Novelty check

Performed 2026-11-11.

- The DLMF errata page, read in full (Versions 1.0.1 to 1.2.8). The tables it mentions are 3.5.17_5,
  3.5.19, 3.5.21, 5.4.1, 18.3.1, 18.8.1, 18.9.1, 18.9.2, 22.4.3, 22.5.2, 22.5.4 and 26.8.1. Tables
  3.5.4, 3.5.5, 3.5.7 and 7.13.3 are not mentioned.
- An in-depth web search for the table numbers together with the printed digit strings: no report found.
- Not checked: correspondence with the DLMF editors, which is not public.

If someone reported these earlier, the credit is theirs; no such record was found.
