"""SER 2027 poster, v0.2: rabbits and wildcats in the Greater Côa Valley.

One A0 portrait poster for the 12th SER World Conference on Ecological
Restoration (Lisbon, 2027), theme "Lands in Motion". Version 0.2 narrows v0.1
to one predator-prey pair, the European wildcat and the European rabbit, and
draws only on the two preprints (both CC BY 4.0):

  Angulo Lopez (2026a), the synthesis: doi:10.5281/zenodo.22997241
  Angulo Lopez (2026b), the connectivity workflow: doi:10.5281/zenodo.22979020

Map 1 redraws the workflow preprint's Fig. 4 (land connectivity for wolf,
wildcat and red deer) from the same raster. Map 2 is the rabbit screen of the
screening code in the source repository (SOURCE below):
research/rewilding-dynamics/scripts/release_candidates.py. Map 3 sets the study
area among the Natura 2000 sites around it (EEA, end-2024). Every number on the
poster is computed here from the v6 data bundle through that code. Nothing is
typed in by hand except dates and figures taken from published sources, which
are cited.

Run:  conda run -n coa python scripts/poster.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import ListedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
from matplotlib.textpath import TextToPath
from rasterio.features import geometry_mask
from shapely.geometry import box

# Source repository (Solo-field-illustrator-project-for-Rewilding-Portugal), screening code and bundle paths
SOURCE = Path("/home/linda/Documents/myData/Solo-field-illustrator-project-for-Rewilding-Portugal/research/"
              "rewilding-dynamics/scripts")
sys.path.insert(0, str(SOURCE))
import release_candidates as rc  # noqa: E402  (computes the layers on import; draws nothing)

ROOT = Path(__file__).resolve().parent.parent
NE = Path("/home/linda/Documents/myData/data-management/data/raw/colab/ne_10m_admin_0_countries.geojson")
OUT = ROOT / "poster"
OUT.mkdir(exist_ok=True)
VERSION = "v0.2"

FIG_W, FIG_H = 33.11, 46.81  # A0 portrait, inches; every position below is a fraction, so another size is one edit
PT_W, PT_H = FIG_W * 72, FIG_H * 72
CREAM, PAPER, NAVY, CORAL, PURPLE, BLUE, SUN, SKY = (rc.CREAM, rc.PAPER, rc.NAVY, rc.CORAL, rc.PURPLE, rc.BLUE,
                                                   rc.SUN, rc.SKY)
MOSAIC = "#dfe6b4"
RIVER = "#5f8fd6"
DISPLAY = rc.DISPLAY
BOLD = font_manager.FontProperties(fname=str(rc.CACHE / "fonts" / "Exo2-700.ttf"))
BODY = font_manager.FontProperties(fname=str(rc.CACHE / "fonts" / "Exo2-400.ttf"))
plt.rcParams["pdf.fonttype"] = 42  # embed TrueType, so the PDF prints as designed
plt.rcParams["hatch.linewidth"] = 1.2

SIZE = 28        # body text, points at A0
SMALL = 22
HEAD = 58

# ---------------------------------------------------------------------------
# Figures from the screen
# ---------------------------------------------------------------------------
cand_km2 = rc.km2(rc.candidate)
habitat_km2 = rc.km2(rc.habitat)
blocks = rc.priority.sort_values("rank")
top2_share = blocks.km2.iloc[:2].sum() / cand_km2
recent_burn_share = rc.recent_burn[rc.inside].mean()
corridor_threshold = np.nanpercentile(rc.land[rc.inside], 67)

# The rock-art core and the land corridor: computed, not assumed (plan v0.2, open question i)
core = gpd.read_file(rc.PROCESSED / "heritage_protection.gpkg", layer="coa_rock_art_core").to_crs(3035)
core_mask = ~geometry_mask(core.geometry, out_shape=rc.land.shape, transform=rc.template.rio.transform())
core_valid = core_mask & rc.inside & ~np.isnan(rc.land)
core_in_corridor = rc.corridor[core_valid].mean()

# The border: how much of the study area is in Spain, and what the v6 model covers there
countries = gpd.read_file(NE, columns=["ADMIN"], bbox=(-8.5, 39.5, -6.0, 42.0)).to_crs(3035)
spain = countries[countries.ADMIN == "Spain"].union_all()
portugal = countries[countries.ADMIN == "Portugal"].union_all()
spain_in = rc.area.intersection(spain)
spain_share = spain_in.area / rc.area.area
spain_mask = ~geometry_mask([spain], out_shape=rc.land.shape, transform=rc.template.rio.transform()) & rc.inside
spain_unmodelled = np.isnan(rc.land[spain_mask]).mean()
border = portugal.boundary.intersection(spain.boundary).intersection(rc.area)

# Natura 2000: the study area against the sites around it (EEA, end-2024)
N2K = Path("/home/linda/Documents/myData/data-management/data/raw/landcover/natura2000/Natura2000_end2024.gpkg")
N2K_GREEN = "#7fae6e"
_sx0, _sy0, _sx1, _sy1 = rc.study.to_crs(rc.PLOT_CRS).total_bounds
region_plot = box(_sx0 - 75000, _sy0 - 6000, _sx1 + 75000, _sy1 + 6000)  # the study area and its neighbours, for the Natura 2000 figures
region = gpd.GeoSeries([region_plot], crs=rc.PLOT_CRS).to_crs(3035).iloc[0]
natura = gpd.read_file(N2K, layer="NaturaSite_polygon", bbox=region.bounds)
natura = natura[natura.intersects(region)]
natura_in = natura[natura.intersects(rc.area)]
natura_u = natura_in.union_all()
natura_share = natura_u.intersection(rc.area).area / rc.area.area
# Natura 2000 in Spain and Portugal, for the overview map (simplified to 300 m, display only)
natura_ib = gpd.read_file(N2K, layer="NaturaSite_polygon", bbox=tuple(gpd.GeoSeries([box(-9.7, 35.9, 3.5, 43.9)], crs=4326).to_crs(3035).total_bounds))
natura_ib = natura_ib[natura_ib.MS.isin(["PT", "ES"])].to_crs(3035)
natura_ib["geometry"] = natura_ib.simplify(300)
cand_in_natura = rc.cand_poly.union_all().intersection(natura_u).area / rc.cand_poly.union_all().area
PAIRS_SHOWN = [("PTZPE0039", "Vale do Côa (PT)"), ("ES0000202", "Campo de Azaba (ES)"),
               ("PTZPE0038", "Douro Internacional e Vale do Águeda (PT)"), ("ES0000118", "Arribes del Duero (ES)"),
               ("PTCON0004", "Malcata (PT)"), ("ES4150032", "El Rebollar (ES)")]

print(f"rabbit mosaic {habitat_km2:.0f} km², candidates {cand_km2:.0f} km², hunting {rc.hunt_share:.1%}, "
      f"two largest blocks {top2_share:.0%}, Faia Brava mosaic {rc.faia_mosaic:.0%}, burned since 2023 "
      f"{recent_burn_share:.2%}; corridor threshold {corridor_threshold:.3f}; rock-art core in corridor "
      f"{core_in_corridor:.1%}; Spain {spain_share:.1%}, unmodelled {spain_unmodelled:.0%}; GBIF rabbit "
      f"{rc.n_rabbit} in {len(rc.rabbit_cells)} cells, wildcat {rc.n_wildcat}; Natura 2000 {natura_share:.1%} of the "
      f"area in {len(natura_in)} sites, {cand_in_natura:.1%} of the candidate area")


# ---------------------------------------------------------------------------
# Text layout: measured wrapping, columns that flow top to bottom
# ---------------------------------------------------------------------------
TTP = TextToPath()


def width_pt(s, prop, size):
    p = prop.copy()
    p.set_size(size)
    return TTP.get_text_width_height_descent(s, p, ismath=False)[0]


def wrap(text, prop, size, width):
    """Greedy word wrap to a width in points, measured on the real font."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = f"{line} {word}".strip()
            if line and width_pt(trial, prop, size) > width:
                out.append(line)
                line = word
            else:
                line = trial
        out.append(line)
    return out


