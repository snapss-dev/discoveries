# discoveries

Small, checkable findings from open data, each with the code that verifies it, sorted by how new they
are.

The work here is done by AI agents (Anthropic's Claude models) under human direction: the agents search
public data, propose a result, and then try to break it. Every finding has its own page with the
evidence needed to check it and credit to whoever had it first.

## How the repository is sorted

| folder | what is in it |
|---|---|
| [`new/`](new) | Verified, and no earlier record found after the novelty check described below. That is a statement about the search, not a guarantee. |
| [`independent-rediscovery/`](independent-rediscovery) | Found independently here, but someone else had it first. Each page names them and says how the earlier work was missed. |
| [`candidates/`](candidates) | Plausible, not confirmed. Needs an expert or data that could not be reached. |
| [`dead-ends/`](dead-ends) | Claimed and then refuted, or searched for and not found. Kept so the reason is on record. |

Below each of these, pages are grouped by field.

## new

| page | what |
|---|---|
| [A072633, smallest counterexample](new/mathematics/A072633-smallest-counterexample/README.md) | The conjecture a(n) = 1 + round(n / log 2) fails at a 330-digit n found by Antonio Sanso. New here: a proof that this n is the smallest counterexample, the bound F(n) <= a(n) <= F(n) + 1, four further counterexamples, and the answer to an open remark in A332101. |
| [A332102](new/mathematics/A332102/README.md) | The conjecture a(n) = round(n / log(3/2) + 3) fails at a 1614-digit n, certified with interval arithmetic. |
| [A100682](new/mathematics/A100682/README.md) | A 2012 conjecture lists six exceptions to a formula for the fourth roots of pentatope numbers. There are more: the next two are near 6 * 10^8 and 1.7 * 10^9, and 61 are listed. |
| [A028576](new/mathematics/A028576/README.md) | A 2026 conjecture of F. Chapoton: n divides a(n) and n^2 divides 3 a(n), for a Möbius sum of squared central binomial coefficients. Proved, with exact bounds at each prime. |
| [A121860, sharp onset](new/mathematics/A121860-sharp-onset/README.md) | lcm(1, ..., n) divides a(n) - 2 for every n except 4. This sharpens a conjecture already proved by others, and settles a form suggested by Peter Luschny. |
| [A229324](new/mathematics/A229324/README.md) | "All terms are apparently multiple of 5" (2013) fails at 10419754, the first term with four prime factors. |
| [A337385](new/mathematics/A337385/README.md) | "Apparently, all terms are divisible by 255255" (2020) fails at 8562829275. |
| [A064169](new/mathematics/A064169/README.md) | A list of four exceptions "tested to 20000" misses five more inside that range. |
| [A000846, A051924](new/mathematics/A000846-A051924/README.md) | Two "only for primes" remarks fail at 16843^2, the square of a Wolstenholme prime. |
| [A044140](new/mathematics/A044140/README.md) | A recurrence guessed from 42 terms fails at the 58th. |
| [A086651](new/mathematics/A086651/README.md) | "It appears that a(6k+3) is always 2. Is this easy to prove?" (2003). A closed form for every term, by induction. |
| [A115066](new/mathematics/A115066/README.md) | Three congruences for the Chebyshev values T_n(n), observed in 2022. |
| [A338857](new/mathematics/A338857/README.md) | The formula printed in the entry has the wrong sign; it agrees with the sequence up to 3000 and first fails at a 39-digit n. |
| [Three short proofs](new/mathematics/short-proofs/README.md) | A069097, A234307, A055210: identities still marked as conjectures in their entries. |

## independent-rediscovery

| page | what | who had it first |
|---|---|---|
| [A072633 counterexample](independent-rediscovery/mathematics/A072633-counterexample/README.md) | The 330-digit counterexample itself | Antonio Sanso, July 2026 |
| [A121860 conjecture](independent-rediscovery/mathematics/A121860-conjecture/README.md) | Modulo any k the sequence is eventually 2 | Haobo Ma and Wenlin Zhang, November 2026 |
| [A202194, A202202](independent-rediscovery/mathematics/A202194/README.md) | Counting binary arrays that avoid 001 and 101 | Christian Krause, June 2026 |
| [A023887](independent-rediscovery/mathematics/A023887/README.md) | An identity for sigma_m(n) | Sela Fried (m = 2); the omega-institute project, September 2026 |
| [A190363](independent-rediscovery/mathematics/A190363/README.md) | A guessed recurrence fails at the 161st term | A contributor to Google DeepMind's formal-conjectures; Daniel Veljjanoski, November 2026 |
| [A139394](independent-rediscovery/mathematics/A139394/README.md) | The conjecture a(n) > 0 fails near 6 * 10^11 | Bays and Hudson, 1978 |
| [A092674](independent-rediscovery/mathematics/A092674/README.md) | A closed form showing the sequence is never negative | Implicit in the companion entry A092673 since 2007 |
| [Arctic islands](independent-rediscovery/geography/arctic-islands/README.md) | Three islands exposed by glacier retreat, with area and elevation time series | Russia's Northern Fleet and the Russian Geographical Society; M. Pelto |
| [TESS eclipsing binaries](independent-rediscovery/astronomy/tess-eclipsing-binaries/README.md) | Two bright eclipsing binaries | IJspeert et al. 2021 and 2024; Battley et al. 2022 |

## candidates

| page | what |
|---|---|
| [Tjibangara 1934 meteorite](candidates/history/tjibangara-1934-meteorite/README.md) | Newspaper reports and an observatory analysis of a 1934 fall in West Java that copies of the official register do not list. |

## dead-ends

| page | what |
|---|---|
| [Borger 1929 meteorite](dead-ends/history/borger-1929-meteorite/README.md) | A reported meteorite that a follow-up article identified as a weathered boulder. |
| [Fixed-point math libraries](dead-ends/software/fixed-point-math-libraries/README.md) | An adversarial search for inputs that break documented rounding or monotonicity guarantees in smart-contract math libraries. None found. |

## How results are produced and checked

- **AI-assisted.** The searches, code, proofs and prose in this repository were written by AI models. A
  human chose the directions and asked the questions. No AI system is an author of anything, and
  nothing here should be cited as peer-reviewed work.
- **Two independent checks.** A numerical claim is accepted only if two implementations that share no
  code agree, with certified interval arithmetic where rounding matters. A proof is accepted only after
  it has been re-derived separately and checked numerically from the definition, and it stays
  unrefereed.
- **The novelty check.** Before a page goes under `new/`, the following are read: every page of the
  relevant revision history, including discussion threads; pending drafts; cross-referenced entries and
  the files attached to them; an in-depth web search with the identifier; and the current large-scale
  efforts in the same area (for integer sequences: Epoch AI's OEIS Open benchmark, Google DeepMind's
  formal-conjectures repository and the omega-institute project). Seven results first taken to be new
  were filed under `independent-rediscovery/` because of this check. It can still miss things.
- **Sensitive locations are withheld.** Positions of possible archaeological sites or wrecks are not
  published here.

## These are not OEIS submissions

Nothing in this repository has been submitted to the On-Line Encyclopedia of Integer Sequences. The OEIS
requires a human author who understands and vouches for every contribution, and it prohibits using AI to
generate the full text of comments
([policy](https://oeis.org/wiki/Use_of_AI_for_OEIS_Submissions_is_Forbidden)). Anyone who wants to use a
result from here in the OEIS or elsewhere should verify it themselves, write it in their own words, and
credit the people named on the page.

## Reproducing

Python 3.11 or later:

    pip install -r requirements.txt

Each page lists the exact commands. `check.gp` files need PARI/GP.

## Corrections

If something here is wrong, or already known, please open an issue. Pages are corrected in place and
moved to the folder that fits.
