"""
Customer 360 + CRM + Marketing Campaigns + Purchases - Data Generator

Génère des données synthétiques pour démo Microsoft Fabric :
- 6 tables CRM (accounts, customers, segments, customer_segments, interactions, customer_profile)
- 5 tables Marketing (campaigns, assets, audiences, sends, events)
- 4 tables Commerce (products, orders, order_lines, returns)
- Corpus texte : customer knowledge notes + email bodies

Auteur : Microsoft Fabric Demo
Date : 2026-01-28
"""

import os
import random
import yaml
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

class Customer360DataGenerator:
    def __init__(self, config_path='config.yaml'):
        """Initialisation du générateur avec configuration YAML"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Seed pour reproductibilité
        seed = self.config.get('random_seed', 42)
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
        
        self.fake = Faker(['fr_FR', 'en_US'])
        
        # Dates de référence
        self.start_date = datetime.strptime(self.config['time_range']['start_date'], '%Y-%m-%d')
        self.end_date = datetime.strptime(self.config['time_range']['end_date'], '%Y-%m-%d')
        
        # Stockage temporaire pour relations
        self.accounts = []
        self.customers = []
        self.segments = []
        self.campaigns = []
        self.assets = []
        self.products = []
        self.orders = []
        self.sends = []
    
    # ========== CRM Tables ==========
    
    def generate_crm_accounts(self):
        """Génère les comptes CRM (B2B)"""
        print("Generating CRM accounts...")
        accounts = []
        industries = self.config['business_params']['account_industries']
        tiers = self.config['business_params']['account_tiers']
        regions = self.config['business_params']['regions']
        
        for i in range(self.config['volumes']['accounts']):
            industry = random.choices(
                [ind['name'] for ind in industries],
                weights=[ind['weight'] for ind in industries]
            )[0]
            
            tier_info = random.choices(
                tiers,
                weights=[t['weight'] for t in tiers]
            )[0]
            
            created_at = self.start_date - timedelta(days=random.randint(30, 730))
            
            account = {
                'account_id': f'ACC_{i+1:06d}',
                'account_name': self.fake.company(),
                'industry': industry,
                'region': random.choice(regions),
                'tier': tier_info['tier'],
                'employee_count': random.randint(*tier_info['employee_range']),
                'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'status': random.choice(['active', 'active', 'active', 'inactive']),
                'annual_revenue_eur': random.randint(100000, 50000000) if tier_info['tier'] != 'smb' else random.randint(50000, 1000000)
            }
            accounts.append(account)
        
        self.accounts = accounts
        df = pd.DataFrame(accounts)
        df.to_csv('../data/raw/crm/crm_accounts.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(accounts)} accounts")
        return df
    
    def generate_crm_customers(self):
        """Génère les clients (contacts B2C/B2B)"""
        print("Generating CRM customers...")
        customers = []
        lifecycle_stages = self.config['business_params']['customer_lifecycle_stages']
        channels = self.config['business_params']['preferred_channels']
        consent_email_rate = self.config['business_params']['consent_email_rate']
        consent_sms_rate = self.config['business_params']['consent_sms_rate']
        
        for i in range(self.config['volumes']['customers']):
            account_id = random.choice(self.accounts)['account_id'] if random.random() < 0.30 else None  # 30% B2B
            
            lifecycle = random.choices(
                [stage['stage'] for stage in lifecycle_stages],
                weights=[stage['weight'] for stage in lifecycle_stages]
            )[0]
            
            first_seen = self.start_date - timedelta(days=random.randint(0, 365))
            
            customer = {
                'customer_id': f'CUST_{i+1:06d}',
                'account_id': account_id,
                'email': self.fake.email(),
                'first_seen_at': first_seen.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'active' if lifecycle in ['lead', 'prospect', 'active', 'at_risk'] else 'churned',
                'locale': random.choice(['fr_FR', 'en_US', 'de_DE', 'es_ES']),
                'lifecycle_stage': lifecycle,
                'consent_email': random.random() < consent_email_rate,
                'consent_sms': random.random() < consent_sms_rate,
                'preferred_channel': random.choice(channels),
                'country': random.choice(['France', 'USA', 'Germany', 'Spain', 'UK'])
            }
            customers.append(customer)
        
        self.customers = customers
        df = pd.DataFrame(customers)
        df.to_csv('../data/raw/crm/crm_customers.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(customers)} customers")
        return df
    
    def generate_crm_segments(self):
        """Génère les segments clients"""
        print("Generating CRM segments...")
        segments = []
        
        segment_definitions = [
            ("High Value", "Customers with CLV > 10K EUR"),
            ("Frequent Buyers", "Purchased 5+ times in last 6 months"),
            ("At Risk", "Churn risk > 60%"),
            ("New Leads", "First seen < 30 days"),
            ("Enterprise Accounts", "Enterprise tier accounts"),
            ("Email Engagers", "Open rate > 40%"),
            ("Mobile Shoppers", "Primarily mobile channel"),
            ("Product - Electronics Fans", "70%+ purchases in Electronics"),
            ("Product - Fashion Lovers", "70%+ purchases in Clothing"),
            ("Low NPS", "NPS score < 6"),
            ("High NPS", "NPS score >= 9"),
            ("Inactive 90d", "No activity in last 90 days"),
            ("VIP", "CLV > 20K EUR + NPS >= 9"),
            ("Discount Seekers", "Always use promo codes"),
            ("Cart Abandoners", "High cart abandonment rate"),
            ("Returns Frequent", "Return rate > 25%"),
            ("B2B SMB", "SMB tier business accounts"),
            ("B2B Enterprise", "Enterprise tier business accounts"),
            ("EMEA Region", "EMEA region customers"),
            ("Americas Region", "Americas region customers"),
            ("APAC Region", "APAC region customers"),
            ("French Speakers", "Locale = fr_FR"),
            ("English Speakers", "Locale = en_US"),
            ("Recent Joiners", "Joined in last 3 months"),
            ("Loyalists", "Active for 12+ months"),
            ("Multi-Channel", "Use 3+ channels"),
            ("Support Heavy Users", "10+ support tickets"),
            ("Never Purchased", "Leads/Prospects with 0 orders"),
            ("One-Time Buyers", "Exactly 1 order"),
            ("Winback Targets", "Churned < 6 months ago"),
            ("Engagement Champions", "Click rate > 20%"),
            ("Bounce Prone", "Bounce rate > 5%"),
            ("Unsubscribe Risk", "Fatigue score high"),
            ("Campaign Responders", "Converted from campaign"),
            ("Organic Customers", "No campaign attribution"),
            ("Holiday Shoppers", "Active Nov-Dec"),
            ("Weekend Browsers", "Activity on weekends"),
            ("Tech Savvy", "Mobile app users"),
            ("Price Sensitive", "Average discount > 15%"),
            ("Premium Buyers", "Average order > 500 EUR")
        ]
        
        for i in range(self.config['volumes']['segments']):
            name, description = segment_definitions[i % len(segment_definitions)]
            segment = {
                'segment_id': f'SEG_{i+1:03d}',
                'segment_name': name,
                'description': description,
                'created_at': (self.start_date - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d %H:%M:%S'),
                'is_active': True
            }
            segments.append(segment)
        
        self.segments = segments
        df = pd.DataFrame(segments)
        df.to_csv('../data/raw/crm/crm_segments.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(segments)} segments")
        return df
    
    def generate_crm_customer_segments(self):
        """Associe clients aux segments"""
        print("Generating customer-segment mappings...")
        mappings = []
        
        # Chaque client appartient à 2-5 segments
        for customer in self.customers:
            num_segments = random.randint(2, 5)
            customer_segments = random.sample(self.segments, num_segments)
            
            for seg in customer_segments:
                start_date = datetime.strptime(customer['first_seen_at'], '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(0, 30))
                end_date = None if random.random() < 0.80 else (start_date + timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d %H:%M:%S')
                
                mapping = {
                    'customer_id': customer['customer_id'],
                    'segment_id': seg['segment_id'],
                    'start_date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_date': end_date
                }
                mappings.append(mapping)
        
        df = pd.DataFrame(mappings)
        df.to_csv('../data/raw/crm/crm_customer_segments.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(mappings)} customer-segment mappings")
        return df
    
    def generate_crm_interactions(self):
        """Génère les interactions CRM"""
        print("Generating CRM interactions...")
        interactions = []
        interaction_types = self.config['business_params']['interaction_types']
        
        for i in range(self.config['volumes']['interactions']):
            customer = random.choice(self.customers)
            interaction_type_info = random.choices(
                interaction_types,
                weights=[it['weight'] for it in interaction_types]
            )[0]
            
            occurred_at = self.fake.date_time_between(start_date=self.start_date, end_date=self.end_date)
            
            satisfaction = random.randint(*interaction_type_info['satisfaction_range']) if random.random() < 0.70 else None
            
            interaction = {
                'interaction_id': f'INT_{i+1:08d}',
                'customer_id': customer['customer_id'],
                'type': interaction_type_info['type'],
                'channel': customer['preferred_channel'],
                'occurred_at': occurred_at.strftime('%Y-%m-%d %H:%M:%S'),
                'topic': random.choice(['billing', 'technical', 'product', 'account', 'feature', 'pricing']),
                'outcome': random.choice(['resolved', 'pending', 'escalated', 'closed']),
                'satisfaction_score': satisfaction,
                'duration_min': random.randint(5, 60) if interaction_type_info['type'] in ['support_ticket', 'sales_call'] else None
            }
            interactions.append(interaction)
        
        df = pd.DataFrame(interactions)
        df.to_csv('../data/raw/crm/crm_interactions.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(interactions)} interactions")
        return df
    
    def generate_crm_customer_profile(self):
        """Génère les profils clients enrichis (scores, KPIs)"""
        print("Generating customer profiles...")
        profiles = []
        churn_dist = self.config['business_params']['churn_risk_distribution']
        clv_params = self.config['business_params']['clv_distribution']
        nps_dist = self.config['business_params']['nps_distribution']
        
        for customer in self.customers:
            churn_category = random.choices(
                [cr['risk'] for cr in churn_dist],
                weights=[cr['weight'] for cr in churn_dist]
            )[0]
            churn_score = random.randint(*[cr['score_range'] for cr in churn_dist if cr['risk'] == churn_category][0])
            
            # CLV basé sur lifecycle
            clv_base = np.random.normal(clv_params['mean'], clv_params['std'])
            if customer['lifecycle_stage'] in ['lead', 'prospect']:
                clv_base *= 0.3
            elif customer['lifecycle_stage'] == 'churned':
                clv_base *= 0.5
            elif customer['lifecycle_stage'] == 'at_risk':
                clv_base *= 0.7
            clv_score = max(clv_params['min'], min(clv_params['max'], clv_base))
            
            # NPS
            rand_nps = random.random() * 100
            if rand_nps < nps_dist['detractors']:
                nps = random.randint(0, 6)
            elif rand_nps < nps_dist['detractors'] + nps_dist['passives']:
                nps = random.randint(7, 8)
            else:
                nps = random.randint(9, 10)
            
            last_contact = self.fake.date_time_between(start_date=self.start_date, end_date=self.end_date)
            
            profile = {
                'customer_id': customer['customer_id'],
                'churn_risk_score': churn_score,
                'clv_score': round(clv_score, 2),
                'nps_last': nps,
                'last_contact_at': last_contact.strftime('%Y-%m-%d %H:%M:%S'),
                'total_interactions': random.randint(0, 20),
                'total_orders': 0,  # Will be updated later
                'total_spend_eur': 0.0,  # Will be updated later
                'avg_order_value_eur': 0.0,
                'open_rate_pct': round(random.uniform(0.05, 0.50), 3),
                'click_rate_pct': round(random.uniform(0.01, 0.20), 3)
            }
            profiles.append(profile)
        
        df = pd.DataFrame(profiles)
        df.to_csv('../data/raw/crm/crm_customer_profile.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(profiles)} customer profiles")
        return df
    
    # ========== Marketing Tables ==========
    
    def generate_marketing_campaigns(self):
        """Génère les campagnes marketing"""
        print("Generating marketing campaigns...")
        campaigns = []
        objectives = self.config['business_params']['campaign_objectives']
        budget_range = self.config['business_params']['campaign_budget_range']
        ab_test_rate = self.config['business_params']['ab_test_rate']
        campaign_duration = self.config['time_range']['campaign_duration_days_avg']
        
        for i in range(self.config['volumes']['campaigns']):
            start_date = self.start_date + timedelta(days=random.randint(0, 300))
            duration = random.randint(campaign_duration - 10, campaign_duration + 20)
            end_date = start_date + timedelta(days=duration)
            
            objective = random.choice(objectives)
            ab_test = random.random() < ab_test_rate
            
            campaign = {
                'campaign_id': f'CAMP_{i+1:03d}',
                'campaign_name': f"{objective.capitalize()} Campaign {self.fake.catch_phrase()}",
                'objective': objective,
                'start_date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end_date': end_date.strftime('%Y-%m-%d %H:%M:%S'),
                'budget_eur': random.randint(budget_range['min'], budget_range['max']),
                'channel': 'email',  # Focus email pour cette démo
                'ab_test_flag': ab_test,
                'status': 'completed' if end_date < self.end_date else 'active'
            }
            campaigns.append(campaign)
        
        self.campaigns = campaigns
        df = pd.DataFrame(campaigns)
        df.to_csv('../data/raw/marketing/marketing_campaigns.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(campaigns)} campaigns")
        return df
    
    def generate_marketing_assets(self):
        """Génère les assets marketing (email templates)"""
        print("Generating marketing assets...")
        assets = []
        languages = self.config['business_params']['email_languages']
        subject_templates = self.config['text_templates']['email_subject_templates']
        assets_per_campaign = self.config['volumes']['assets_per_campaign']
        
        asset_id = 1
        for campaign in self.campaigns:
            num_assets = 2 if campaign['ab_test_flag'] else 1
            num_assets = min(num_assets, assets_per_campaign)
            
            for variant_idx in range(num_assets):
                variant = chr(65 + variant_idx)  # A, B, C...
                
                objective = campaign['objective']
                subjects = subject_templates.get(objective, subject_templates['engagement'])
                subject = random.choice(subjects)
                
                # Personnalisation du subject
                subject = subject.replace('{month}', random.choice(['janvier', 'février', 'mars']))
                subject = subject.replace('{discount}', str(random.choice([10, 15, 20, 25])))
                subject = subject.replace('{name}', '{customer_name}')  # Template variable
                subject = subject.replace('{brand}', 'BrandCo')
                
                asset = {
                    'asset_id': f'ASSET_{asset_id:05d}',
                    'campaign_id': campaign['campaign_id'],
                    'asset_type': 'email_template',
                    'subject': subject,
                    'language': random.choice(languages),
                    'variant': variant if campaign['ab_test_flag'] else None,
                    'created_at': (datetime.strptime(campaign['start_date'], '%Y-%m-%d %H:%M:%S') - timedelta(days=random.randint(5, 15))).strftime('%Y-%m-%d %H:%M:%S')
                }
                assets.append(asset)
                asset_id += 1
        
        self.assets = assets
        df = pd.DataFrame(assets)
        df.to_csv('../data/raw/marketing/marketing_assets.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(assets)} assets")
        return df
    
    def generate_marketing_audiences(self):
        """Génère les audiences (lien campagnes ↔ segments)"""
        print("Generating marketing audiences...")
        audiences = []
        
        for i, campaign in enumerate(self.campaigns):
            # Chaque campagne cible 1-3 segments
            num_segments = random.randint(1, 3)
            targeted_segments = random.sample(self.segments, num_segments)
            
            for seg in targeted_segments:
                audience = {
                    'audience_id': f'AUD_{i+1:03d}_{seg["segment_id"]}',
                    'campaign_id': campaign['campaign_id'],
                    'segment_id': seg['segment_id'],
                    'criteria_json': f'{{"segment": "{seg["segment_name"]}", "min_clv": {random.randint(1000, 5000)}}}'
                }
                audiences.append(audience)
        
        df = pd.DataFrame(audiences)
        df.to_csv('../data/raw/marketing/marketing_audiences.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(audiences)} audiences")
        return df
    
    def generate_marketing_sends(self):
        """Génère les envois d'emails"""
        print("Generating marketing sends...")
        sends = []
        send_id = 1
        
        # Pour chaque campagne, envoyer aux clients des segments ciblés
        for campaign in self.campaigns:
            campaign_start = datetime.strptime(campaign['start_date'], '%Y-%m-%d %H:%M:%S')
            campaign_end = datetime.strptime(campaign['end_date'], '%Y-%m-%d %H:%M:%S')
            
            # Trouver les segments ciblés
            campaign_assets = [a for a in self.assets if a['campaign_id'] == campaign['campaign_id']]
            
            if not campaign_assets:
                continue
            
            # Sélectionner un sous-ensemble aléatoire de clients (pas tous)
            num_sends = random.randint(5000, 15000)
            num_sends = min(num_sends, len(self.customers))
            
            customers_to_send = random.sample(self.customers, num_sends)
            
            for customer in customers_to_send:
                # Respecter le consentement email
                if not customer['consent_email']:
                    continue
                
                # Assigner un asset (A/B test)
                asset = random.choice(campaign_assets)
                
                send_at = self.fake.date_time_between(start_date=campaign_start, end_date=campaign_end)
                
                send = {
                    'send_id': f'SEND_{send_id:08d}',
                    'campaign_id': campaign['campaign_id'],
                    'asset_id': asset['asset_id'],
                    'customer_id': customer['customer_id'],
                    'send_at': send_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                sends.append(send)
                send_id += 1
                
                if send_id > self.config['volumes']['sends']:
                    break
            
            if send_id > self.config['volumes']['sends']:
                break
        
        self.sends = sends[:self.config['volumes']['sends']]  # Cap au volume configuré
        df = pd.DataFrame(self.sends)
        df.to_csv('../data/raw/marketing/marketing_sends.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(self.sends)} sends")
        return df
    
    def generate_marketing_events(self):
        """Génère les événements marketing (open, click, bounce, unsubscribe)"""
        print("Generating marketing events...")
        events = []
        event_rates = self.config['business_params']['marketing_event_rates']
        ab_lift = self.config['business_params']['ab_test_lift']
        cta_templates = self.config['text_templates']['email_cta_templates']
        
        event_id = 1
        
        for send in self.sends:
            send_time = datetime.strptime(send['send_at'], '%Y-%m-%d %H:%M:%S')
            
            # Récupérer l'asset pour savoir si c'est variant A ou B
            asset = next((a for a in self.assets if a['asset_id'] == send['asset_id']), None)
            is_variant_b = asset and asset['variant'] == 'B'
            
            # Ajuster les taux selon variant
            open_rate = event_rates['open_rate_baseline']
            click_rate = event_rates['click_rate_baseline']
            
            if is_variant_b:
                open_rate *= (1 + random.uniform(*ab_lift['open_lift_range']))
                click_rate *= (1 + random.uniform(*ab_lift['click_lift_range']))
            
            # Bounce event
            if random.random() < event_rates['bounce_rate']:
                bounce_event = {
                    'event_id': f'EVT_{event_id:08d}',
                    'send_id': send['send_id'],
                    'customer_id': send['customer_id'],
                    'event_type': 'bounce',
                    'event_at': send_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'url_clicked': None,
                    'device': None,
                    'user_agent': None
                }
                events.append(bounce_event)
                event_id += 1
                continue  # Pas d'autres events si bounce
            
            # Open event
            if random.random() < open_rate:
                open_time = send_time + timedelta(hours=random.randint(1, 48))
                open_event = {
                    'event_id': f'EVT_{event_id:08d}',
                    'send_id': send['send_id'],
                    'customer_id': send['customer_id'],
                    'event_type': 'open',
                    'event_at': open_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'url_clicked': None,
                    'device': random.choice(['desktop', 'mobile', 'tablet']),
                    'user_agent': self.fake.user_agent()
                }
                events.append(open_event)
                event_id += 1
                
                # Click event (conditionnel à open)
                if random.random() < click_rate:
                    click_time = open_time + timedelta(minutes=random.randint(1, 30))
                    click_event = {
                        'event_id': f'EVT_{event_id:08d}',
                        'send_id': send['send_id'],
                        'customer_id': send['customer_id'],
                        'event_type': 'click',
                        'event_at': click_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'url_clicked': f'https://example.com/promo/{random.choice(cta_templates).lower().replace(" ", "-")}',
                        'device': open_event['device'],
                        'user_agent': open_event['user_agent']
                    }
                    events.append(click_event)
                    event_id += 1
            
            # Unsubscribe event
            if random.random() < event_rates['unsubscribe_rate']:
                unsub_time = send_time + timedelta(days=random.randint(0, 7))
                unsub_event = {
                    'event_id': f'EVT_{event_id:08d}',
                    'send_id': send['send_id'],
                    'customer_id': send['customer_id'],
                    'event_type': 'unsubscribe',
                    'event_at': unsub_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'url_clicked': None,
                    'device': None,
                    'user_agent': None
                }
                events.append(unsub_event)
                event_id += 1
            
            if event_id > self.config['volumes']['events']:
                break
        
        df = pd.DataFrame(events[:self.config['volumes']['events']])
        df.to_csv('../data/raw/marketing/marketing_events.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(events)} marketing events")
        return df
    
    # ========== Commerce Tables ==========
    
    def generate_products(self):
        """Génère le catalogue produits"""
        print("Generating products...")
        products = []
        categories = self.config['business_params']['product_categories']
        
        product_id = 1
        for category_info in categories:
            num_products = int(self.config['volumes']['products'] * category_info['weight'] / 100)
            
            for _ in range(num_products):
                price = random.uniform(*category_info['price_range'])
                margin_pct = random.uniform(*category_info['margin_range'])
                
                product = {
                    'product_id': f'PROD_{product_id:05d}',
                    'product_name': self.fake.catch_phrase(),
                    'category': category_info['category'],
                    'brand': self.fake.company(),
                    'price_eur': round(price, 2),
                    'margin_pct': round(margin_pct, 3),
                    'sku': self.fake.bothify(text='??-####-??'),
                    'in_stock': random.choice([True, True, True, False])
                }
                products.append(product)
                product_id += 1
        
        self.products = products
        df = pd.DataFrame(products)
        df.to_csv('../data/raw/commerce/products.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(products)} products")
        return df
    
    def generate_orders(self):
        """Génère les commandes avec attribution marketing"""
        print("Generating orders...")
        orders = []
        channels = self.config['business_params']['order_channels']
        conversion_baseline = self.config['business_params']['conversion_baseline']
        conversion_post_open = self.config['business_params']['conversion_post_open']
        conversion_post_click = self.config['business_params']['conversion_post_click']
        attribution_window = self.config['time_range']['attribution_window_days']
        promo_usage = self.config['business_params']['promo_code_usage']
        
        # Créer un mapping customer -> derniers events marketing
        customer_events = {}
        for send in self.sends:
            cust_id = send['customer_id']
            if cust_id not in customer_events:
                customer_events[cust_id] = []
            customer_events[cust_id].append({
                'send_id': send['send_id'],
                'campaign_id': send['campaign_id'],
                'send_at': datetime.strptime(send['send_at'], '%Y-%m-%d %H:%M:%S')
            })
        
        order_id = 1
        for customer in self.customers:
            # Nombre de commandes selon lifecycle
            if customer['lifecycle_stage'] in ['lead', 'prospect', 'churned']:
                num_orders = random.choices([0, 1], weights=[0.80, 0.20])[0]
            elif customer['lifecycle_stage'] == 'at_risk':
                num_orders = random.randint(1, 3)
            else:  # active
                num_orders = random.randint(2, 6)
            
            for _ in range(num_orders):
                order_at = self.fake.date_time_between(start_date=self.start_date, end_date=self.end_date)
                
                # Attribution marketing
                attributed_campaign = None
                if customer['customer_id'] in customer_events:
                    recent_sends = [
                        evt for evt in customer_events[customer['customer_id']]
                        if (order_at - evt['send_at']).days <= attribution_window and evt['send_at'] < order_at
                    ]
                    if recent_sends:
                        # Last touch attribution
                        last_touch = max(recent_sends, key=lambda x: x['send_at'])
                        attributed_campaign = last_touch['campaign_id']
                
                # Promo code usage
                promo_code = f'PROMO{random.randint(100, 999)}' if random.random() < promo_usage else None
                
                order = {
                    'order_id': f'ORD_{order_id:07d}',
                    'customer_id': customer['customer_id'],
                    'order_at': order_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'channel': random.choice(channels),
                    'total_amount_eur': 0.0,  # Will be calculated from order_lines
                    'promo_code': promo_code,
                    'attributed_campaign_id': attributed_campaign,
                    'status': random.choice(['completed', 'completed', 'completed', 'pending', 'canceled'])
                }
                orders.append(order)
                order_id += 1
                
                if order_id > self.config['volumes']['orders']:
                    break
            
            if order_id > self.config['volumes']['orders']:
                break
        
        self.orders = orders
        df = pd.DataFrame(orders)
        df.to_csv('../data/raw/commerce/orders.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(orders)} orders")
        return df
    
    def generate_order_lines(self):
        """Génère les lignes de commande"""
        print("Generating order lines...")
        order_lines = []
        discount_avg = self.config['business_params']['discount_rate_avg']
        lines_per_order = self.config['volumes']['order_lines_avg']
        
        line_id = 1
        order_totals = {}
        
        for order in self.orders:
            num_lines = random.randint(max(1, lines_per_order - 1), lines_per_order + 2)
            order_products = random.sample(self.products, min(num_lines, len(self.products)))
            
            order_total = 0.0
            
            for product in order_products:
                qty = random.randint(1, 5)
                unit_price = product['price_eur']
                discount = round(unit_price * random.uniform(0, discount_avg * 2) * qty, 2) if order['promo_code'] else 0.0
                
                line_total = (unit_price * qty) - discount
                order_total += line_total
                
                line = {
                    'order_line_id': f'LINE_{line_id:08d}',
                    'order_id': order['order_id'],
                    'product_id': product['product_id'],
                    'qty': qty,
                    'unit_price_eur': unit_price,
                    'discount_eur': discount,
                    'line_total_eur': round(line_total, 2)
                }
                order_lines.append(line)
                line_id += 1
            
            order_totals[order['order_id']] = round(order_total, 2)
        
        # Mettre à jour les totaux des commandes
        for order in self.orders:
            order['total_amount_eur'] = order_totals.get(order['order_id'], 0.0)
        
        # Re-sauvegarder orders avec totaux
        pd.DataFrame(self.orders).to_csv('../data/raw/commerce/orders.csv', index=False, encoding='utf-8')
        
        df = pd.DataFrame(order_lines)
        df.to_csv('../data/raw/commerce/order_lines.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(order_lines)} order lines")
        return df
    
    def generate_returns(self):
        """Génère les retours"""
        print("Generating returns...")
        returns = []
        return_reasons = self.config['business_params']['return_reasons']
        
        # ~17% des commandes ont un retour
        orders_to_return = random.sample(self.orders, min(self.config['volumes']['returns'], len(self.orders)))
        
        for i, order in enumerate(orders_to_return):
            order_date = datetime.strptime(order['order_at'], '%Y-%m-%d %H:%M:%S')
            return_date = order_date + timedelta(days=random.randint(1, 30))
            
            reason_info = random.choices(
                return_reasons,
                weights=[r['weight'] for r in return_reasons]
            )[0]
            
            # Montant remboursé = partiel ou total
            refund = order['total_amount_eur'] * random.uniform(0.50, 1.0)
            
            ret = {
                'return_id': f'RET_{i+1:06d}',
                'order_id': order['order_id'],
                'customer_id': order['customer_id'],
                'created_at': return_date.strftime('%Y-%m-%d %H:%M:%S'),
                'reason': reason_info['reason'],
                'amount_refunded_eur': round(refund, 2),
                'status': random.choice(['approved', 'approved', 'pending', 'rejected'])
            }
            returns.append(ret)
        
        df = pd.DataFrame(returns)
        df.to_csv('../data/raw/commerce/returns.csv', index=False, encoding='utf-8')
        print(f"✅ Generated {len(returns)} returns")
        return df
    
    # ========== Text Corpus ==========
    
    def generate_customer_knowledge_notes(self):
        """Génère les notes CRM en .txt"""
        print("Generating customer knowledge notes (.txt)...")
        output_dir = Path('../data/raw/text/customer_knowledge_notes')
        topics = self.config['text_templates']['customer_note_topics']
        sentiments_info = self.config['text_templates']['customer_note_sentiments']
        
        # Générer pour un sous-ensemble de clients (20 000 max)
        customers_to_generate = random.sample(self.customers, min(self.config['volumes']['customer_notes'], len(self.customers)))
        
        for customer in customers_to_generate:
            sentiment_info = random.choices(
                sentiments_info,
                weights=[s['weight'] for s in sentiments_info]
            )[0]
            sentiment = sentiment_info['sentiment']
            topic = random.choice(topics)
            
            # Fake PII for demo (redaction)
            fake_phone = self.fake.phone_number()
            fake_email = customer['email']
            
            # Template de note
            note_content = f"""CUSTOMER_ID: {customer['customer_id']}
DATE: {self.fake.date_this_year().strftime('%Y-%m-%d')}
TOPIC: {topic}
LANGUAGE: fr
SENTIMENT: {sentiment}
TAGS: crm, customer_knowledge, {topic.replace('_', ' ')}

--- BEGIN NOTE ---

{self._generate_note_text(customer, topic, sentiment, fake_phone, fake_email)}

--- END NOTE ---
"""
            
            filename = output_dir / f"{customer['customer_id']}.txt"
            filename.write_text(note_content, encoding='utf-8')
        
        print(f"✅ Generated {len(customers_to_generate)} customer knowledge notes")
    
    def _generate_note_text(self, customer, topic, sentiment, phone, email):
        """Génère le texte de la note CRM"""
        if sentiment == 'positive':
            templates = [
                f"Le client {customer['customer_id']} s'est montré très satisfait de nos services. Discussion constructive autour de {topic.replace('_', ' ')}. A mentionné une préférence pour le canal {customer['preferred_channel']}. Contact : {email} / {phone}. Opportunité d'upsell identifiée.",
                f"Excellent échange avec le client. Thème principal : {topic.replace('_', ' ')}. Le client apprécie particulièrement notre réactivité. Coordonnées : {email}, {phone}. Prochaine étape : follow-up dans 2 semaines.",
                f"Interaction très positive. Client loyal, segment premium probable. Sujet : {topic.replace('_', ' ')}. Mentionné intérêt pour nos nouveaux produits. Email : {email}, téléphone : {phone}."
            ]
        elif sentiment == 'neutral':
            templates = [
                f"Échange standard avec {customer['customer_id']}. Sujet : {topic.replace('_', ' ')}. Pas de problème majeur signalé. Canal préféré : {customer['preferred_channel']}. Contact : {email} ou {phone}.",
                f"Note de routine. Le client a posé quelques questions sur {topic.replace('_', ' ')}. Réponses fournies. Coordonnées : {email} / {phone}. RAS.",
                f"Interaction neutre, demande d'information basique. Thème : {topic.replace('_', ' ')}. Client semble satisfait mais pas enthousiaste. Email : {email}, tel : {phone}."
            ]
        else:  # negative
            templates = [
                f"⚠️ Problème signalé par {customer['customer_id']}. Sujet : {topic.replace('_', ' ')}. Client mécontent. Escalade nécessaire. Contact urgent : {email} / {phone}. Action corrective requise.",
                f"Interaction difficile. Le client exprime des frustrations concernant {topic.replace('_', ' ')}. Risque de churn élevé. Coordonnées : {email}, {phone}. Proposition de geste commercial à valider.",
                f"Note d'alerte : insatisfaction client. Thème : {topic.replace('_', ' ')}. Plusieurs tentatives de contact sans succès. Email : {email}, téléphone : {phone}. Superviseur à impliquer."
            ]
        
        return random.choice(templates)
    
    def generate_email_bodies(self):
        """Génère les corps d'emails marketing en .txt"""
        print("Generating email bodies (.txt)...")
        output_dir = Path('../data/raw/text/email_bodies')
        cta_templates = self.config['text_templates']['email_cta_templates']
        
        for asset in self.assets:
            # Récupérer la campagne associée
            campaign = next((c for c in self.campaigns if c['campaign_id'] == asset['campaign_id']), None)
            if not campaign:
                continue
            
            objective = campaign['objective']
            variant = asset['variant'] or 'A'
            
            # Template email selon objectif
            email_body = f"""ASSET_ID: {asset['asset_id']}
CAMPAIGN_ID: {asset['campaign_id']}
DATE: {asset['created_at']}
LANGUAGE: {asset['language']}
VARIANT: {variant}
SUBJECT: {asset['subject']}

--- BEGIN EMAIL ---

Bonjour {{{{customer_name}}}},

{self._generate_email_text(objective, variant)}

{random.choice(cta_templates).upper()}

Cordialement,
L'équipe BrandCo

---
Pour vous désabonner, cliquez ici : {{{{unsubscribe_link}}}}
---

--- END EMAIL ---
"""
            
            filename = output_dir / f"{asset['asset_id']}.txt"
            filename.write_text(email_body, encoding='utf-8')
        
        print(f"✅ Generated {len(self.assets)} email bodies")
    
    def _generate_email_text(self, objective, variant):
        """Génère le corps de l'email selon l'objectif"""
        if objective == 'acquisition':
            if variant == 'A':
                return "Nous sommes ravis de vous accueillir ! Découvrez notre catalogue complet et profitez de 15% de réduction sur votre première commande avec le code WELCOME15."
            else:
                return "Bienvenue dans la communauté BrandCo ! En exclusivité pour vous : -20% sur toute votre première commande avec NEWCLIENT20. Offre limitée à 48h."
        elif objective == 'retention':
            if variant == 'A':
                return "Vous nous manquez ! Voici une sélection personnalisée de produits qui pourraient vous plaire. Profitez de 10% de réduction avec le code BACKAGAIN."
            else:
                return "Ça fait longtemps ! Pour vous remercier de votre fidélité, nous vous offrons -15% sur votre prochaine commande. Code : LOYAL15."
        elif objective == 'upsell':
            if variant == 'A':
                return "Passez à la vitesse supérieure avec notre offre Premium. Fonctionnalités avancées, support prioritaire et remises exclusives vous attendent."
            else:
                return "Upgrade maintenant et bénéficiez de 30 jours d'essai gratuit de notre formule Premium. Sans engagement, annulation possible à tout moment."
        elif objective == 'winback':
            if variant == 'A':
                return "On vous a perdu ? Revenez et profitez d'une offre spéciale : -25% sur tout le site pendant 7 jours. Code : COMEBACK25."
            else:
                return "Vous nous avez manqué ! Voici un bon d'achat de 30€ valable sur votre prochaine commande. Utilisez le code MISSYOU30 avant le 31/12."
        else:  # engagement
            if variant == 'A':
                return "Participez à notre enquête de satisfaction et tentez de gagner un bon d'achat de 100€. Votre avis compte vraiment pour nous !"
            else:
                return "Dites-nous ce que vous pensez ! Répondez à notre sondage en 2 minutes et recevez -10% sur votre prochaine commande. Code : SURVEY10."
    
    # ========== Main Orchestration ==========
    
    def create_output_directories(self):
        """Crée tous les dossiers nécessaires pour la génération des données"""
        directories = [
            '../data/raw/crm',
            '../data/raw/marketing',
            '../data/raw/commerce',
            '../data/raw/text/customer_knowledge_notes',
            '../data/raw/text/email_bodies'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ Output directories created")
    
    def generate_all(self):
        """Génère toutes les données"""
        print("\n🚀 Starting Customer 360 data generation...\n")
        
        # Créer les dossiers de sortie
        self.create_output_directories()
        
        # CRM
        self.generate_crm_accounts()
        self.generate_crm_customers()
        self.generate_crm_segments()
        self.generate_crm_customer_segments()
        self.generate_crm_interactions()
        self.generate_crm_customer_profile()
        
        # Marketing
        self.generate_marketing_campaigns()
        self.generate_marketing_assets()
        self.generate_marketing_audiences()
        self.generate_marketing_sends()
        self.generate_marketing_events()
        
        # Commerce
        self.generate_products()
        self.generate_orders()
        self.generate_order_lines()
        self.generate_returns()
        
        # Text Corpus
        self.generate_customer_knowledge_notes()
        self.generate_email_bodies()
        
        print("\n✅ All data generated successfully!")
        print(f"\n📊 Summary:")
        print(f"  CRM: {len(self.accounts)} accounts, {len(self.customers)} customers, {len(self.segments)} segments")
        print(f"  Marketing: {len(self.campaigns)} campaigns, {len(self.assets)} assets, {len(self.sends)} sends")
        print(f"  Commerce: {len(self.products)} products, {len(self.orders)} orders")
        print(f"  Text: {self.config['volumes']['customer_notes']} notes, {len(self.assets)} email bodies")

if __name__ == '__main__':
    generator = Customer360DataGenerator('config.yaml')
    generator.generate_all()
