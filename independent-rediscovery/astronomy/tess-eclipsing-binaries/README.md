# Two bright eclipsing binaries that turned out to be catalogued

Status: **killed** as a discovery; **rediscovery** of published results. Produced with AI assistance;
see the repository README.

## What was claimed

A screen of TESS light curves (the MIT Quick-Look Pipeline, 200 s cadence) for every star brighter than
Gaia G = 9.8 in the two newest sectors turned up eclipse-like signals in 175 stars. Of these, 139 were
already known variables. An agent reported two bright stars among the rest as uncatalogued eclipsing
binaries:

| star | TIC | T mag | period | depth |
|---|---|---|---|---|
| HD 176729 (HIP 93784), A0V | 464583002 | 7.46 | 6.0731 d | about 8% |
| HD 158910, A1m | 73928163 | 7.96 | 4.0054 d | about 6%, secondary 0.8% |

## What is true

The eclipses are real and on target. A pixel-level check on the raw TESS full-frame cutouts for
HD 176729 gives a depth of 8.1 to 8.4% in three separate sectors, with the difference-image centroid
within 4 arcseconds of the star.

**Both were already published.**

- HD 176729 is in the eclipsing-binary table of IJspeert et al. 2021 (A&A 652, A120) with period
  6.07295 d and depth 0.077, in IJspeert et al. 2024 (A&A 691, A242), and in Battley et al. 2022
  (MNRAS 511, 4285).
- HD 158910 is in IJspeert et al. 2024 and in Battley et al. 2022 (listed there at half the period).

The agent had reported these catalogues as checked and negative. A query of every VizieR catalogue at the
star's position showed the entries within minutes.

## What is left

- Neither star had an entry in the AAVSO Variable Star Index on 2026-11-11 (cone search of 3 arcminutes),
  although both are published. That is a gap in an index, not a discovery.
- A third, fainter signal (HD 6856, TIC 402041440, period 3.0129 d, two equal eclipses of 1.3%) was not
  found in those tables, but a star of G = 12.6 lies 4.3 arcseconds away and could be the eclipsing one.
  It has not been checked further.

## Lesson

"Not in the catalogue" must be re-run by whoever makes the claim public. A position query across all
catalogues is cheap and should come first.

## Data and credits

TESS data from the Mikulski Archive for Space Telescopes (MAST); light curves from the MIT Quick-Look
Pipeline. Catalogue access through VizieR (CDS, Strasbourg) and its mirrors.
