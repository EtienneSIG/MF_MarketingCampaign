# Schéma de Données - Customer 360 + CRM + Marketing + Commerce

Ce document décrit le schéma complet des **15 tables** et du **corpus texte** de la démo.

---

## 📐 Architecture Relationnelle

```
CRM:
  accounts (1) ←─── (N) customers (1) ←─── (N) customer_segments (N) ───→ (1) segments
      ↓                    ↓                                                       ↓
      └────────────────────┼───────────────────────────────────────────────────────┘
                           ↓
                    interactions
                    customer_profile

Marketing:
  campaigns (1) ←─── (N) assets
      ↓                    ↓
      ├─── (N) audiences (N) ───→ segments
      └─── (N) sends ←─── assets
               ↓
          marketing_events
               ↓
          (attribution)
               ↓
Commerce:      orders (N) ───→ customers
               ↓
          order_lines (N) ───→ products
               ↓
            returns
```

---

## 📊 Tables CRM (6 tables)

### 1. `crm_accounts`

**Description** : Comptes entreprises (B2B).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `account_id` | STRING | Identifiant unique compte | PK, format `ACC_XXXXXX` |
| `account_name` | STRING | Nom de l'entreprise | |
| `industry` | STRING | Secteur d'activité | Technology, Retail, Finance... |
| `region` | STRING | Région géographique | EMEA, Americas, APAC |
| `tier` | STRING | Niveau du compte | enterprise, mid_market, smb |
| `employee_count` | INT | Nombre d'employés | |
| `created_at` | TIMESTAMP | Date de création du compte | |
| `status` | STRING | Statut | active, inactive |
| `annual_revenue_eur` | INT | Revenu annuel estimé (EUR) | |

**Volume** : 2 000 lignes

**Distribution** :
- Industry : Technology (25%), Retail (20%), Finance/Healthcare (15% chacun), Manufacturing/Education (10%), Other (5%)
- Tier : SMB (60%), Mid-market (30%), Enterprise (10%)

---

### 2. `crm_customers`

**Description** : Clients/contacts individuels (B2C et B2B).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `customer_id` | STRING | Identifiant unique client | PK, format `CUST_XXXXXX` |
| `account_id` | STRING | Lien vers compte (si B2B) | FK → `accounts.account_id`, nullable |
| `email` | STRING | Email du client | Unique |
| `first_seen_at` | TIMESTAMP | Première interaction | |
| `status` | STRING | Statut client | active, churned |
| `locale` | STRING | Langue/locale | fr_FR, en_US, de_DE, es_ES |
| `lifecycle_stage` | STRING | Étape du cycle de vie | lead, prospect, active, at_risk, churned |
| `consent_email` | BOOLEAN | Consentement marketing email | |
| `consent_sms` | BOOLEAN | Consentement marketing SMS | |
| `preferred_channel` | STRING | Canal de contact préféré | email, phone, chat, in_app |
| `country` | STRING | Pays | France, USA, Germany, Spain, UK |

**Volume** : 20 000 lignes

**Cardinalité** :
- `customers.account_id` → `accounts.account_id` : Many-to-One (30% des clients liés à un account)

---

### 3. `crm_segments`

**Description** : Segments clients pour ciblage marketing.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `segment_id` | STRING | Identifiant unique segment | PK, format `SEG_XXX` |
| `segment_name` | STRING | Nom du segment | |
| `description` | STRING | Description/critères | |
| `created_at` | TIMESTAMP | Date de création | |
| `is_active` | BOOLEAN | Segment actif ? | |

**Volume** : 40 lignes

**Exemples** : "High Value", "Frequent Buyers", "At Risk", "Email Engagers", "VIP", etc.

---

### 4. `crm_customer_segments`

**Description** : Association clients ↔ segments (Many-to-Many).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `customer_id` | STRING | Identifiant client | FK → `customers.customer_id` |
| `segment_id` | STRING | Identifiant segment | FK → `segments.segment_id` |
| `start_date` | TIMESTAMP | Date d'entrée dans segment | |
| `end_date` | TIMESTAMP | Date de sortie (null si actif) | Nullable |

**Volume** : ~60 000 lignes (2-5 segments par client)

**Cardinalité** :
- `customer_segments.customer_id` → `customers.customer_id` : Many-to-One
- `customer_segments.segment_id` → `segments.segment_id` : Many-to-One

---

### 5. `crm_interactions`

