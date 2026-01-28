# Exemples de Questions pour Fabric Data Agent (Scénario Marketing)

## 🎯 Objectif

Ce document fournit **20 exemples de questions** avec les **réponses attendues** pour tester et valider le Fabric Data Agent dans le contexte Customer 360 + CRM + Marketing Campaigns + Commerce.

Chaque exemple inclut :
- La question posée
- La réponse attendue (format et contenu)
- Les tables utilisées
- Le type de visualisation suggéré

---

## 📊 Catégorie 1 : Exploration Simple (5 questions)

### 1. Combien de clients avons-nous au total ?

**Réponse attendue** :
> 20 000 clients au total.
> 
> *Source : table `crm_customers`*

**Tables** : `crm_customers`  
**Visualisation** : Card/KPI  
**Complexité** : ⭐ (très simple)

---

### 2. Quelle est la répartition des clients par étape du cycle de vie ?

**Réponse attendue** :
> Répartition par lifecycle_stage :
> - Active : 10 000 clients (50%)
> - Prospect : 4 000 clients (20%)
> - Lead : 3 000 clients (15%)
> - At Risk : 2 000 clients (10%)
> - Churned : 1 000 clients (5%)
> 
> *Source : table `crm_customers`, colonne `lifecycle_stage`*

**Tables** : `crm_customers`  
**Visualisation** : Funnel chart ou Donut chart  
**Complexité** : ⭐ (simple)

---

### 3. Combien de campagnes marketing avons-nous lancées ?

**Réponse attendue** :
> 20 campagnes marketing au total.
> 
> Répartition par objectif :
> - Acquisition : 5 campagnes
> - Retention : 6 campagnes
> - Upsell : 4 campagnes
> - Winback : 3 campagnes
> - Engagement : 2 campagnes
> 
> *Source : table `marketing_campaigns`*

**Tables** : `marketing_campaigns`  
**Visualisation** : Bar chart horizontal  
**Complexité** : ⭐ (simple)

---

### 4. Combien de commandes avons-nous traitées au total ?

**Réponse attendue** :
> 60 000 commandes sur la période.
> 
> *Source : table `orders`*

**Tables** : `orders`  
**Visualisation** : Card/KPI  
**Complexité** : ⭐ (simple)

---

### 5. Combien de segments clients avons-nous définis ?

**Réponse attendue** :
> 40 segments clients actifs.
> 
> Exemples de segments :
> - High Value
> - Frequent Buyers
> - At Risk
> - Email Engagers
> - VIP
> - New Customers
> 
> *Source : table `crm_segments`*

**Tables** : `crm_segments`  
**Visualisation** : Card/KPI + Table  
**Complexité** : ⭐ (simple)

---

## 💰 Catégorie 2 : Métriques Commerce (5 questions)

### 6. Quel est le chiffre d'affaires total généré ?

**Réponse attendue** :
> Chiffre d'affaires total : **~12 millions €**
> 
> Calculé comme : SUM(quantity × unit_price × (1 - discount)) depuis `order_lines`.
> 
> *Source : table `order_lines`*

**Tables** : `order_lines`  
**Visualisation** : Card/KPI  
**Complexité** : ⭐⭐ (calcul multi-colonnes)

---

### 7. Quel est le panier moyen par commande ?

**Réponse attendue** :
> Panier moyen : **~200€** par commande.
> 
> Calculé comme : Total revenue (12M€) / Nombre de commandes (60 000).
> 
> *Source : tables `orders` et `order_lines`*

**Tables** : `orders`, `order_lines`  
**Visualisation** : Card/KPI  
**Complexité** : ⭐⭐ (jointure + division)

---

### 8. Quels sont les 5 produits les plus vendus en quantité ?

**Réponse attendue** :
> Top 5 produits les plus vendus :
> 1. Produit A (PROD_00001) : 3 456 unités
> 2. Produit B (PROD_00015) : 2 987 unités
> 3. Produit C (PROD_00032) : 2 543 unités
> 4. Produit D (PROD_00048) : 2 198 unités
> 5. Produit E (PROD_00067) : 1 876 unités
> 
> *Source : jointure `products` et `order_lines`, agrégation par produit, tri DESC*

