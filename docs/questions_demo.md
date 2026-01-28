# Questions Démonstration - Fabric Data Agent (Customer 360 + Marketing)

Ces 15 questions sont conçues pour démontrer les capacités du Fabric Data Agent sur le dataset Customer 360.

---

## 📊 Level 1 : Questions Basiques (Comptes, Segments)

### Question 1 : "Combien de clients avons-nous ?"

**Réponse attendue** : 20 000 clients au total.

**Tables utilisées** : `crm_customers`

---

### Question 2 : "Quels sont les 5 segments les plus populaires ?"

**Réponse attendue** : Liste des segments par nombre de clients (ex: "Frequent Buyers", "High Value", "At Risk"...).

**Tables utilisées** : `crm_segments`, `crm_customer_segments`

---

### Question 3 : "Combien de campagnes ont été lancées cette année ?"

**Réponse attendue** : 20 campagnes au total.

**Tables utilisées** : `marketing_campaigns`

---

## 🎯 Level 2 : Attribution Marketing

### Question 4 : "Quel est le ROI moyen de nos campagnes marketing ?"

**Réponse attendue** : ROI calculé = (Revenue - Budget) / Budget. Environ +400-500%.

**Calcul** :
- Revenue attribué = SUM(orders WHERE attributed_campaign_id IS NOT NULL)
- Budget total = SUM(campaigns.budget_eur)

**Tables utilisées** : `marketing_campaigns`, `orders`

---

### Question 5 : "Quelle campagne a généré le plus de revenue ?"

**Réponse attendue** : Nom de la campagne + revenue total (ex: "Black Friday Campaign : 240 000 EUR").

**Tables utilisées** : `marketing_campaigns`, `orders` (jointure sur `attributed_campaign_id`)

---

### Question 6 : "Combien de commandes sont attribuables au marketing vs organic ?"

**Réponse attendue** :
- Attributed (campaign_id NOT NULL) : ~9% (5 500 commandes)
- Organic (campaign_id NULL) : ~91% (54 500 commandes)

**Tables utilisées** : `orders`

---

## 📧 Level 3 : Performance Email Marketing

### Question 7 : "Quel est le taux d'ouverture moyen de nos emails ?"

**Réponse attendue** : ~22% (open events / total sends).

**Calcul** :
- Opens = COUNT(marketing_events WHERE event_type = 'open')
- Sends = COUNT(marketing_sends)

**Tables utilisées** : `marketing_sends`, `marketing_events`

---

### Question 8 : "Quel est le click-through rate (CTR) ?"

**Réponse attendue** : ~8% (clicks / opens).

**Calcul** :
- Clicks = COUNT(marketing_events WHERE event_type = 'click')
- Opens = COUNT(marketing_events WHERE event_type = 'open')

**Tables utilisées** : `marketing_events`

---

### Question 9 : "Les A/B tests apportent-ils de la valeur ?"

**Réponse attendue** : Oui, variant B montre +5-30% d'amélioration sur open/click rates.

**Analyse** : Comparer performances des assets variant A vs B au sein des mêmes campagnes.

**Tables utilisées** : `marketing_assets`, `marketing_sends`, `marketing_events`

---

## 💰 Level 4 : CLV et Segmentation

### Question 10 : "Quel est le CLV moyen par segment ?"

**Réponse attendue** : Tableau segment_name → avg(clv_score).

**Exemples attendus** :
- VIP : 15 000 EUR
- High Value : 8 000 EUR
- Frequent Buyers : 3 500 EUR
- At Risk : 1 200 EUR

**Tables utilisées** : `crm_customer_profile`, `crm_customer_segments`, `crm_segments`

---

### Question 11 : "Quel segment a le meilleur taux de conversion post-campagne ?"

**Réponse attendue** : "Frequent Buyers" ou "High Value" (conversion ~15-18%).

**Calcul** :
- Pour chaque segment, compter customers avec attributed orders / customers ayant reçu sends

**Tables utilisées** : `crm_segments`, `crm_customer_segments`, `marketing_sends`, `orders`

---

### Question 12 : "Combien de clients sont à risque de churn ?"

**Réponse attendue** : ~4 000 clients (churn_risk_score > 60).

**Tables utilisées** : `crm_customer_profile`

---

## 📈 Level 5 : Impact Business

### Question 13 : "Quelle est la corrélation entre open rate et conversion ?"

**Réponse attendue** : Les clients avec open_rate > 30% ont une conversion 3-5× supérieure.

**Analyse** :
- Segmenter customers par tranche open_rate_pct
- Calculer conversion rate par tranche

**Tables utilisées** : `crm_customer_profile`, `orders`

---

### Question 14 : "Quel est le taux de retour des commandes attribuées aux campagnes ?"

**Réponse attendue** : ~15-17% (vs ~17% global).

**Calcul** :
- Returns sur orders avec attributed_campaign_id / total orders attributed

**Tables utilisées** : `returns`, `orders`

---

### Question 15 : "Les clients avec sentiment négatif achètent-ils moins ?"

**Réponse attendue** : Oui, conversion rate ~0.9% vs 14% pour sentiment positif.

**Analyse** : Croiser sentiment (extrait des customer_knowledge_notes via AI transform) avec total_orders.

**Tables utilisées** : `customer_knowledge_notes` (AI transformed), `crm_customer_profile`

---

## 🚀 Questions Bonus (Avancées)

### Bonus 1 : "Quel est le coût d'acquisition client (CAC) ?"

**Calcul** : Budget campagnes acquisition / Nombre nouveaux clients acquis

**Réponse attendue** : ~50-80 EUR/client.

---

### Bonus 2 : "Quelle est la lifetime value moyenne des clients acquis via campagne vs organic ?"

**Analyse** : Comparer CLV des customers avec first_order attribué vs non attribué.

**Réponse attendue** : Clients acquis via campagne ont CLV légèrement supérieure (+10-15%).

---

### Bonus 3 : "Quels produits sont les plus mentionnés dans les emails marketing ?"

**Analyse** : Extraction d'entités depuis email_bodies (AI transform).

**Réponse attendue** : Catégories "Electronics" et "Clothing" les plus mentionnées.

---

## ✅ Validation

Ces questions permettent de valider :
- ✅ Attribution marketing (last-touch)
- ✅ Segmentation client
- ✅ Performance campagnes (ROI, open/click rates)
- ✅ CLV et churn prediction
- ✅ A/B testing impact
- ✅ Sentiment analysis (via AI transforms)
- ✅ Corrélations CRM ↔ Marketing ↔ Commerce

---

*Ces questions sont à poser au Fabric Data Agent après configuration (voir `fabric_setup.md`).*