class Column:
    """A text column: x, width and current y are figure fractions; y moves down as blocks are added."""

    def __init__(self, fig, x, width, top):
        self.fig, self.x, self.w, self.y = fig, x, width, top

    def gap(self, pt):
        self.y -= pt / PT_H

    def head(self, text, colour=CORAL, size=HEAD):
        for line in wrap(text.upper(), DISPLAY, size, self.w * PT_W):
            self.fig.text(self.x, self.y, line, fontproperties=DISPLAY, fontsize=size, color=colour, va="top")
            self.gap(size * 1.02)
        self.gap(size * 0.08)

    def kicker(self, text, colour=NAVY, size=SMALL):
        self.fig.text(self.x, self.y, text.upper(), fontproperties=BOLD, fontsize=size, color=colour, va="top")
        self.gap(size * 1.7)

    def para(self, text, size=SIZE, prop=BODY, colour=NAVY, spacing=1.38, width=None, x=None):
        lines = wrap(text, prop, size, (width or self.w) * PT_W)
        self.fig.text(x if x is not None else self.x, self.y, "\n".join(lines), fontproperties=prop, fontsize=size,
                      color=colour, va="top", linespacing=spacing)
        self.gap(len(lines) * size * spacing + size * 0.55)

    def items(self, items, size=SIZE, spacing=1.36, colour=NAVY):
        """Numbered items (i), (ii)... with a hanging indent and the lead words in bold."""
        indent = width_pt("(viii) ", BODY, size) / PT_W
        for n, (lead, text) in enumerate(items):
            mark = f"({['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'][n]})"
            self.fig.text(self.x, self.y, mark, fontproperties=BOLD, fontsize=size, color=CORAL, va="top")
            body = f"{lead} {text}" if lead else text
            lines = wrap(body, BODY, size, (self.w - indent) * PT_W)
            first = lines[0]
            if lead and first.startswith(lead):
                self.fig.text(self.x + indent, self.y, lead, fontproperties=BOLD, fontsize=size, color=colour,
                              va="top")
                rest = first[len(lead):]
                self.fig.text(self.x + indent + width_pt(lead, BOLD, size) / PT_W, self.y, rest,
                              fontproperties=BODY, fontsize=size, color=colour, va="top")
            else:
                self.fig.text(self.x + indent, self.y, first, fontproperties=BODY, fontsize=size, color=colour,
                              va="top")
            if len(lines) > 1:
                self.fig.text(self.x + indent, self.y - size * spacing / PT_H, "\n".join(lines[1:]),
                              fontproperties=BODY, fontsize=size, color=colour, va="top", linespacing=spacing)
            self.gap(len(lines) * size * spacing + size * 0.5)

    def axes(self, height_pt, width=None, x=None):
        ax = self.fig.add_axes([x if x is not None else self.x, self.y - height_pt / PT_H, width or self.w,
                                height_pt / PT_H])
        self.gap(height_pt)
        return ax


