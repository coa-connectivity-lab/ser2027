# SER 2027 poster: rabbits, wildcats, pond turtles and a free-flowing river

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23638438.svg)](https://doi.org/10.5281/zenodo.23638438)

A poster for the 12th SER World Conference on Ecological Restoration (Lisbon, 30 August to 3 September 2027), thematic series "Lands in Motion". It brings three things onto one A0 page:
- the rabbit release screen (prey for the wildcat) and the pond turtle pool screen, on one map with the two UNESCO World Heritage areas of the Greater Côa Valley, Portugal
- three plates drawn after the valley's Iron Age fine-line engravings
- figures from the open Côa eco-connectivity workflow

![Poster preview](poster/poster.png)

## Files

```
poster/poster.pdf     A0 portrait (841 x 1189 mm), fonts embedded, images at 300 dpi
poster/poster.png     preview, 100 dpi
poster/AnguloLopez_2026_SER2027_poster_v0.1_150dpi.png   high-resolution PNG, 4967 x 7022 px (print, zoom)
poster/AnguloLopez_2026_SER2027_poster_v0.1_web.png      web PNG, 2000 x 2828 px (sharing)
scripts/poster.py     draws the poster; every figure on it is computed from the data
img/plate-*.jpg       the three plates, 3200 x 4000 px, no caption band
abstract.md           draft SER abstract
codemeta.json         machine-readable metadata (CodeMeta 3.0)
CITATION.cff          citation metadata
```

## Poster summary

(i) **Rabbits:** 1,045 km² of candidate release area lies inside the top third of the wildcat's land corridors, in ten priority survey blocks. 87% of it is on hunting land, so a rabbit baseline needs the hunters.

(ii) **Wildcat:** the wildcat is supported, not released. The measure is neutering of domestic cats near villages, with mesopredator monitoring, and GBIF has no wildcat record in the study area.

(iii) **Pond turtles:** 96 pools held water all year in 2021, and 48 lie on better-connected rivers. Thirteen of those 48 are inside the Côa rock-art core. Only one is within 2 km of a rabbit area, so the prey-buffer hypothesis (H6) can be tested at one site now.

(iv) **The river:** the Côa is free-flowing because the 1995 campaign "As gravuras não sabem nadar" (the engravings can't swim) stopped the dam that would have drowned its rock art.

(v) **Across the border:** 26% of the study area (2,694 km²) lies in Spain, along 166 km of border. Natura 2000 covers 32% of the study area, in sites that face each other across the border. Examples are Douro Internacional e Vale do Águeda and Arribes del Duero, Vale do Côa and Campo de Azaba, and Malcata and El Rebollar. The v6 connectivity model stops at the border, with no current on 96% of the Spanish side. The next step is a transfrontier study.

These are screening maps, not release sites. Every candidate needs a field survey first.

## Hypotheses

H1 Rabbits follow the grazing mosaic. 
H2 Wildcat habitat tracks rabbit habitat. 
H3 Fire resets the rabbit mosaic, for better and worse. 
H4 Water connectivity is limited by summer flow, not by barriers alone. 
H5 Pond turtles persist where summer pools persist. 
H6 A rabbit baseline protects the turtle. 
H7 The rock-art corridor is also the best combined corridor.

## Rebuild

The poster reads the screening layers from the source repository, [Solo-field-illustrator-project-for-Rewilding-Portugal](https://github.com/coa-connectivity-lab/Solo-field-illustrator-project-for-Rewilding-Portugal), file `research/rewilding-dynamics/scripts/release_candidates.py`. That script reads the [Côa Valley Eco-Connectivity v6](https://www.data.gouv.fr/datasets/coa-valley-eco-connectivity-v6) bundle, ESA WorldCover 2021, JRC Global Surface Water 2021 and GBIF records generalised to 5 km.

To rebuild:
1. Set `SOURCE` at the top of `scripts/poster.py` to your clone.
2. Set `BUNDLE`, `GBIF` and `HYDRO` in `release_candidates.py` to your copies.
3. Run:

```bash
conda run -n coa python scripts/poster.py
```

It needs geopandas, rioxarray, rasterio, scipy, matplotlib and Pillow, plus GDAL for the first remote raster fetch. The fonts, Bebas Neue and Exo 2 (both SIL OFL), download on first run.

The plates come from `research/rewilding-dynamics/scripts/digital_plates.py --print` in the same source repository. They are digital studies; scans of the hand-cut plates will replace them when ready.

## Sources

- Angulo Lopez, L. (2026a). *Rabbits, wildcats, pond turtles and a river that stayed: a synthesis and research agenda for trophic and hydrological rewilding in the Greater Côa Valley, Portugal*. Preprint, Zenodo. <https://doi.org/10.5281/zenodo.22997241>
- Angulo Lopez, L. (2026b). *Movement, Water, Connection: a reproducible Python connectivity workflow and field illustration for the Greater Côa Valley rewilding landscape, Portugal*. Preprint, Zenodo. <https://doi.org/10.5281/zenodo.22979020>
- Workflow: <https://github.com/coa-connectivity-lab/eco-connectivity-workflow>

The full source list is in the poster footer.

## Cite

Angulo Lopez, L. (2026). *Rabbits, wildcats, pond turtles and a free-flowing river: one open connectivity screen for trophic and hydrological rewilding in the Greater Côa Valley, Portugal* (Version v0.1) [Poster]. 12th SER World Conference on Ecological Restoration, Lisbon. Zenodo. <https://doi.org/10.5281/zenodo.23638438>

The Zenodo record holds the A0 PDF, a preview and a snapshot of this repository at the deposited commit.

## Licence

Text and map: CC BY 4.0. Plates: CC BY-NC 4.0. Code: MIT. See [LICENSE](LICENSE).

## AI assistance

The code and the first draft of the text were written with Claude (Anthropic), following the author's method and direction, and were reviewed by the author.
