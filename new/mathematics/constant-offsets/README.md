# Eighteen OEIS constants whose offset does not match the size of the number

Status: **verified** for twelve entries, **read from the entry** for six; **new?** (2026-11-11). Small
errata. Produced with AI assistance; see the repository README. Not submitted to the OEIS.

For a decimal expansion the OEIS offset says where the decimal point is: with listed digits
d1, d2, d3, ... and offset o, the constant is 0.d1 d2 d3 ... * 10^o. So 5.57... has offset 1 and
0.54... has offset 0. In the entries below the digits are right and the offset is not.

## Recomputed from the name

| entry | constant | value | offset listed | offset that fits |
|---|---|---|---|---|
| [A110993](https://oeis.org/A110993) | Zeta(Zeta(10)) | 1006.0317... | 1 | 4 |
| [A111513](https://oeis.org/A111513) | abs(log_10(sine of 1 degree)) | 1.7581... | 0 | 1 |
| [A113272](https://oeis.org/A113272) | Gamma(1/4)^4/Pi^3 | 5.5728... | 0 | 1 |
| [A113477](https://oeis.org/A113477) | Gamma(1/3)^3/(2^(4/3)*Pi) | 2.4286... | 0 | 1 |
| [A114610](https://oeis.org/A114610) | Sum_{k=-inf..inf} log(2)/(2^(-k/2) + 2^(k/2))^2 | 1.00000000004885... | 0 | 1 |
| [A248181](https://oeis.org/A248181) | Sum_{h>=0} 1/binomial(h, floor(h/2)) | 3.2091... | 0 | 1 |
| [A319129](https://oeis.org/A319129) | (1 + sqrt(3) + sqrt(2*sqrt(3)))/2 | 2.2966... | 0 | 1 |
| [A160205](https://oeis.org/A160205) | (989043+524338*sqrt(2))/809^2 | 2.6441... | 11 | 1 |
| [A156547](https://oeis.org/A156547) | central angle of a regular dodecahedron, arccos(sqrt(5)/3), in radians | 0.7297... | 1 | 0 |
| [A242600](https://oeis.org/A242600) | -dilog(phi) = -polylog(2, 1-phi) | 0.5421... | 1 | 0 |
| [A246644](https://oeis.org/A246644) | real root of s^3 - s^2 + s - 1/3 = 0 | 0.4424... | 1 | 0 |
| [A293380](https://oeis.org/A293380) | r with 0 = Sum_{n>=1} (1/2 - r^n)^n/n | 0.5471... | 1 | 0 |

Zeta(Zeta(10)) is large because Zeta(10) = 1.000994..., just to the right of the pole of the zeta
function at 1.

## Read from the entry, not recomputed

In six more entries the example line printed in the entry itself contradicts the offset:

| entry | what it is | example line begins | offset listed | offset that fits |
|---|---|---|---|---|
| [A102521](https://oeis.org/A102521) | value of Ahmed's 2nd integral | 0.590489270886... | 1 | 0 |
| [A179449](https://oeis.org/A179449) | volume of the great icosahedron with edge length 1 | 0.318305009375... | 1 | 0 |
| [A245698](https://oeis.org/A245698) | expected distance from a random point of a unit equilateral triangle (see entry) | 0.265614417336... | 1 | 0 |
| [A301862](https://oeis.org/A301862) | probability that two random chords of a circle intersect (see entry) | 0.586636292439... | 1 | 0 |
| [A301863](https://oeis.org/A301863) | the same for another way of choosing chords | 0.678106805449... | 1 | 0 |
| [A301864](https://oeis.org/A301864) | the same for chords of a sphere projected onto a plane | 0.727754185434... | 1 | 0 |

For these the digits were confirmed against the entry's own Mathematica expression, and the size of
the number was taken from that expression and from the example line. The last three are probabilities,
which cannot exceed 1.

## Check

    python check.py

evaluates the twelve constants of the first table from their names with mpmath (and with Arb balls for
those built from functions Arb provides), checks that the first nine listed digits are those of the
constant, and prints the offset that fits beside the one listed. Output in `check.log`.

## How these were found, and limits

After a screen of 14474 constant entries for wrong digits (see the page "A261114 and A333507"), the
6260 decimal expansions whose digits had been confirmed through a closed form or Mathematica expression
were tested for the relation between offset and size. 6212 fit. Of the rest, those listed here are the
ones that hold up when read against the name; the others were artefacts of the screen (entries that
serve two purposes, expressions in other units, numbers with millions of digits). Entries whose digits
could not be confirmed by the screen were not tested, so this is not a complete list.

## Novelty check

Performed 2026-11-11.

- Live entries re-fetched from oeis.org: all eighteen show the offsets listed above.
- Every page of the eighteen revision histories with their discussion threads, and the draft pages (no
  pending edit). In seventeen entries the offset has never been edited since the first recorded
  revision. In A111513 it was changed from 1 to 0 in revision #2 (N. J. A. Sloane, Jan 09 2009), so
  for that entry the present value was a deliberate edit; the value of the constant in the present name
  is 1.758..., for which the convention gives 1. None of the discussion threads (the longest is for
  A319129, about its programs) mentions the offset.
- Google DeepMind formal-conjectures file list, Epoch AI's OEIS Open list, and the omega-institute
  project (issue search only): no mention of any of the eighteen.
- No web search was made; offsets of constants are corrected routinely by OEIS editors, and these may
  be fixed at any time.
