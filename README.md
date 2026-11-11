# discoveries

Small, checkable findings from open data, each with the code that verifies it.

The work here is done by AI agents (Anthropic's Claude models) under human direction: the agents search
public data, propose a result, and then try to break it. Every finding has its own page with the
evidence needed to check it, an honest label for how far it has been verified, and credit to whoever had
it first. Rediscoveries and dead ends are kept too, labelled as such.

## Status labels

| label | meaning |
|---|---|
| **verified** | Checked by at least two independent methods; the scripts are on the page. |
| **new?** | No earlier record found in the relevant catalogue, its revision history, or a web search. That is a statement about the search, not a guarantee. |
| **rediscovery** | Found independently here, but someone else had it first. Credit is on the page. |
| **candidate** | Plausible, not confirmed. Needs an expert or data that could not be reached. |
| **killed** | Claimed, then refuted on checking. Kept so the reason is on record. |

## Findings

### Integer sequences (OEIS)

| page | what | status |
|---|---|---|
| [A072633](oeis/A072633/README.md) | The conjecture a(n) = 1 + round(n / log 2) first fails at a 330-digit n, found by Antonio Sanso in July 2026. Added here: a proof that it is the smallest counterexample, the bound F(n) <= a(n) <= F(n) + 1, and the next four counterexamples. | counterexample: **rediscovery** (Sanso); minimality: **verified**, **new?** |
| [A028576](oeis/A028576/README.md) | A 2026 conjecture of F. Chapoton: n divides a(n) and n^2 divides 3 a(n), for a Möbius sum of squared central binomial coefficients. Proved, with exact bounds at each prime. | **verified**, **new?** |
| [A086651](oeis/A086651/README.md) | "It appears that a(6k+3) is always 2. Is this easy to prove?" (2003). Yes: closed form for every term, by induction. | **verified**, **new?** |
| [A202194, A202202](oeis/A202194/README.md) | Binary arrays avoiding 001 and 101 in rows and columns number 2RC·binomial(R+C-2, R-1). Proves a 2020 conjecture and a 2011 empirical table. | **verified**, **new?** |
| [A121860](oeis/A121860/README.md) | A 2025 conjecture: modulo any k the sequence is eventually constant, equal to 2. True for all n >= (k+2)^2. | **verified**, **new?** |
| [A115066](oeis/A115066/README.md) | Three congruences for the Chebyshev values T_n(n), observed in 2022. | **verified**, **new?** |
| [A092674](oeis/A092674/README.md) | A conjecture open in the entry since 2004 (a(n) is never negative), with the closed form a(n) = phi(n) - mu(n) + [n even] mu(n/2). | **verified**, **new?** |
| [Four short proofs](oeis/short-proofs/README.md) | A069097, A234307, A055210, A023887: identities still marked as conjectures in their entries. | **verified**, **new?** |

### Earth and sky

| page | what | status |
|---|---|---|
| [Arctic islands](geography/arctic-islands/README.md) | Three islands exposed by glacier retreat in Novaya Zemlya and Franz Josef Land, found in satellite imagery and then traced to earlier Russian and glaciological reports. Adds area and elevation time series. | **rediscovery** |
| [Lost meteorites](history/lost-meteorites/README.md) | Newspaper reports of a 1934 fall in West Java, with an observatory analysis, that copies of the official register do not list; and a 1929 Dutch report that a follow-up article refutes. | **candidate**; **killed** |
| [TESS eclipsing binaries](astronomy/tess-eclipsing-binaries/README.md) | Two bright eclipsing binaries reported as uncatalogued; both were in published catalogues. | **killed** (**rediscovery**) |

## How results are produced and checked

- **AI-assisted.** The searches, code, proofs and prose in this repository were written by AI models. A
  human chose the directions and asked the questions. No AI system is an author of anything, and
  nothing here should be cited as peer-reviewed work.
- **Two independent checks.** A numerical claim is accepted only if two implementations that share no
  code agree, with certified interval arithmetic where rounding matters. A proof is accepted only after
  it has been re-derived separately and checked numerically from the definition, and it stays labelled
  as unrefereed.
- **Novelty is checked, and can still be wrong.** The first result found here turned out to have been
  posted by someone else three and a half months earlier; it was visible only in a revision history.
  Each page says exactly what was searched.
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

If something here is wrong, or already known, please open an issue. Pages are corrected in place.
