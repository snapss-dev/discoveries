# Islands released by glaciers: 213 coastal tiles from the Antarctic Peninsula to Greenland searched, one candidate, the rest known or nothing

Status: **dead end with coverage** (one candidate and one rediscovery are filed on their own pages).
Searched on 2026-11-11. Produced with AI assistance; see the repository README.

## The question

Where does a current map still draw land as attached to the mainland, usually through a glacier, while
recent satellite images show it surrounded by water? An earlier pass covered the Russian Arctic and
Svalbard (page `independent-rediscovery/geography/arctic-islands`). This pass covered the regions below.

## Method

For each Sentinel-2 tile (110 km square, 20 m pixels) up to three low-cloud late-summer scenes of 2025
and 2026 were read. A pixel is water if it is water (NDWI above 0.15, near infrared below 0.12) in any
of the scenes, so drifting ice does not bridge a channel. Connected non-water bodies that touch neither
the tile edge nor missing data were compared with OpenStreetMap land polygons (download of 2026-11-11).
A body counts as a candidate when more than half of it lies inside a mapped land polygon at least four
times its size, at least 30 % of it is free of snow and ice, the water around it connects to mapped sea
(or to a lake of more than 1 km²), ice is present within 3 km, and the water around it does not lie on
steep ground in the Copernicus 30 m elevation model (median slope under 8 degrees; this removes terrain
shadow, the main false alarm). What remained was looked at by eye on contact sheets and, where it
looked real, on Landsat scenes back to the 1980s. The detector was adjusted during the run: the first
regions used a minimum body size of 0.05 km² and the later ones 0.024 km² (candidates were cut at
0.05 km² throughout), and Patagonia, Tierra del Fuego, Alaska, east Greenland, Canada and the Antarctic
Peninsula used two scenes per tile instead of three. `detect.py` is the final version.

## Coverage and calibration

From `check.py`:

| region | tiles | with coast, analysed | mapped islands in them | recovered | left for inspection |
|---|---|---|---|---|---|
| South Georgia | 10 | 5 | 49 | 27 (55 %) | 12 |
| Patagonia, 46 to 52.5 S | 24 | 22 | 1494 | 374 (25 %) | 10 |
| Tierra del Fuego, 54 to 55.3 S, 68 to 72.5 W | 11 | 10 | 485 | 121 (25 %) | 0 |
| North-west Greenland, 72 to 76.7 N | 48 | 23 | 572 | 461 (81 %) | 6 |
| West Greenland, 68 to 72 N | 24 | 20 | 938 | 671 (72 %) | 10 |
| South-east Greenland, 60 to 68.7 N | 81 | 31 | 1118 | 730 (65 %) | 11 |
| East Greenland, 68.7 to 74.5 N, part | 35 | 28 | 72 | 64 (89 %) | 11 |
| South-east Ellesmere and north Devon, 72 to 84 W, part | 24 | 19 | 88 | 66 (75 %) | 6 |
| Alaska coast, 132 to 151 W | 83 | 32 | 766 | 404 (53 %) | 15 |
| Antarctic Peninsula, 62.8 to 68 S | 52 | 30 | 636 | 292 (46 %) | 10 |
| total | 392 | 220 | 6218 | 3210 (52 %) | 91 |

Seven tiles on the boundary between the two west Greenland regions are counted twice: 385 distinct
tiles, 213 of them analysed.

"Mapped islands" are OpenStreetMap islands of 0.05 to 100 km² lying wholly inside valid data; "recovered"
means the detector found a water-enclosed body on them. The South Georgia figure of 12 was taken before
the slope filter was added; all 12 were terrain shadow.

Recall is far from complete, and worst in the Chilean channels. On one Patagonian tile every miss was
traced: of 102 mapped islands not recovered, 62 were joined in the 20 m mask to a body reaching the tile
edge (the mainland or a large island) and 38 to a neighbouring island, across channels narrower than
about 60 m (the detector closes gaps of two pixels); two had other causes.
An island separated from a glacier by less than about 60 m of water would be missed in the same way.

Documented separations recovered:

- **Prow Knob, Alsek Lake, Alaska** (became an island in the summer of 2025; NASA Earth Observatory,
  "Alaska's Brand New Island", 2025): found at 59.194 N, 138.066 W, 4.63 km².
- **The Cape Caledon islets, Devon Island** (M. Pelto, 4 September 2018): two of the three found. Filed
  as `independent-rediscovery/geography/cape-caledon-islands`.
- The long-known islands of Vitus Lake at the Bering Glacier front, Alaska (9.1 and 1.4 km²).

## Outcome

- One candidate: an ice-capped islet at the front of Døcker Smith Gletscher, Melville Bay, isolated since
  2021 (page `candidates/geography/docker-smith-islet`).
- South Georgia, Tierra del Fuego, west, south-east and east Greenland: nothing. What was flagged was
  terrain shadow, lake islands on old tundra far from any ice front, or a coarse or shifted mapped
  coastline (common in south-east Greenland).
- Patagonia: no island in the fjords. Three lake islands near ice fronts (51.390 S, 73.296 W, 0.50 km²;
  50.754 S, 73.128 W, 0.12 km²; 50.819 S, 73.124 W, 0.07 km²) were not followed up, so nothing is
  claimed for them.
- Alaska: only the known islands above. Tiles without sea coast were skipped, so inland proglacial
  lakes were not searched.
- Antarctic Peninsula: the ten bodies left were looked at once on a contact sheet. Eight are mapped
  islands whose OpenStreetMap outline is shifted (Biscoe Islands, South Shetland Islands). Two small
  rock patches at ice edges in Marguerite Bay (67.19 S, 67.58 W, 0.07 km²; 67.78 S, 67.65 W, 0.05 km²)
  were not followed up. With 14 % of the pixels cloudy and fast ice not handled, this region counts as
  glanced at, not searched.

## Not covered

The rest of Antarctica, north and north-east Greenland above 76.7 N and 74.5 N, south-west Greenland, the rest of the Canadian Arctic, British Columbia, Iceland, the other
sub-Antarctic islands, and lakes away from the sea. Fjords choked with ice all summer (for example
Ilulissat Icefjord) cannot be searched this way. Cloud left 10 % of the Patagonian and Fuegian tiles
without data.

## How to check

`check.py` rebuilds the table from the per-tile logs (`tiles_*.csv`, which name the scenes used) and
confirms the three recoveries from the candidate lists (`triage_*.csv`). `detect.py` and
`triage_sheet.py` are the search itself; they read imagery over the network and take about a minute per
tile. Two contact sheets are included as examples.

## Data and credits

Contains modified Copernicus Sentinel data (2025 to 2026), read from the Earth Search catalogue.
Copernicus DEM GLO-30. Coastline: OpenStreetMap contributors.
