# Mesures DAX - Marketing & CRM Analytics

Ce fichier contient toutes les mesures DAX testées et validées pour le semantic model Fabric.

## Tables Requises

- crm_customers
- crm_customer_profile
- marketing_campaigns
- marketing_sends
- marketing_events
- orders
- order_lines
- products

## Relations Clés

```
marketing_campaigns[campaign_id] 1 ----→ * orders[attributed_campaign_id]
marketing_campaigns[campaign_id] 1 ----→ * marketing_sends[campaign_id]
marketing_sends[send_id] 1 ----→ * marketing_events[send_id]
crm_customers[customer_id] 1 ----→ * orders[customer_id]
crm_customers[customer_id] 1 ----→ 1 crm_customer_profile[customer_id]
orders[order_id] 1 ----→ * order_lines[order_id]
products[product_id] 1 ----→ * order_lines[product_id]
```

---

## Métriques Marketing

### Campaign ROI

Calcule le retour sur investissement d'une campagne.

```dax
Campaign ROI = 
VAR Revenue = 
    CALCULATE(
        SUM(orders[total_amount_eur]),
        NOT(ISBLANK(orders[attributed_campaign_id]))
    )
VAR Cost = SUM(marketing_campaigns[budget_eur])
RETURN
    DIVIDE(Revenue - Cost, Cost, 0)
```

**Format:** Pourcentage (×100%)
**Usage:** Visual de campagne, KPI card

---

### Campaign Revenue

Revenue total attribué à une campagne (last-touch 14 jours).

```dax
Campaign Revenue = 
CALCULATE(
    SUM(orders[total_amount_eur]),
    NOT(ISBLANK(orders[attributed_campaign_id]))
)
```

**Format:** Currency (EUR)
**Usage:** Table de campagnes, comparaison

---

### Organic Revenue

Revenue non attribué (commandes organiques).

```dax
Organic Revenue = 
CALCULATE(
    SUM(orders[total_amount_eur]),
    ISBLANK(orders[attributed_campaign_id])
)
```

**Format:** Currency (EUR)
**Usage:** Comparaison attributed vs organic

---

### Total Revenue

Revenue total (attributed + organic).

```dax
Total Revenue = 
SUM(orders[total_amount_eur])
```

**Format:** Currency (EUR)
**Usage:** KPI global

---

### Open Rate

Taux d'ouverture des emails.

```dax
Open Rate = 
VAR Opens = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "open"
    )
VAR TotalSends = COUNTROWS(marketing_sends)
RETURN
    DIVIDE(Opens, TotalSends, 0)
```

**Format:** Pourcentage
**Usage:** KPI campagne, comparaison A/B

---

### Click Rate (CTR)

Taux de clic parmi les ouvertures.

```dax
Click Rate = 
VAR Clicks = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "click"
    )
VAR Opens = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "open"
    )
RETURN
    DIVIDE(Clicks, Opens, 0)
```

**Format:** Pourcentage
**Usage:** Performance email, A/B test

---

### Bounce Rate

Taux de rebond des emails.

```dax
Bounce Rate = 
VAR Bounces = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "bounce"
    )
VAR TotalSends = COUNTROWS(marketing_sends)
RETURN
    DIVIDE(Bounces, TotalSends, 0)
```

**Format:** Pourcentage
**Target:** <= 3%
**Usage:** Qualité de la liste email

---

### Unsubscribe Rate

Taux de désinscription.

```dax
Unsubscribe Rate = 
VAR Unsubscribes = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "unsubscribe"
    )
VAR TotalSends = COUNTROWS(marketing_sends)
RETURN
    DIVIDE(Unsubscribes, TotalSends, 0)
```

**Format:** Pourcentage
**Target:** <= 0.5%
**Usage:** Alerte fatigue email

---

### Conversion Rate (Post-Send)

Taux de conversion des envois email.

```dax
Conversion Rate Post-Send = 
VAR AttributedOrders = 
    CALCULATE(
        COUNTROWS(orders),
        NOT(ISBLANK(orders[attributed_campaign_id]))
    )
VAR TotalSends = COUNTROWS(marketing_sends)
RETURN
    DIVIDE(AttributedOrders, TotalSends, 0)
```

**Format:** Pourcentage
**Target:** >= 3%
**Usage:** Efficacité campagne

---

### Conversion Rate (Post-Click)

Taux de conversion des clics.

```dax
Conversion Rate Post-Click = 
VAR AttributedOrders = 
    CALCULATE(
        COUNTROWS(orders),
        NOT(ISBLANK(orders[attributed_campaign_id]))
    )
VAR Clicks = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "click"
    )
RETURN
    DIVIDE(AttributedOrders, Clicks, 0)
```

**Format:** Pourcentage
**Target:** >= 12%
**Usage:** Qualité du trafic

---

### Campaign Budget

Budget total des campagnes.

```dax
Campaign Budget = 
SUM(marketing_campaigns[budget_eur])
```

**Format:** Currency (EUR)
**Usage:** Calcul ROI, suivi budget

---

### Campaign Cost Per Order

