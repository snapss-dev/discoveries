# Unreported 2026 rock avalanches on glaciers: none found, with a detector that missed a known one

Status: **dead end** (searched, nothing found; weak negative). Produced with AI assistance; see the
repository README.

## The idea

Large rock avalanches onto glaciers leave a dark debris sheet on bright ice. Many happen in ranges where
nobody is watching, and some are first noticed on satellite images. Comparing late-summer Sentinel-2
images of 2025 and 2026 should show the new ones.

## What was done

For ten glacier regions (Alaska Range, Chugach, Wrangell, St. Elias, Fairweather, Iliamna, the Coast
Mountains and southern British Columbia, Karakoram, Pamir), the five least cloudy Sentinel-2 scenes
between 15 July and 20 September of each year were composited at 80 m. A pixel counted as changed if it
was bright snow or ice in every 2025 scene (green reflectance above 0.25, snow index above 0.4) and dark
in every 2026 scene (green below 0.18, snow index below 0.3). Connected patches of at least 0.3 km2 were
ranked and looked at on contact sheets, and the best were followed through every available scene.

Area tested: 143 tiles, about 105,500 km2 of snow and ice (an upper bound, because tile overlaps are
counted twice). The second pass recomputed this figure from the first pass's stored composites.

## Result

No new rock avalanche. The detector flagged patches in three regions on its final run (Chugach 6,
St. Elias 9, Karakoram 4) and none in six others; the first pass judged none of them to be an
avalanche deposit.

## Why this is only a weak negative

The first pass reported that the detector did not flag a known recent rock avalanche on Red Glacier at
Iliamna volcano. A detector that misses a known event cannot rule out unknown ones. A possible reason,
not tested: the rule requires bright ice in every 2025 scene, and debris that falls on ice that was
already partly dark fails it. For a second test site in the St. Elias Mountains the first pass left
before-and-after images but no recorded outcome. Deposits smaller than 0.3 km2, and anything hidden by
cloud or early snow in the 2026 window, were out of reach by design.

## What the second pass did

It recomputed the tested area, read the detection logs for every region and looked at one calibration
image pair. It did not repeat the scan.

## Data and credits

Copernicus Sentinel-2 Level-2A, read through a public STAC catalogue.
