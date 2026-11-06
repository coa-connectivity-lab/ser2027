# Plan: poster and abstract v0.2, a wildcat-rabbit poster

Linda Angulo Lopez, 6 November 2026

## Why a v0.2

Version 0.1 ([doi:10.5281/zenodo.23638438](https://doi.org/10.5281/zenodo.23638438), 25 Oct 2026) tried to carry three species, a river, a heritage story, three drawings and a cross-border section on one A0 sheet. The review in PR #2 (`notes-vr.md`, merged 6 Nov) found it hard to read without the preprints: no clear goal or questions up front, hypotheses buried at the bottom, one map that tries to show everything, and panels that read as asides.

Version 0.2 narrows the poster to **one predator-prey pair, the European wildcat and the European rabbit**, built on the maps of the Côa Valley Eco-Connectivity v6 notebook (`Solo-field-illustrator-project-for-Rewilding-Portugal/research/eco-connectivity/notebook/coa_eco_connectivity_story_v6.ipynb`). Decisions taken on 6 Nov:

(i) Wildcat and rabbit only. The pond turtle, the pool screen and hypotheses H4-H6 leave the poster; they stay in the preprint for a later piece.
(ii) The three drawing panels and their captions are removed.
(iii) The Global Artivism illustrations become a faded background wallpaper, on the poster only.
(iv) The reviewer's notes in `notes-vr.md` are the checklist for text and map.

## 1. Poster (`scripts/poster.py`)

### Structure, top to bottom

| Block | v0.1 | v0.2 |
| --- | --- | --- |
| Header | title, subtitle, SER banner, links | title on one line, subtitle, author, affiliation, ORCID; SER banner removed |
| Question | none | one sentence goal and the hypotheses H1-H3, stated up front |
| Map block | one combined map (rabbit, turtle, heritage) | two maps side by side: (a) wildcat land corridors, (b) rabbit screen inside them |
| Left flank | "Three animals, one chain" + Method | "Two species, one chain" (rabbit to wildcat, with grazing and fire) + Method in three lines |
| Right flank | "New animals in an old line" (3 plates) + "Across the border" | "The wildcat: protected, not released" (panel text in `wildcat-summary.md`) + one line on Spain |
| Bottom row | river / what the screen shows / what we propose | Results / Recommendations / Why the Côa (river and rock-art corridor, short) |
| Footer | hypotheses + references | references, data and links (preprints, GitHub, data.gouv.fr, Zenodo) |

### Maps

(a) **Wildcat corridors.** Redraw the land-group current (wolf, wildcat, red deer) from `land_normalized_current.tif` in the v6 bundle (`release_candidates.py`, `RASTERS`), the source of notebook map `03_land_connectivity.png`, in the poster's palette. Show the top third, which is the corridor used by the rabbit screen. Fire history (`09_fire_history.png`, `fire_last_burn_year.tif`) as a hatched overlay for burns since 2023, which H3 excludes.

(b) **Rabbit screen.** Reuse `draw_rabbit_map()` logic in `release_candidates.py`: candidate area (1,045 km²), the ten priority survey blocks ranked, hunting land outlined (87% of the candidate area), rabbit GBIF records as 5 km cells.

Fixes from the review, both maps: (i) no north arrow or scale bar on the main maps, keep them on the inset only, without a black border; (ii) clip rivers and the border to the study area; (iii) the Côa in blue, as the other rivers, only wider; (iv) larger legend keys; (v) no wildcat symbol in blue (and there are no GBIF wildcat records to plot, so say so in the caption instead of drawing an empty layer); (vi) one short subtitle per map that states its single result.

### Text

(i) **Goal and questions first.** "Can the rabbit, the wildcat's main prey, be restored inside the corridors the wildcat already uses?" Then H1 Rabbits follow the grazing mosaic; H2 Wildcat habitat tracks rabbit habitat; H3 Fire resets the rabbit mosaic, for better and worse.
(ii) **Define the screen** (reviewer: "what is a good rabbit mosaic?"), from `release_candidates.py`: at least 20% grassland or cropland (food) and at least 20% tree cover or shrubland (cover, warrens) within about 500 m, under 5% built land, not burned since 2023, away from road verges, inside the top third of the wildcat's land corridors, blocks of 1 km² or more.
(iii) **Results and recommendations apart.** Results: the candidate area, the ten blocks, the hunting share, no GBIF wildcat record. Recommendations: a rabbit baseline with hunters, cat neutering and mesopredator monitoring, adding the rabbit to the workflow, a study that extends the model into Spain (say "extend the model into Spain", not "transfrontier study").
(iv) **The wildcat panel**: from `wildcat-summary.md`, with "supported, not released" spelled out: the existing wildcat is protected (neutering of domestic cats near villages, mesopredator monitoring), and no individuals are released.
(v) **Why the Côa**, two or three sentences: the river is free-flowing because the 1995 campaign "As gravuras não sabem nadar" stopped a dam to save the rock art; the rock-art core sits on the land corridor (H7, if the numbers support it). This answers the reviewer's question on the link between rock art and the study.
(vi) "Species", not "animals", throughout; British spelling; GBIF spelled out once.

### Background wallpaper

Use the Global Artivism illustrations `movement.jpg`, `water.jpg` and `connection.jpg` (`~/Documents/myData/global-artivism/img/`) as one faded layer behind the panels (about 10-15% opacity, desaturated towards the cream paper colour), never behind a map or under small text. Draw it first with `fig.figimage` or a full-figure axes at `zorder=0`.

**Licence to settle first**: the illustrations are CC BY-NC 4.0 (`global-artivism/README.md`); the poster on Zenodo is CC BY 4.0. Either release these three images under CC BY 4.0 for this use (you hold the rights), or state on the poster and on Zenodo that the background illustrations are CC BY-NC 4.0 and the rest CC BY 4.0. Keep them out of the source zip in both cases, and load them from the global-artivism folder at build time.

### Files to remove or change

- `img/plate-*.jpg`: no longer used by the poster; delete from the repo (they stay in the global-artivism repo).
- `poster.py`: remove the plates block, the pond turtle map and text, H4-H6; add the two maps, the background, the new blocks above.
- Output names: `AnguloLopez_2026_SER2027_poster_v0.2.pdf`, `..._preview.png`, `..._150dpi.png`, `..._web.png`.

## 2. Abstract (`abstract.md`)

Start from the reviewer's structure (setting, methods, results, next steps), then:

(i) **New title**, proposed: *Rabbits and wildcats in a free-flowing valley: an open connectivity screen for trophic rewilding in the Greater Côa Valley, Portugal*.
(ii) Remove the bracketed reviewer questions and answer them in the text: why the rock art matters (the river and the corridor), which maps (wildcat corridors and the rabbit screen).
(iii) Remove the pond turtle sentences and the drawings sentence.
(iv) Check the rabbit's IUCN status on the Red List before choosing between "Endangered" (v0.1) and "Near Threatened" (the reviewer); cite the assessment year.
(v) "We" rather than "Rewilding Portugal conducted": the study is Linda's, with Rewilding Portugal as affiliation, unless Rewilding Portugal confirms otherwise.
(vi) British spelling ("analysed"); keep the closing question, rewritten for two species: "Which predators will the next chapter of the Côa include, and who decides?"
(vii) Recount the words once the call opens on 3 Dec (v0.1 draft: 289 words).
(viii) Keywords: drop pond turtle, *Emys orbicularis* and free-flowing rivers (keep "free-flowing rivers" only if the "Why the Côa" panel stays); add mesopredators, hunting land, fire.

## 3. Repository metadata

- `README.md`: summary rewritten for two species; the Hypotheses section keeps H1-H3 and says where H4-H7 live (the preprint); add the screen criteria.
- `codemeta.json` and `CITATION.cff`: version 0.2.0, new title, new keywords, date.
- `notes-vr.md`: keep; tick each point when done, or answer it in the PR.
- `wildcat-summary.md`: becomes the wildcat panel text; delete once it is in `poster.py`.

## 4. Zenodo

Linda adds v0.2 herself as a new version of the same record (Zenodo, "New version" on 10.5281/zenodo.23638438), so the concept DOI stays the same. What to upload and fill in:

- Files: the v0.2 PDF, a preview PNG and the source zip of the tagged release `v0.2.0` (without the background images, see the licence note).
- Title and keywords as in section 2; description rewritten for the wildcat and the rabbit.
- Licence: CC BY 4.0, with the note on the background illustrations if they stay CC BY-NC.
- Related identifiers: keep the two preprints, the data.gouv.fr dataset and the GitHub repository; add `isNewVersionOf` v0.1 (Zenodo adds it).
- Contributors: credit the reviewer (GitHub `VRConservation`) as "Other" or in the description, once you have their name and their agreement.

## 5. Order of work and checks

1. Settle the background licence and the rabbit's IUCN status.
2. Branch `poster-v0.2`. Maps first (a, b), then text blocks, then the background.
3. Build: `python scripts/poster.py` (needs the v6 bundle and the caches named in `release_candidates.py`). Check: A0 portrait, fonts embedded, every figure on the poster matches the numbers `release_candidates.py` prints, no "turtle" left (`grep -i turtle scripts/poster.py abstract.md README.md`), the background is invisible behind the maps.
4. Abstract and metadata.
5. Ask the reviewer to look at the draft PDF in a PR before the Zenodo version.
6. Merge and tag `v0.2.0`; Linda adds the new Zenodo version; update the abstract's submission on 3 Dec (deadline 29 Jan 2027).

## Open questions, with proposed answers (to confirm)

(i) **Keep the "Why the Côa" panel?** Yes, but as two sentences, not a panel: one line under the header or at the foot of the left flank. It is the reviewer's missing link between the rock art and the study, and the reason the site is worth a poster. Say only what is measured: the river is free-flowing because the 1995 campaign stopped the dam to save the rock art; the rock-art core lies on the land corridor. **Before claiming the second half, compute it**: add to `release_candidates.py` the share of the rock-art core (`heritage_protection.gpkg`) inside the top third of the land current, and print it with the other figures. If the share is not clearly above a third, drop the corridor claim and keep the river sentence only. H7 stays in the preprint either way.

(ii) **Where does the Spain line go?** Two places, no panel. On map (a), shade the Spanish side and label it: "The model stops at the border: 26% of the study area, no current on 96% of it." In the recommendations, as the last item: "Extend the model into Spain, to test whether the wildcat corridors continue into Campo de Azaba, El Rebollar and Arribes del Duero." The Natura 2000 and Biosphere Reserve detail moves to the README.

(iii) **Which illustrations for the background?** *Movement* (Vale Carapito: herbivores, with a predator at the foot, "large herbivores and predators keep the valley open and alive") as the main wallpaper, since it is the predator-prey plate; *Connection* (Côa gorge and Penascosa) only behind the "Why the Côa" lines, if at all. Leave out *Water* (the Paul de Toirões wetland belongs to the turtle story that leaves the poster). Three conditions:
- **Re-render, don't stretch.** The JPEGs are 1,600 × 2,000 px, about 48 dpi across an A0 sheet. Re-render the plate from `digital_landscapes.py` (in `Solo-field-illustrator-project-for-Rewilding-Portugal/research/rewilding-dynamics/scripts/`) at poster size, as line work only.
- **No caption band and no logo.** The gallery JPEGs carry the plate caption and the Global Artivism Month logo at the bottom; neither belongs in the background.
- **Recolour.** Drop the grey stone texture; draw the lines in a pale tint of the poster's coral on the cream paper, about 10-15% strength, so the maps and text stay clean.