**Description** : Interactions CRM (tickets, appels, feedback).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `interaction_id` | STRING | Identifiant unique interaction | PK, format `INT_XXXXXXXX` |
| `customer_id` | STRING | Identifiant client | FK → `customers.customer_id` |
| `type` | STRING | Type d'interaction | support_ticket, sales_call, onboarding, feedback, complaint |
| `channel` | STRING | Canal utilisé | email, phone, chat, in_app |
| `occurred_at` | TIMESTAMP | Date/heure de l'interaction | |
| `topic` | STRING | Sujet | billing, technical, product, account, feature, pricing |
| `outcome` | STRING | Résultat | resolved, pending, escalated, closed |
| `satisfaction_score` | INT | Score de satisfaction (1-5) | Nullable |
| `duration_min` | INT | Durée en minutes | Nullable |

**Volume** : 80 000 lignes (~4 interactions/client)

**Distribution types** :
- support_ticket (30%), sales_call (25%), feedback (20%), onboarding (15%), complaint (10%)

---

### 6. `crm_customer_profile`

**Description** : Profil enrichi des clients (scores, KPIs).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `customer_id` | STRING | Identifiant client | PK/FK → `customers.customer_id` |
| `churn_risk_score` | INT | Score de risque de churn (0-100) | |
| `clv_score` | FLOAT | Customer Lifetime Value estimée (EUR) | |
| `nps_last` | INT | Dernier score NPS (0-10) | |
| `last_contact_at` | TIMESTAMP | Dernière interaction | |
| `total_interactions` | INT | Nombre total d'interactions | |
| `total_orders` | INT | Nombre de commandes | Mis à jour après orders |
| `total_spend_eur` | FLOAT | Dépenses totales (EUR) | Mis à jour après orders |
| `avg_order_value_eur` | FLOAT | Panier moyen (EUR) | |
| `open_rate_pct` | FLOAT | Taux d'ouverture emails (0-1) | |
| `click_rate_pct` | FLOAT | Taux de clic emails (0-1) | |

**Volume** : 20 000 lignes (1 par client)

**Cardinalité** : One-to-One avec `customers`

---

## 📧 Tables Marketing (5 tables)

### 7. `marketing_campaigns`

**Description** : Campagnes marketing.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `campaign_id` | STRING | Identifiant unique campagne | PK, format `CAMP_XXX` |
| `campaign_name` | STRING | Nom de la campagne | |
| `objective` | STRING | Objectif | acquisition, retention, upsell, winback, engagement |
| `start_date` | TIMESTAMP | Date de début | |
| `end_date` | TIMESTAMP | Date de fin | |
| `budget_eur` | INT | Budget (EUR) | |
| `channel` | STRING | Canal principal | email (focus pour cette démo) |
| `ab_test_flag` | BOOLEAN | A/B test actif ? | |
| `status` | STRING | Statut | active, completed |

**Volume** : 20 lignes

**Distribution** : acquisition, retention, upsell, winback, engagement (répartition équilibrée)

---

### 8. `marketing_assets`

**Description** : Assets marketing (templates email).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `asset_id` | STRING | Identifiant unique asset | PK, format `ASSET_XXXXX` |
| `campaign_id` | STRING | Campagne associée | FK → `campaigns.campaign_id` |
| `asset_type` | STRING | Type d'asset | email_template |
| `subject` | STRING | Objet de l'email | |
| `language` | STRING | Langue | fr, en, de, es |
| `variant` | STRING | Variante A/B | A, B, null |
| `created_at` | TIMESTAMP | Date de création | |

**Volume** : 60 lignes (3 assets/campagne en moyenne, dont certains A/B)

**Cardinalité** :
- `assets.campaign_id` → `campaigns.campaign_id` : Many-to-One

---

### 9. `marketing_audiences`

**Description** : Audiences ciblées (lien campagnes ↔ segments).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `audience_id` | STRING | Identifiant unique audience | PK |
| `campaign_id` | STRING | Campagne | FK → `campaigns.campaign_id` |
| `segment_id` | STRING | Segment ciblé | FK → `segments.segment_id` |
| `criteria_json` | STRING | Critères additionnels (JSON) | |

**Volume** : ~40 lignes (1-3 segments/campagne)

**Cardinalité** :
- `audiences.campaign_id` → `campaigns.campaign_id` : Many-to-One
- `audiences.segment_id` → `segments.segment_id` : Many-to-One

---

### 10. `marketing_sends`

**Description** : Envois d'emails individuels.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `send_id` | STRING | Identifiant unique envoi | PK, format `SEND_XXXXXXXX` |
| `campaign_id` | STRING | Campagne | FK → `campaigns.campaign_id` |
| `asset_id` | STRING | Asset utilisé | FK → `assets.asset_id` |
| `customer_id` | STRING | Destinataire | FK → `customers.customer_id` |
| `send_at` | TIMESTAMP | Date/heure d'envoi | |

**Volume** : 200 000 lignes (~10 envois/client)

**Cardinalités** :
- `sends.campaign_id` → `campaigns.campaign_id` : Many-to-One
- `sends.asset_id` → `assets.asset_id` : Many-to-One
- `sends.customer_id` → `customers.customer_id` : Many-to-One