def panel_box(fig, x, y0, y1, w, colour=PAPER, edge=None):
    pad = 22 / PT_W
    fig.patches.append(FancyBboxPatch((x - pad, y1 - pad), w + 2 * pad, y0 - y1 + 2 * pad, transform=fig.transFigure,
                                      boxstyle=f"round,pad=0,rounding_size={10 / PT_W}", facecolor=colour,
                                      edgecolor=edge or colour, linewidth=2, zorder=-1))


def fit_size(text, prop, size, width):
    """Largest size, from `size` down, at which `text` fits on one line."""
    while width_pt(text, prop, size) > width and size > 10:
        size -= 1
    return size


# ---------------------------------------------------------------------------
# Poster: header / question and chain / two maps / Natura 2000 and key figures / four panels / references
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=CREAM)

# ---- Header: title, subtitle, author only (review, notes-vr.md) ------------
HEAD_Y = 0.917
hdr = fig.add_axes([0, HEAD_Y, 1, 1 - HEAD_Y])
hdr.set_facecolor(NAVY)
hdr.set_xticks([])
hdr.set_yticks([])
for side in hdr.spines.values():
    side.set_visible(False)
rc.band(fig, HEAD_Y - 0.006, 0.006, [CORAL, PURPLE, BLUE, SUN])
TITLE = "Rabbits and wildcats in the Greater Côa Valley".upper()
t_size = fit_size(TITLE, DISPLAY, 150, 0.94 * PT_W)
fig.text(0.03, 0.987, TITLE, fontproperties=DISPLAY, fontsize=t_size, color=CREAM, va="top")
fig.text(0.03, 0.944, "An open connectivity screen for trophic rewilding in northern Portugal",
         fontproperties=BODY, fontsize=40, color=CREAM, va="top")
fig.text(0.03, 0.930, "Linda Angulo Lopez  ·  Rewilding Portugal  ·  ORCID 0009-0009-5689-7148",
         fontproperties=BOLD, fontsize=30, color=SUN, va="top")

# ---- The question, the hypotheses and the chain, up front ------------------------
Q_TOP = 0.898
Q = Column(fig, 0.03, 0.56, Q_TOP)
Q.kicker("The question", CORAL, size=24)
Q.para("Can the rabbit, the wildcat's main prey, be restored inside the corridors the wildcat already uses?",
       size=40, prop=BOLD, spacing=1.15)
Q.para("The European rabbit (Oryctolagus cuniculus) is the keystone prey of the Iberian Peninsula, and Endangered in "
       "its native range (IUCN, 2019); the European wildcat (Felis silvestris) depends on it. Where apex predators "
       "return, they can hold foxes and other mid-sized predators in check (Jiménez et al., 2019); where rabbits "
       "crash, those predators switch to other prey (Finlayson et al., 2021). The Côa has no lynx: can the wildcat, "
       "with its prey restored, play part of that role?", size=20)
hyps = [("H1", "Rabbits follow the grazing mosaic."),
        ("H2", "Wildcat habitat tracks rabbit habitat."),
        ("H3", "Fire resets the rabbit mosaic, for better and worse.")]
for h, text in hyps:
    fig.text(Q.x, Q.y, h, fontproperties=DISPLAY, fontsize=40, color=CORAL, va="top")
    fig.text(Q.x + 0.035, Q.y - 5 / PT_H, text, fontproperties=BODY, fontsize=26, color=NAVY, va="top")
    Q.gap(46)
Q.para("Hypotheses from the synthesis preprint (Angulo Lopez, 2026a, §6), tested with the connectivity workflow "
       "(Angulo Lopez, 2026b).", size=17, colour="#5b5146")
fig.text(0.62, Q_TOP, "TWO SPECIES, ONE CHAIN", fontproperties=BOLD, fontsize=24, color=CORAL, va="top")
chain = fig.add_axes([0.62, Q.y + 0.004, 0.35, Q_TOP - 0.012 - Q.y])
chain.set_xlim(0, 10)
chain.set_ylim(0.2, 5.6)
chain.set_axis_off()
nodes = {"Grazing\nand fire": (1.0, 4.4), "Open\nmosaic": (3.6, 4.4), "Rabbit": (6.2, 4.4), "Wildcat": (8.85, 4.4),
         "Domestic\ncats": (6.2, 1.2), "Foxes and\nmesopredators": (8.85, 1.2)}
