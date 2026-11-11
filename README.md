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
| [ERC interface identifiers](new/software/erc-165-identifiers/README.md) | Twenty-seven interface identifiers and selectors printed in Ethereum ERC documents do not match the signatures printed beside them, seven of them in Final or Last Call standards. A contract written from the text and one using the compiler's value answer `supportsInterface` differently. |
| [ERC-7857 storage slot](new/software/erc-7857-storage-slot/README.md) | The storage constant in a Final ERC's reference contract is not the ERC-7201 slot of the namespace it names. |
| [SLIP-0132 prefixes](new/software/slip-0132-version-prefixes/README.md) | Three rows of a key-prefix registry print prefixes their version bytes cannot produce. |
| [NIST DLMF table digits](new/reference-works/dlmf-table-last-digits/README.md) | Six entries in four tables of the NIST Digital Library of Mathematical Functions are not the correctly rounded values, and none is in its errata list. |
| [Wikipedia: wrong digits](new/reference-works/wikipedia-decimal-values/README.md) | Wrong digits in 17 English Wikipedia articles, found by recomputation: the standard normal table at z = 0.16 (since 2014), eight of ten listed zeros of the zeta function, chi-squared critical values, and others. |
| [Wikipedia: integer lists](new/reference-works/wikipedia-integer-tables/README.md) | Four integer lists that differ from recomputation: the count of five-digit prime quadruplets (26, not 27), a missing perfect totient number, a missing divisor, a repeated prime. |
| [A332786 and A330718](new/mathematics/A332786-A330718/README.md) | 16843^2 answers the "weak pseudoprime" questions in both entries. A second, independent computation of the A332786 result filed separately, extended to A330718. |
| [A246754](new/mathematics/A246754/README.md) | A listed term is one too large: 13993959^13993959 has exactly 10^8 digits. The entry's formula overshoots at the same places. |
| [A320065](new/mathematics/A320065/README.md) | A 2025 Lambert W formula first fails at n = 3431, then at the end of every block. |
| [A059923, A207976](new/mathematics/A059923-A207976/README.md) | Two formulas of the form floor(x^n), stated as fact, fail from n = 24 and n = 27. |
| [V627 Peg, 1905 outburst](new/astronomy/v627-peg-1905-outburst/README.md) | Six Harvard plates from August 1905 show the dwarf nova V627 Peg in outburst, 37 years before the earliest outburst in the literature. Measured twice, the second time from the plate pixels. |
| [A072633, smallest counterexample](new/mathematics/A072633-smallest-counterexample/README.md) | The conjecture a(n) = 1 + round(n / log 2) fails at a 330-digit n found by Antonio Sanso. New here: a proof that this n is the smallest counterexample, the bound F(n) <= a(n) <= F(n) + 1, four further counterexamples, and the answer to an open remark in A332101. |
| [A332102](new/mathematics/A332102/README.md) | The conjecture a(n) = round(n / log(3/2) + 3) fails at a 1614-digit n, certified with interval arithmetic. |
| [A100682](new/mathematics/A100682/README.md) | A 2012 conjecture lists six exceptions to a formula for the fourth roots of pentatope numbers. There are more: the next two are near 6 * 10^8 and 1.7 * 10^9, and 61 are listed. |
| [A271817](new/mathematics/A271817/README.md) | Three new terms of a sequence untouched since 2016: a(10) = a(11) = 2352655113 and a(12) = 17546197568. |
| [A254069](new/mathematics/A254069/README.md) | A new term, a(4) = 909764941: the first run of eight consecutive odd numbers with no squarefree member, in the entry's terms. |
| [A028576](new/mathematics/A028576/README.md) | A 2026 conjecture of F. Chapoton: n divides a(n) and n^2 divides 3 a(n), for a Möbius sum of squared central binomial coefficients. Proved, with exact bounds at each prime. |
| [A121860, sharp onset](new/mathematics/A121860-sharp-onset/README.md) | lcm(1, ..., n) divides a(n) - 2 for every n except 4. This sharpens a conjecture already proved by others, and settles a form suggested by Peter Luschny. |
| [A229324](new/mathematics/A229324/README.md) | "All terms are apparently multiple of 5" (2013) fails at 10419754, the first term with four prime factors. |
| [A337385](new/mathematics/A337385/README.md) | "Apparently, all terms are divisible by 255255" (2020) fails at 8562829275. |
| [A064169](new/mathematics/A064169/README.md) | A list of four exceptions "tested to 20000" misses five more inside that range. |
| [A000846, A051924](new/mathematics/A000846-A051924/README.md) | Two "only for primes" remarks fail at 16843^2, the square of a Wolstenholme prime. |
| [A332786](new/mathematics/A332786/README.md) | "Is 7^2 the only weak pseudoprime?" (2020). No: 16843^2 is another. |
| [A036283](new/mathematics/A036283/README.md) | Two wrong values in a 10000-term b-file, with a proof of the relation a(n) = 6 A202318(n) that exposes them. The relation is stated without proof in A202318. |
| [A227728](new/mathematics/A227728/README.md) | The b-file is wrong from n = 643 on, 358 entries. The conjectured recurrence holds for the corrected terms up to 1000. |
| [A044140](new/mathematics/A044140/README.md) | A recurrence guessed from 42 terms fails at the 58th. |
| [A285563](new/mathematics/A285563/README.md) | An empirical generating function matches 36 terms and fails at the 37th. |
| [A086651](new/mathematics/A086651/README.md) | "It appears that a(6k+3) is always 2. Is this easy to prove?" (2003). A closed form for every term, by induction. |
| [A115066](new/mathematics/A115066/README.md) | Three congruences for the Chebyshev values T_n(n), observed in 2022. |
| [A338857](new/mathematics/A338857/README.md) | The formula printed in the entry has the wrong sign; it agrees with the sequence up to 3000 and first fails at a 39-digit n. |
| [A123855](new/mathematics/A123855/README.md) | "It appears that 2^k divides a(2^k-1)" (2006), for a double sum of prime powers. A short proof. |
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
| [A243013](independent-rediscovery/mathematics/A243013/README.md) | The seventh term of a count of graceful graphs should be 37, not 36 | Already listed correctly in A308544 |
| [A226183](independent-rediscovery/mathematics/A226183/README.md) | The formula printed in the entry is wrong at n = 10 | Jon E. Schoenfield and Kevin Ryde, in the entry's own discussion thread, 2021 |
| [A092674](independent-rediscovery/mathematics/A092674/README.md) | A closed form showing the sequence is never negative | Implicit in the companion entry A092673 since 2007 |
| [A091817](independent-rediscovery/mathematics/A091817/README.md) | Leroy Quet's conjecture that every term is an integer | Foundation-0's math0 project, October 2026; a classical congruence (Sun and Zhao, 2013) |
| [A276531](independent-rediscovery/mathematics/A276531/README.md) | Every term of a Somos-like recurrence is an integer | Michael Somos, 2016, in the entry |
| [A006579](independent-rediscovery/mathematics/A006579/README.md) | A 2025 conjecture fails at a 14-digit number | Varun Vejalla, June 2025, in A018804 |
| [Arctic islands](independent-rediscovery/geography/arctic-islands/README.md) | Three islands exposed by glacier retreat, with area and elevation time series | Russia's Northern Fleet and the Russian Geographical Society; M. Pelto |
| [TESS eclipsing binaries](independent-rediscovery/astronomy/tess-eclipsing-binaries/README.md) | Two bright eclipsing binaries | IJspeert et al. 2021 and 2024; Battley et al. 2022 |

