# Guide de Déploiement - Microsoft Fabric (Scénario Marketing Campaigns)

## 🎯 Objectif

Ce guide décrit **étape par étape** comment déployer la démo Customer 360 + CRM + Marketing Campaigns + Commerce dans Microsoft Fabric.

**Prérequis** :
- Un compte Microsoft Fabric (trial ou licence)
- Les données générées localement (voir README.md)
- Un workspace Fabric créé

**Durée estimée** : 45-60 minutes

---

## 📋 Vue d'Ensemble du Déploiement

```
Étape 1: Créer un Lakehouse
Étape 2: Uploader les données vers OneLake
Étape 3: Créer des OneLake Shortcuts
Étape 4: Appliquer Shortcut Transformations AI sur les textes
Étape 5: Charger les CSV en tables Delta
Étape 6: Créer un Semantic Model
Étape 7: Configurer le Fabric Data Agent
Étape 8: Tester et valider
```

---

## Étape 1 : Créer un Lakehouse

### 1.1 Accéder au Workspace

1. Ouvrir [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. Sélectionner ou créer un workspace (ex: `Demo-Marketing360`)
3. Vérifier que vous êtes dans l'expérience **Data Engineering**

### 1.2 Créer le Lakehouse

1. Cliquer sur **+ New** → **Lakehouse**
2. Nom : `Marketing360_Lakehouse`
3. Cliquer sur **Create**

✅ **Résultat attendu** : Un Lakehouse vide avec deux sections : **Tables** et **Files**.

---

## Étape 2 : Uploader les Données vers OneLake

### 2.1 Préparer les Données Locales

Sur votre machine locale, les données générées sont dans :
```
data/
├── raw/
│   ├── crm/
│   │   ├── accounts.csv
│   │   ├── customers.csv
│   │   ├── segments.csv
│   │   ├── customer_segments.csv
│   │   ├── interactions.csv
│   │   └── customer_profile.csv
│   ├── marketing/
│   │   ├── campaigns.csv
│   │   ├── assets.csv
│   │   ├── audiences.csv
│   │   ├── sends.csv
│   │   └── events.csv
│   ├── commerce/
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   ├── order_lines.csv
│   │   └── returns.csv
│   └── text/
│       ├── customer_knowledge_notes/
│       │   ├── CUST_000001.txt
│       │   ├── CUST_000002.txt
│       │   └── ... (20 000 fichiers)
│       └── email_bodies/
│           ├── ASSET_001.txt
│           ├── ASSET_002.txt
│           └── ... (60 fichiers)
```

### 2.2 Upload via l'Interface Fabric

**Option A : Upload direct (pour petits volumes)**

1. Dans le Lakehouse, aller dans **Files**
2. Créer une structure de dossiers :
   - Cliquer sur **Upload** → **Upload folder**
   - Sélectionner `data/raw/crm`
   - Répéter pour `data/raw/marketing`, `data/raw/commerce`, et `data/raw/text`

**Option B : Upload via OneLake File Explorer (recommandé)**

1. Installer [OneLake File Explorer](https://www.microsoft.com/en-us/download/details.aspx?id=105222) (Windows uniquement)
2. Ouvrir OneLake File Explorer
3. Naviguer vers votre workspace → `Marketing360_Lakehouse` → **Files**
4. Copier-coller les dossiers `crm/`, `marketing/`, `commerce/`, et `text/` depuis votre explorateur Windows

**Option C : Upload via API/CLI (pour automatisation)**

```bash
# Nécessite azcopy ou un script Azure CLI
azcopy copy "data/raw/*" "https://<onelake-path>/Files/raw/" --recursive
```

✅ **Résultat attendu** : Structure de dossiers visible dans **Files** du Lakehouse.

---

## Étape 3 : Créer des OneLake Shortcuts

### 3.1 Principe des Shortcuts

Les **OneLake Shortcuts** créent des liens symboliques sans duplication de données.
Ils permettent de "monter" des données externes (ADLS, S3, etc.) ou internes (autre Lakehouse).

**Pour cette démo** : On va créer des shortcuts vers les fichiers uploadés (optionnel si déjà dans le Lakehouse, mais utile pour démontrer la fonctionnalité).

### 3.2 Créer un Shortcut (Exemple : CSV CRM)

1. Dans le Lakehouse, section **Files**
2. Clic droit sur la racine → **New shortcut**
3. Choisir **OneLake** (pour lier des fichiers déjà dans Fabric)
4. Sélectionner :
   - **Workspace** : Demo-Marketing360
   - **Item** : Marketing360_Lakehouse
   - **Path** : `Files/raw/crm`
5. Nommer le shortcut : `crm_data`
6. Cliquer sur **Create**

Répéter pour `marketing`, `commerce`, et `text` si vous voulez démontrer plusieurs shortcuts.

> **Note** : Si les fichiers sont déjà dans le Lakehouse, cette étape est conceptuelle pour la démo. 
> Dans un scénario réel, les shortcuts pointeraient vers un storage externe (ADLS Gen2, S3, etc.).

✅ **Résultat attendu** : Icône de shortcut visible dans Files, sans duplication de données.

---

## Étape 4 : Appliquer Shortcut Transformations AI sur les Textes

### 4.1 Principe des Shortcut Transformations

**Shortcut Transformations AI** (preview) transforme automatiquement des fichiers non structurés (txt, pdf, images) en tables Delta queryables.

Pour les fichiers texte (customer knowledge notes + email bodies), Fabric peut extraire :
- **Sentiment** (positif/neutre/négatif)
- **Résumé** (summary du contenu)
- **PII Detection** (emails, téléphones, noms)
- **Entity Extraction** (organisations, produits, montants)
- **Topics** (sujets détectés)

### 4.2 Créer une Transformation AI pour Customer Knowledge Notes

1. Dans le Lakehouse, aller dans **Files** → `raw/text/customer_knowledge_notes/`
2. Clic droit sur le dossier `customer_knowledge_notes` → **New AI transformation** (ou **Apply AI skills**)
   - Si l'option n'est pas visible, vérifier que la preview est activée dans les paramètres du tenant
3. Configurer la transformation :
   - **Source** : `customer_knowledge_notes/` (tous les .txt)
   - **Destination** : Table Delta `customer_knowledge_transformed`
   - **AI Skills à appliquer** :
     - ✅ Sentiment Analysis
     - ✅ Summarization
     - ✅ PII Detection
     - ✅ Entity Extraction
     - ✅ Key Phrase Extraction
4. Cliquer sur **Create transformation**

### 4.3 Créer une Transformation AI pour Email Bodies

1. Dans le Lakehouse, aller dans **Files** → `raw/text/email_bodies/`
2. Clic droit sur le dossier `email_bodies` → **New AI transformation**
3. Configurer la transformation :
   - **Source** : `email_bodies/` (tous les .txt)
   - **Destination** : Table Delta `email_bodies_transformed`
   - **AI Skills à appliquer** :
     - ✅ Sentiment Analysis
     - ✅ Summarization
     - ✅ PII Detection
     - ✅ Key Phrase Extraction
4. Cliquer sur **Create transformation**

### 4.4 Exécuter les Transformations

1. Les transformations se lancent automatiquement
2. Suivre le progrès dans le **Monitoring** (Activity pane)
3. Temps estimé : 
   - Customer knowledge notes : 15-20 minutes pour 20 000 fichiers
   - Email bodies : 2-3 minutes pour 60 fichiers

✅ **Résultat attendu** : Deux nouvelles tables Delta `customer_knowledge_transformed` et `email_bodies_transformed` apparaissent dans **Tables**.

### 4.5 Vérifier le Schéma des Tables Transformées

**Table `customer_knowledge_transformed`**

Colonnes attendues :
- `customer_id` (extrait du nom de fichier CUST_XXXXXX)
- `content` (texte complet de la note)
- `summary` (résumé généré)
- `sentiment` (positive/neutral/negative)
- `sentiment_score` (0-1)
- `pii_detected` (liste des PII trouvées)
- `entities_detected` (organisations, produits, montants)
- `key_phrases` (sujets principaux)
- `_metadata` (informations système)

**Table `email_bodies_transformed`**

Colonnes attendues :
- `asset_id` (extrait du nom de fichier ASSET_XXX)
- `content` (texte complet de l'email)
- `summary` (résumé généré)
- `sentiment` (positive/neutral/negative)
- `sentiment_score` (0-1)
- `key_phrases` (sujets principaux)
- `_metadata` (informations système)

**Exemple de requête test** :
```sql
-- Vérifier les notes clients
SELECT customer_id, sentiment, LEFT(summary, 100) AS summary_preview, pii_detected
FROM customer_knowledge_transformed
LIMIT 10;

-- Vérifier les emails
SELECT asset_id, sentiment, LEFT(summary, 100) AS summary_preview
FROM email_bodies_transformed
LIMIT 10;
```

> **Troubleshooting** : Si les tables n'apparaissent pas, rafraîchir le Lakehouse ou vérifier les logs de transformation.

---

## Étape 5 : Charger les CSV en Tables Delta

### 5.1 Créer des Tables depuis les CSV

Pour chaque fichier CSV, créer une table Delta.

**Méthode A : Via l'interface (pour démo interactive)**

1. Dans **Files**, naviguer vers `raw/crm/customers.csv`
2. Clic droit → **Load to new table**
3. Configurer :
   - **Table name** : `crm_customers`
   - **Delimiter** : Comma
   - **First row has headers** : ✅ Yes
   - **Infer schema** : ✅ Yes
4. Cliquer sur **Load**

Répéter pour toutes les tables :

**Tables CRM (6)** :
- `crm_accounts` (accounts.csv)
- `crm_customers` (customers.csv)
- `crm_segments` (segments.csv)
- `crm_customer_segments` (customer_segments.csv)
- `crm_interactions` (interactions.csv)
- `crm_customer_profile` (customer_profile.csv)

**Tables Marketing (5)** :
- `marketing_campaigns` (campaigns.csv)
- `marketing_assets` (assets.csv)
- `marketing_audiences` (audiences.csv)
- `marketing_sends` (sends.csv)
- `marketing_events` (events.csv)

**Tables Commerce (4)** :
- `products` (products.csv)
- `orders` (orders.csv)
- `order_lines` (order_lines.csv)
- `returns` (returns.csv)

**Méthode B : Via Notebook (pour automatisation)**

Créer un Notebook dans le Lakehouse :

```python
# Notebook: Load CSV to Delta Tables

from pyspark.sql import SparkSession

# Chemins des fichiers CRM
crm_files = {
    "crm_accounts": "Files/raw/crm/accounts.csv",
    "crm_customers": "Files/raw/crm/customers.csv",
    "crm_segments": "Files/raw/crm/segments.csv",
    "crm_customer_segments": "Files/raw/crm/customer_segments.csv",
    "crm_interactions": "Files/raw/crm/interactions.csv",
    "crm_customer_profile": "Files/raw/crm/customer_profile.csv"
}

# Chemins des fichiers Marketing
marketing_files = {
    "marketing_campaigns": "Files/raw/marketing/campaigns.csv",
    "marketing_assets": "Files/raw/marketing/assets.csv",
    "marketing_audiences": "Files/raw/marketing/audiences.csv",
    "marketing_sends": "Files/raw/marketing/sends.csv",
    "marketing_events": "Files/raw/marketing/events.csv"
}

# Chemins des fichiers Commerce
commerce_files = {
    "products": "Files/raw/commerce/products.csv",
    "orders": "Files/raw/commerce/orders.csv",
    "order_lines": "Files/raw/commerce/order_lines.csv",
    "returns": "Files/raw/commerce/returns.csv"
}

# Fusionner tous les fichiers
all_files = {**crm_files, **marketing_files, **commerce_files}

# Charger chaque CSV en table Delta
for table_name, file_path in all_files.items():
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df.write.format("delta").mode("overwrite").saveAsTable(table_name)
    print(f"✅ Table {table_name} créée avec {df.count()} lignes")
```

Exécuter le notebook (Ctrl+Enter sur chaque cellule).

✅ **Résultat attendu** : 15 tables CSV + 2 tables AI transformées = **17 tables au total** dans **Tables**.

### 5.2 Vérifier les Types de Données

Quelques vérifications importantes :

```sql
-- Vérifier que les dates sont bien en TIMESTAMP
DESCRIBE crm_customers;
-- Attendu: first_seen_at TIMESTAMP

DESCRIBE orders;
-- Attendu: order_date TIMESTAMP

DESCRIBE marketing_sends;
-- Attendu: sent_at TIMESTAMP

-- Vérifier les nombres
DESCRIBE order_lines;
-- Attendu: quantity INT, unit_price DECIMAL, total_price DECIMAL

DESCRIBE crm_customer_profile;
-- Attendu: clv_score FLOAT, churn_risk_score INT
```

Si les types sont incorrects (ex: date en STRING), ajuster avec :

```python
from pyspark.sql.functions import to_timestamp, col

# Corriger les timestamps des orders
df = spark.table("orders")
df = df.withColumn("order_date", to_timestamp(col("order_date"), "yyyy-MM-dd HH:mm:ss"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("orders")

# Corriger les timestamps des marketing_sends
df = spark.table("marketing_sends")
df = df.withColumn("sent_at", to_timestamp(col("sent_at"), "yyyy-MM-dd HH:mm:ss"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("marketing_sends")
```

---

## Étape 6 : Créer un Semantic Model

Le **Semantic Model** (ex-Analysis Services) structure les données pour Power BI et le Data Agent.

### 6.1 Créer le Semantic Model

1. Dans le Lakehouse, cliquer sur **New semantic model** (en haut à droite)
2. Nom : `Marketing360_Model`
3. Sélectionner les tables à inclure :
   - ✅ **CRM** : crm_accounts, crm_customers, crm_segments, crm_customer_segments, crm_interactions, crm_customer_profile
   - ✅ **Marketing** : marketing_campaigns, marketing_assets, marketing_audiences, marketing_sends, marketing_events
   - ✅ **Commerce** : products, orders, order_lines, returns
   - ✅ **AI Transformed** : customer_knowledge_transformed, email_bodies_transformed
4. Cliquer sur **Confirm**

### 6.2 Définir les Relations

Ouvrir le Semantic Model et créer les relations :

1. Cliquer sur **Model view** (icône diagramme)
2. Créer les relations suivantes (drag & drop entre tables) :

**Relations CRM**

| Table From | Colonne From | Table To | Colonne To | Cardinalité |
|------------|--------------|----------|------------|-------------|
| `crm_customers` | `account_id` | `crm_accounts` | `account_id` | Many-to-One |
| `crm_customer_segments` | `customer_id` | `crm_customers` | `customer_id` | Many-to-One |
| `crm_customer_segments` | `segment_id` | `crm_segments` | `segment_id` | Many-to-One |
| `crm_interactions` | `customer_id` | `crm_customers` | `customer_id` | Many-to-One |
| `crm_customer_profile` | `customer_id` | `crm_customers` | `customer_id` | One-to-One |

**Relations Marketing**

| Table From | Colonne From | Table To | Colonne To | Cardinalité |
|------------|--------------|----------|------------|-------------|
| `marketing_assets` | `campaign_id` | `marketing_campaigns` | `campaign_id` | Many-to-One |
| `marketing_audiences` | `campaign_id` | `marketing_campaigns` | `campaign_id` | Many-to-One |
| `marketing_audiences` | `segment_id` | `crm_segments` | `segment_id` | Many-to-One |
| `marketing_sends` | `campaign_id` | `marketing_campaigns` | `campaign_id` | Many-to-One |
| `marketing_sends` | `asset_id` | `marketing_assets` | `asset_id` | Many-to-One |
| `marketing_sends` | `customer_id` | `crm_customers` | `customer_id` | Many-to-One |
| `marketing_events` | `send_id` | `marketing_sends` | `send_id` | Many-to-One |

**Relations Commerce**

| Table From | Colonne From | Table To | Colonne To | Cardinalité |
|------------|--------------|----------|------------|-------------|
| `orders` | `customer_id` | `crm_customers` | `customer_id` | Many-to-One |
| `order_lines` | `order_id` | `orders` | `order_id` | Many-to-One |
| `order_lines` | `product_id` | `products` | `product_id` | Many-to-One |
| `returns` | `order_id` | `orders` | `order_id` | Many-to-One |

**Relations AI Transformed**

| Table From | Colonne From | Table To | Colonne To | Cardinalité |
|------------|--------------|----------|------------|-------------|
| `customer_knowledge_transformed` | `customer_id` | `crm_customers` | `customer_id` | Many-to-One (*) |
| `email_bodies_transformed` | `asset_id` | `marketing_assets` | `asset_id` | One-to-One (*) |

(*) Ces relations dépendent de la qualité de l'extraction des IDs par l'AI. Vérifier que les IDs sont correctement parsés.

### 6.3 Créer des Mesures DAX

Dans le Semantic Model, aller dans **Data view** et créer une **New measure** :

```dax
// ============================================
// Mesures CRM
// ============================================

Total Customers = COUNTROWS(crm_customers)

Active Customers = 
CALCULATE(
    [Total Customers],
    crm_customers[status] = "active"
)

Churned Customers = 
CALCULATE(
    [Total Customers],
    crm_customers[status] = "churned"
)

Churn Rate % = 
DIVIDE(
    [Churned Customers],
    [Total Customers],
    0
) * 100

Avg CLV = AVERAGE(crm_customer_profile[clv_score])

Avg Churn Risk = AVERAGE(crm_customer_profile[churn_risk_score])

Avg NPS = AVERAGE(crm_customer_profile[nps_last])

Total Interactions = COUNTROWS(crm_interactions)

Avg Satisfaction = AVERAGE(crm_interactions[satisfaction_score])

// ============================================
// Mesures Marketing
// ============================================

Total Campaigns = COUNTROWS(marketing_campaigns)

Active Campaigns = 
CALCULATE(
    [Total Campaigns],
    marketing_campaigns[status] = "active"
)

Total Marketing Budget = SUM(marketing_campaigns[budget_eur])

Total Email Sends = COUNTROWS(marketing_sends)

Total Email Events = COUNTROWS(marketing_events)

// Taux d'ouverture
Email Opens = 
CALCULATE(
    [Total Email Events],
    marketing_events[event_type] = "open"
)

Open Rate % = 
DIVIDE(
    [Email Opens],
    [Total Email Sends],
    0
) * 100

// Taux de clic
Email Clicks = 
CALCULATE(
    [Total Email Events],
    marketing_events[event_type] = "click"
)

Click Rate % = 
DIVIDE(
    [Email Clicks],
    [Total Email Sends],
    0
) * 100

// Taux de bounce
Email Bounces = 
CALCULATE(
    [Total Email Events],
    marketing_events[event_type] = "bounce"
)

Bounce Rate % = 
DIVIDE(
    [Email Bounces],
    [Total Email Sends],
    0
) * 100

// Taux de désinscription
Email Unsubscribes = 
CALCULATE(
    [Total Email Events],
    marketing_events[event_type] = "unsubscribe"
)

Unsubscribe Rate % = 
DIVIDE(
    [Email Unsubscribes],
    [Total Email Sends],
    0
) * 100

// ============================================
// Mesures Commerce
// ============================================

Total Orders = COUNTROWS(orders)

Total Revenue = 
SUMX(
    order_lines,
    order_lines[quantity] * order_lines[unit_price] * (1 - order_lines[discount])
)

Avg Order Value = DIVIDE([Total Revenue], [Total Orders])

Total Returns = COUNTROWS(returns)

Return Rate % = 
DIVIDE(
    [Total Returns],
    [Total Orders],
    0
) * 100

Total Products Sold = SUM(order_lines[quantity])

// ============================================
// Mesures d'Attribution Marketing
// ============================================

// Orders attributed to marketing (last-touch attribution)
Marketing Attributed Orders = 
CALCULATE(
    [Total Orders],
    orders[attribution_source] = "marketing"
)

Marketing Attributed Revenue = 
CALCULATE(
    [Total Revenue],
    orders[attribution_source] = "marketing"
)

// ROI Marketing
Marketing ROI % = 
DIVIDE(
    [Marketing Attributed Revenue] - [Total Marketing Budget],
    [Total Marketing Budget],
    0
) * 100

// ============================================
// Mesures Combinées Customer 360
// ============================================

Revenue per Customer = 
DIVIDE(
    [Total Revenue],
    [Total Customers],
    0
)

Orders per Customer = 
DIVIDE(
    [Total Orders],
    [Total Customers],
    0
)

Customers Who Ordered = 
CALCULATE(
    DISTINCTCOUNT(orders[customer_id])
)

Conversion Rate % = 
DIVIDE(
    [Customers Who Ordered],
    [Total Customers],
    0
) * 100

// ============================================
// Mesures Temporelles
// ============================================

Revenue YTD = 
TOTALYTD(
    [Total Revenue],
    orders[order_date]
)

Orders MTD = 
TOTALMTD(
    [Total Orders],
    orders[order_date]
)
```

### 6.4 Publier le Semantic Model

1. Cliquer sur **File** → **Save**
2. Le modèle est automatiquement publié dans le workspace

✅ **Résultat attendu** : Semantic Model disponible dans le workspace, prêt pour Power BI et Data Agent.

---

## Étape 7 : Configurer le Fabric Data Agent

### 7.1 Activer la Preview Data Agent

1. Aller dans **Settings** (⚙️) → **Tenant settings** → **Admin Portal**
2. Rechercher **Fabric Data Agent** (ou **Copilot for Data**)
3. Activer la preview pour le workspace

### 7.2 Créer le Data Agent

1. Dans le workspace, cliquer sur **+ New** → **Data Agent** (ou **Copilot**)
2. Nom : `Marketing360_Agent`
3. Sélectionner la source :
   - **Type** : Semantic Model
   - **Source** : `Marketing360_Model`
4. Cliquer sur **Create**

### 7.3 Configurer les Instructions (System Prompt)

1. Ouvrir le Data Agent
2. Aller dans **Settings** → **Instructions**
3. Coller le contenu de [`data_agent_instructions.md`](data_agent_instructions.md)
4. Sauvegarder

### 7.4 Tester le Data Agent

Poser une première question :
```
Combien de clients avons-nous au total ?
```

Réponse attendue : `20 000 clients`

Si la réponse est correcte ✅, passer à l'étape 8.

Si la réponse est incorrecte ❌ :
- Vérifier que le Semantic Model est bien publié
- Vérifier les relations entre tables
- Vérifier que les instructions sont bien configurées

---

## Étape 8 : Tester et Valider

### 8.1 Questions de Validation

Poser les questions de [`questions_demo.md`](questions_demo.md).

**Exemples de questions à tester** :

1. ✅ Combien de clients avons-nous au total ?
2. ✅ Quel est le taux de churn actuel ?
3. ✅ Quelle est la CLV moyenne de nos clients ?
4. ✅ Combien de campagnes marketing sont actives ?
5. ✅ Quel est le taux d'ouverture moyen des emails ?
6. ✅ Quel est le taux de clic moyen des emails ?
7. ✅ Quel est le ROI marketing global ?
8. ✅ Quelle campagne a généré le plus de revenu ?
9. ✅ Quels segments sont les plus rentables ?
10. ✅ Quel est le panier moyen ?

**Critère de succès** : Au moins 80% des questions fonctionnent correctement.

### 8.2 Créer un Dashboard Power BI

1. Dans le workspace, cliquer sur **+ New** → **Report**
2. Sélectionner `Marketing360_Model` comme source
3. Créer quelques visuels rapides :
   
**Page 1 : Vue d'Ensemble**
   - Card : Total Customers, Active Customers, Churn Rate %
   - Card : Total Revenue, Total Orders, Avg Order Value
   - Donut : Customers by Lifecycle Stage
   - Line Chart : Revenue by Month

**Page 2 : Marketing Performance**
   - Card : Total Campaigns, Total Email Sends, Total Marketing Budget
   - Card : Open Rate %, Click Rate %, Marketing ROI %
   - Bar Chart : Email Events by Type (open, click, bounce, unsubscribe)
   - Table : Top Campaigns by Revenue

**Page 3 : Customer 360**
   - Scatter Chart : CLV Score vs Churn Risk Score
   - Bar Chart : Customers by Segment
   - Table : Top Customers by CLV
   - Line Chart : Avg NPS over Time

4. Sauvegarder le rapport : `Marketing360_Dashboard`

### 8.3 Vérifier les Permissions

Si la démo doit être partagée :
1. Aller dans **Workspace settings** → **Access**
2. Ajouter les viewers/contributors selon les besoins
3. Vérifier que le Semantic Model est partagé (hérite des permissions du workspace)

---

## 🎉 Déploiement Terminé

Vous avez maintenant :
- ✅ Un Lakehouse avec 17 tables Delta (15 CSV + 2 AI transformed)
- ✅ Des OneLake Shortcuts (optionnel)
- ✅ Des AI Transformations sur les customer knowledge notes et email bodies
- ✅ Un Semantic Model complet avec relations et mesures
- ✅ Un Data Agent fonctionnel
- ✅ Un dashboard Power BI multi-pages

**Prochaines étapes** :
- Tester toutes les questions de la démo ([questions_demo.md](questions_demo.md))
- Personnaliser le dashboard Power BI
- Préparer le pitch de présentation ([demo_story.md](demo_story.md))
- Explorer les insights des AI transformations

---

## 🔧 Troubleshooting

### Problème : Les fichiers texte ne sont pas transformés

**Symptômes** : Les tables `customer_knowledge_transformed` ou `email_bodies_transformed` n'existent pas

**Solutions** :
1. Vérifier que la preview **Shortcut Transformations AI** est activée
2. Vérifier que les fichiers .txt sont bien présents dans `Files/raw/text/`
3. Réessayer la transformation manuellement
4. Vérifier les quotas du tenant (limitations preview)
5. Pour les 20 000 fichiers customer knowledge notes, vérifier que le traitement ne timeout pas (peut nécessiter de traiter par batch)

**Alternative** : Créer une table simplifiée manuellement avec un Notebook :

```python
import os
from pyspark.sql.types import StructType, StructField, StringType

# Lire tous les fichiers customer knowledge notes
notes = []
files_path = "/lakehouse/default/Files/raw/text/customer_knowledge_notes/"

for file in os.listdir(files_path):
    if file.endswith(".txt"):
        with open(os.path.join(files_path, file), "r", encoding="utf-8") as f:
            content = f.read()
            customer_id = file.replace(".txt", "")
            notes.append({
                "customer_id": customer_id,
                "content": content,
                "summary": "Manual summary",  # À générer avec Azure OpenAI si besoin
                "sentiment": "neutral"  # À calculer
            })

# Créer DataFrame et table Delta
schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("content", StringType(), True),
    StructField("summary", StringType(), True),
    StructField("sentiment", StringType(), True)
])

df = spark.createDataFrame(notes, schema)
df.write.format("delta").mode("overwrite").saveAsTable("customer_knowledge_transformed")
```

---

### Problème : Le Data Agent ne répond pas correctement

**Symptômes** : Réponses incohérentes ou erreurs

**Solutions** :
1. Vérifier que le Semantic Model est publié (statut "Active")
2. Vérifier les relations entre tables (doivent être correctes)
3. Vérifier que toutes les mesures DAX sont bien calculées (pas d'erreur)
4. Simplifier la question (utiliser des termes exacts des colonnes)
5. Consulter les instructions du Data Agent et ajuster si nécessaire
6. Vérifier les logs d'erreur dans **Monitoring**

**Exemple** :
- ❌ "Quel est le taux de conversion des emails ?" (ambigu : click ou order ?)
- ✅ "Quel est le taux de clic des emails ?" (terme exact : `Click Rate %`)

---

### Problème : Erreurs de type de données

**Symptômes** : Les dates sont en texte, les calculs échouent

**Solutions** :
1. Réimporter les CSV avec `inferSchema=True` (Notebook)
2. Caster manuellement les colonnes :

```python
from pyspark.sql.functions import to_timestamp, col

# Corriger les timestamps des orders
df = spark.table("orders")
df = df.withColumn("order_date", to_timestamp(col("order_date"), "yyyy-MM-dd HH:mm:ss"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("orders")

# Corriger les timestamps des marketing_sends
df = spark.table("marketing_sends")
df = df.withColumn("sent_at", to_timestamp(col("sent_at"), "yyyy-MM-dd HH:mm:ss"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("marketing_sends")

# Corriger les timestamps des crm_interactions
df = spark.table("crm_interactions")
df = df.withColumn("occurred_at", to_timestamp(col("occurred_at"), "yyyy-MM-dd HH:mm:ss"))
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("crm_interactions")
```

3. Vérifier l'encodage UTF-8 des CSV (pas de BOM)

---

### Problème : Relations Many-to-Many non supportées

**Symptômes** : Erreur lors de la création de relations entre `crm_customer_segments` et autres tables

**Solution** :
Les relations Many-to-Many sont supportées dans les Semantic Models récents. Si vous rencontrez des problèmes :
1. Vérifier que vous utilisez la dernière version du Semantic Model
2. Créer des tables de pont (bridge tables) si nécessaire
3. Utiliser des relations inactives et les activer dans les mesures DAX avec `USERELATIONSHIP()`

---

### Problème : Performance lente du Data Agent

**Symptômes** : Réponses lentes (>30 secondes)

**Solutions** :
1. Optimiser les mesures DAX (éviter les calculs complexes en nested)
2. Créer des agrégations (aggregations) dans le Semantic Model
3. Réduire le nombre de tables exposées au Data Agent
4. Vérifier que les index Delta sont à jour
5. Utiliser des tables précalculées pour les KPIs principaux

---

### Problème : Permissions insuffisantes

**Symptômes** : "Access denied" ou "Not authorized"

**Solutions** :
1. Vérifier que vous êtes **Admin** ou **Member** du workspace
2. Vérifier les permissions sur le Lakehouse (doit être partagé)
3. Vérifier les permissions sur le Semantic Model (hérite du workspace par défaut)
4. Vérifier que la licence Fabric est active

---

## 📚 Ressources Complémentaires

- [Documentation OneLake Shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts)
- [AI Transformations in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/ai-transformations)
- [Fabric Data Agent (Copilot)](https://learn.microsoft.com/en-us/fabric/data-science/data-agent)
- [Semantic Model Best Practices](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- [DAX Formulas Reference](https://learn.microsoft.com/en-us/dax/)
- [Marketing Analytics Patterns](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema#marketing-analytics)

---

## ✅ Checklist de Déploiement

Cochez au fur et à mesure :

- [ ] Lakehouse créé
- [ ] Données uploadées (15 CSV + 20 060 fichiers texte)
- [ ] OneLake Shortcuts créés (optionnel)
- [ ] AI Transformations appliquées sur customer knowledge notes
- [ ] AI Transformations appliquées sur email bodies
- [ ] 17 tables Delta créées et vérifiées (15 CSV + 2 AI)
- [ ] Semantic Model créé
- [ ] Relations CRM définies (5 relations)
- [ ] Relations Marketing définies (7 relations)
- [ ] Relations Commerce définies (4 relations)
- [ ] Relations AI Transformed définies (2 relations)
- [ ] Mesures DAX ajoutées (CRM, Marketing, Commerce, Attribution)
- [ ] Data Agent configuré
- [ ] Instructions du Data Agent ajoutées
- [ ] Questions de test validées (≥80%)
- [ ] Dashboard Power BI créé (3 pages)
- [ ] Permissions partagées (si nécessaire)

**Si toutes les cases sont cochées, la démo est prête ! 🚀**

---

## 💡 Cas d'Usage Avancés

### Analyse d'Attribution Marketing

Utiliser les données pour répondre à :
- Quelle campagne a le meilleur ROI ?
- Quel segment répond le mieux aux emails ?
- Les tests A/B apportent-ils de la valeur ?
- Quel est le délai moyen entre l'email et l'achat ?

**Requête exemple** :
```sql
-- Attribution last-touch : orders dans les 7 jours après un clic email
SELECT 
    mc.campaign_name,
    COUNT(DISTINCT o.order_id) AS attributed_orders,
    SUM(ol.total_price) AS attributed_revenue,
    mc.budget_eur,
    (SUM(ol.total_price) - mc.budget_eur) / mc.budget_eur * 100 AS roi_pct
FROM marketing_campaigns mc
JOIN marketing_sends ms ON mc.campaign_id = ms.campaign_id
JOIN marketing_events me ON ms.send_id = me.send_id AND me.event_type = 'click'
JOIN orders o ON ms.customer_id = o.customer_id 
    AND o.order_date BETWEEN me.occurred_at AND DATEADD(day, 7, me.occurred_at)
JOIN order_lines ol ON o.order_id = ol.order_id
GROUP BY mc.campaign_name, mc.budget_eur
ORDER BY roi_pct DESC;
```

### Analyse de Sentiment des Notes Clients

Utiliser `customer_knowledge_transformed` pour :
- Identifier les clients mécontents (sentiment négatif)
- Prioriser les interventions CRM
- Corréler sentiment et churn risk

**Requête exemple** :
```sql
-- Clients avec sentiment négatif ET churn risk élevé
SELECT 
    c.customer_id,
    c.lifecycle_stage,
    cp.churn_risk_score,
    ck.sentiment,
    ck.summary,
    cp.total_spend_eur
FROM crm_customers c
JOIN crm_customer_profile cp ON c.customer_id = cp.customer_id
JOIN customer_knowledge_transformed ck ON c.customer_id = ck.customer_id
WHERE ck.sentiment = 'negative'
  AND cp.churn_risk_score > 70
ORDER BY cp.total_spend_eur DESC;
```

### Optimisation des Email Templates

Utiliser `email_bodies_transformed` pour :
- Analyser le sentiment des emails
- Identifier les key phrases qui performent
- Tester l'impact du tone sur l'engagement

**Requête exemple** :
```sql
-- Corrélation entre sentiment de l'email et taux de clic
SELECT 
    ma.asset_name,
    eb.sentiment,
    COUNT(DISTINCT ms.send_id) AS total_sends,
    COUNT(DISTINCT CASE WHEN me.event_type = 'click' THEN me.send_id END) AS total_clicks,
    COUNT(DISTINCT CASE WHEN me.event_type = 'click' THEN me.send_id END) * 100.0 / COUNT(DISTINCT ms.send_id) AS click_rate_pct
FROM marketing_assets ma
JOIN email_bodies_transformed eb ON ma.asset_id = eb.asset_id
JOIN marketing_sends ms ON ma.asset_id = ms.asset_id
LEFT JOIN marketing_events me ON ms.send_id = me.send_id
GROUP BY ma.asset_name, eb.sentiment
ORDER BY click_rate_pct DESC;
```

---

**Happy deploying! 🎯📧**

*Ce guide a été créé pour Microsoft Fabric et optimisé pour les démos marketing.*