species = ("Rabbit", "Wildcat")
for name, (x, y) in nodes.items():
    colour = CORAL if name in species else (PURPLE if y < 3 else NAVY)
    chain.text(x, y, name, ha="center", va="center", fontproperties=BOLD, fontsize=22,
               color="white" if name in species else colour,
               bbox=dict(boxstyle="round,pad=0.5", linewidth=2.5, edgecolor=colour,
                         facecolor=colour if name in species else PAPER))


def arrow(a, b, colour, style="-", label=None, lx=0, ly=0.45):
    (x0, y0), (x1, y1) = nodes[a], nodes[b]
    chain.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=30, color=colour, lw=3,
                                    linestyle=style, shrinkA=55, shrinkB=55))
    if label:
        chain.text((x0 + x1) / 2 + lx, (y0 + y1) / 2 + ly, label, ha="center", va="bottom", fontproperties=BOLD,
                   fontsize=19, color=colour)


arrow("Grazing\nand fire", "Open\nmosaic", NAVY, label="H3", ly=0.5)
arrow("Open\nmosaic", "Rabbit", CORAL, label="H1", ly=0.5)
arrow("Rabbit", "Wildcat", CORAL, label="H2", ly=0.5)
arrow("Domestic\ncats", "Wildcat", PURPLE, style=(0, (3, 2)))
chain.text(6.75, 3.05, "hybridisation", fontproperties=BODY, fontsize=19, color=PURPLE, ha="left", va="center")
arrow("Wildcat", "Foxes and\nmesopredators", NAVY, style=(0, (3, 2)))
chain.text(9.1, 2.8, "held in\ncheck?", fontproperties=BODY, fontsize=19, color=NAVY, ha="left", va="center")
panel_box(fig, 0.03, Q_TOP + 0.004, Q.y, 0.94, colour=PAPER)

# ---- Maps: the centre of the poster -------------------------------------------
TOP = Q.y - 0.016
XM, WM = [0.03, 0.515], 0.455  # two map panels across the page
s = rc.study.to_crs(rc.PLOT_CRS)
bx0, by0, bx1, by1 = s.total_bounds
PAD = 2500
map_w = 0.238                  # each map; its legend sits beside it, in the rest of the panel
map_h_pt = map_w * PT_W * (by1 - by0 + 2 * PAD) / (bx1 - bx0 + 2 * PAD)
LEG_X = map_w + 0.01           # legend column, relative to the panel's left edge
area_plot = gpd.GeoSeries([rc.area], crs=3035).to_crs(rc.PLOT_CRS).iloc[0]
hydro = gpd.read_file(rc.HYDRO, bbox=tuple(rc.study.to_crs(4326).total_bounds))
big_rivers = hydro[hydro.ORD_STRA >= 6].to_crs(rc.PLOT_CRS).clip(area_plot)
rivers = rc.rivers.to_crs(rc.PLOT_CRS).clip(area_plot)
coa = rc.coa.to_crs(rc.PLOT_CRS).clip(area_plot)
spain_plot = gpd.GeoSeries([spain_in], crs=3035).to_crs(rc.PLOT_CRS)
border_plot = gpd.GeoSeries([border], crs=3035).to_crs(rc.PLOT_CRS)


def base(ax):
    ax.set_facecolor(PAPER)
    s.plot(ax=ax, color=CREAM, zorder=0)


def water_and_border(ax):
    big_rivers.plot(ax=ax, color=RIVER, linewidth=2.6, zorder=6)
    rivers.plot(ax=ax, color=RIVER, linewidth=1.2, zorder=6)
    coa.plot(ax=ax, color="white", linewidth=11, zorder=7)
    coa.plot(ax=ax, color=RIVER, linewidth=6.5, zorder=7.1)
    border_plot.plot(ax=ax, color=NAVY, linewidth=3.5, linestyle=(0, (6, 2, 1, 2)), zorder=8)
    s.boundary.plot(ax=ax, color=NAVY, linewidth=1.8, zorder=8)
    ax.set_xlim(bx0 - PAD, bx1 + PAD)
    ax.set_ylim(by0 - PAD, by1 + PAD)
    ax.set_axis_off()


def tag(ax, x, y, text, colour=NAVY, ha="center", size=22):
    ax.text(x, y, text, fontproperties=BOLD, fontsize=size, color=colour, ha=ha, va="center", zorder=11,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=PAPER, edgecolor="none", alpha=0.9))


es_pt = spain_plot.iloc[0].representative_point()
mid = coa.union_all().interpolate(0.45, normalized=True)