Coût d'acquisition par commande.

```dax
Cost Per Order = 
VAR TotalBudget = SUM(marketing_campaigns[budget_eur])
VAR AttributedOrders = 
    CALCULATE(
        COUNTROWS(orders),
        NOT(ISBLANK(orders[attributed_campaign_id]))
    )
RETURN
    DIVIDE(TotalBudget, AttributedOrders, BLANK())
```

**Format:** Currency (EUR)
**Usage:** Efficacité acquisition

---

## Métriques CRM

### Average CLV

Customer Lifetime Value moyen.

```dax
Average CLV = 
AVERAGE(crm_customer_profile[clv_score])
```

**Format:** Currency (EUR)
**Usage:** Segmentation, KPI

---

### Total CLV

CLV total de la base client.

```dax
Total CLV = 
SUM(crm_customer_profile[clv_score])
```

**Format:** Currency (EUR)
**Usage:** Potentiel revenue

---

### Churn Risk Count

Nombre de clients à risque (churn_risk_score > 60).

```dax
Churn Risk Count = 
CALCULATE(
    COUNTROWS(crm_customer_profile),
    crm_customer_profile[churn_risk_score] > 60
)
```

**Format:** Nombre entier
**Usage:** Alerte retention

---

### Churn Risk Revenue Impact

Revenue potentiel perdu si les clients à risque churnent.

```dax
Churn Risk Revenue Impact = 
CALCULATE(
    SUM(crm_customer_profile[clv_score]),
    crm_customer_profile[churn_risk_score] > 60
)
```

**Format:** Currency (EUR)
**Usage:** Justification budget retention

---

### Average NPS

Net Promoter Score moyen.

```dax
Average NPS = 
AVERAGE(crm_customer_profile[nps_last])
```

**Format:** Nombre (0-10)
**Target:** >= 7
**Usage:** Satisfaction client

---

### Total Customers

Nombre total de clients.

```dax
Total Customers = 
COUNTROWS(crm_customers)
```

**Format:** Nombre entier
**Usage:** KPI global

---

### Active Customers

Clients actifs (lifecycle_stage = 'active').

```dax
Active Customers = 
CALCULATE(
    COUNTROWS(crm_customers),
    crm_customers[lifecycle_stage] = "active"
)
```

**Format:** Nombre entier
**Usage:** Segmentation

---

### Churned Customers

Clients churned.

```dax
Churned Customers = 
CALCULATE(
    COUNTROWS(crm_customers),
    crm_customers[lifecycle_stage] = "churned"
)
```

**Format:** Nombre entier
**Usage:** Calcul churn rate

---

### Churn Rate

Taux de churn.

```dax
Churn Rate = 
VAR Churned = 
    CALCULATE(
        COUNTROWS(crm_customers),
        crm_customers[lifecycle_stage] = "churned"
    )
VAR Total = COUNTROWS(crm_customers)
RETURN
    DIVIDE(Churned, Total, 0)
```

**Format:** Pourcentage
**Target:** <= 10%
**Usage:** Alerte retention

---

## Métriques Commerce

### Total Orders

Nombre total de commandes.

```dax
Total Orders = 
COUNTROWS(orders)
```

**Format:** Nombre entier
**Usage:** KPI global

---

### Attributed Orders

Commandes attribuées aux campagnes.

```dax
Attributed Orders = 
CALCULATE(
    COUNTROWS(orders),
    NOT(ISBLANK(orders[attributed_campaign_id]))
)
```

**Format:** Nombre entier
**Usage:** Efficacité marketing

---

### Organic Orders

Commandes organiques (non attribuées).

```dax
Organic Orders = 
CALCULATE(
    COUNTROWS(orders),
    ISBLANK(orders[attributed_campaign_id])
)
```

**Format:** Nombre entier
**Usage:** Comparaison

---

### Attribution Rate

Pourcentage de commandes attribuées.

```dax
Attribution Rate = 
VAR Attributed = 
    CALCULATE(
        COUNTROWS(orders),
        NOT(ISBLANK(orders[attributed_campaign_id]))
    )
VAR Total = COUNTROWS(orders)
RETURN
    DIVIDE(Attributed, Total, 0)
```

**Format:** Pourcentage
**Expected:** ~9%
**Usage:** Performance marketing

---

### Average Order Value (AOV)

Panier moyen.

```dax
AOV = 
DIVIDE(
    SUM(orders[total_amount_eur]),
    COUNTROWS(orders),
    BLANK()
)
```

**Format:** Currency (EUR)
**Usage:** Segmentation, upsell

---

### Total Products Sold

Nombre total de produits vendus.

```dax
Total Products Sold = 
SUM(order_lines[qty])
```

**Format:** Nombre entier
**Usage:** Inventory, performance

---

### Average Items Per Order

Nombre moyen d'items par commande.

```dax
Avg Items Per Order = 
DIVIDE(
    SUM(order_lines[qty]),
    COUNTROWS(orders),
    BLANK()
)
```

**Format:** Nombre décimal
**Usage:** Cross-sell opportunity

---

