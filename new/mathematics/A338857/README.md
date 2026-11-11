# A338857: the printed formula has the wrong sign, and fails at a 39-digit n

Status: **verified**, **new?** (2026-11-11). A correction to an entry, not new mathematics. Produced
with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A338857](https://oeis.org/A338857) (Gerhard Kirchner, 2020): with S(n, k) = sum_{j=n..k} 1/(2j+1),
a(n) = k + 1 for the k with S(n, k-1) < 1 <= S(n, k). It arises from a "camel and water bags" transport
problem and begins 1, 8, 15, 23, 30, 38, ... The entry says:

> Conjecture: a(n) = ceiling(n*exp(2)+(exp(2)+exp(-2))/(24*n)), verified for n<=3000.

## Result

The sign inside the bracket should be a minus. Since S(n, k) = (psi(k + 3/2) - psi(n + 1/2))/2 and
psi(x + 1/2) = log x + 1/(24 x^2) + ..., the crossover is at
n e^2 + (e^2 - e^-2)/(24n) + O(n^-3). The author's own linked note derives the coefficient with the
minus sign; the formula line in the entry has a plus.

For n <= 3000 both versions give the same integers, which is why the check in the entry passed. They
first differ at

    n = 541727237873320516868722558441138350267,

where a(n) = 4002852950964714093701063853934751122173, the printed formula gives ...174, and the
formula with the minus sign gives ...173.

## Check

    python check.py

computes a(n) from the digamma function at 150 digits (validated against exact rational sums for
n <= 400), confirms that both formulas agree with a(n) for n <= 3000, and prints the three values at the
39-digit n. Output in `check.log`.

## Limits

The corrected formula is not proved either. The agent that found this checked it for n <= 20000 and at
every continued-fraction candidate of e^2 below 10^400 without finding a failure.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads (an editor asked in
2020 for the formula to be labelled a conjecture; the sign was not discussed); the draft page (no pending
edit); an in-depth web search with the sequence number; Epoch AI's OEIS Open conjecture list; and the
omega-institute project's issues and code. None mentions the sign or a counterexample.