def map_title(col, number, title, caption):
    big = HEAD + 40
    col.fig.text(col.x, col.y, number, fontproperties=DISPLAY, fontsize=big, color=CORAL, va="top")
    nx = col.x + width_pt(number, DISPLAY, big) / PT_W + 0.01
    col.fig.text(nx, col.y - 14 / PT_H, title.upper(), fontproperties=DISPLAY, fontsize=HEAD + 14, color=CORAL,
                 va="top")
    col.gap(big * 1.0)
    col.para(caption, size=SMALL + 1)


def legend_beside(col, top_y, handles, title=None):
    leg = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(col.x + LEG_X, top_y), ncol=1,
                     prop=BODY.copy(), frameon=False, labelcolor=NAVY, handlelength=2.0, handleheight=1.6,
                     labelspacing=0.9, title=title, alignment="left")
    for t in leg.get_texts():
        t.set_fontsize(SMALL)
    if title:
        leg.get_title().set_fontproperties(BOLD.copy())
        leg.get_title().set_fontsize(SMALL)
        leg.get_title().set_color(NAVY)
    # wrap long labels to the legend column
    for t in leg.get_texts():
        t.set_text("\n".join(wrap(t.get_text(), BODY, SMALL, (WM - LEG_X - 0.03) * PT_W)))
    return leg


# ---- Map 1: where the wildcat can move (the workflow preprint's Fig. 4) ------
M1 = Column(fig, XM[0], WM, TOP)
map_title(M1, "1", "Where the wildcat can move",
          "Land connectivity for wolf, wildcat and red deer, fire-aware: warm colours show where movement "
          "concentrates. Redrawn from the same raster as Fig. 4 of the workflow preprint (Angulo Lopez, 2026b). GBIF "
          "holds no wildcat record in the study area, so the corridor is modelled, not observed.")
map_top = M1.y
ax1 = M1.axes(map_h_pt, width=map_w)
base(ax1)
cur = rc.template.copy(data=np.where(rc.inside, rc.land, np.nan).astype("float32")).rio.write_nodata(np.nan)
cur = cur.rio.reproject(rc.PLOT_CRS)
cx0, cy0, cx1, cy1 = cur.rio.bounds()
norm = TwoSlopeNorm(vmin=0.85, vcenter=1.0, vmax=1.2)
im = ax1.imshow(cur.values, extent=(cx0, cx1, cy0, cy1), cmap="RdYlBu_r", norm=norm, interpolation="nearest",
                zorder=1)
spain_plot.plot(ax=ax1, color=CREAM, alpha=0.65, hatch="//", edgecolor="#b8ab95", linewidth=0, zorder=3)
water_and_border(ax1)
tag(ax1, es_pt.x, es_pt.y, "SPAIN\nthe model stops\nat the border", "#5b5146")
tag(ax1, mid.x - 3500, mid.y, "River Côa", RIVER, ha="right")

# colour bar and legend, beside the map
cax = fig.add_axes([M1.x + LEG_X + 0.01, map_top - 0.215, 0.022, 0.17])
cb = fig.colorbar(im, cax=cax, orientation="vertical", ticks=[0.85, 1.0, 1.2])
cb.ax.set_yticklabels(["impeded", "1", "concentrated"], fontproperties=BODY, fontsize=SMALL, color=NAVY)
cb.outline.set_visible(False)
cb.ax.tick_params(length=0, pad=8)
fig.text(M1.x + LEG_X, map_top - 0.012, "Normalised current,\nland group", fontproperties=BOLD, fontsize=SMALL,
         color=NAVY, va="top")
legend_beside(M1, map_top - 0.235, [
    Line2D([], [], color=RIVER, lw=7, label="River Côa"),
    Line2D([], [], color=NAVY, lw=3.5, ls=(0, (6, 2, 1, 2)), label="Portugal-Spain border"),
    Patch(facecolor=CREAM, edgecolor="#b8ab95", hatch="//", label=f"Spain, {spain_share:.0%} of the study area, "
                                                                   "not modelled"),
])

M1.gap(20)

# ---- Map 2: where to restore rabbits (the rabbit screen) -------------------------
M2 = Column(fig, XM[1], WM, TOP)
map_title(M2, "2", "Where to restore rabbits",
          f"Rabbit mosaic inside the top third of those corridors: {cand_km2:,.0f} km² in blocks of 1 km² or more. "
          "The ten priority survey blocks carry the most corridor current, ranked 1 to 10. Screening maps, not "
          "release sites: every block needs a field survey.")
map_top2 = M2.y
ax2 = M2.axes(map_h_pt, width=map_w)
base(ax2)
grid = rc.template.copy(data=np.where(rc.habitat_only, 1, np.where(rc.candidate, 2, 0)).astype("float32"))
grid = grid.where(grid > 0).rio.write_nodata(np.nan).rio.reproject(rc.PLOT_CRS)
gx0, gy0, gx1, gy1 = grid.rio.bounds()
ax2.imshow(grid.values, extent=(gx0, gx1, gy0, gy1), cmap=ListedColormap([MOSAIC, CORAL]), vmin=1, vmax=2,
           interpolation="nearest", zorder=1)