**Tables** : `products`, `order_lines`  
**Visualisation** : Bar chart horizontal  
**Complexité** : ⭐⭐ (jointure + tri)

---

### 9. Quel est le taux de retour des commandes ?

**Réponse attendue** :
> Taux de retour : **16.7%** (10 000 retours sur 60 000 commandes).
> 
> Distribution par raison :
> - Défectueux : 4 000 (40%)
> - Mauvaise taille : 2 500 (25%)
> - Changement d'avis : 2 000 (20%)
> - Autre : 1 500 (15%)
> 
> *Source : tables `returns` et `orders`*

**Tables** : `returns`, `orders`  
**Visualisation** : Donut chart  
**Complexité** : ⭐⭐ (filtre + pourcentage)

---

### 10. Quelle est l'évolution du chiffre d'affaires par mois ?

**Réponse attendue** :
> Évolution mensuelle du CA :
> - Janvier 2025 : 850 K€
> - Février 2025 : 920 K€
> - Mars 2025 : 1 050 K€
> - Avril 2025 : 980 K€
> - Mai 2025 : 1 100 K€
> - Juin 2025 : 1 150 K€
> - Juillet 2025 : 1 050 K€
> - Août 2025 : 1 020 K€
> - Septembre 2025 : 1 180 K€
> - Octobre 2025 : 1 250 K€
> - Novembre 2025 : 1 450 K€ (Black Friday)
> - Décembre 2025 : 1 520 K€ (Noël)
> 
> *Tendance : Hausse progressive avec pics saisonniers.*
> 
> *Source : `order_lines` jointure `orders`, agrégation par mois*

**Tables** : `orders`, `order_lines`  
**Visualisation** : Line chart  
**Complexité** : ⭐⭐⭐ (temporalité + agrégation)

---

## 📧 Catégorie 3 : Performance Marketing (5 questions)

### 11. Combien d'emails avons-nous envoyés au total ?

**Réponse attendue** :
> **200 000 envois d'emails** au total.
> 
> *Source : table `marketing_sends`*

**Tables** : `marketing_sends`  
**Visualisation** : Card/KPI  
**Complexité** : ⭐ (simple)

---

### 12. Quel est le taux d'ouverture moyen des emails ?

**Réponse attendue** :
> Taux d'ouverture moyen : **22%**
> 
> 44 000 opens sur 200 000 sends.
> 
> Variation par type de campagne :
> - Retention : 28% (le plus élevé)
> - Acquisition : 20%
> - Upsell : 24%
> - Winback : 18%
> - Engagement : 26%
> 
> *Source : tables `marketing_sends` et `marketing_events` (filtre event_type='open')*

**Tables** : `marketing_sends`, `marketing_events`  
**Visualisation** : Gauge + Bar chart  
**Complexité** : ⭐⭐⭐ (jointure + pourcentage + groupby)

---

### 13. Quel est le taux de clic moyen des emails ?

**Réponse attendue** :
> Taux de clic moyen : **8%**
> 
> 16 000 clicks sur 200 000 sends.
> 
> Variation par objectif :
> - Upsell : 10% (meilleur taux)
> - Retention : 9%
> - Engagement : 8%
> - Acquisition : 7%
> - Winback : 6%
> 
> *Source : tables `marketing_sends` et `marketing_events` (filtre event_type='click')*

**Tables** : `marketing_sends`, `marketing_events`  
**Visualisation** : Gauge + Bar chart  
**Complexité** : ⭐⭐⭐ (jointure + pourcentage + groupby)

---

### 14. Quel est le taux de bounce et de désinscription ?

**Réponse attendue** :
> **Taux de bounce** : 4% (8 000 bounces sur 200 000 sends)
> 
> **Taux de désinscription** : 1% (2 000 unsubscribes sur 200 000 sends)
> 
> Distribution des bounces :
> - Hard bounce : 60%
> - Soft bounce : 40%
> 
> *Source : table `marketing_events` (filtres event_type='bounce' et 'unsubscribe')*

