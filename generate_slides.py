from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# Couleurs du thème Carrefour
BLEU_FONCE = RGBColor(0x0D, 0x1B, 0x3E)   # #0D1B3E
ROUGE = RGBColor(0xCC, 0x00, 0x00)          # #CC0000
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
GRIS_CLAIR = RGBColor(0xF5, 0xF5, 0xF5)
BLEU_MOYEN = RGBColor(0x1A, 0x3A, 0x6B)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

def add_background(slide, color):
    from pptx.util import Emu
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, color, text=None, font_size=18, font_color=BLANC, bold=False, align=PP_ALIGN.LEFT):
    from pptx.util import Inches, Pt
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    if text:
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = align
        run = p.add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.color.rgb = font_color
        run.font.bold = bold
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=14, color=BLANC, bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    return txBox

def add_paragraph(tf, text, font_size=12, color=BLANC, bold=False, bullet=False, indent=0):
    from pptx.util import Pt
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    if indent > 0:
        p.level = indent
    run = p.add_run()
    run.text = ("• " if bullet else "") + text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    return p

# ============================================================
# SLIDE 1 — TITRE SECTION : ANALYSE & CONTEXTE — BENCHMARK
# ============================================================
slide_layout = prs.slide_layouts[6]  # Blank
slide = prs.slides.add_slide(slide_layout)
add_background(slide, BLEU_FONCE)

# Numéro de section
add_rect(slide, 0.3, 0.2, 1.2, 0.45, ROUGE, "01 —\nBENCHMARK", font_size=9, bold=True, align=PP_ALIGN.CENTER)

# Titre
add_text_box(slide, 1.7, 0.15, 10, 0.6, "Benchmark omnicanal — Positionnement concurrentiel", font_size=26, color=BLANC, bold=True)

# Ligne rouge déco
add_rect(slide, 0.3, 0.85, 12.7, 0.04, ROUGE)

# En-têtes colonnes
cols = ["Critère", "Carrefour", "Leclerc", "Amazon Fresh", "Lidl", "Auchan"]
col_widths = [2.8, 1.7, 1.7, 1.7, 1.7, 1.7]
col_colors = [BLEU_MOYEN, RGBColor(0x1A,0x5C,0xA8), RGBColor(0x1A,0x8C,0x4E), RGBColor(0xFF,0x6B,0x00), RGBColor(0x0D,0x4F,0x8B), RGBColor(0xB8,0x00,0x00)]
x = 0.3
for i, (col, w, c) in enumerate(zip(cols, col_widths, col_colors)):
    add_rect(slide, x, 1.0, w - 0.05, 0.5, c, col, font_size=11, bold=True, align=PP_ALIGN.CENTER)
    x += w

# Données
rows = [
    ["Programme fidélité",    "★★★★",  "★★★",   "★★",      "★",    "★★★"],
    ["Application mobile",    "★★★★",  "★★★",   "★★★★★",   "★★",   "★★★"],
    ["Click & Collect",       "★★★",   "★★★★",  "★★★★★",   "★",    "★★★"],
    ["Personnalisation offres","★★★",   "★★",    "★★★★★",   "★",    "★★"],
    ["Expérience en magasin", "★★★",   "★★★",   "★★",      "★★★★", "★★★"],
    ["Livraison express",     "★★★",   "★★",    "★★★★★",   "★",    "★★"],
    ["Intégration data",      "★★★",   "★★",    "★★★★★",   "★",    "★★"],
]
row_colors = [RGBColor(0x1A,0x2B,0x52), RGBColor(0x16,0x25,0x48)]
y = 1.55
for idx, row in enumerate(rows):
    rc = row_colors[idx % 2]
    x = 0.3
    for i, (val, w) in enumerate(zip(row, col_widths)):
        fc = BLANC if i > 0 else RGBColor(0xDD, 0xDD, 0xDD)
        add_rect(slide, x, y, w - 0.05, 0.44, rc, val, font_size=11 if i > 0 else 10, font_color=fc, align=PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT)
        x += w
    y += 0.45

# Note de bas
add_text_box(slide, 0.3, 7.0, 12, 0.35, "Echelle de maturité omnicanale (1 = faible, 5 = excellent) — Analyse indicative 2025", font_size=9, color=RGBColor(0xAA,0xAA,0xAA))

