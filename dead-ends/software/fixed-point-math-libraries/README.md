# Fixed-point math libraries: no documented guarantee broken

Status: **dead end** (nothing found). This is not an audit. Produced with AI assistance; see the
repository README.

## The idea

Smart-contract math libraries state guarantees for their integer approximations of exp, ln, roots and
price conversions: a rounding direction, monotonicity, an error bound. Random testing rarely lands where
rounding goes wrong, so the inputs were chosen adversarially instead: at and beside every internal
range-reduction boundary, where the true result is nearly an integer in the output scale, across
consecutive inputs for monotonicity, and exhaustively where the domain is small.

## What was tested, and the outcome

Libraries were taken from their public repositories on 2026-11-11. Each function was ported to Python
with exact integer arithmetic and compared with exact or 300 to 400 bit references.

| library, function | documented claim | test | outcome |
|---|---|---|---|
| Solady `expWad`, `lnWad`, `lambertW0Wad` | monotonically increasing | about 51, 52 and 70 million consecutive pairs around every range-reduction boundary and branch threshold | holds |
| Solady `sqrt`, `cbrt`, `sqrtWad`, `cbrtWad` | rounded down | exhaustive below 2^17; n^2 ± 1 and n^3 ± 1 at every bit length | holds |
| Solady `log2`, `log10`, `log256` and their `Up` forms | floor, or rounded up | b^k - 2 to b^k + 2 for every k | holds |
| Uniswap v3 `getTickAtSqrtRatio` (v4 is arithmetically identical) | greatest tick whose price is at most the input | **exhaustive**: all 1,774,545 ticks | holds |
| Uniswap `FullMath` `mulDiv`, `mulDivRoundingUp` | exact floor and ceiling | 800,000 adversarial inputs | holds |
| Balancer v2 `powDown`, `powUp` | bracket the true power, given a relative error of at most 1e-14 | inputs at the edges of the high-precision window and at the exponent limits | holds; largest error 1.3e-15 |
| ABDKMath64x64 `divuu`, `sqrtu` | rounded toward zero, rounded down | adversarial, and exhaustive at small sizes | holds |
| PRBMath `SD59x18.avg` | rounded toward zero | exhaustive on [-300, 300]^2 plus extremes | holds |

For information only, since no accuracy is claimed there: Uniswap's `getSqrtRatioAtTick` is within one
unit of the true value for negative ticks, and for positive ticks is off by a relative 5e-20 at most,
sometimes below the true value.

## Why this is weak evidence

- None of it ran on a real EVM. The Python ports were validated against the repositories' own test
  values (284 for Solady, 41 for Uniswap; Balancer against its official Python port on 60,000 inputs),
  but a port can share a misreading with its author.
- A search shows where a violation is not. Only the Uniswap tick check and the small-input ranges are
  exhaustive.
- This result comes from one agent and was not re-run by a second one.
- Not covered: PRBMath `exp`, `log2`, `log10`, `pow` (no stated error bound), Uniswap `SqrtPriceMath`,
  Vyper and Rust libraries.
