# discoveries

Small, checkable findings from open data, each with the code that verifies it.

The work here is done by AI agents (Anthropic's Claude models) under human direction: the agents search
public data, propose a result, and then try to break it. A result is listed only with the scripts and
logs needed to check it independently, and with an honest label for how far it has been verified and
whether it is new.

## Status labels

| label | meaning |
|---|---|
| **verified** | Checked by at least two independent methods; the scripts are in this repository. |
| **new?** | No earlier record found after reading the relevant catalogue, its revision history and a web search. That is a statement about the search, not a guarantee. |
| **rediscovery** | Found independently here, but someone else had it first. Credit is given in the entry. |
| **candidate** | Plausible, not confirmed. Needs an expert or data that was not reachable. |
| **killed** | Announced by an agent, then refuted on checking. Kept in the log so the mistake is visible. |

## Index

| entry | what | status |
|---|---|---|
| [oeis/A072633](oeis/A072633/README.md) | The conjecture a(n) = 1 + round(n / log 2) first fails at a 330-digit n. That n was found by Antonio Sanso in July 2026. Added here: a proof that it is the smallest counterexample, the bound F(n) <= a(n) <= F(n) + 1, and the next four counterexamples. | counterexample: **rediscovery** (Sanso). Minimality: **verified**, **new?** |
| [oeis/A092674](oeis/A092674/README.md) | A conjecture open in the entry since 2004 (a(n) is never negative) is true, with a closed form: a(n) = phi(n) - mu(n) + [n even] mu(n/2). | **verified**, **new?** |
| [log/2026-11-11](log/2026-11-11.md) | First sprint: fourteen search lanes, what each found, and what was wrong. | mixed |

## How results are produced and checked

- **AI-assisted.** The searches, code, proofs and prose in this repository were written by AI models. A
  human chose the directions and asked the questions. No AI system is an author of anything, and
  nothing here should be cited as peer-reviewed work.
- **Two independent checks.** A numerical claim is accepted only if two implementations that share no
  code agree, with certified interval arithmetic where rounding matters. A proof is accepted only after
  a separate review that re-derives it, and it stays labelled as unrefereed.
- **Novelty is checked, and can still be wrong.** The first result announced here turned out to have been
  posted by someone else three and a half months earlier; it was visible only in a revision history. The
  log records this and the other mistakes.
- **Negative results are kept.** A lane that found nothing, or a claim that died on checking, stays in
  the log.

## These are not OEIS submissions

Nothing in this repository has been submitted to the On-Line Encyclopedia of Integer Sequences. The OEIS
requires a human author who understands and vouches for every contribution, and it prohibits using AI to
generate the full text of comments
([policy](https://oeis.org/wiki/Use_of_AI_for_OEIS_Submissions_is_Forbidden)). Anyone who wants to use a
result from here in the OEIS or elsewhere should verify it themselves, write it in their own words, and
credit the people named in the entry.

## Reproducing

Python 3.11 or later:

    pip install -r requirements.txt

Each entry's README lists the exact commands and their run times. `check.gp` files need PARI/GP.

## Corrections

If something here is wrong, or already known, please open an issue. Entries are corrected in place and
the correction is noted in the log.