**Contraintes métier** : Respecte `customers.consent_email = true`

---

### 11. `marketing_events`

**Description** : Événements marketing (open, click, bounce, unsubscribe).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `event_id` | STRING | Identifiant unique événement | PK, format `EVT_XXXXXXXX` |
| `send_id` | STRING | Envoi associé | FK → `sends.send_id` |
| `customer_id` | STRING | Client | FK → `customers.customer_id` |
| `event_type` | STRING | Type d'événement | open, click, bounce, unsubscribe |
| `event_at` | TIMESTAMP | Date/heure de l'événement | |
| `url_clicked` | STRING | URL cliquée (si click) | Nullable |
| `device` | STRING | Type d'appareil | desktop, mobile, tablet, null |
| `user_agent` | STRING | User agent | Nullable |

**Volume** : 200 000 lignes

**Distribution** :
- Bounce : ~3%
- Open : ~22% (parmi non-bounced)
- Click : ~8% (parmi opens)
- Unsubscribe : ~0.5%

**Cardinalités** :
- `events.send_id` → `sends.send_id` : Many-to-One
- `events.customer_id` → `customers.customer_id` : Many-to-One

---

## 🛒 Tables Commerce (4 tables)

### 12. `products`

**Description** : Catalogue produits.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `product_id` | STRING | Identifiant unique produit | PK, format `PROD_XXXXX` |
| `product_name` | STRING | Nom du produit | |
| `category` | STRING | Catégorie | Electronics, Clothing, Home & Garden, Sports, Books, Beauty, Food |
| `brand` | STRING | Marque | |
| `price_eur` | FLOAT | Prix unitaire (EUR) | |
| `margin_pct` | FLOAT | Marge (0-1) | |
| `sku` | STRING | SKU | |
| `in_stock` | BOOLEAN | En stock ? | |

**Volume** : 150 lignes

**Distribution catégories** : Electronics (25%), Clothing (20%), Home & Garden (15%), Sports (15%), Books (10%), Beauty (10%), Food (5%)

---

### 13. `orders`

**Description** : Commandes clients.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `order_id` | STRING | Identifiant unique commande | PK, format `ORD_XXXXXXX` |
| `customer_id` | STRING | Client | FK → `customers.customer_id` |
| `order_at` | TIMESTAMP | Date/heure de commande | |
| `channel` | STRING | Canal d'achat | web, mobile_app, in_store, phone |
| `total_amount_eur` | FLOAT | Montant total (EUR) | Calculé depuis order_lines |
| `promo_code` | STRING | Code promo utilisé | Nullable |
| `attributed_campaign_id` | STRING | Attribution last-touch (14j) | FK → `campaigns.campaign_id`, nullable |
| `status` | STRING | Statut | completed, pending, canceled |

**Volume** : 60 000 lignes (~3 commandes/client)

**Cardinalités** :
- `orders.customer_id` → `customers.customer_id` : Many-to-One
- `orders.attributed_campaign_id` → `campaigns.campaign_id` : Many-to-One (nullable)

**Règle d'attribution** : Last touch dans fenêtre de 14 jours post-click/post-open

---

### 14. `order_lines`

**Description** : Lignes de commande (détail produits).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `order_line_id` | STRING | Identifiant unique ligne | PK, format `LINE_XXXXXXXX` |
| `order_id` | STRING | Commande | FK → `orders.order_id` |
| `product_id` | STRING | Produit | FK → `products.product_id` |
| `qty` | INT | Quantité | |
| `unit_price_eur` | FLOAT | Prix unitaire (EUR) | |
| `discount_eur` | FLOAT | Réduction appliquée (EUR) | |
| `line_total_eur` | FLOAT | Total ligne (EUR) | (unit_price × qty) - discount |

**Volume** : ~180 000 lignes (3 lignes/commande en moyenne)

**Cardinalités** :
- `order_lines.order_id` → `orders.order_id` : Many-to-One
- `order_lines.product_id` → `products.product_id` : Many-to-One

---

### 15. `returns`

**Description** : Retours de commandes.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `return_id` | STRING | Identifiant unique retour | PK, format `RET_XXXXXX` |
| `order_id` | STRING | Commande retournée | FK → `orders.order_id` |
| `customer_id` | STRING | Client | FK → `customers.customer_id` |
| `created_at` | TIMESTAMP | Date de création retour | |
| `reason` | STRING | Raison du retour | defective, wrong_item, not_as_described, changed_mind, other |
| `amount_refunded_eur` | FLOAT | Montant remboursé (EUR) | |
| `status` | STRING | Statut | approved, pending, rejected |

**Volume** : 10 000 lignes (~17% taux de retour)

**Cardinalités** :
- `returns.order_id` → `orders.order_id` : Many-to-One
- `returns.customer_id` → `customers.customer_id` : Many-to-One