rc.hunting.to_crs(rc.PLOT_CRS).clip(area_plot).boundary.plot(ax=ax2, color="#a89c88", linewidth=0.5, zorder=2)
faia = rc.faia.to_crs(rc.PLOT_CRS)
faia.plot(ax=ax2, facecolor="none", edgecolor="#3f7d3a", linewidth=3.5, zorder=4)
rc.rabbit_cells.to_crs(rc.PLOT_CRS).boundary.plot(ax=ax2, color=NAVY, linewidth=2.4, linestyle=(0, (2, 1.5)),
                                                   zorder=5)
spain_plot.plot(ax=ax2, color=CREAM, alpha=0.65, hatch="//", edgecolor="#b8ab95", linewidth=0, zorder=3)
pr = blocks.to_crs(rc.PLOT_CRS)
pr.boundary.plot(ax=ax2, color=NAVY, linewidth=2.6, zorder=5)
water_and_border(ax2)
for r in pr.itertuples():
    c = r.geometry.representative_point()
    ax2.text(c.x, c.y, str(r.rank), fontproperties=DISPLAY, fontsize=36, color="white", ha="center", va="center",
             zorder=10, bbox=dict(boxstyle="circle,pad=0.2", facecolor=NAVY, edgecolor="none"))
fp = faia.union_all().representative_point()
tag(ax2, fp.x + 4000, fp.y, "Faia Brava", "#3f7d3a", ha="left")
legend_beside(M2, map_top2, [
    Patch(facecolor=CORAL, label="Rabbit candidate area, survey first"),
    Patch(facecolor=CORAL, edgecolor=NAVY, linewidth=2.5, label="Priority survey block, 1 to 10"),
    Patch(facecolor=MOSAIC, label="Rabbit mosaic outside the corridors"),
    Line2D([], [], color="#a89c88", lw=2, label="Hunting zones (ICNF)"),
    Line2D([], [], color=NAVY, lw=2.5, ls=(0, (2, 1.5)), label="GBIF rabbit records, 5 km cells"),
    Line2D([], [], color="#3f7d3a", lw=3.5, label="Faia Brava private reserve"),
    Line2D([], [], color=RIVER, lw=7, label="River Côa"),
    Patch(facecolor=CREAM, edgecolor="#b8ab95", hatch="//", label="Spain, not modelled"),
])
M2.gap(20)

row_bottom = min(M1.y, M2.y)
for x in XM:
    panel_box(fig, x, TOP + 0.004, row_bottom, WM, colour=PAPER)

# ---- Natura 2000 around the study area: the location map, with the key figures -------
K_TOP = row_bottom - 0.013
nat_w = 0.32
# Overview: Spain and Portugal, with all their Natura 2000 sites (EPSG:3035)
IB = box(-9.7, 35.9, 3.5, 43.9)
ib = gpd.GeoSeries([IB], crs=4326).to_crs(3035).iloc[0]
ix0, iy0, ix1, iy1 = ib.bounds
nat_h_pt = nat_w * PT_W * (iy1 - iy0) / (ix1 - ix0)
axn = fig.add_axes([0.03, K_TOP - nat_h_pt / PT_H, nat_w, nat_h_pt / PT_H])
axn.set_facecolor(SKY)
world = gpd.read_file(NE, columns=["ADMIN"], bbox=IB.bounds).to_crs(3035).clip(ib)
world[~world.ADMIN.isin(["Portugal", "Spain"])].plot(ax=axn, color="#efece6", edgecolor="#cfc9bf", linewidth=0.6)
world[world.ADMIN == "Portugal"].plot(ax=axn, color="#e0ddd6", edgecolor="#8d806b", linewidth=1.0)
world[world.ADMIN == "Spain"].plot(ax=axn, color="#d0ccc4", edgecolor="#8d806b", linewidth=1.0)
natura_ib.plot(ax=axn, color=N2K_GREEN, alpha=0.75, edgecolor="none")
rc.study.to_crs(3035).boundary.plot(ax=axn, color=CORAL, linewidth=3.5, zorder=5)
axn.text(ix0 + 0.13 * (ix1 - ix0), iy0 + 0.55 * (iy1 - iy0), "PORTUGAL", fontproperties=BOLD, fontsize=20,
         color=NAVY, ha="center", rotation=90)
axn.text(ix0 + 0.52 * (ix1 - ix0), iy0 + 0.62 * (iy1 - iy0), "SPAIN", fontproperties=BOLD, fontsize=24,
         color="#5b5146", ha="center")
sx0, sy0 = ix0 + 0.05 * (ix1 - ix0), iy0 + 0.05 * (iy1 - iy0)  # scale bar on this location map only
axn.plot([sx0, sx0 + 200000], [sy0, sy0], color=NAVY, linewidth=4, solid_capstyle="butt")
axn.text(sx0 + 100000, sy0 + 15000, "200 km", fontproperties=BODY, fontsize=16, color=NAVY, ha="center")
axn.set_xlim(ix0, ix1)
axn.set_ylim(iy0, iy1)
axn.set_xticks([])
axn.set_yticks([])
for side in axn.spines.values():
    side.set_visible(False)