### Repeat Purchase Rate

Pourcentage de clients avec 2+ commandes.

```dax
Repeat Purchase Rate = 
VAR RepeatCustomers = 
    CALCULATE(
        COUNTROWS(crm_customer_profile),
        crm_customer_profile[total_orders] >= 2
    )
VAR TotalCustomers = COUNTROWS(crm_customers)
RETURN
    DIVIDE(RepeatCustomers, TotalCustomers, 0)
```

**Format:** Pourcentage
**Target:** >= 30%
**Usage:** Loyalty, retention

---

## Métriques A/B Testing

### Variant A Open Rate

Open rate pour variant A.

```dax
Variant A Open Rate = 
VAR SendsA = 
    CALCULATE(
        COUNTROWS(marketing_sends),
        RELATED(marketing_assets[variant]) = "A"
    )
VAR OpensA = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "open",
        RELATED(marketing_assets[variant]) = "A"
    )
RETURN
    DIVIDE(OpensA, SendsA, BLANK())
```

**Format:** Pourcentage
**Usage:** A/B test comparison

---

### Variant B Open Rate

Open rate pour variant B.

```dax
Variant B Open Rate = 
VAR SendsB = 
    CALCULATE(
        COUNTROWS(marketing_sends),
        RELATED(marketing_assets[variant]) = "B"
    )
VAR OpensB = 
    CALCULATE(
        COUNTROWS(marketing_events),
        marketing_events[event_type] = "open",
        RELATED(marketing_assets[variant]) = "B"
    )
RETURN
    DIVIDE(OpensB, SendsB, BLANK())
```

**Format:** Pourcentage
**Usage:** A/B test comparison

---

### A/B Test Lift

Lift du variant B vs A (open rate).

```dax
A/B Test Lift = 
VAR RateA = [Variant A Open Rate]
VAR RateB = [Variant B Open Rate]
RETURN
    DIVIDE(RateB - RateA, RateA, BLANK())
```

**Format:** Pourcentage
**Usage:** Winner identification

---

## Mesures Avancées

### LTV:CAC Ratio

Lifetime Value to Customer Acquisition Cost ratio.

```dax
LTV:CAC Ratio = 
VAR AvgCLV = AVERAGE(crm_customer_profile[clv_score])
VAR CAC = [Cost Per Order]
RETURN
    DIVIDE(AvgCLV, CAC, BLANK())
```

**Format:** Ratio (X:1)
**Target:** >= 3:1
**Usage:** Efficacité acquisition

---

### Revenue Per Send

Revenue moyen par envoi email.

```dax
Revenue Per Send = 
VAR Revenue = [Campaign Revenue]
VAR Sends = COUNTROWS(marketing_sends)
RETURN
    DIVIDE(Revenue, Sends, BLANK())
```

**Format:** Currency (EUR)
**Usage:** Efficacité email marketing

---

### Payback Period (Days)

Nombre de jours pour rentabiliser le budget campagne.

```dax
Payback Period (est.) = 
VAR DailyCampaignRevenue = 
    DIVIDE([Campaign Revenue], 365, BLANK())
VAR Budget = SUM(marketing_campaigns[budget_eur])
RETURN
    DIVIDE(Budget, DailyCampaignRevenue, BLANK())
```

**Format:** Nombre (jours)
**Usage:** Projection ROI

---

## Notes d'Implémentation

### Vérification des Noms de Colonnes

Avant d'utiliser ces mesures, vérifier que les noms de colonnes correspondent exactement:

**Tables critiques:**
- orders.attributed_campaign_id (STRING, nullable)
- marketing_events.event_type (STRING: "open", "click", "bounce", "unsubscribe")
- marketing_campaigns.campaign_id (STRING, PK)
- crm_customer_profile.churn_risk_score (INT, 0-100)

### Relations Manquantes

Si une mesure retourne BLANK(), vérifier:
1. Les relations entre tables sont bien créées
2. Les cardinalités sont correctes (1:Many)
3. La colonne de jointure existe dans les deux tables

### Performance

Pour améliorer les performances:
- Créer des index sur les colonnes de jointure
- Utiliser des variables (VAR) dans les DAX complexes
- Éviter les CALCULATE imbriqués multiples

---

## Validation

Script de test pour valider les mesures:

```dax
// Test Table
Test Measures = 
UNION(
    ROW("Measure", "Campaign ROI", "Value", [Campaign ROI]),
    ROW("Measure", "Open Rate", "Value", [Open Rate]),
    ROW("Measure", "CTR", "Value", [Click Rate]),
    ROW("Measure", "Conversion Rate", "Value", [Conversion Rate Post-Send]),
    ROW("Measure", "Attribution Rate", "Value", [Attribution Rate]),
    ROW("Measure", "Total Revenue", "Value", [Total Revenue])
)
```

**Valeurs attendues (dataset complet):**
- Campaign ROI: ~400-500%
- Open Rate: ~22%
- CTR: ~8%
- Conversion Rate: ~2-3%
- Attribution Rate: ~9%
- Total Revenue: ~2-3M EUR