**Tables** : `marketing_events`, `marketing_sends`  
**Visualisation** : Cards + Donut chart  
**Complexité** : ⭐⭐ (filtres + pourcentages)

---

### 15. Quelle campagne a le meilleur taux d'engagement (open + click) ?

**Réponse attendue** :
> Top 5 campagnes par engagement :
> 
> 1. **"Retour Client VIP"** (CAMP_008) : 38% engagement (30% open, 8% click)
> 2. **"Offre Exclusive"** (CAMP_015) : 35% engagement
> 3. **"Welcome New Year"** (CAMP_001) : 33% engagement
> 4. **"Flash Sale 48h"** (CAMP_012) : 31% engagement
> 5. **"Recommandations Perso"** (CAMP_007) : 29% engagement
> 
> *Source : `marketing_campaigns` jointure `marketing_sends` et `marketing_events`*

**Tables** : `marketing_campaigns`, `marketing_sends`, `marketing_events`  
**Visualisation** : Bar chart horizontal  
**Complexité** : ⭐⭐⭐⭐ (jointures multiples + calculs)

---

## 🎯 Catégorie 4 : CRM & Customer 360 (5 questions)

### 16. Quelle est la CLV (Customer Lifetime Value) moyenne ?

**Réponse attendue** :
> CLV moyenne : **950€** par client.
> 
> Variation par segment :
> - High Value : 3 200€
> - VIP : 2 800€
> - Frequent Buyers : 1 500€
> - Active : 800€
> - At Risk : 600€
> 
> *Source : table `crm_customer_profile`, colonne `clv_score`*

**Tables** : `crm_customer_profile`, `crm_customer_segments`, `crm_segments`  
**Visualisation** : Card + Bar chart  
**Complexité** : ⭐⭐ (moyenne + jointure)

---

### 17. Quel est le taux de churn actuel ?

**Réponse attendue** :
> Taux de churn : **5%** (1 000 clients churned sur 20 000).
> 
> Évolution du churn par mois :
> - Janvier 2025 : 3%
> - Février 2025 : 4%
> - Mars 2025 : 5%
> - Avril 2025 : 6% (pic)
> - Mai 2025 : 5%
> - Juin 2025 : 4%
> 
> *Action : Campagne winback lancée en avril a réduit le churn.*
> 
> *Source : table `crm_customers`, colonne `status`*

**Tables** : `crm_customers`  
**Visualisation** : Gauge + Line chart  
**Complexité** : ⭐⭐⭐ (pourcentage + évolution temporelle)

---

### 18. Quel est le score NPS moyen de nos clients ?

**Réponse attendue** :
> Score NPS moyen : **7.2/10**
> 
> Distribution :
> - Promoters (9-10) : 35%
> - Passives (7-8) : 45%
> - Detractors (0-6) : 20%
> 
> **Net Promoter Score** : +15% (35% - 20%)
> 
> *Source : table `crm_customer_profile`, colonne `nps_last`*

**Tables** : `crm_customer_profile`  
**Visualisation** : Gauge + Donut chart  
**Complexité** : ⭐⭐⭐ (calcul NPS + distribution)

---

### 19. Quels clients ont un risque de churn élevé (score > 70) ?

**Réponse attendue** :
> **1 200 clients** ont un churn risk score > 70.
> 
> Profil type :
> - Segment : 40% "At Risk", 30% "Active", 20% "Frequent Buyers", 10% autres
> - CLV moyenne : 1 100€ (au-dessus de la moyenne !)
> - NPS moyen : 5.8/10
> - Dernière commande : >90 jours en moyenne
> - Taux d'ouverture email : <10%
> 
> ⚠️ **Action recommandée** : Campagne de rétention urgente (budget suggéré : 25 000€).
> 
> *Source : table `crm_customer_profile`, filtre `churn_risk_score > 70`*

