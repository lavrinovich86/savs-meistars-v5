#!/usr/bin/env python3
"""Ģenerē jumta plāna SVG fragmentu lapai (index.html).

Ģeometrija ir shematiska rekonstrukcija pēc pasūtītāja iesniegtā aerofoto:
korpusu proporcijas nolasītas no attēla, izmēri pieņemti. Tas nav uzmērījums
un nav būvprojekta dokumentācija.

Lietošana:  python3 tools/drawings.py > build/roof.svg
"""

# --- ģeometrija metros -------------------------------------------------------

# Trīs korpusi, katrs dziļāks par iepriekšējo — kāpņveida silueta pamats.
A = (0.0, 4.0, 8.4, 16.2)       # kreisais spārns  (x0, y0, x1, y1)
B = (8.4, 2.0, 14.8, 16.8)      # vidusdaļa
C = (14.8, 0.0, 30.0, 18.0)     # galvenais korpuss, divas paralēlas kores

VALLEY_Y = 9.2                  # notekvags starp galvenā korpusa korēm

# Kores. Četrslīpju jumts, vienāds slīpums, kore korpusa dziļuma vidū;
# šļauktnes garums = puse no dziļuma.
RIDGE_A = (6.1, 10.1, 8.4, 10.1)
RIDGE_B = (8.4, 9.4, 14.8, 9.4)
RIDGE_C1 = (14.8, 4.6, 25.4, 4.6)
RIDGE_C2 = (14.8, 13.6, 25.6, 13.6)
RIDGES = [RIDGE_A, RIDGE_B, RIDGE_C1, RIDGE_C2]

# Šļauktnes (hip lines) — tur, kur jumts nogriezts trīsstūrī.
HIPS = [
    ((0.0, 4.0), (6.1, 10.1)),
    ((0.0, 16.2), (6.1, 10.1)),
    ((30.0, 0.0), (25.4, 4.6)),
    ((30.0, 9.2), (25.4, 4.6)),
    ((30.0, 9.2), (25.6, 13.6)),
    ((30.0, 18.0), (25.6, 13.6)),
]

# Ārējā kontūra pa pārkarēm.
OUTLINE = [
    (0.0, 4.0), (8.4, 4.0), (8.4, 2.0), (14.8, 2.0), (14.8, 0.0),
    (30.0, 0.0), (30.0, 18.0), (14.8, 18.0), (14.8, 16.8),
    (8.4, 16.8), (8.4, 16.2), (0.0, 16.2),
]

# Jumta elementi, nolasīti no foto.
CHIMNEY = (17.5, 4.2, 18.4, 5.3)
VENTS = [(16.1, 4.9), (19.8, 8.0), (19.5, 11.8)]
SKYLIGHTS = [(23.6, 16.5), (25.0, 16.5), (26.4, 16.5)]

# --- saules paneļu masīvs ----------------------------------------------------

PW, PH, GAP = 1.70, 1.05, 0.06     # paneļa izmērs plānā un atstarpe

# Zonas, kur paneļu nav: jumta logi un skurstenis ar apkalpes joslu.
KEEP_OUT = [
    (23.2, 16.1, 27.6, 17.8),   # jumta logu josla
    (17.1, 3.8, 18.8, 5.7),     # skurstenis
]


def free(x, y, w, h):
    return all(x >= kx1 or x + w <= kx0 or y >= ky1 or y + h <= ky0
               for kx0, ky0, kx1, ky1 in KEEP_OUT)


def panels(x0, x1, eave, ridge, cut=None, edge=0.30, top=0.35, bottom=0.35):
    """Paneļu režģis uz dienvidu nogāzes, apgriezts pie šļauktnes.

    cut(x, y) -> True, ja punkts ir nogāzes iekšpusē.
    """
    out = []
    y = eave - bottom - PH
    while y >= ridge + top:
        x = x0 + edge
        while x + PW <= x1 - edge:
            corners = [(x, y), (x + PW, y), (x, y + PH), (x + PW, y + PH)]
            if (cut is None or all(cut(cx, cy) for cx, cy in corners)) \
                    and free(x, y, PW, PH):
                out.append((x, y))
            x += PW + GAP
        y -= PH + GAP
    return out