T = Column(fig, 0.03 + nat_w + 0.02, 0.31, K_TOP)
T.head("Natura 2000 around the study area", size=40)
T.para(f"The study area (coral outline) among the Natura 2000 sites of Spain and Portugal. "
       f"Natura 2000 covers "
       f"{natura_share:.0%} of the study area, in {len(natura_in)} sites, and {cand_in_natura:.0%} of the rabbit "
       "candidate area. The sites face each other across the border, but the model stops at it.", size=18)
T.para("Facing sites: " + "; ".join(f"{PAIRS_SHOWN[k][1]} and {PAIRS_SHOWN[k + 1][1]}"
                                    for k in range(0, len(PAIRS_SHOWN), 2)) + ".", size=17, prop=BOLD,
       colour="#3f7d3a", spacing=1.25)
T.para("Douro Internacional and Arribes del Duero are natural parks of the Meseta Ibérica transboundary Biosphere "
       "Reserve (UNESCO, 2015). EEA Natura 2000, end-2024, SPA and SCI combined; Natural Earth.", size=15,
       colour="#5b5146")

stats = [(f"{cand_km2:,.0f}", "km² of rabbit candidate\narea inside the corridors"),
         ("10", "priority survey\nblocks"),
         (f"{rc.hunt_share:.0%}", "of the candidate area\non hunting land"),
         (f"{rc.n_rabbit}", f"GBIF rabbit records,\nin {len(rc.rabbit_cells)} cells of 5 km"),
         (str(rc.n_wildcat), "GBIF wildcat records\nin the study area"),
         (f"{spain_share:.0%}", "of the study area in Spain,\nnot yet modelled")]