**Tables** : `crm_customer_profile`, `crm_customer_segments`, `crm_segments`  
**Visualisation** : Card + Table avec alerte  
**Complexité** : ⭐⭐⭐⭐ (filtre + profiling)

---

### 20. Combien de clients sont dans plusieurs segments simultanément ?

**Réponse attendue** :
> **15 000 clients** sont dans plusieurs segments (75% des clients).
> 
> Distribution :
> - 1 segment : 5 000 clients (25%)
> - 2 segments : 7 000 clients (35%)
> - 3 segments : 5 500 clients (27.5%)
> - 4+ segments : 2 500 clients (12.5%)
> 
> *Cela démontre la richesse de la segmentation pour ciblage marketing.*
> 
> *Source : table `crm_customer_segments`, agrégation par customer_id*

**Tables** : `crm_customer_segments`, `crm_customers`  
**Visualisation** : Bar chart  
**Complexité** : ⭐⭐⭐ (agrégation + groupby)

---

## 🔗 Catégorie 5 : Attribution Marketing & ROI (5 questions avancées)

### 21. Quel est le ROI marketing global ?

**Réponse attendue** :
> **ROI Marketing global** : **+285%**
> 
> Budget marketing total : 240 000€
> Revenue attribué au marketing : 925 000€
> Profit net : 685 000€
> 
> ROI = (925 000 - 240 000) / 240 000 = +285%
> 
> *Source : table `marketing_campaigns` (budget) et `orders` (attribution_source='marketing')*

**Tables** : `marketing_campaigns`, `orders`, `order_lines`  
**Visualisation** : Card + Waterfall chart  
**Complexité** : ⭐⭐⭐⭐ (calcul ROI + attribution)

---

### 22. Quelle campagne a généré le plus de revenu ?

**Réponse attendue** :
> Top 5 campagnes par revenu attribué (last-touch) :
> 
> 1. **"Black Friday 2025"** (CAMP_014) : 185 000€ revenue, 25 000€ budget → **ROI +640%**
> 2. **"Welcome New Year"** (CAMP_001) : 95 000€ revenue, 15 000€ budget → **ROI +533%**
> 3. **"VIP Exclusive"** (CAMP_008) : 78 000€ revenue, 8 000€ budget → **ROI +875%** 🏆
> 4. **"Retour Client At Risk"** (CAMP_011) : 72 000€ revenue, 12 000€ budget → **ROI +500%**
> 5. **"Flash Sale 48h"** (CAMP_012) : 65 000€ revenue, 10 000€ budget → **ROI +550%**
> 
> *Note : CAMP_008 a le meilleur ROI mais volume plus faible (ciblage VIP).*
> 
> *Source : `orders` (filtre attribution_campaign_id) jointure `marketing_campaigns`*

**Tables** : `marketing_campaigns`, `orders`, `order_lines`  
**Visualisation** : Table avec tri + highlight  
**Complexité** : ⭐⭐⭐⭐⭐ (attribution + calculs multiples)

---

### 23. Quels segments sont les plus rentables pour le marketing ?

**Réponse attendue** :
> Top 5 segments par ROI marketing :
> 
> 1. **VIP** : ROI +920% (petit volume, très réactifs)
> 2. **High Value** : ROI +680%
> 3. **Frequent Buyers** : ROI +450%
> 4. **Email Engagers** : ROI +380%
> 5. **At Risk** : ROI +250% (campagnes de rétention efficaces)
> 
> *Insight : Les segments "premium" ont le meilleur ROI mais représentent 20% du volume. Les segments "at risk" offrent un bon équilibre volume/ROI.*
> 
> *Source : `crm_segments` → `marketing_audiences` → `marketing_sends` → `orders` (attribution)*

**Tables** : `crm_segments`, `marketing_audiences`, `marketing_sends`, `orders`, `order_lines`  
**Visualisation** : Scatter plot (Volume vs ROI)  
**Complexité** : ⭐⭐⭐⭐⭐ (jointures multiples + calcul ROI par segment)

---