# Paneļi tikai uz dienvidu nogāzēm — tā, kā redzams foto.
ARRAY_A = panels(0.0, 8.4, 16.2, 10.1, cut=lambda x, y: x >= 16.2 - y)
ARRAY_B = panels(8.4, 14.8, 16.8, 9.4)
ARRAY_C1 = panels(14.8, 30.0, VALLEY_Y, 4.6, cut=lambda x, y: x <= y + 20.8)
ARRAY_C2 = panels(14.8, 30.0, 18.0, 13.6, cut=lambda x, y: x <= y + 12.0)
ARRAYS = [("A", ARRAY_A), ("B", ARRAY_B), ("C1", ARRAY_C1), ("C2", ARRAY_C2)]
TOTAL = sum(len(a) for _, a in ARRAYS)

# --- elektroietaise ----------------------------------------------------------

INVERTER = (2.6, 8.4)      # invertors tehniskajā telpā
BOARD = (3.2, 14.4)        # ievadsadalne
EARTH = (1.2, 15.4)        # zemējuma kopne

DC_ROUTES = [
    [(4.9, 12.4), (4.9, 10.6), (3.3, 10.6), (3.3, 9.0)],
    [(11.2, 11.9), (11.2, 10.3), (6.3, 10.3), (6.3, 8.9), (3.6, 8.9)],
    [(20.6, 12.3), (20.6, 11.0), (15.3, 11.0), (15.3, 8.7), (3.9, 8.7)],
    [(20.6, 6.5), (20.6, 8.3), (15.9, 8.3), (15.9, 8.5), (4.2, 8.5)],
]
AC_ROUTE = [(3.4, 9.6), (3.4, 13.6), (4.0, 13.6), (4.0, 14.6)]
EARTH_ROUTE = [(2.7, 15.0), (1.7, 15.0), (1.7, 15.4)]

# --- zīmēšana ----------------------------------------------------------------

SX, SY, SC = 200.0, 300.0, 72.0    # nobīde un mērogs uz SVG vienībām


def p(x, y):
    return f"{SX + x * SC:.0f},{SY + y * SC:.0f}"


def poly(pts, close=False):
    d = " ".join(p(*q) for q in pts)
    return d + (" " + p(*pts[0]) if close else "")


def line(a, b, cls):
    return f'<polyline class="{cls}" points="{poly([a, b])}"/>'


def rect(x, y, w, h, cls):
    return (f'<rect class="{cls}" x="{SX + x * SC:.0f}" y="{SY + y * SC:.0f}" '
            f'width="{w * SC:.0f}" height="{h * SC:.0f}"/>')


def text(x, y, s, cls="an", anchor="start"):
    return (f'<text class="{cls}" x="{SX + x * SC:.0f}" y="{SY + y * SC:.0f}" '
            f'text-anchor="{anchor}">{s}</text>')


def dim_h(x0, x1, y, label):
    """Horizontāla izmēra līnija ar galiem."""
    o = []
    o.append(f'<polyline class="dim" points="{poly([(x0, y), (x1, y)])}"/>')
    for x in (x0, x1):
        o.append(f'<polyline class="dim-tick" points="{poly([(x, y - 0.22), (x, y + 0.22)])}"/>')
    o.append(text((x0 + x1) / 2, y - 0.30, label, "dim-txt", "middle"))
    return "".join(o)


def dim_v(y0, y1, x, label):
    o = []
    o.append(f'<polyline class="dim" points="{poly([(x, y0), (x, y1)])}"/>')
    for y in (y0, y1):
        o.append(f'<polyline class="dim-tick" points="{poly([(x - 0.22, y), (x + 0.22, y)])}"/>')
    o.append(f'<g transform="rotate(-90 {SX + x * SC:.0f} {SY + (y0 + y1) / 2 * SC:.0f})">'
             + text(x, (y0 + y1) / 2 - 0.30, label, "dim-txt", "middle") + '</g>')
    return "".join(o)


