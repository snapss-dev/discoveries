# Wide companions of nearby planet hosts in Gaia DR3: all 157 pairs were already catalogued

Status: **dead end** as a discovery (searched, nothing new). One side observation about an archive field
is recorded below. Produced with AI assistance; see the repository README.

## What was searched

Co-moving companions of confirmed exoplanet host stars: every Gaia DR3 source within 1 pc projected
(at most 0.5 degrees) of a host whose parallax matches the host's within 3 sigma and whose proper motion
differs by less than a bound orbit allows (the criterion of El-Badry, Rix and Heintz 2021).

Covered: the 1001 confirmed hosts nearest the Sun in the NASA Exoplanet Archive (all 867 with parallax
above 13.72 mas, about 73 pc, and 134 more out to about 89 pc). Not covered: hosts farther away, the 908
hosts known only as TESS candidates, and companions without a Gaia parallax (cool brown dwarfs), which is
where something new would most likely be.

## Result

157 co-moving pairs. 140 are in the catalogue of El-Badry, Rix and Heintz (MNRAS 506, 2269, 2021; 1.8
million pairs) and the other 17 are in the Washington Double Star Catalog. None is new.

The search recovered the standard cases it should: HD 189733 B, HD 80606 and HD 80607, 16 Cyg A and B,
and the WD 1856+534 triple.

## Side observation

For 60 of these hosts the NASA Exoplanet Archive gives the number of stars in the system (`sy_snum`) as
1, although a catalogued co-moving companion exists. Six were checked by hand on 2026-11-11 against the
live archive and the ESA Gaia archive:

| host | archive `sy_snum` | separation | projected | companion G | parallax difference | proper-motion difference (limit for a bound pair) |
|---|---|---|---|---|---|---|
| HD 155918 | 1 | 3.6" | 98 au | 13.1 | 2.6 sigma | 13.7 (51.4) mas/yr |
| BD+63 1405 | 1 | 2.6" | 97 au | 13.5 | 1.5 sigma | 18.5 (37.2) mas/yr |
| HD 23472 | 1 | 9.6" | 374 au | 15.8 | 1.4 sigma | 1.2 (18.6) mas/yr |
| HD 109988 | 1 | 20.3" | 865 au | 16.8 | 0.8 sigma | 8.8 (11.2) mas/yr |
| HD 109271 | 1 | 5.4" | 303 au | 16.3 | 2.2 sigma | 2.2 (14.6) mas/yr |
| TOI-1824 | 1 | 7.2" | 427 au | 14.3 | 1.9 sigma | 3.1 (11.4) mas/yr |

This is a gap in a database field, not a discovery: the companions are in a published catalogue, and
some are probably also in the companion surveys of M. Mugrauer and co-workers, which were not checked.
The other 54 hosts were not re-checked in the second pass.

## How to check

    python check.py            (reads hand_check.json)
    python check.py --fetch    (asks the NASA Exoplanet Archive and the Gaia archive again)

## Limits

- The first pass could not reach SIMBAD or the main VizieR site and used mirrors; its Gaia queries timed
  out partway down the list, which is why the search stops near 89 pc.
- The second pass re-ran only the six rows above. The count of 157 pairs and the catalogue matches are
  the first pass's.

## Credits

Gaia DR3 (ESA); NASA Exoplanet Archive; K. El-Badry, H.-W. Rix and T. Heintz for the binary catalogue;
the Washington Double Star Catalog (US Naval Observatory).