### 24. Les tests A/B ont-ils un impact significatif ?

**Réponse attendue** :
> **Oui**, les tests A/B augmentent les performances de **+30% en moyenne**.
> 
> Campagnes avec A/B test (10 campagnes) :
> - Open rate moyen : 26%
> - Click rate moyen : 10%
> - Conversion rate : 3.2%
> 
> Campagnes sans A/B test (10 campagnes) :
> - Open rate moyen : 20%
> - Click rate moyen : 7%
> - Conversion rate : 2.1%
> 
> **Recommandation** : Systématiser les tests A/B pour toutes les campagnes acquisition et upsell.
> 
> *Source : table `marketing_campaigns` (filtre ab_test_flag), jointure `marketing_sends` et `marketing_events`*

**Tables** : `marketing_campaigns`, `marketing_sends`, `marketing_events`, `orders`  
**Visualisation** : Comparison bar chart  
**Complexité** : ⭐⭐⭐⭐ (segmentation + comparaison)

---

### 25. Quel est le délai moyen entre un clic email et une commande ?

**Réponse attendue** :
> Délai moyen : **2.5 jours** entre le clic et la commande.
> 
> Distribution :
> - <1 heure : 15% (achat impulsif)
> - 1-24 heures : 35%
> - 1-3 jours : 30%
> - 4-7 jours : 15%
> - >7 jours : 5%
> 
> *Insight : 50% des conversions se font dans les 24h. Fenêtre d'attribution de 7 jours capture 95% des conversions.*
> 
> *Source : `marketing_events` (filtre click) jointure `orders`, calcul DATEDIFF*

**Tables** : `marketing_events`, `marketing_sends`, `orders`  
**Visualisation** : Histogram  
**Complexité** : ⭐⭐⭐⭐⭐ (jointure temporelle complexe)

---

## 🎯 Questions Bonus (pour aller plus loin)

### B1. Quels clients ont cliqué sur un email mais n'ont jamais acheté ?

**Réponse attendue** :
> **850 clients** ont cliqué sur un email mais n'ont jamais commandé.
> 
> Profil type :
> - Lifecycle stage : 70% "lead", 20% "prospect", 10% "active"
> - Segment principal : "Email Engagers" (mais pas "Buyers")
> - Nombre moyen de clics : 3.2
> - CLV prédictive : 0€ (pas encore convertis)
> 
> **Action recommandée** : Campagne de conversion avec offre spéciale première commande (-20% + livraison gratuite).
> 
> *Source : `marketing_events` (clicks) exclusion jointure avec `orders`*

**Tables** : `marketing_events`, `marketing_sends`, `crm_customers`, `orders`  
**Visualisation** : Table + Donut (segments)  
**Complexité** : ⭐⭐⭐⭐⭐ (anti-join)

---

### B2. Affiche l'évolution du taux de conversion par mois

**Réponse attendue** :
> [Graphique line chart avec évolution mensuelle]
> 
> Tendance : Le taux de conversion augmente progressivement grâce à l'amélioration des campagnes (A/B testing, ciblage).
> 
> - Janvier 2025 : 1.8%
> - Février 2025 : 2.0%
> - Mars 2025 : 2.3%
> - Avril 2025 : 2.5%
> - Mai 2025 : 2.7%
> - Juin 2025 : 2.9%
> - Juillet 2025 : 2.8%
> - Août 2025 : 3.0%
> - Septembre 2025 : 3.2%
> - Octobre 2025 : 3.4%
> - Novembre 2025 : 4.1% (Black Friday)
> - Décembre 2025 : 4.3% (Noël)
> 
> *Source : `marketing_sends` jointure `orders`, agrégation par mois*

**Tables** : `marketing_sends`, `orders`  
**Visualisation** : Line chart  
**Complexité** : ⭐⭐⭐⭐ (temporalité + taux de conversion)

---

### B3. Quels clients VIP ont un NPS inférieur à 6 ?