def build():
    o = []

    # --- fona režģis (500 mm solis, retinātā versija) ---
    g = []
    step = 1.0
    x = 0.0
    while x <= 32.0:
        g.append(f'<polyline points="{poly([(x, -1.6), (x, 19.8)])}"/>')
        x += step
    y = -1.6
    while y <= 19.8:
        g.append(f'<polyline points="{poly([(-1.6, y), (32.0, y)])}"/>')
        y += step
    o.append('<g class="grid" aria-hidden="true">' + "".join(g) + '</g>')

    # --- A-ARH: kontūra, kores, šļauktnes ---
    a = [f'<polyline class="wall" points="{poly(OUTLINE, close=True)}"/>']
    for r in RIDGES:
        a.append(line((r[0], r[1]), (r[2], r[3]), "ridge"))
    a.append(line((14.8, VALLEY_Y), (25.4, VALLEY_Y), "valley"))
    for h in HIPS:
        a.append(line(h[0], h[1], "hip"))
    # kāpnes starp korpusiem (kores augstumu starpība)
    a.append(line((8.4, 10.1), (8.4, 9.4), "hip"))
    a.append(line((14.8, 9.4), (14.8, 4.6), "hip"))
    a.append(line((14.8, 13.6), (14.8, 9.4), "hip"))
    o.append('<g data-layer="arh">' + "".join(a) + '</g>')

    # --- A-JUMT: skurstenis, ventilācija, jumta logi ---
    j = [rect(CHIMNEY[0], CHIMNEY[1], CHIMNEY[2] - CHIMNEY[0], CHIMNEY[3] - CHIMNEY[1], "feat")]
    j.append(text(CHIMNEY[2] + 0.35, CHIMNEY[1] + 0.55, "SKURSTENIS"))
    for vx, vy in VENTS:
        j.append(f'<circle class="feat" cx="{SX + vx * SC:.0f}" cy="{SY + vy * SC:.0f}" r="16"/>')
    for sx_, sy_ in SKYLIGHTS:
        j.append(rect(sx_, sy_, 0.80, 1.00, "feat"))
    j.append(text(SKYLIGHTS[0][0] - 0.2, 15.55, "JUMTA LOGI — 3 gab."))
    o.append('<g data-layer="jumt">' + "".join(j) + '</g>')

    # --- S-PV: saules paneļi ---
    s = []
    for name, arr in ARRAYS:
        for (x_, y_) in arr:
            s.append(rect(x_, y_, PW, PH, "pv"))
    s.append(text(0.0, 1.5, f"SAULES PANEĻI — {TOTAL} gab., novērtējums pēc aerofoto"))
    o.append('<g data-layer="pv">' + "".join(s) + '</g>')

    # --- E-ELT: elektroietaise ---
    e = []
    for r in DC_ROUTES:
        e.append(f'<polyline class="dc" points="{poly(r)}"/>')
    e.append(f'<polyline class="ac" points="{poly(AC_ROUTE)}"/>')
    e.append(f'<polyline class="pe" points="{poly(EARTH_ROUTE)}"/>')

    e.append(rect(INVERTER[0] - 0.55, INVERTER[1] - 0.45, 1.10, 0.90, "box"))
    e.append(text(INVERTER[0], INVERTER[1] + 0.10, "INV", "an-b", "middle"))
    e.append(text(INVERTER[0] - 0.75, INVERTER[1] - 0.85, "INVERTORS"))

    e.append(rect(BOARD[0] - 0.55, BOARD[1] - 0.45, 1.10, 0.90, "box"))
    e.append(text(BOARD[0], BOARD[1] + 0.10, "IS", "an-b", "middle"))
    e.append(text(BOARD[0] + 1.25, BOARD[1] + 0.15, "IEVADSADALNE"))

    e.append(f'<circle class="box" cx="{SX + EARTH[0] * SC:.0f}" cy="{SY + EARTH[1] * SC:.0f}" r="26"/>')
    e.append(text(EARTH[0] - 0.95, EARTH[1] + 0.15, "PE"))
    o.append('<g data-layer="elt">' + "".join(e) + '</g>')

    # --- M-IZM: izmēri un ziemeļu bulta ---
    m = [
        dim_h(0.0, 8.4, 19.4, "8400"),
        dim_h(8.4, 14.8, 19.4, "6400"),
        dim_h(14.8, 30.0, 19.4, "15200"),
        dim_v(0.0, 18.0, 31.2, "18000"),
    ]
    # ziemeļu bulta
    nx, ny = 31.1, 2.6
    m.append(f'<circle class="north" cx="{SX + nx * SC:.0f}" cy="{SY + ny * SC:.0f}" r="52"/>')
    m.append(f'<polyline class="north-a" points="{poly([(nx, ny + 0.55), (nx, ny - 0.62)])}"/>')
    m.append(f'<polygon class="north-f" points="{poly([(nx - 0.16, ny - 0.30), (nx, ny - 0.72), (nx + 0.16, ny - 0.30)])}"/>')
    m.append(text(nx, ny + 1.05, "Z", "an-b", "middle"))
    o.append('<g data-layer="izm">' + "".join(m) + '</g>')

    return "\n".join(o)


# =============================================================================
# Fasāde (dienvidrietumu skats) pēc pasūtītāja iesniegtā zemes līmeņa foto.
# Foto ir agrāks par aerofoto: uz tā saules paneļu vēl nav, jumts ir metāla
# dakstiņi. Augstumi pieņemti, proporcijas nolasītas no attēla.
# =============================================================================