## candidates

| page | what |
|---|---|
| [Euclid Q1 lens candidates](candidates/astronomy/euclid-q1-lens-candidates/README.md) | Four possible strong gravitational lenses in Euclid early-release imaging; two plausible, two weak, none in the published lists. |
| [Earthwork screening](candidates/archaeology/earthwork-screening/README.md) | Eight screens of open lidar and imagery for unrecorded earthworks, with calibration results and confidence. No positions are given. |
| [Great Lakes bathymetry](candidates/archaeology/great-lakes-bathymetry-screening/README.md) | One wreck-shaped body in open lidar bathymetry, from an uncalibrated detector. Position withheld. |
| [Tjibangara 1934 meteorite](candidates/history/tjibangara-1934-meteorite/README.md) | Newspaper reports and an observatory analysis of a 1934 fall in West Java that copies of the official register do not list. |
| [Four possible outbursts on Harvard plates](candidates/astronomy/harvard-plate-outbursts/README.md) | GY Cet in 1943, V624 Peg in 1938, V355 UMa in 1930 and V4641 Sgr in 1901: bright images on old plates with no report found. Not re-measured. |
| [Ring earthwork in Yonne](candidates/archaeology/yonne-ring-earthwork/README.md) | A bank and ditch 70 m across under forest in French lidar, on no map from 1750 to today. Undated, and the official register is closed. |
| [Ring enclosure near Boca do Acre](candidates/archaeology/acre-ring-enclosure/README.md) | A ring 156 m across in land cleared in 2021, with the plan of an Acre geoglyph, 29 km from the nearest registered site. A modern track is not excluded. |
| [Two possible cairns in Galloway](candidates/archaeology/galloway-cairns/README.md) | Hollow-topped mounds in Scottish lidar that match recorded cairns nearby and have no record of their own. Weak. |

## dead-ends

| page | what |
|---|---|
| [Wide companions of planet hosts](dead-ends/astronomy/wide-companions-of-planet-hosts/README.md) | All 157 co-moving companions found in Gaia DR3 were already catalogued. Side note: some hosts listed as single in an archive have a catalogued companion. |
| [Rock avalanches, 2026](dead-ends/geoscience/rock-avalanches-2026/README.md) | No unreported 2026 rock avalanche found on glaciers, with a detector that missed a known one. |
| [Mexico G-LiHT lidar](dead-ends/archaeology/mexico-gliht-lidar/README.md) | No unrecorded platforms found in NASA lidar strips outside the Maya area; the search was partial. |
| [Borger 1929 meteorite](dead-ends/history/borger-1929-meteorite/README.md) | A reported meteorite that a follow-up article identified as a weathered boulder. |
| [Core EIP and BIP examples](dead-ends/software/eip-bip-test-vectors/README.md) | About 1,050 worked examples and test vectors in core Ethereum and Bitcoin proposals recomputed. None wrong. |
| [A136616](dead-ends/mathematics/A136616/README.md) | A harmonic-number formula searched for a failure with the continued-fraction method, below 10^10000. None found; still unproved. |
| [Fixed-point math libraries](dead-ends/software/fixed-point-math-libraries/README.md) | An adversarial search for inputs that break documented rounding or monotonicity guarantees in smart-contract math libraries. None found. |
| [Scottish lidar look-alikes](dead-ends/archaeology/scottish-lidar-lookalikes/README.md) | Five mounds and rings that looked like cairns in lidar and were a quarry, a gravel pit, a rock knoll, heaps and scrub. |

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
  formal-conjectures repository, the omega-institute project and Foundation-0's math0; for a variable
  star: its entry in the AAVSO index, the papers on the star, and other observatories' plate archives).
  Ten results first taken to be new were filed under `independent-rediscovery/` because of this check.
  It can still miss things.
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