**Réponse attendue** :
> **18 clients VIP** ont un NPS < 6 (insatisfaits).
> 
> Profil type :
> - CLV moyenne : 2 950€ (très élevée !)
> - Churn risk score moyen : 75 (élevé)
> - Dernière interaction : >60 jours
> - Principale raison d'insatisfaction (via interactions) : retards livraison (40%), qualité produit (35%)
> 
> ⚠️ **Alerte critique** : Risque de perdre 53 100€ de CLV (18 × 2 950€).
> 
> **Action urgente** : Contact personnalisé par Account Manager + geste commercial.
> 
> *Source : `crm_customer_segments` (segment VIP) jointure `crm_customer_profile` (filtre nps_last < 6)*

**Tables** : `crm_customer_segments`, `crm_segments`, `crm_customer_profile`, `crm_interactions`  
**Visualisation** : Table avec alerte rouge  
**Complexité** : ⭐⭐⭐⭐ (filtres multiples + calcul d'impact)

---

## 📋 Guide d'Utilisation

### Comment Tester ces Questions

1. **Ordre recommandé** : Commencer par les questions simples (catégorie 1), puis augmenter la complexité
2. **Validation** : Vérifier que la réponse est cohérente (chiffres dans les bons ordres de grandeur)
3. **Flexibilité** : Reformuler si la première tentative échoue (utiliser termes exacts des colonnes)
4. **Focus Marketing** : Les catégories 3 et 5 sont spécifiques au marketing et démontrent la valeur de Fabric pour les équipes Marketing

### Critères de Succès

| Niveau | Questions réussies | Commentaire |
|--------|-------------------|-------------|
| ⭐ Basic | 15+/25 | Fonctionnel pour démo |
| ⭐⭐ Good | 20+/25 | Très bon niveau |
| ⭐⭐⭐ Excellent | 23+/25 | Production-ready |

### Troubleshooting

| Problème | Solution |
|----------|----------|
| Réponse incorrecte | Vérifier les relations dans le Semantic Model (18 relations) |
| Timeout sur attribution | Filtrer sur période plus courte ou campagne spécifique |
| "Je ne peux pas répondre" | Reformuler avec termes exacts des colonnes |
| Graphique non généré | Demander explicitement "en graphique" ou "visualise" |
| ROI incorrect | Vérifier que les mesures DAX sont bien définies |

---

## 🎨 Variations de Questions (pour Improvisation)

Vous pouvez varier les questions en changeant :
- **La période** : "ce trimestre", "en novembre 2025", "depuis début 2025"
- **Le segment** : "clients VIP", "clients At Risk", "Email Engagers"
- **La campagne** : "campagne Black Friday", "campagnes de retention"
- **Le canal** : "par email" (focus de cette démo)
- **L'objectif** : "campagnes acquisition", "campagnes upsell"

**Exemple de variations** :
- "Quel est le ROI de la campagne Black Friday ?"
- "Combien de clients VIP ont cliqué sur un email ce mois-ci ?"
- "Quel est le taux de conversion des campagnes upsell ?"
- "Quels segments ont le meilleur engagement email ?"

---

## 🎯 Scénarios de Démo Recommandés

### Scénario 1 : "Prouver le ROI Marketing"
Questions à enchaîner : 21 → 22 → 23 → 24  
**Pitch** : Démontrer l'impact mesurable des campagnes marketing sur le business.

### Scénario 2 : "Identifier les clients à risque"
Questions à enchaîner : 17 → 19 → B3  
**Pitch** : Utiliser la data pour prévenir le churn des clients à haute valeur.

### Scénario 3 : "Optimiser les campagnes email"
Questions à enchaîner : 12 → 13 → 15 → 24  
**Pitch** : Améliorer l'engagement email grâce aux insights data.

### Scénario 4 : "Customer 360 complet"
Questions à enchaîner : 1 → 2 → 16 → 18 → 19  
**Pitch** : Vue holistique du client (CRM + comportement + risques).

---

*Ces 25 exemples couvrent l'ensemble des capacités attendues du Fabric Data Agent pour la démo Customer 360 + Marketing Campaigns.*