EX, EY, ESC = 200.0, 1180.0, 72.0     # nulles līmenis un mērogs fasādei


def e(x, h):
    """Fasādes koordinātas: x metros, h — augstums no zemes."""
    return f"{EX + x * ESC:.0f},{EY - h * ESC:.0f}"


def epoly(pts, close=False):
    d = " ".join(e(*q) for q in pts)
    return d + (" " + e(*pts[0]) if close else "")


def etext(x, h, s, cls="an", anchor="start"):
    return (f'<text class="{cls}" x="{EX + x * ESC:.0f}" y="{EY - h * ESC:.0f}" '
            f'text-anchor="{anchor}">{s}</text>')


# Galvenais korpuss
EAVE, RIDGE = 3.6, 8.2
HOUSE = (0.0, 17.6)
RIDGE_X = (5.2, 12.4)

# Šķērsjumts ar logu bēniņu stāvā — foto redzamais ķieģeļu zelminis
GABLE = (7.0, 11.0, 4.8, 8.6)          # x0, x1, dzegas augstums, kores augstums
GABLE_WIN = (7.9, 10.1, 5.7, 7.2)      # x0, x1, palodze, augšmala
LOWER_WIN = (6.2, 8.6, 1.9, 2.9)

CHIMNEY_X = (3.0, 3.9)
CHIMNEY_TOP = 9.8

# Nojume uz balstiem — foto labajā pusē
CANOPY = (17.6, 29.0)
POSTS = [18.2, 22.0, 25.8, 28.4]
POST_H, BEAM_H, CANOPY_TOP = 3.0, 3.25, 5.6


def roof_h(x):
    """Galvenā jumta augstums dotajā x (divslīpju profils skatā)."""
    if x <= RIDGE_X[0]:
        return EAVE + (RIDGE - EAVE) * (x - HOUSE[0]) / (RIDGE_X[0] - HOUSE[0])
    if x >= RIDGE_X[1]:
        return EAVE + (RIDGE - EAVE) * (HOUSE[1] - x) / (HOUSE[1] - RIDGE_X[1])
    return RIDGE