---

## 📝 Corpus Texte (2 dossiers)

### `data/raw/text/customer_knowledge_notes/*.txt`

**Description** : Notes CRM par client (knowledge base).

**Format** :
```
CUSTOMER_ID: CUST_XXXXXX
DATE: YYYY-MM-DD
TOPIC: product_inquiry|pricing_negotiation|...
LANGUAGE: fr
SENTIMENT: positive|neutral|negative
TAGS: crm, customer_knowledge, ...

--- BEGIN NOTE ---
Texte libre de la note (5-10 lignes).
Inclut des fake PII (email, téléphone) pour démo AI redaction.
--- END NOTE ---
```

**Volume** : 20 000 fichiers (1 par client)

**Utilisation Fabric** : AI Transformation pour extraction sentiment, topics, PII redaction, entity recognition

---

### `data/raw/text/email_bodies/*.txt`

**Description** : Corps des emails marketing.

**Format** :
```
ASSET_ID: ASSET_XXXXX
CAMPAIGN_ID: CAMP_XXX
DATE: YYYY-MM-DD HH:MM:SS
LANGUAGE: fr|en|de|es
VARIANT: A|B
SUBJECT: ...

--- BEGIN EMAIL ---
Bonjour {{customer_name}},

Texte de l'email (3-5 paragraphes).
Inclut CTA et mentions produits.

DÉCOUVRIR MAINTENANT

Cordialement,
L'équipe BrandCo
--- END EMAIL ---
```

**Volume** : 60 fichiers (1 par asset)

**Utilisation Fabric** : AI Transformation pour summarization, entity extraction, language detection

---

## 🔗 Relations Clés (Recap)

### CRM ↔ Marketing
- `customers` ←→ `sends` (Many-to-Many via `sends`)
- `segments` ←→ `campaigns` (Many-to-Many via `audiences`)

### Marketing ↔ Commerce
- `campaigns` ←→ `orders` via `attributed_campaign_id` (attribution last-touch)

### CRM ↔ Commerce
- `customers` ←→ `orders` (Many-to-One)
- `customers` ←→ `returns` (Many-to-One)

---

## 📐 Mesures DAX Recommandées

### CLV (Customer Lifetime Value)

```dax
CLV = SUM(orders[total_amount_eur]) * AVERAGE(products[margin_pct])
```

### Conversion Rate

```dax
Conversion_Rate = 
DIVIDE(
    COUNTROWS(FILTER(customers, customers[total_orders] > 0)),
    COUNTROWS(customers),
    0
)
```

### Campaign ROI

```dax
Campaign_ROI = 
VAR Revenue = CALCULATE(SUM(orders[total_amount_eur]), orders[attributed_campaign_id] <> BLANK())
VAR Cost = SUM(campaigns[budget_eur])
RETURN DIVIDE(Revenue - Cost, Cost, 0)
```

### Open Rate

```dax
Open_Rate = 
DIVIDE(
    COUNTROWS(FILTER(marketing_events, marketing_events[event_type] = "open")),
    COUNTROWS(sends),
    0
)
```

### Click Through Rate (CTR)

```dax
CTR = 
VAR Opens = COUNTROWS(FILTER(marketing_events, marketing_events[event_type] = "open"))
VAR Clicks = COUNTROWS(FILTER(marketing_events, marketing_events[event_type] = "click"))
RETURN DIVIDE(Clicks, Opens, 0)
```

### Churn Rate

```dax
Churn_Rate = 
DIVIDE(
    COUNTROWS(FILTER(customers, customers[lifecycle_stage] = "churned")),
    COUNTROWS(customers),
    0
)
```

### Return Rate

```dax
Return_Rate = 
DIVIDE(
    COUNTROWS(returns),
    COUNTROWS(orders),
    0
)
```

---

## ✅ Vérifications de Cohérence

### Contraintes référentielles

```sql
-- Tous les customer_id dans orders existent dans customers
SELECT COUNT(*) FROM orders o 
LEFT JOIN customers c ON o.customer_id = c.customer_id 
WHERE c.customer_id IS NULL;
-- Attendu : 0

-- Tous les attributed_campaign_id existent
SELECT COUNT(*) FROM orders o 
LEFT JOIN campaigns c ON o.attributed_campaign_id = c.campaign_id 
WHERE o.attributed_campaign_id IS NOT NULL AND c.campaign_id IS NULL;
-- Attendu : 0

-- Consentement email respecté
SELECT COUNT(*) FROM sends s
JOIN customers c ON s.customer_id = c.customer_id
WHERE c.consent_email = false;
-- Attendu : 0
```

---

**Note** : Ce schéma permet des analyses d'attribution marketing, segmentation client, CLV, churn prediction, et optimisation de campagnes.

