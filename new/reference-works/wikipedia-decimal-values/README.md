# English Wikipedia: wrong digits in tables of function values and constants, found by recomputation

Status: **verified** by two independent computations; no earlier report found on the talk pages
(2026-11-11). Produced with AI assistance; see the repository README. Nothing was edited or reported.

## What was done

Numeric tables in English Wikipedia articles on special functions, constants and statistical tables were
extracted from the wikitext and recomputed with certified ball arithmetic (Arb, through python-flint)
and, separately, with mpmath. A printed value is called wrong only when it is neither the correctly
rounded nor the truncated value. A truncated value in a table that otherwise rounds is listed as well
and described as truncated. Revision ids are those current on 2026-11-11.

About 7,500 table values were recomputed this way (see "What was checked and found correct" below). The
entries that failed are listed here.

## 1. Statistical tables: Φ(0.16) and z = ±1.36 in the standard normal table; five χ² values; one t value

Article [Standard normal table](https://en.wikipedia.org/wiki/Standard_normal_table), revision
1353520618. The four tables hold 1290 values.

| table | entry | printed | value | correct to 5 places |
|---|---|---|---|---|
| Cumulative, positive z | z = 0.16 | 0.56360 | 0.5635595 | 0.56356 |
| Complementary cumulative | z = 0.16 | 0.43640 | 0.4364405 | 0.43644 |
| Cumulative, negative z | z = −1.36 | 0.08692 | 0.0869150 | 0.08691 |
| Complementary cumulative | z = 1.36 | 0.08692 | 0.0869150 | 0.08691 |
| Cumulative, positive z | z = 1.36 | 0.91308 | 0.9130850 | 0.91309 |

The first four are wrong under either convention; the last is the truncated value in a table that
rounds. The entry for z = 0.16 is off by four units in the fifth place. It looks like a four-place value (0.5636,
which is correct to four places) padded with a zero. The values 0.43640 and 0.56360 entered the article
on 2014-10-14 (revisions 629563304 and 629570601) and have stood for twelve years. The entries at ±1.36
are a borderline rounding: the true value 0.08691496 lies just below the half-way point.

The other 1285 values are correctly rounded, including the 80 values for z = 0 to 79 in the large-z
table.

These numbers are copied. On 2026-11-11 the z-table at stattables.com showed the same three values
(0.56360 at z = 0.16, 0.91308 at z = 1.36, 0.08692 at z = −1.36).

### Chi-squared and Student's t critical values

Article [Chi-squared distribution](https://en.wikipedia.org/wiki/Chi-squared_distribution), revision
1378642953, table of χ² values against p-values for 1 to 10 degrees of freedom (110 values, two
decimals):

| degrees of freedom | p-value | printed | value | correct |
|---|---|---|---|---|
| 1 | 0.50 | 0.46 | 0.4549 | 0.45 |
| 4 | 0.70 | 2.20 | 2.1947 | 2.19 |
| 5 | 0.95 | 1.14 | 1.1455 | 1.15 |
| 6 | 0.95 | 1.63 | 1.6354 | 1.64 |
| 9 | 0.95 | 3.32 | 3.3251 | 3.33 |

The first two are wrong under rounding and under truncation; the last three are truncated. All five are
what one can get from a three-decimal table value (0.455, 2.195, 1.145, 1.635, 3.325) by rounding or
cutting it a second time. The table's footnote cites a table taken from Fisher and Yates and says "Two values have
been corrected, 7.82 with 7.81 and 4.60 with 4.61", so editors have already repaired two entries of the
same kind; these five remain. The other 105 values are correctly rounded.

Article [Student's t-distribution](https://en.wikipedia.org/wiki/Student%27s_t-distribution), revision
1384902396, table of critical values (396 values for finite degrees of freedom, three decimals): one
entry is truncated instead of rounded. For 23 degrees of freedom at the one-sided 99.95% level the table
has 3.767; the value is 3.76763, which rounds to 3.768. The other 395 are correctly rounded.

## 2. Riemann zeta function: eight of the ten zeros listed are wrong in their last digits

Article [Riemann zeta function](https://en.wikipedia.org/wiki/Riemann_zeta_function), revision
1381421819, table "First few nontrivial zeros". Each value is printed to 15 decimals and followed by an
ellipsis.

| zero | printed | imaginary part to 20 decimals |
|---|---|---|
| 1 | 14.134725141734693 | 14.13472514173469379046 |
| 2 | 21.022039638771552 | 21.02203963877155499263 |
| 3 | 25.010857580145689 | 25.01085758014568876321 |
| 4 | 30.424876125859512 | 30.42487612585951321031 |
| 5 | 32.935061587739192 | 32.93506158773918969066 |
| 6 | 37.586178158825668 | 37.58617815882567125722 |
| 7 | 40.918719012147498 | 40.91871901214749518740 |
| 8 | 43.327073280915002 | 43.32707328091499951950 |
| 9 | 48.005150881167161 | 48.00515088116715972794 |
| 10 | 49.773832477672300 | 49.77383247767230218192 |

Zero 1 is the truncated value and zero 3 the rounded value; the other eight are wrong under either
reading, by two to three units in the last place (zero 8 is wrong from the twelfth decimal on). Seven of
the printed values (zeros 3, 4, 5, 7, 8, 9, 10) are exactly the nearest IEEE double printed to 15
decimals, so the table shows binary rounding noise beyond the sixteenth significant digit. The values
entered the article on 2026-10-20 (revision 1381155264). The sister article "Particular values of the
Riemann zeta function" lists the same ten zeros to 18 decimals, all correct (truncated).

## 3. Riemann–Siegel theta function: the Gram point g_0

Article [Riemann–Siegel theta function](https://en.wikipedia.org/wiki/Riemann%E2%80%93Siegel_theta_function),
revision 1362805456. The value 17.8455995405... is printed twice (in "Curve discussion" as a root of θ,
and in the table of Gram points). The root is 17.84559954041086..., so the tenth decimal should be 4
under rounding and under truncation. The other 17 Gram points in the table are right (16 agree with truncation,
one is rounded). The value has been in the article since 2012-09-18 (revision 513443919).

## 4. Bickley–Naylor functions: five values of Ki_3

Article [Bickley–Naylor functions](https://en.wikipedia.org/wiki/Bickley%E2%80%93Naylor_functions),
revision 1315193899, table of Ki_1, Ki_2, Ki_3 (78 values, nine decimals).

| entry | printed | value |
|---|---|---|
| Ki_3(0) = π/4 | 0.785398162 | 0.7853981634 |
| Ki_3(0.2) | 0.612064472 | 0.6120644711 |
| Ki_3(0.3) | 0.541862953 | 0.5418629541 |
| Ki_3(0.4) | 0.480375442 | 0.4803754414 |
| Ki_3(0.5) | 0.426358257 | 0.4263582565 |

Each is one unit off in the ninth decimal. Three further entries are truncated where the rest of the
table is rounded (Ki_1(0.2), Ki_1(8.0), Ki_3(9.0)), and Ki_1(0.1) is printed with eight decimals. The
table was installed on 2020-12-26 (revision 996459639); the edit summary says the table entries "were
replaced higher precision values and extended up to x=10".

## 5. Deltoidal icositetrahedron: the edge ratio

Article [Deltoidal icositetrahedron](https://en.wikipedia.org/wiki/Deltoidal_icositetrahedron), revision
1360220212, section "Side Lengths": "The side lengths of these kites can be expressed in the ratio
0.7731900694928638:1." The ratio of the short to the long edge is (4 + √2)/7 = 0.7734590803390136. The
printed number is wrong from the fourth decimal. It also contradicts the same article, which gives the
inverse ratio 2 − 1/√2 ≈ 1.292893 a few lines earlier and, in the next sentence, the two lengths
0.707106785 and 0.914213565, whose quotient is 0.77346. The ratio was recomputed here from coordinates
(the polar dual of the rhombicuboctahedron). In the article since 2024-07-27 (revision 1237051818).

## 6. Brun's constant in "List of mathematical constants": a continued fraction of a truncated decimal

Article [List of mathematical constants](https://en.wikipedia.org/wiki/List_of_mathematical_constants),
revision 1381551884, table "Mathematical constants sorted by their representations as continued
fractions". The row for Brun's constant gives the decimal 1.90216 05831 and the continued fraction

    [1; 1, 9, 4, 1, 1, 8, 3, 4, 7, 1, 3, 3, 1, 2, 1, 1, 12, 4, 2, 1, …]

These 21 partial quotients are exactly the continued fraction of the terminating decimal 1.9021605823,
which is not the decimal printed in the same row. Brun's constant is not known to that many places: Nicely's interval 1.902160583209 ±
0.000000000781 (quoted in OEIS A065421) fixes only the first nine partial quotients, [1; 1, 9, 4, 1, 1,
8, 3, 4]. The tenth printed term, 7, already disagrees with the decimal printed in the same row
(1.9021605831 expands as [1; 1, 9, 4, 1, 1, 8, 3, 4, 4, ...]), and the terms after the ninth carry no
information about the constant.

In the same article, the main table's 102 decimal expansions were compared digit by digit with the OEIS
entries they cite: all agree.

## 7. Single values

| article (revision) | quantity | printed | value |
|---|---|---|---|
| Golden ratio (1383178188) | φ³ | 4.236067978… | 4.2360679775 |
| Golden ratio (1383178188) | φ⁴ | 6.854101967… | 6.8541019662 |
| Particular values of the gamma function (1384636908) | Γ(3/2) = √π/2 | 0.886 226 925 452 758 0137 | 0.88622692545275801365 (19 places: …0136) |
| Double exponential function (1367789660) | Vardi's constant | 1.264084735305302 | 1.2640847353053011 |
| List of numbers (1384024365) | e^π | 23.14069263277925… | 23.140692632779269 |
| Feller's coin-tossing constants (1301558165) | β₂ = 1 + 1/√5, in the worked example | 1.44721356… | 1.44721359 (as in the article's own table) |
| Unary coding (1384494539) | φ | 1.61803398879… | 1.61803398875 |
| Partial Euler Product (1382838720) | e, in a displayed formula | 2.718281728459 | 2.718281828459 |

The two golden-ratio values are what one gets by adding the rounded values above them (1.618033989 +
2.618033989, then 2.618033989 + 4.236067978); in the article since 2022-06-01 (revision 1090973011).
Γ(3/2) is half of the rounded Γ(1/2) printed on the line above it; in the article since 2016-10-03
(revision 742472328).

## What was checked and found correct

Recomputed with both methods, no error: Q-function (82 values), Error function (64), Particular values
of the Riemann zeta function (37, 18 to 23 digits), the gamma-function extrema in Particular values of
the gamma function (20, 28 digits), 68–95–99.7 rule (37), Stieltjes constants (15, 46 digits; the
entries for n = 10^4 and 10^5 with Arb only), Reciprocal gamma function (30 Taylor coefficients, 40 digits), Natural logarithm
of 2 (141), Factorial (21), Gauss–Kronrod quadrature formula (20; three K15 weights are truncated where
the others are rounded), Prime-counting function (the table to 10^22: π(x) against OEIS A006880, the
x/log x and li(x) columns with Arb), Table of divisors (divisor lists, d, σ, s and the
deficient/abundant/prime/highly composite notes for n ≤ 1000). The full list with counts is in
`checked.csv`.

## Check

    python check.py

recomputes every value in sections 1 to 7 (1,937 values) from `wikitext_excerpts.json` (the relevant
wikitext with its revision id) in about 30 seconds; output in `check.log`. Lines marked WRONG are
neither rounded nor truncated values; lines marked ok-trunc are truncated in a table that otherwise
rounds.

## Limits

- Wikipedia changes. The findings are tied to the revision ids given; a later revision may already
  differ.
- Arb gives rigorous enclosures for sections 1, 2, 4 and 7. For the χ² and t tables the test is a
  rigorous one: the distribution function is evaluated with Arb half a unit below and above each printed
  value. The Gram points are enclosed by a certified sign change of θ. The Kronrod rule is built exactly and its roots isolated rigorously.
- The date a value entered an article was found by bisection over revisions, which assumes the value
  stayed once it was added. Dates were not determined for the items in section 7 other than the golden
  ratio and Γ(3/2), nor for the χ² and t tables.
- Only the listed tables were recomputed. Tables whose values depend on a judgement of the literature
  were not touched.
- The observation about stattables.com is a single look at one site, not a survey.

## Novelty check

Performed 2026-11-11 for each article: the current talk page was fetched and searched for the printed
value, and a full-text search of the article's talk pages and archives was run for the same strings.
No talk page mentions any of these values as wrong. Two near misses, neither a report: the talk page of
Riemann–Siegel theta function contains a 2013 link whose address carries the correct digits
17.84559954041; and the search for 4.236067978 returned a sandbox subpage (Talk:Golden ratio/sandbox),
which was not read. An in-depth web search for the Standard normal table values found the article and its
copies, and no correction. The talk pages of Chi-squared distribution and Student's t-distribution were
searched for the values in question (0.455, 0.46, 2.20, 3.767, 3.768): no mention. Talk-page archives
were reached only through the search, not read page by page.
