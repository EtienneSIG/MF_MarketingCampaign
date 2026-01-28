# AGENTS.md - Conventions de Développement

## 📋 Contexte du Projet

Ce repository contient une **démo Microsoft Fabric** pour le Customer 360 avec CRM et Marketing :
- OneLake + Shortcuts
- AI Shortcut Transformations (customer notes + emails → tables structurées)
- Fabric Data Agent (questions marketing/CRM en langage naturel)
- Customer 360 : CRM + Marketing Campaigns + Commerce avec attribution

**Langue principale** : Français (code en anglais, docs en français)

---

## 🏗️ Structure du Repo

```
Scenario 3 - Marketing Campagn/
├── data/
│   └── raw/
│       ├── crm/                # 6 CSV (accounts, customers, segments...)
│       ├── marketing/          # 5 CSV (campaigns, assets, sends, events...)
│       ├── commerce/           # 4 CSV (products, orders, order_lines, returns)
│       └── text/
│           ├── customer_knowledge_notes/  # 20 000 .txt
│           └── email_bodies/              # 60 .txt
├── src/
│   ├── generate_data.py        # Script principal de génération (~900 lignes)
│   ├── config.yaml             # Configuration (volumes, taux, distributions)
│   └── lib/                    # Helpers (si nécessaire)
├── docs/
│   ├── schema.md               # Dictionnaire de données (15 tables)
│   ├── demo_story.md           # Scénario "Du Lead au Champion"
│   ├── questions_demo.md       # 15 questions Data Agent
│   ├── fabric_setup.md         # Guide déploiement Fabric
│   ├── data_agent_instructions.md
│   └── data_agent_examples.md
├── requirements.txt
├── README.md
└── AGENTS.md                   # Ce fichier
```

---

## 🎯 Conventions de Code

### Noms de Variables et Colonnes

- **Colonnes de tables** : `snake_case` (ex: `customer_id`, `attributed_campaign_id`)
- **Variables Python** : `snake_case` (ex: `campaigns_df`, `send_metadata`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `CONFIG_FILE`, `ATTRIBUTION_WINDOW_DAYS`)
- **Noms de classes** : `PascalCase` (ex: `Customer360DataGenerator`)

### Identifiants Métier

Format standardisé :
- Accounts : `ACC_XXXXXX` (6 chiffres)
- Customers : `CUST_XXXXXX` (6 chiffres)
- Segments : `SEG_XXX` (3 chiffres)
- Interactions : `INT_XXXXXXXX` (8 chiffres)
- Campaigns : `CAMP_XXX` (3 chiffres)
- Assets : `ASSET_XXXXX` (5 chiffres)
- Sends : `SEND_XXXXXXXX` (8 chiffres)
- Events : `EVT_XXXXXXXX` (8 chiffres)
- Products : `PROD_XXXXX` (5 chiffres)
- Orders : `ORD_XXXXXXX` (7 chiffres)
- Order Lines : `LINE_XXXXXXXX` (8 chiffres)
- Returns : `RET_XXXXXX` (6 chiffres)

### Dates et Formats

- **Dates** : ISO 8601 (`YYYY-MM-DD HH:MM:SS`)
- **Encoding** : UTF-8 (tous les fichiers)
- **CSV separator** : virgule (`,`)
- **Decimal separator** : point (`.`)

---

## 🔧 Commandes Fréquentes

### Génération de Données

```powershell
# Générer toutes les données avec config par défaut
cd src
python generate_data.py

# Modifier les volumes : éditer src/config.yaml puis relancer
```

### Vérifications

```powershell
# Vérifier le nombre de lignes générées (CRM)
Get-ChildItem data\raw\crm\*.csv | ForEach-Object { 
    Write-Host "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines - 1) lignes"
}

# Vérifier marketing
Get-ChildItem data\raw\marketing\*.csv | ForEach-Object { 
    Write-Host "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines - 1) lignes"
}

# Vérifier commerce
Get-ChildItem data\raw\commerce\*.csv | ForEach-Object { 
    Write-Host "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines - 1) lignes"
}

# Compter les fichiers texte
(Get-ChildItem data\raw\text\customer_knowledge_notes\*.txt | Measure-Object).Count
(Get-ChildItem data\raw\text\email_bodies\*.txt | Measure-Object).Count

# Vérifier l'encodage UTF-8
Get-Content data\raw\crm\crm_customers.csv -Encoding UTF8 | Select-Object -First 5
```

