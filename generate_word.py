from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Marges ──
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

# ── Helpers ──
def heading(doc, text, level=1, color=(13,27,62)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.color.rgb = RGBColor(*color)
    return p

def body(doc, text, bold_part=None):
    p = doc.add_paragraph()
    if bold_part and bold_part in text:
        parts = text.split(bold_part, 1)
        p.add_run(parts[0])
        r = p.add_run(bold_part)
        r.bold = True
        if len(parts) > 1:
            p.add_run(parts[1])
    else:
        p.add_run(text)
    p.style.font.size = Pt(11)
    return p

def bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.3 * (level + 1))
    run = p.add_run(text)
    run.font.size = Pt(11)
    return p

def tip(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    run = p.add_run("💡 " + text)
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0, 100, 180)
    return p

def separator(doc):
    doc.add_paragraph("─" * 80)

# ═══════════════════════════════════════════════════════════
# PAGE DE TITRE
# ═══════════════════════════════════════════════════════════
title = doc.add_heading("GUIDE DE PRÉSENTATION", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in title.runs:
    run.font.color.rgb = RGBColor(13, 27, 62)

sub = doc.add_paragraph("Carrefour — Stratégie Omnicanale 2025-2026")
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.runs[0].font.size = Pt(14)
sub.runs[0].font.bold = True
sub.runs[0].font.color.rgb = RGBColor(180, 0, 0)

sub2 = doc.add_paragraph("Cas pratique 2 — Grande Distribution | Analyse & Contexte + Section 06")
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub2.runs[0].font.size = Pt(11)
sub2.runs[0].font.color.rgb = RGBColor(80, 80, 80)

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# INTRODUCTION : POURQUOI CE TRAVAIL ?
# ═══════════════════════════════════════════════════════════
heading(doc, "0. Pourquoi ce travail ? L'objectif du cas pratique", level=1)

body(doc, "Carrefour est le leader de la grande distribution en France (~20% de part de marché). Pourtant, comme tous les grands acteurs physiques, il fait face à un défi majeur : ses clients achètent de moins en moins en un seul canal. Ils comparent en ligne, achètent en magasin, utilisent l'application, commandent en Drive...")

body(doc, "L'objectif du cas pratique est triple :")
bullet(doc, "Fidéliser les clients magasin qui risquent de partir vers des concurrents plus digitaux (Amazon, Leclerc)")
bullet(doc, "Proposer une stratégie omnicanale cohérente qui unifie tous les points de contact")
bullet(doc, "Définir les outils concrets et un plan d'action opérationnel sur 12 mois")

tip(doc, "Quand tu présentes : commence toujours par le PROBLÈME avant la solution. Les slides commencent par les chiffres et les défis de Carrefour, pas par les solutions. C'est volontaire.")

doc.add_paragraph("")

# ═══════════════════════════════════════════════════════════
# SECTION 01 — ANALYSE & CONTEXTE
# ═══════════════════════════════════════════════════════════
heading(doc, "1. ANALYSE & CONTEXTE — Ce qu'il faut savoir et pourquoi", level=1, color=(180,0,0))
body(doc, "C'est la première partie de la présentation. Elle sert à poser le diagnostic avant de proposer des solutions. Sans cette base, les recommandations sembleraient arbitraires.")

doc.add_paragraph("")

# 1.1 Carrefour en chiffres
heading(doc, "1.1 Carrefour en chiffres — Pourquoi ces données ?", level=2)
body(doc, "Ces chiffres montrent la puissance mais aussi la complexité de Carrefour :")

bullet(doc, "~90 Md€ de chiffre d'affaires → C'est le 2e distributeur mondial. Ce n'est pas une PME, chaque changement stratégique coûte cher et prend du temps.")
bullet(doc, "13 000+ magasins dans 30+ pays → L'omnicanalité doit fonctionner à très grande échelle, pas juste dans 10 magasins pilotes.")
bullet(doc, "2 400 points de vente en France → Le réseau physique est un atout énorme. Beaucoup de concurrents n'ont pas ça.")
bullet(doc, "12 M membres actifs Carrefour+ → La base clients fidèles existe déjà. Le programme de fidélité est un levier à activer, pas à créer.")
bullet(doc, "8 M téléchargements de l'app → L'app existe et est utilisée. Il faut l'améliorer, pas en créer une nouvelle.")
bullet(doc, "900+ Points Drive → 2e acteur e-commerce alimentaire en France. Le Drive est déjà ancré dans les habitudes.")

tip(doc, "À l'oral, tu peux dire : 'Ces chiffres montrent que Carrefour a DÉJÀ les ressources. Le problème n'est pas l'absence d'outils, c'est qu'ils ne sont pas connectés entre eux.'")

doc.add_paragraph("")

# 1.2 Forces & Défis
heading(doc, "1.2 Forces & Défis — Le SWOT simplifié", level=2)

body(doc, "FORCES (ce que Carrefour fait bien) :")
bullet(doc, "Leader GMS en France (~20% de part de marché) → Position dominante à défendre, pas juste à consolider")
bullet(doc, "Programme Carrefour+ avec 12M membres actifs → Mine d'or de données clients inexploitée")
bullet(doc, "Réseau logistique mature et capillaire → Capacité à livrer partout en France rapidement")
bullet(doc, "Application mobile avec 8M de téléchargements → Présence digitale réelle")
bullet(doc, "900+ Points Drive → Déjà bien implanté sur le créneau click & collect")

doc.add_paragraph("")
body(doc, "DÉFIS (ce que Carrefour doit corriger) :")
bullet(doc, "Expérience fragmentée entre web, app et magasin → Le client n'a pas la même expérience selon le canal. C'est le problème central.")
bullet(doc, "Données clients silotées — pas de vue 360° → Les données de l'app, du POS magasin, du site web et de la carte de fidélité ne se parlent pas.")
bullet(doc, "Taux d'attrition élevé chez les 25-40 ans → La génération la plus connectée quitte Carrefour pour des enseignes plus digitales.")
bullet(doc, "Délais Click & Collect encore trop longs → Le C&C existe mais pas assez rapide vs Amazon ou Leclerc.")
bullet(doc, "Incohérence prix/promos offline vs online → Un client peut voir un prix différent en magasin et sur l'app. Problème de confiance.")

tip(doc, "Astuce présentation : Pour chaque défi, relie-le à une solution concrète de la stratégie. Ex : 'Les données silotées → c'est pour ça qu'on propose une CDP (Customer Data Platform)'")

doc.add_paragraph("")

# 1.3 Benchmark
heading(doc, "1.3 Benchmark concurrentiel — Pourquoi comparer ?", level=2)
body(doc, "Le benchmark répond à la question : 'Où se situe Carrefour par rapport à la concurrence ?' C'est indispensable pour justifier les choix stratégiques.")

body(doc, "LES CONCURRENTS ANALYSÉS et pourquoi ils ont été choisis :")
bullet(doc, "Leclerc → Principal concurrent direct, même positionnement grande distribution, fort sur le C&C")
bullet(doc, "Amazon Fresh → La menace digitale pure. Meilleur sur data, personnalisation et livraison express")
bullet(doc, "Lidl → Concurrent sur le prix, fort sur l'expérience en magasin, faible sur le digital")
bullet(doc, "Auchan → Concurrent direct sur le segment hypermarché")

doc.add_paragraph("")
body(doc, "CE QUE LE BENCHMARK RÉVÈLE :")
bullet(doc, "Programme fidélité : Carrefour (4/5) est bon mais Amazon personnalise mieux")
bullet(doc, "Application mobile : Carrefour (4/5) — Amazon est à 5/5. L'écart est réel mais rattrapable.")
bullet(doc, "Click & Collect : Leclerc surpasse Carrefour (4 vs 3). C'est un point faible prioritaire à corriger.")
bullet(doc, "Personnalisation offres : C'est là que l'écart est le plus grand. Amazon utilise l'IA, Carrefour utilise des segments basiques.")
bullet(doc, "Expérience en magasin : Carrefour et Leclerc sont égaux (3/5). Lidl surprend avec 4/5 grâce à son concept épuré.")
bullet(doc, "Livraison express : Gros retard vs Amazon. Mais ce n'est pas le cœur de métier de Carrefour.")

tip(doc, "Message clé du benchmark : Carrefour est bon partout mais excellent nulle part. La stratégie omnicanale vise à devenir leader sur 2-3 critères clés : fidélité, C&C et personnalisation.")

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# SECTION 02 — PARCOURS CLIENT (CJM)
# ═══════════════════════════════════════════════════════════
heading(doc, "2. CARTOGRAPHIE DU PARCOURS CLIENT (CJM)", level=1, color=(180,0,0))
body(doc, "Le CJM (Customer Journey Map) montre comment un vrai client vit son expérience Carrefour, étape par étape.")

heading(doc, "Le Persona : Paul, 25 ans, étudiant", level=2)
body(doc, "Pourquoi ce profil ? Paul représente la cible prioritaire : jeune, connecté, sensible au prix, qui utilise le digital naturellement mais risque de choisir un concurrent plus pratique.")

bullet(doc, "Phase 1 — Découverte : Paul voit une pub Carrefour sur les réseaux sociaux (Social Commerce). Il clique et atterrit sur l'app.")
bullet(doc, "Phase 2 — Considération : Paul utilise l'app pour faire sa liste, vérifier les stocks et comparer les prix. L'app lui propose des coupons personnalisés.")
bullet(doc, "Phase 3 — Achat : Paul est en magasin. Il utilise Scan & Go pour scanner ses articles et payer sans passer en caisse. Il suit son budget en temps réel.")
bullet(doc, "Phase 4 — Fidélisation : Le lendemain, Paul reçoit une notification de gamification et laisse un avis positif sur Google Maps.")

tip(doc, "À l'oral : 'Ce parcours montre que chaque étape implique un outil différent. Si ces outils ne sont pas connectés, on perd Paul à chaque transition.'")

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# SECTION 03 — STRATÉGIE OMNICANALE
# ═══════════════════════════════════════════════════════════
heading(doc, "3. STRATÉGIE OMNICANALE — Les 3 axes", level=1, color=(180,0,0))
body(doc, "L'objectif central : passer du commerce classique (chaque canal fonctionne seul) au commerce unifié (tous les canaux connectés, sans friction).")

heading(doc, "Axe 1 — Expérience physique augmentée", level=2)
bullet(doc, "Bornes interactives en rayon : conseils, disponibilité des produits, redirection vers l'app si rupture de stock")
bullet(doc, "Click & Collect optimisé : zones dédiées, notification SMS/push dès que la commande est prête, objectif délai < 2h sur 100% du réseau")

heading(doc, "Axe 2 — Collecte & gestion des données clients (CDP)", level=2)
body(doc, "C'est le cœur technique de toute la stratégie. La CDP (Customer Data Platform) centralise toutes les données client :")
bullet(doc, "Sources : transactions magasin (POS), app mobile, site e-commerce, carte fidélité Carrefour+, bornes Scan & Go")
bullet(doc, "Résultat : un identifiant client unique cross-canal → Carrefour sait que Paul qui achète en magasin est le même Paul qui commande en ligne")
bullet(doc, "Usages : segmentation, personnalisation, scoring prédictif (qui risque de partir ?), campagnes ciblées")

heading(doc, "Axe 3 — Optimisation des 3 parcours clés", level=2)
bullet(doc, "WEB → MAGASIN : recherche app/web → réservation → notification → Scan & Go → points fidélité crédités")
bullet(doc, "MAGASIN → WEB : découverte en rayon → scan code-barres → liste de courses → commande en ligne si rupture → Drive ou livraison")
bullet(doc, "CLICK & COLLECT : commande app → confirmation SMS → préparation < 2h → retrait borne dédiée → évaluation NPS")

tip(doc, "Message clé : Peu importe par où le client entre (web, magasin, app), il vit la même expérience fluide et cohérente.")

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# SECTION 04 — OUTILS & TECHNOLOGIES
# ═══════════════════════════════════════════════════════════
heading(doc, "4. OUTILS & TECHNOLOGIES — L'écosystème technique", level=1, color=(180,0,0))
body(doc, "La stratégie repose sur 4 familles d'outils. Tu n'as pas besoin de tout connaître en détail, mais tu dois comprendre À QUOI ça sert.")

heading(doc, "CRM & Data", level=2)
bullet(doc, "Salesforce CRM → Gestion de la relation client, historique des interactions")
bullet(doc, "CDP Segment → Centralise et unifie toutes les données clients en temps réel")
bullet(doc, "Snowflake Data Cloud → Stockage et analyse de très grandes quantités de données")

heading(doc, "Digital & App", level=2)
bullet(doc, "App Carrefour+ → Hub omnicanal (liste de courses, Scan & Go, coupons, localisation produit, push géolocalisé, suivi commande)")
bullet(doc, "Adobe Experience Manager → Gestion du contenu web et app de façon cohérente sur tous les canaux")
bullet(doc, "Salesforce Marketing Cloud → Envoi des campagnes email/SMS/push personnalisées")

heading(doc, "Logistique", level=2)
bullet(doc, "Manhattan WMS → Gestion des entrepôts et des stocks en temps réel")
bullet(doc, "Curbside Pickup → Système de retrait en voiture sans descendre")
bullet(doc, "Routific Last-Mile → Optimisation des tournées de livraison à domicile")

heading(doc, "Analytics & IA", level=2)
bullet(doc, "Google Vertex AI → Algorithmes de recommandation et personnalisation (comme Amazon)")
bullet(doc, "Tableau / Looker → Tableaux de bord KPI en temps réel pour les managers")
bullet(doc, "AB Tasty → Tests A/B sur le site et l'app pour améliorer l'expérience")

tip(doc, "À l'oral : 'On n'a pas choisi ces outils au hasard. Chaque outil répond à un défis identifié dans l'analyse : les silos de données → CDP, le délai C&C → Manhattan WMS, la personnalisation → Google Vertex AI.'")

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# SECTION 05 — KPI & INDICATEURS
# ═══════════════════════════════════════════════════════════
heading(doc, "5. KPI & INDICATEURS — Comment mesurer le succès ?", level=1, color=(180,0,0))
body(doc, "Les KPIs servent à savoir si la stratégie fonctionne. Chaque objectif stratégique a son indicateur chiffré.")

heading(doc, "Indicateurs de fidélisation & expérience client", level=2)
bullet(doc, "Taux de rétention client (12 mois) > 65% → Est-ce que les clients reviennent ?")
bullet(doc, "Taux d'utilisation Carrefour+ > 40% → Est-ce que le programme fidélité est activé ?")
bullet(doc, "Valeur vie client (LTV) +20%/N-1 → Est-ce que chaque client dépense plus qu'avant ?")
bullet(doc, "Taux d'attrition (churn) < 15% → Est-ce qu'on perd moins de clients ?")
bullet(doc, "NPS Omnicanal > 50 pts → Les clients recommandent-ils Carrefour ?")
bullet(doc, "Score CSAT post-achat > 4,2/5 → Sont-ils satisfaits après chaque achat ?")
bullet(doc, "Taux d'abandon panier web < 60% → Est-ce que le site convertit mieux ?")
bullet(doc, "Délai moyen Click & Collect < 2 heures → L'objectif logistique est-il atteint ?")

heading(doc, "Indicateurs commerciaux & performance cross-canal", level=2)
bullet(doc, "+20% Croissance ventes cross-canal → Les clients qui utilisent plusieurs canaux achètent-ils plus ?")
bullet(doc, "+30% CA Click & Collect → Le C&C génère-t-il plus de revenus ?")
bullet(doc, "+18% Panier moyen omnicanal vs mono-canal → Un client omnicanal dépense-t-il plus qu'un client mono-canal ?")
bullet(doc, "+40% ROI campagnes ciblées vs mass → La personnalisation est-elle plus rentable que le marketing de masse ?")
bullet(doc, "> 15% Taux conversion Scan & Go → Les clients qui scannent en magasin achètent-ils plus ?")
bullet(doc, "> 28% Taux d'ouverture emails personnalisés → Les emails ciblés sont-ils lus ?")

tip(doc, "Message clé des KPIs : Chaque chiffre est une cible à atteindre, pas juste un rêve. Le suivi mensuel permet de corriger la trajectoire rapidement si nécessaire.")

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# SECTION 06 — QUE FAIRE EN CAS D'ÉCHEC ?
# ═══════════════════════════════════════════════════════════
heading(doc, "6. QUE FAIRE EN CAS DE NON FONCTIONNEMENT ?", level=1, color=(180,0,0))
body(doc, "Cette section répond à la question : 'Et si ça ne marche pas ?' C'est une marque de maturité stratégique d'anticiper les échecs. Les meilleurs plans incluent toujours un plan B.")

heading(doc, "6.1 Les 6 risques principaux identifiés", level=2)

risques_data = [
    ("Faible adoption de l'app Carrefour+", "Moyenne", "Élevé", "Si le taux d'utilisation reste sous 20% après 3 mois de lancement"),
    ("Délais Click & Collect non respectés", "Élevée", "Élevé", "Si le délai moyen dépasse 2h sur plus de 30% des commandes"),
    ("Résistance des équipes en magasin", "Moyenne", "Moyen", "Si le NPS interne est inférieur à 30 sur l'adoption des outils"),
    ("Silos de données persistants (CDP)", "Faible", "Très élevé", "Si la CDP n'est pas opérationnelle à M3 comme prévu"),
    ("Concurrence agressive", "Élevée", "Moyen", "Si Carrefour perd plus de 2% de part de marché en 6 mois"),
    ("Budget dépassé ou retard de déploiement", "Moyenne", "Élevé", "Si le dépassement budgétaire dépasse 15%"),
]

for risque, prob, impact, signal in risques_data:
    p = doc.add_paragraph()
    r1 = p.add_run(f"• {risque} ")
    r1.bold = True
    r1.font.size = Pt(11)
    r2 = p.add_run(f"[Probabilité : {prob} | Impact : {impact}]")
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(100, 100, 100)
    r2.font.italic = True
    p2 = doc.add_paragraph()
    p2.paragraph_format.left_indent = Inches(0.4)
    r3 = p2.add_run(f"Signal d'alerte : {signal}")
    r3.font.size = Pt(10)
    r3.font.color.rgb = RGBColor(180, 80, 0)

doc.add_paragraph("")

heading(doc, "6.2 Les mesures correctives (Plan B)", level=2)

heading(doc, "Si l'app n'est pas adoptée :", level=3)
bullet(doc, "Campagne de communication en magasin (affichage + caissiers ambassadeurs formés)")
bullet(doc, "Offre de bienvenue : -10% sur la 1ère commande via app pour les non-utilisateurs")
bullet(doc, "Refonte UX de l'onboarding pour simplifier la prise en main")
bullet(doc, "Analyse des barrières à l'adoption via enquêtes clients")

heading(doc, "Si les délais Click & Collect ne sont pas respectés :", level=3)
bullet(doc, "Renforcement des équipes de préparation aux heures de pointe")
bullet(doc, "Révision des créneaux de commande disponibles (limiter les créneaux si capacité insuffisante)")
bullet(doc, "Partenariat avec un prestataire logistique externe en backup")
bullet(doc, "Mise en place d'un système de priorisation des commandes urgentes")

heading(doc, "Si la CDP n'est pas opérationnelle à temps :", level=3)
bullet(doc, "Utilisation temporaire des données CRM existantes (Salesforce) en attendant")
bullet(doc, "Report de la Phase 2 (Activation digitale) de 1 mois maximum")
bullet(doc, "Audit technique immédiat et recrutement d'un intégrateur externe spécialisé")

heading(doc, "Si les équipes résistent au changement :", level=3)
bullet(doc, "Programme de formation accéléré (e-learning + ateliers pratiques en magasin)")
bullet(doc, "Désignation d'ambassadeurs digitaux dans chaque hypermarché pilote")
bullet(doc, "Incentives liés à l'adoption des outils (prime trimestrielle pour les équipes performantes)")
bullet(doc, "Communication interne renforcée sur les bénéfices concrets pour les employés")

doc.add_paragraph("")

heading(doc, "6.3 La gouvernance — Qui décide quoi ?", level=2)
body(doc, "Pour que le plan de contingence fonctionne, il faut une gouvernance claire :")

bullet(doc, "Comité de pilotage mensuel : revue complète des KPIs vs objectifs, présence DSI + Directeur e-commerce + DG")
bullet(doc, "Seuils d'alerte automatiques : si un KPI dépasse le seuil → réunion de crise déclenchée sous 72h")
bullet(doc, "Responsable par axe : Data/CDP → DSI | App & digital → Directeur e-commerce | Expérience magasin → Directeurs régionaux")
bullet(doc, "Tableau de bord temps réel (Tableau/Looker) accessible à tous les responsables d'axe")
bullet(doc, "Rapport trimestriel au CODIR avec recommandations d'ajustement et décisions prises")

doc.add_paragraph("")

heading(doc, "6.4 Le processus de révision stratégique", level=2)
bullet(doc, "M3 : Bilan Phase 1 (Fondations data) — CDP opérationnelle ? Données unifiées ?")
bullet(doc, "M6 : Bilan Phase 2 (Activation digitale) — App adoptée ? Premières campagnes personnalisées lancées ?")
bullet(doc, "M9 : Bilan Phase 3 (Optimisation parcours) — C&C < 2h généralisé ? Scan & Go déployé dans 200 magasins ?")
bullet(doc, "M12 : Bilan annuel complet + définition de la roadmap 2027 + présentation CODIR & parties prenantes")

tip(doc, "À l'oral : 'Cette section prouve qu'on ne présente pas une stratégie naïve. On a réfléchi à ce qui pourrait mal se passer et on a des réponses concrètes pour chaque scénario.'")

doc.add_paragraph("")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════
# CONCLUSION GÉNÉRALE
# ═══════════════════════════════════════════════════════════
heading(doc, "7. CONCLUSION — Les 3 convictions pour réussir", level=1, color=(180,0,0))

body(doc, "La présentation se conclut sur 3 principes fondamentaux qui résument toute la stratégie :")

doc.add_paragraph("")

p = doc.add_paragraph()
r = p.add_run("01 — Unifier la donnée")
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = RGBColor(13, 27, 62)
body(doc, "Sans vue 360° client, aucune personnalisation n'est possible. Tant que les données de l'app, du magasin et du site web ne se parlent pas, Carrefour ne peut pas offrir une vraie expérience omnicanale. La CDP est donc le fondement de toute la stratégie, pas juste un outil parmi d'autres.")

doc.add_paragraph("")

p = doc.add_paragraph()
r = p.add_run("02 — Supprimer les frictions")
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = RGBColor(13, 27, 62)
body(doc, "Les clients omnicanaux achètent +18% et restent plus longtemps. Chaque friction (temps d'attente, incohérence de prix, application compliquée) est une raison de partir chez un concurrent. L'objectif n'est pas d'avoir le plus d'outils, mais d'avoir les bons outils parfaitement intégrés.")

doc.add_paragraph("")

p = doc.add_paragraph()
r = p.add_run("03 — Récompenser partout")
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = RGBColor(13, 27, 62)
body(doc, "Un programme fidélité omnicanal est le levier de rétention n°1. Paul doit gagner des points qu'il achète en magasin, via l'app, en Drive ou en livraison. Si les points ne sont crédités que dans un canal, le programme perd son sens et son efficacité.")

doc.add_paragraph("")

heading(doc, "Le message final à retenir pour ta présentation :", level=2)
body(doc, "Carrefour a tous les atouts : le réseau, les clients, l'app, le programme fidélité. Il manque LA COHÉRENCE entre ces éléments. La stratégie omnicanale n'est pas une révolution, c'est une unification intelligente de ce qui existe déjà.")

tip(doc, "Commence ta présentation par : 'Carrefour n'a pas un problème de moyens. Il a un problème de connexion.' Ça capte l'attention immédiatement.")

doc.add_paragraph("")
separator(doc)

footer = doc.add_paragraph("Document préparé pour le Cas Pratique 2 — Stratégie Omnicanale 2025-2026 | Carrefour — Grande Distribution")
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.runs[0].font.size = Pt(9)
footer.runs[0].font.color.rgb = RGBColor(120, 120, 120)

# Sauvegarde
output = "/home/user/rbconsulting.github.io/Guide_Presentation_Carrefour_Rodrin.docx"
doc.save(output)
print(f"Fichier généré : {output}")
