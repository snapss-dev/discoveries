# A115066: three congruences for the Chebyshev values T_n(n)

Status: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry

[A115066](https://oeis.org/A115066): a(n) = T_n(n), the Chebyshev polynomial of the first kind evaluated
at x = n: 1, 1, 7, 99, 1921, 47525, ... It carries the remark (Peter Bala, 1 February 2022): "It appears
that a(2*n+1) == 0 (mod (2*n+1)^2) and 2*a(4*n+2) == -2 (mod (4*n+2)^4), while for k > 1,
2*a(2^k*(2*n+1)) == 2 (mod (2^k*(2*n+1))^4)."

## Result

All three congruences hold. In terms of m:

- m odd: T_m(m) is divisible by m^2; more precisely T_m(m) = (-1)^((m-1)/2) m^2 modulo m^3.
- m = 2 modulo 4: 2 T_m(m) = -2 modulo m^4.
- m = 0 modulo 4: 2 T_m(m) = 2 modulo m^4.

## Proof

**Odd m = 2r + 1.** T_m is an odd polynomial with integer coefficients, and its linear coefficient is
T_m'(0) = m U_(m-1)(0) = (-1)^r m. So T_m(x) = (-1)^r m x + x^3 (integer polynomial), and at x = m this
is (-1)^r m^2 plus a multiple of m^3.

**Even m = 2r.** T_(2r)(x) = T_r(2x^2 - 1). Expand T_r around -1: T_r(-1 + y) is an integer polynomial in
y with constant term T_r(-1) = (-1)^r and linear coefficient T_r'(-1) = r U_(r-1)(-1) = (-1)^(r-1) r^2.
With y = 2x^2:

    T_m(x) = (-1)^r + (-1)^(r-1) * 2 r^2 x^2 + 4 x^4 (integer polynomial).

At x = m = 2r we have 2 r^2 x^2 = m^4 / 2, so

    2 T_m(m) = 2 (-1)^r + (-1)^(r-1) m^4 + 8 m^4 (integer),

which is 2 (-1)^r modulo m^4. Finally r is odd exactly when m = 2 modulo 4. ∎

## Check

    python check.py 500

verifies all three congruences, and the sharper one for odd m, for every n <= 500. Output in `check.log`.

## Novelty check

The published entry and the first page of its revision history (to February 2022) show no proof. A web
search found nothing further. Older history pages were not read. Checked 2026-11-11.