---

## 📝 Guidelines de Modification

### Ajouter une Nouvelle Colonne à une Table

1. Modifier la fonction `generate_XXX()` dans `generate_data.py`
2. Mettre à jour `docs/schema.md` (description de la colonne)
3. Régénérer les données
4. Mettre à jour le Semantic Model dans Fabric (si déployé)

**Exemple** : Ajouter `email_verified` (boolean) dans `crm_customers`

```python
# Dans generate_crm_customers()
customer = {
    'customer_id': f'CUST_{i+1:06d}',
    # ... autres colonnes
    'email_verified': random.random() < 0.85,  # 85% vérifié
    'first_seen_at': ...
}
```

### Ajouter un Nouveau Segment

1. Éditer `src/config.yaml` → augmenter `volumes.segments`
2. Ajouter une définition dans `generate_crm_segments()` (liste `segment_definitions`)
3. Relancer `generate_data.py`

**Exemple** :

```python
segment_definitions = [
    # ... existants
    ("Mobile First", "Customers using mobile app 80%+ of time"),
    ("Weekend Shoppers", "Primarily shop on Saturdays/Sundays"),
]
```

### Modifier les Taux Marketing

Les taux sont configurables dans `config.yaml` :

```yaml
business_params:
  marketing_event_rates:
    open_rate_baseline: 0.22      # 22% open rate → modifier ici
    click_rate_baseline: 0.08     # 8% click rate
  
  conversion_baseline: 0.02       # 2% conversion sans campagne
  conversion_post_click: 0.12     # 12% après click
  
  ab_test_lift:
    open_lift_range: [0.05, 0.20]  # +5% à +20% variant B
```

### Modifier les Templates d'Emails

Les templates sont dans `_generate_email_text()` de `generate_data.py`.

**Structure** :
- Par `objective` (acquisition, retention, upsell, winback, engagement)
- Par `variant` (A ou B pour A/B test)

Ajouter un nouveau template pour un objectif spécifique.

---

## 🧪 Tests et Validation

### Vérifier la Cohérence Référentielle

```python
# Après génération, lancer ces checks

import pandas as pd

customers_df = pd.read_csv('data/raw/crm/crm_customers.csv')
orders_df = pd.read_csv('data/raw/commerce/orders.csv')
sends_df = pd.read_csv('data/raw/marketing/marketing_sends.csv')

# Tous les customer_id dans orders existent dans customers ?
assert orders_df['customer_id'].isin(customers_df['customer_id']).all()

# Tous les customer_id dans sends existent dans customers ?
assert sends_df['customer_id'].isin(customers_df['customer_id']).all()

# Tous les sends respectent le consentement email ?
sends_with_consent = sends_df.merge(customers_df[['customer_id', 'consent_email']], on='customer_id')
assert sends_with_consent['consent_email'].all()

print("✅ Cohérence référentielle OK")
```

### Vérifier les Distributions

```python
# Distribution des lifecycle stages
print(customers_df['lifecycle_stage'].value_counts(normalize=True))
# Attendu : active ~40%, at_risk ~15%, churned ~10%, etc.

# Distribution des conversions
attributed = orders_df['attributed_campaign_id'].notna().sum()
organic = orders_df['attributed_campaign_id'].isna().sum()
print(f"Attributed: {attributed} ({attributed/len(orders_df)*100:.1f}%)")
print(f"Organic: {organic} ({organic/len(orders_df)*100:.1f}%)")
# Attendu : attributed ~9%, organic ~91%

# Taux d'ouverture
events_df = pd.read_csv('data/raw/marketing/marketing_events.csv')
opens = len(events_df[events_df['event_type'] == 'open'])
total_sends = len(sends_df)
print(f"Open rate: {opens/total_sends*100:.1f}%")
# Attendu : ~22%
```

---

## 🚨 Erreurs Fréquentes et Solutions

### Erreur : `UnicodeDecodeError` lors de la lecture des CSV

**Cause** : Encodage incorrect (BOM ou non UTF-8)

**Solution** :
```python
# Forcer UTF-8 sans BOM
df.to_csv(filepath, index=False, encoding='utf-8')
```