gx = 0.03 + nat_w + 0.02 + 0.31 + 0.015
gw = 0.97 - gx
for i, (big, small) in enumerate(stats):
    cx = gx + (i % 2 + 0.5) * gw / 2
    cy = K_TOP - 0.002 - (i // 2) * 0.054
    fig.text(cx, cy, big, fontproperties=DISPLAY, fontsize=62, color=CORAL, va="top", ha="center")
    fig.text(cx, cy - 66 / PT_H, small, fontproperties=BODY, fontsize=16, color=NAVY, va="top", ha="center",
             linespacing=1.2)
K_BOTTOM = min(K_TOP - nat_h_pt / PT_H, T.y, K_TOP - 0.002 - 2 * 0.054 - (66 + 2 * 16 * 1.25) / PT_H)
panel_box(fig, 0.03, K_TOP + 0.004, K_BOTTOM, 0.94, colour=PAPER)

# ---- Bottom row: method / results / the wildcat / recommendations ----------------
ROW_TOP = K_BOTTOM - 0.011
XB, WB = [0.03, 0.27, 0.51, 0.75], 0.22
ROW_SIZE = 18
RH = 40
P0 = Column(fig, XB[0], WB, ROW_TOP)
P0.head("Method", size=RH)
P0.items([
    ("Study area.", "10,230 km² on a 100 m grid: the Côa and 30 km around it, extended to its catchment."),
    ("Ten species, three groups", "(land, water, air), after Prima et al. (2024). The wildcat is in the land group, "
                                  "with the wolf and red deer. Suitability from GBIF records (Random Forest)."),
    ("Circuit theory in pure Python,", "with penalties for fire (MODIS, 2015 to July 2025), 22 barriers recorded in "
                                       "the field and two UNESCO areas (Angulo Lopez, 2026b)."),
    ("Rabbit screen.", "At least 20% grassland or cropland and 20% tree cover or shrubland within about 500 m (ESA "
                       "WorldCover 2021), under 5% built, not burned since 2023, 200 m or more from a road, in the top "
                       "third of the land current."),
    ("Limits.", "Training accuracy of 0.78 to 0.99 is not validation."),
], size=ROW_SIZE)

P1 = Column(fig, XB[1], WB, ROW_TOP)
P1.head("What the maps show", size=RH)
P1.items([
    ("Mosaic is common, corridors are not.", f"Rabbit mosaic covers {habitat_km2:,.0f} km²; {cand_km2:,.0f} km² of "
                                             "it lies inside the wildcat's corridors."),
    ("Two blocks carry a quarter.", f"The ten blocks range from {blocks.km2.min():.0f} to {blocks.km2.max():.0f} km²; "
                                    f"the two largest hold {top2_share:.0%} of the candidate area."),
    ("Hunters hold the land.", f"{rc.hunt_share:.0%} of the candidate area is in hunting zones. Faia Brava is "
                               f"{rc.faia_mosaic:.0%} rabbit mosaic but carries little corridor current, so none of "
                               "it is a candidate."),
    ("Recent fire removes little:", f"{recent_burn_share:.1%} of the study area burned from 2023 on, so H3 cannot "
                                    "yet be tested."),
    ("Habitat, not counts.", f"{rc.n_rabbit} rabbit records and no wildcat record in GBIF: the screen needs field "
                             "data."),
], size=ROW_SIZE)

P2 = Column(fig, XB[2], WB, ROW_TOP)
P2.head("Protected, not released", size=RH)
P2.para("No wildcats are released. The existing population is protected, and the work goes into its prey and its "
        "neighbours. Wildcat records are generalised to 5 km before they reach a map.", size=ROW_SIZE)
P2.items([
    ("Keep it wild.", "Hybridisation with domestic cats is the main threat, with persecution (Angulo Lopez, 2026a): "
                      "neuter domestic cats near villages."),
    ("Restore its prey,", "inside its corridors (map 2)."),
    ("Watch the mesopredators.", "Where rabbits crash, foxes and cats switch to other prey (Derham et al., 2018; "
                                 "Finlayson et al., 2021). Monitoring starts before any rabbit release."),
], size=ROW_SIZE)

P3 = Column(fig, XB[3], WB, ROW_TOP)
P3.head("What we propose", size=RH)
P3.items([
    ("A rabbit baseline", "in the ten priority blocks, with the hunters (H1, H3)."),
    ("Cat neutering and mesopredator monitoring", "before and during any rabbit release."),
    ("Camera traps on a 5 km grid", "to test H2."),
    ("The rabbit as a focal species", "in the workflow, then rerun the corridors."),
    ("Extend the model into Spain:", "Campo de Azaba, El Rebollar, Arribes del Duero."),
], size=ROW_SIZE)
P3.kicker("Why the Côa", CORAL, size=19)
P3.para("The river is free-flowing because a 1995 campaign, \"As gravuras não sabem nadar\", stopped a dam to save its "
        "rock art (suspended 17 January 1996; UNESCO, 1998).", size=ROW_SIZE)
P3.para("Which predators will the next chapter of the Côa include, and who decides?", size=27, prop=BOLD,
        colour=CORAL, spacing=1.2)
bottom = min(P0.y, P1.y, P2.y, P3.y)
for x in XB:
    panel_box(fig, x, ROW_TOP + 0.004, bottom, WB, colour=PAPER)

# ---- References and links, at the bottom (review) ------------------------------
foot_top = bottom - 0.009
F = Column(fig, 0.03, 0.94, foot_top)
F.para("Angulo Lopez, L. (2026a). Synthesis and research agenda for trophic rewilding in the Greater Côa Valley "
       "(hypotheses H1-H3). Preprint, Zenodo, doi:10.5281/zenodo.22997241.  Angulo Lopez, L. (2026b). Movement, "
       "Water, Connection: a reproducible Python connectivity workflow and field illustration for the Greater Côa "
       "Valley rewilding landscape, Portugal. Preprint, Zenodo, doi:10.5281/zenodo.22979020.  Data: Côa Valley "
       "Eco-Connectivity v6, Etalab 2.0, data.gouv.fr/datasets/coa-valley-eco-connectivity-v6.  Poster code: "
       "github.com/coa-connectivity-lab/ser2027.  Derham, T. et al. (2018). Phil. Trans. R. Soc. B 373, "
       "doi:10.1098/rstb.2018.0127.  Finlayson, G. et al. (2021). Restoration Ecology 30, doi:10.1111/rec.13552.  "
       "Jiménez, J. et al. (2019). Biological Conservation, doi:10.1016/j.biocon.2019.108234.  Prima, M.-C. et al. "
       "(2024). Methods in Ecology and Evolution.  Villafuerte, R. and Delibes-Mateos, M. (2019). Oryctolagus "
       "cuniculus. IUCN Red List, e.T41291A45189779.  ESA WorldCover 10 m 2021 v200, CC BY 4.0.  HydroRIVERS v1.0.  "
       "NASA MODIS MCD64A1.  OpenStreetMap contributors (ODbL).  ICNF hunting zones.  DGPC heritage boundaries.  "
       "Natural Earth.  GBIF.org occurrences, generalised to 5 km.  Resolução do Conselho de Ministros n.º 14/1996.  "
       "Maps: EPSG:3763; every figure is computed in scripts/poster.py from the v6 bundle.  Code written with AI "
       "assistance (Claude, Anthropic) from the author's method and direction, and reviewed by the author.  Review of "
       "v0.1: VRConservation (GitHub).  Linda Angulo Lopez, 2026, poster " + VERSION + ". Text and maps CC BY 4.0; "
       "code MIT.", size=12, spacing=1.28)
rc.band(fig, 0, 0.006, [BLUE, PURPLE, CORAL, SUN])

print(f"question band ends {Q.y:.3f}; maps {TOP:.3f} to {row_bottom:.3f} (map 1 {M1.y:.3f}, map 2 {M2.y:.3f}); "
      f"key figures {K_TOP:.3f} to {K_BOTTOM:.3f}; bottom row {ROW_TOP:.3f} to {bottom:.3f}; "
      f"references {foot_top:.3f} to {F.y:.3f}")
fig.savefig(OUT / "poster.pdf", facecolor=CREAM, dpi=300)  # map rasters at 300 dpi
fig.savefig(OUT / "poster.png", facecolor=CREAM, dpi=100)
print("wrote", OUT / "poster.pdf", "and poster.png")