# Enseignements
add_rect(slide, 0.3, 6.5, 12.7, 0.45, RGBColor(0xCC,0x00,0x00),
    "✅ Leader GMS mais en retard vs Amazon sur la data   ⚠️ Leclerc surperforme sur le C&C   🎯 Levier Carrefour : réseau physique + Carrefour+",
    font_size=10, bold=False, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2 — TITRE SECTION 06
# ============================================================
slide = prs.slides.add_slide(slide_layout)
add_background(slide, BLEU_FONCE)

# Grand numéro décoratif
add_text_box(slide, 0.2, 0.5, 3, 5, "6", font_size=200, color=RGBColor(0x1A,0x2B,0x52), bold=True)

# Ligne rouge
add_rect(slide, 1.2, 3.8, 0.08, 1.8, ROUGE)

# Titre
add_text_box(slide, 1.5, 3.7, 9, 1.2, "Que faire en cas de\nnon fonctionnement\nde la stratégie ?", font_size=34, color=BLANC, bold=True)

# Sous-titre
add_text_box(slide, 1.5, 5.1, 9, 0.6, "Plan de contingence & mesures correctives", font_size=16, color=RGBColor(0xCC,0xCC,0xCC))

# Ligne rouge bas
add_rect(slide, 0, 7.1, 13.33, 0.15, ROUGE)

# ============================================================
# SLIDE 3 — RISQUES & SCÉNARIOS D'ÉCHEC
# ============================================================
slide = prs.slides.add_slide(slide_layout)
add_background(slide, BLANC)

# Header
add_rect(slide, 0, 0, 13.33, 0.9, BLEU_FONCE)
add_rect(slide, 0.3, 0.18, 1.5, 0.5, ROUGE, "06 —\nPLAN", font_size=9, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, 2.0, 0.2, 10, 0.55, "Risques & scénarios d'échec identifiés", font_size=22, color=BLANC, bold=True)

# En-têtes tableau
headers = ["Risque", "Probabilité", "Impact", "Signal d'alerte"]
widths = [3.8, 1.9, 1.9, 5.3]
h_colors = [BLEU_MOYEN, RGBColor(0x8B,0x00,0x00), RGBColor(0x8B,0x00,0x00), RGBColor(0x1A,0x5C,0x3A)]
x = 0.3
for h, w, c in zip(headers, widths, h_colors):
    add_rect(slide, x, 1.05, w - 0.05, 0.45, c, h, font_size=11, bold=True, align=PP_ALIGN.CENTER)
    x += w

risques = [
    ["Faible adoption de l'app Carrefour+",     "Moyenne",  "Élevé",      "Taux utilisation < 20%"],
    ["Délais Click & Collect non respectés",    "Élevée",   "Élevé",      "Délai moyen > 2h"],
    ["Résistance des équipes en magasin",       "Moyenne",  "Moyen",      "NPS interne < 30"],
    ["Silos de données persistants (CDP)",      "Faible",   "Très élevé", "CDP non opérationnel à M3"],
    ["Concurrence agressive (Amazon, Leclerc)", "Élevée",   "Moyen",      "Perte part de marché > 2%"],
    ["Budget dépassé / retard déploiement",     "Moyenne",  "Élevé",      "Dépassement > 15% budget"],
]
prob_colors = {"Faible": RGBColor(0x2E,0x7D,0x32), "Moyenne": RGBColor(0xF5,0x7C,0x00), "Élevée": RGBColor(0xC6,0x28,0x28)}
impact_colors = {"Moyen": RGBColor(0xF5,0x7C,0x00), "Élevé": RGBColor(0xC6,0x28,0x28), "Très élevé": RGBColor(0x8B,0x00,0x00)}
row_bg = [RGBColor(0xF0,0xF4,0xF8), RGBColor(0xE8,0xEE,0xF5)]

y = 1.55
for idx, row in enumerate(risques):
    rc = row_bg[idx % 2]
    x = 0.3
    for i, (val, w) in enumerate(zip(row, widths)):
        if i == 1:
            bg = prob_colors.get(val, BLEU_MOYEN)
            fc = BLANC
        elif i == 2:
            bg = impact_colors.get(val, BLEU_MOYEN)
            fc = BLANC
        else:
            bg = rc
            fc = BLEU_FONCE
        add_rect(slide, x, y, w - 0.05, 0.5, bg, val, font_size=10, font_color=fc, align=PP_ALIGN.CENTER if i in [1,2] else PP_ALIGN.LEFT)
        x += w
    y += 0.52

# ============================================================
# SLIDE 4 — PLAN DE CONTINGENCE
# ============================================================
slide = prs.slides.add_slide(slide_layout)
add_background(slide, BLANC)

add_rect(slide, 0, 0, 13.33, 0.9, BLEU_FONCE)
add_rect(slide, 0.3, 0.18, 1.5, 0.5, ROUGE, "06 —\nPLAN", font_size=9, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, 2.0, 0.2, 10, 0.55, "Plan B — Mesures correctives par scénario", font_size=22, color=BLANC, bold=True)

scenarios = [
    {
        "title": "🔴  App Carrefour+ peu adoptée",
        "color": RGBColor(0xC6,0x28,0x28),
        "actions": [
            "Campagne communication en magasin (affichage, caissiers ambassadeurs)",
            "Offre de bienvenue : -10% sur la 1ère commande via app",
            "Simplification UX et refonte de l'onboarding"
        ]
    },
    {
        "title": "🟠  Délais Click & Collect non respectés",
        "color": RGBColor(0xE6,0x5C,0x00),
        "actions": [
            "Renforcement des équipes de préparation en heures de pointe",
            "Révision des créneaux de commande disponibles",
            "Partenariat avec un prestataire logistique externe en backup"
        ]
    },
    {
        "title": "🟡  CDP non opérationnelle à temps",
        "color": RGBColor(0xC8,0x9A,0x00),
        "actions": [
            "Utilisation temporaire des données CRM existantes (Salesforce)",
            "Report de la phase 2 (Activation digitale) de 1 mois",
            "Audit technique et recrutement d'un intégrateur externe"
        ]
    },
]

y = 1.05
col_x = [0.3, 4.55, 8.8]
for i, (sc, cx) in enumerate(zip(scenarios, col_x)):
    add_rect(slide, cx, y, 4.0, 0.5, sc["color"], sc["title"], font_size=10, bold=True)
    ay = y + 0.55
    for action in sc["actions"]:
        box = slide.shapes.add_textbox(Inches(cx), Inches(ay), Inches(4.0), Inches(0.55))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = "• " + action
        run.font.size = Pt(10)
        run.font.color.rgb = BLEU_FONCE
        ay += 0.6

# Bloc résistance équipes
add_rect(slide, 0.3, 3.4, 12.7, 0.45, BLEU_MOYEN, "🟢  Résistance des équipes en magasin", font_size=11, bold=True)
actions_eq = [
    "• Programme de formation accéléré (e-learning + ateliers pratiques en magasin)",
    "• Désignation d'ambassadeurs digitaux dans chaque hypermarché pilote",
    "• Incentives liés à l'adoption des outils (prime trimestrielle)"
]
y2 = 3.95
for a in actions_eq:
    add_text_box(slide, 0.5, y2, 12.3, 0.38, a, font_size=10, color=BLEU_FONCE)
    y2 += 0.4

# ============================================================
# SLIDE 5 — GOUVERNANCE & SUIVI
# ============================================================
slide = prs.slides.add_slide(slide_layout)
add_background(slide, BLANC)

add_rect(slide, 0, 0, 13.33, 0.9, BLEU_FONCE)
add_rect(slide, 0.3, 0.18, 1.5, 0.5, ROUGE, "06 —\nPLAN", font_size=9, bold=True, align=PP_ALIGN.CENTER)
add_text_box(slide, 2.0, 0.2, 10, 0.55, "Gouvernance & Pilotage de la stratégie", font_size=22, color=BLANC, bold=True)

# 3 colonnes gouvernance
gov_items = [
    {
        "title": "Comité de pilotage\nmensuel",
        "color": BLEU_MOYEN,
        "points": ["Revue complète des KPIs vs objectifs", "Décisions d'ajustement opérationnel", "Présence DSI + Directeur e-commerce + DG"]
    },
    {
        "title": "Seuils d'alerte\ndéfinis",
        "color": RGBColor(0xC6,0x28,0x28),
        "points": ["KPI hors cible → réunion de crise 72h", "Tableau de bord temps réel (Tableau/Looker)", "Alertes automatiques si seuil franchi"]
    },
    {
        "title": "Responsables\npar axe",
        "color": RGBColor(0x1A,0x7A,0x4A),
        "points": ["Data/CDP → DSI", "App & digital → Dir. e-commerce", "Expérience magasin → Dir. régionaux"]
    },
]
cx = 0.3
for item in gov_items:
    add_rect(slide, cx, 1.05, 4.0, 0.8, item["color"], item["title"], font_size=13, bold=True, align=PP_ALIGN.CENTER)
    ay = 1.95
    for pt in item["points"]:
        box = slide.shapes.add_textbox(Inches(cx), Inches(ay), Inches(4.0), Inches(0.5))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = "✓ " + pt
        run.font.size = Pt(10)
        run.font.color.rgb = BLEU_FONCE
        ay += 0.5
    cx += 4.25

# Processus de révision
add_rect(slide, 0.3, 3.6, 12.7, 0.45, BLEU_FONCE, "PROCESSUS DE RÉVISION STRATÉGIQUE", font_size=12, bold=True, align=PP_ALIGN.CENTER)

etapes = [
    ("M3", "Bilan\nPhase 1"),
    ("M6", "Bilan\nPhase 2"),
    ("M9", "Bilan\nPhase 3"),
    ("M12", "Bilan\nannuel +\nRoadmap 2027"),
]
step_colors = [BLEU_MOYEN, RGBColor(0x1A,0x7A,0x4A), RGBColor(0xE6,0x5C,0x00), ROUGE]
sx = 1.0
for (month, label), sc in zip(etapes, step_colors):
    add_rect(slide, sx, 4.2, 1.5, 0.6, sc, month, font_size=18, bold=True, align=PP_ALIGN.CENTER)
    add_text_box(slide, sx, 4.85, 1.5, 0.7, label, font_size=9, color=BLEU_FONCE, align=PP_ALIGN.CENTER)
    if sx < 8:
        add_rect(slide, sx + 1.5, 4.42, 1.2, 0.15, RGBColor(0xCC,0xCC,0xCC))
    sx += 2.7

# Rapport CODIR
add_rect(slide, 0.3, 5.7, 12.7, 0.5, RGBColor(0xF0,0xF4,0xF8),
    "📊  Rapport trimestriel au CODIR avec recommandations d'ajustement — Présentation résultats & parties prenantes à M12",
    font_size=10, font_color=BLEU_FONCE, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 6 — CONCLUSION DE LA SECTION
# ============================================================
slide = prs.slides.add_slide(slide_layout)
add_background(slide, BLEU_FONCE)

add_text_box(slide, 0.5, 0.4, 12, 0.6, "CONCLUSION", font_size=13, color=RGBColor(0xAA,0xAA,0xAA))
add_rect(slide, 0.5, 0.95, 1.5, 0.07, ROUGE)
add_text_box(slide, 0.5, 1.1, 11, 1.5, '"Une stratégie robuste\nanticipe ses échecs."', font_size=40, color=BLANC, bold=True)

convictions = [
    ("01", "Mesurer en continu",    "Les KPIs sont des signaux d'alerte, pas juste des objectifs annuels.",   BLEU_MOYEN),
    ("02", "Agir vite",             "Décision corrective sous 72h max dès détection d'un écart significatif.", RGBColor(0x1A,0x7A,0x4A)),
    ("03", "Apprendre & itérer",    "Chaque échec partiel nourrit la roadmap 2027 et renforce la résilience.", RGBColor(0xE6,0x5C,0x00)),
]
y = 2.8
for num, title, desc, color in convictions:
    add_rect(slide, 0.5, y, 0.7, 0.65, color, num, font_size=18, bold=True, align=PP_ALIGN.CENTER)
    add_text_box(slide, 1.35, y, 4.0, 0.35, title, font_size=14, color=BLANC, bold=True)
    add_text_box(slide, 1.35, y + 0.35, 11.0, 0.35, desc, font_size=11, color=RGBColor(0xCC,0xCC,0xCC))
    y += 0.9

# Ligne rouge bas
add_rect(slide, 0, 7.1, 13.33, 0.15, ROUGE)

# Sauvegarde
output_path = "/home/user/rbconsulting.github.io/Carrefour_Slides_Rodrin.pptx"
prs.save(output_path)
print(f"Fichier généré : {output_path}")