### Erreur : Les dates sont en STRING dans Fabric

**Cause** : Inférence de schéma incorrecte

**Solution** : Caster manuellement
```python
from pyspark.sql.functions import to_timestamp
df = df.withColumn("order_at", to_timestamp("order_at", "yyyy-MM-dd HH:mm:ss"))
```

### Erreur : ROI > 10 000% ou valeurs aberrantes

**Cause** : Problème dans l'attribution (trop de commandes attribuées) ou budget trop faible

**Solution** : Vérifier que `attributed_campaign_id` est NULL pour majorité des orders (~91%)

```python
# Vérifier distribution attribution
print(orders_df['attributed_campaign_id'].isna().sum() / len(orders_df))
# Attendu : ~0.91
```

### Erreur : Corpus texte vides ou mal formatés

**Cause** : Problème dans `generate_customer_knowledge_notes()` ou `generate_email_bodies()`

**Solution** : Vérifier que :
- Les templates retournent bien des strings
- L'encodage UTF-8 est préservé dans l'écriture
- Les headers (CUSTOMER_ID, DATE...) sont présents

---

## 📚 Documentation à Maintenir

### Après Modification de `generate_data.py`

1. Mettre à jour `docs/schema.md` si colonnes changées
2. Mettre à jour `README.md` si volumes changés
3. Mettre à jour `docs/data_agent_examples.md` si nouvelles métriques

### Après Modification de `config.yaml`

1. Documenter les nouveaux paramètres dans `README.md`
2. Mettre à jour les valeurs par défaut dans `docs/fabric_setup.md`

---

## 🎨 Suggestions d'Extension

### Idées pour Améliorer la Démo

1. **Ajouter des événements web** : Table `web_events` (page views, cart adds, checkouts)
2. **Simuler du multi-touch attribution** : Créer `attribution_touchpoints` (first-touch, last-touch, linear)
3. **Ajouter des campagnes SMS** : Répliquer la structure email pour SMS
4. **Intégrer des données publicitaires** : Table `ad_campaigns` (Facebook, Google Ads avec impressions, clicks, CPC)
5. **Créer un scoring ML** : Table `propensity_scores` (propensity to buy, to churn, to upgrade)

### Nouvelles Tables Possibles

```python
# Table : web_events
{
    'event_id': 'WEB_XXXXXXXX',
    'customer_id': 'CUST_XXXXXX',
    'session_id': 'SESS_XXXXXXXX',
    'event_type': 'page_view|add_to_cart|checkout|purchase',
    'event_at': datetime,
    'page_url': str,
    'referrer': str,
    'device': 'desktop|mobile|tablet'
}

# Table : ad_campaigns (paid media)
{
    'ad_campaign_id': 'ADCAMP_XXX',
    'platform': 'facebook|google|linkedin',
    'impressions': int,
    'clicks': int,
    'spend_eur': float,
    'conversions': int
}

# Table : propensity_scores (ML predictions)
{
    'customer_id': 'CUST_XXXXXX',
    'propensity_to_buy': float,  # 0-1
    'propensity_to_churn': float,
    'propensity_to_upgrade': float,
    'predicted_clv': float,
    'scored_at': datetime
}
```

---

## 🔐 Sécurité et Conformité

### PII (Personally Identifiable Information)

**Toutes les PII dans ce repo sont FICTIVES** :
- Emails : générés par Faker (`@example.com`)
- Téléphones : générés par Faker (formats français fictifs)
- Noms : générés par Faker (noms français aléatoires)

**Redaction dans les customer_knowledge_notes** :
- Les PII détectées par AI Transformations sont marquées pour démo
- Pas de vraie PII à redacter (tout est synthétique)

### RGPD / GDPR

**Ce dataset ne contient AUCUNE donnée réelle**, donc :
- ✅ Pas de consentement requis (données synthétiques)
- ✅ Pas de droit à l'oubli (clients fictifs)
- ✅ Utilisable librement pour formation/démo

**⚠️ ATTENTION** : Ne jamais utiliser de vraies données clients/marketing dans ce repo.

---

## 🤖 Utilisation de Copilot sur ce Repo

### Questions Fréquentes à Poser