def build_elev():
    o = []

    # --- režģis ---
    g = []
    x = -1.0
    while x <= 31.0:
        g.append(f'<polyline points="{epoly([(x, -0.8), (x, 11.4)])}"/>')
        x += 1.0
    h = -0.8
    while h <= 11.4:
        g.append(f'<polyline points="{epoly([(-1.0, h), (31.0, h)])}"/>')
        h += 1.0
    o.append('<g class="grid" aria-hidden="true">' + "".join(g) + '</g>')

    # --- A-ARH: apjoms ---
    a = []
    a.append(f'<polyline class="wall" points="{epoly([(HOUSE[0], 0.0), (HOUSE[0], EAVE), (RIDGE_X[0], RIDGE), (RIDGE_X[1], RIDGE), (HOUSE[1], EAVE), (HOUSE[1], 0.0)], close=True)}"/>')
    a.append(f'<polyline class="ridge" points="{epoly([(HOUSE[0], EAVE), (HOUSE[1], EAVE)])}"/>')

    # šķērsjumta zelminis
    gx0, gx1, ge, gr = GABLE
    a.append(f'<polyline class="wall" points="{epoly([(gx0, 0.0), (gx0, ge), ((gx0 + gx1) / 2, gr), (gx1, ge), (gx1, 0.0)])}"/>')
    a.append(f'<polyline class="ridge" points="{epoly([(gx0, ge), (gx1, ge)])}"/>')

    # logi
    for wx0, wx1, s_, t_ in (GABLE_WIN, LOWER_WIN):
        a.append(f'<polyline class="win" points="{epoly([(wx0, s_), (wx1, s_), (wx1, t_), (wx0, t_)], close=True)}"/>')
    mid = (GABLE_WIN[0] + GABLE_WIN[1]) / 2
    a.append(f'<polyline class="win" points="{epoly([(mid, GABLE_WIN[2]), (mid, GABLE_WIN[3])])}"/>')

    # skurstenis
    cx0, cx1 = CHIMNEY_X
    a.append(f'<polyline class="feat" points="{epoly([(cx0, roof_h(cx0)), (cx0, CHIMNEY_TOP), (cx1, CHIMNEY_TOP), (cx1, roof_h(cx1))])}"/>')
    a.append(f'<polyline class="feat" points="{epoly([(cx0 - 0.18, CHIMNEY_TOP), (cx1 + 0.18, CHIMNEY_TOP), (cx1 + 0.18, CHIMNEY_TOP + 0.30), (cx0 - 0.18, CHIMNEY_TOP + 0.30)], close=True)}"/>')

    # nojume
    nx0, nx1 = CANOPY
    a.append(f'<polyline class="wall" points="{epoly([(nx0, BEAM_H), (nx1, BEAM_H), ((nx0 + nx1) / 2, CANOPY_TOP)], close=True)}"/>')
    a.append(f'<polyline class="ridge" points="{epoly([(nx0, POST_H), (nx1, POST_H)])}"/>')
    for px in POSTS:
        a.append(f'<polyline class="wall" points="{epoly([(px - 0.09, 0.0), (px - 0.09, POST_H), (px + 0.09, POST_H), (px + 0.09, 0.0)])}"/>')

    # zemes līnija
    a.append(f'<polyline class="ground" points="{epoly([(-1.0, 0.0), (31.0, 0.0)])}"/>')
    o.append('<g data-layer="arh">' + "".join(a) + '</g>')

    # --- A-JUMT: ķieģeļu mūra raksts un jumta segums ---
    j = []
    h = 0.25
    while h < EAVE:
        j.append(f'<polyline class="brick" points="{epoly([(HOUSE[0] + 0.12, h), (HOUSE[1] - 0.12, h)])}"/>')
        h += 0.25
    h = ge + 0.25
    while h < gr - 0.25:
        half = (gx1 - gx0) / 2 * (gr - h) / (gr - ge)
        j.append(f'<polyline class="brick" points="{epoly([((gx0 + gx1) / 2 - half + 0.1, h), ((gx0 + gx1) / 2 + half - 0.1, h)])}"/>')
        h += 0.25
    # metāla dakstiņu solis uz jumta nogāzes
    x = HOUSE[0] + 0.4
    while x < RIDGE_X[0]:
        j.append(f'<polyline class="tile" points="{epoly([(x, roof_h(x)), (x + 0.02, roof_h(x))])}"/>')
        x += 0.35
    o.append('<g data-layer="jumt">' + "".join(j) + '</g>')

    # --- M-IZM ---
    m = []
    m.append(f'<polyline class="dim" points="{epoly([(HOUSE[0], -0.55), (nx1, -0.55)])}"/>')
    for x in (HOUSE[0], HOUSE[1], nx1):
        m.append(f'<polyline class="dim-tick" points="{epoly([(x, -0.35), (x, -0.75)])}"/>')
    m.append(etext((HOUSE[0] + HOUSE[1]) / 2, -0.95, "17600", "dim-txt", "middle"))
    m.append(etext((HOUSE[1] + nx1) / 2, -0.95, "11400", "dim-txt", "middle"))

    m.append(f'<polyline class="dim" points="{epoly([(-0.55, 0.0), (-0.55, RIDGE)])}"/>')
    for h_ in (0.0, EAVE, RIDGE):
        m.append(f'<polyline class="dim-tick" points="{epoly([(-0.75, h_), (-0.35, h_)])}"/>')
    m.append(f'<g transform="rotate(-90 {EX - 0.9 * ESC:.0f} {EY - EAVE / 2 * ESC:.0f})">'
             + etext(-0.9, EAVE / 2, "3600", "dim-txt", "middle") + '</g>')
    m.append(f'<g transform="rotate(-90 {EX - 0.9 * ESC:.0f} {EY - (EAVE + RIDGE) / 2 * ESC:.0f})">'
             + etext(-0.9, (EAVE + RIDGE) / 2, "4600", "dim-txt", "middle") + '</g>')

    m.append(etext(nx0 + 0.3, CANOPY_TOP + 0.45, "NOJUME UZ BALSTIEM"))
    m.append(etext(cx1 + 0.35, CHIMNEY_TOP - 0.35, "SKURSTENIS"))
    m.append(etext(gx1 + 1.2, gr + 0.75, "BĒNIŅU STĀVA LOGS"))
    m.append(f'<polyline class="dim" points="{epoly([(gx1 + 1.1, gr + 0.62), (GABLE_WIN[1], GABLE_WIN[3])])}"/>')
    m.append(etext(HOUSE[0] + 0.2, -1.55, "METĀLA DAKSTIŅI · ĶIEĢEĻU MŪRIS"))
    o.append('<g data-layer="izm">' + "".join(m) + '</g>')

    return "\n".join(o)


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "roof"
    print(build_elev() if which == "elev" else build())
    if which == "roof":
        parts = " ".join(f"{n}={len(a)}" for n, a in ARRAYS)
        print(f"paneļi: {parts} kopā={TOTAL}", file=sys.stderr)