**Génération de code** :
- "Ajoute une colonne `sms_consent` (boolean) dans crm_customers"
- "Crée une fonction pour générer des campagnes SMS (similaire aux email)"
- "Ajoute un template d'email pour l'objectif 'cross_sell'"

**Modification de config** :
- "Change les volumes pour avoir 50 000 clients et 100 000 commandes"
- "Ajoute un nouveau segment 'VIP Premium' (CLV > 30K EUR)"

**Debugging** :
- "Pourquoi le ROI dépasse 1000% pour certaines campagnes ?"
- "Comment corriger l'attribution (trop de commandes attribuées) ?"

**Documentation** :
- "Génère un exemple de requête SQL pour calculer le CAC (cost per acquisition)"
- "Ajoute un diagramme de funnel de conversion dans demo_story.md"

**Métriques Marketing** :
- "Explique le calcul du CLV et crée une mesure DAX"
- "Comment calculer le LTV:CAC ratio ?"

### Prompts Efficaces

✅ **Bon prompt** :
> "Dans generate_data.py, ajoute une colonne `email_fatigue_score` (0-100) dans crm_customer_profile. Corrélation : +1 point par envoi email, -10 points par click, -20 points par order."

❌ **Prompt vague** :
> "Ajoute une colonne fatigue"

### Contexte à Fournir

Lorsque vous posez une question à Copilot, mentionner :
- Le fichier concerné (`generate_data.py`, `config.yaml`, etc.)
- Le type de modification (ajout, suppression, refactoring)
- Les contraintes (format, distribution, cohérence, métriques marketing)

---

## 🧮 Métriques Marketing de Référence

### ROI (Return On Investment)

**Formule** :
```
ROI = (Revenue - Cost) / Cost
```

**Objectifs** :
- Campagnes acquisition : ROI ≥ +100%
- Campagnes rétention : ROI ≥ +300%
- Campagnes upsell : ROI ≥ +500%

---

### Conversion Rate

**Formule** :
```
Conversion Rate = Orders / Sends (ou Clicks selon contexte)
```

**Objectifs** :
- Post-send : ≥ 3%
- Post-open : ≥ 8%
- Post-click : ≥ 12%

---

### CLV (Customer Lifetime Value)

**Formule** :
```
CLV = Total Spend × Avg Margin %
```

**Objectifs** :
- CLV moyen : ≥ 5 000 EUR
- Top 10% CLV : ≥ 15 000 EUR

---

### Open Rate & CTR

| Métrique | Formule | Objectif |
|----------|---------|----------|
| Open Rate | Opens / Sends | ≥ 20% |
| CTR | Clicks / Opens | ≥ 5% |
| Bounce Rate | Bounces / Sends | ≤ 3% |
| Unsubscribe Rate | Unsubscribes / Sends | ≤ 0.5% |

---

### Attribution Last-Touch

**Règle** : Fenêtre de **14 jours** post-click ou post-open.

**Formule** :
```
Attributed Order = Order dans les 14j après dernier marketing event (click > open)
```

---

## ✅ Checklist avant Commit

Avant de commit des modifications :

- [ ] Code formatté (PEP8 pour Python)
- [ ] `generate_data.py` s'exécute sans erreur
- [ ] Données générées testées (volumes corrects, FK cohérentes)
- [ ] `docs/schema.md` mis à jour si schéma changé
- [ ] `README.md` mis à jour si volumes/features changés
- [ ] Pas de données réelles ajoutées (PII fictives uniquement)
- [ ] Encodage UTF-8 vérifié sur tous les fichiers
- [ ] Config YAML valide (pas d'erreur de syntaxe)
- [ ] Métriques marketing cohérentes (ROI >0%, conversion <100%, etc.)

---

## 📞 Support

Pour questions techniques sur le code :
- Ouvrir une issue GitHub
- Utiliser Copilot Chat avec contexte du fichier

Pour questions sur Microsoft Fabric :
- Consulter [`docs/fabric_setup.md`](docs/fabric_setup.md)
- Voir la [documentation officielle](https://learn.microsoft.com/en-us/fabric/)

Pour questions sur les métriques marketing :
- Consulter `docs/data_agent_instructions.md` (formules ROI, CLV, conversion)

---

**Happy coding! 🚀**

*Ces instructions sont optimisées pour GitHub Copilot et Copilot Chat dans le contexte marketing/CRM.*
