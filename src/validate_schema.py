"""
Script de Validation des Noms de Colonnes - Marketing Campaign Demo

Vérifie que tous les noms de colonnes correspondent au schéma attendu
et que les données sont cohérentes pour les DAX queries.

Usage:
    cd src
    python validate_schema.py
"""

import pandas as pd
import sys
from pathlib import Path

class SchemaValidator:
    def __init__(self, data_root='../data/raw'):
        self.data_root = Path(data_root)
        self.errors = []
        self.warnings = []
        
    def validate_all(self):
        """Exécute toutes les validations"""
        print("=" * 80)
        print("VALIDATION DES SCHEMAS - Marketing Campaign Demo")
        print("=" * 80)
        print()
        
        # Validation des tables CRM
        self.validate_crm_tables()
        
        # Validation des tables Marketing
        self.validate_marketing_tables()
        
        # Validation des tables Commerce
        self.validate_commerce_tables()
        
        # Validation des relations
        self.validate_relationships()
        
        # Afficher le résumé
        self.print_summary()
        
        return len(self.errors) == 0
    
    def validate_crm_tables(self):
        """Valide les tables CRM"""
        print("--- Validation CRM Tables ---")
        
        # crm_customers
        customers = self.load_csv('crm/crm_customers.csv')
        if customers is not None:
            self.check_columns(customers, 'crm_customers', [
                'customer_id', 'account_id', 'email', 'first_seen_at',
                'status', 'locale', 'lifecycle_stage', 'consent_email',
                'consent_sms', 'preferred_channel', 'country'
            ])
            
            # Vérifier que customer_id est au bon format
            sample_id = customers['customer_id'].iloc[0]
            if not sample_id.startswith('CUST_'):
                self.errors.append("crm_customers.customer_id doit être au format 'CUST_XXXXXX'")
        
        # crm_customer_profile
        profile = self.load_csv('crm/crm_customer_profile.csv')
        if profile is not None:
            self.check_columns(profile, 'crm_customer_profile', [
                'customer_id', 'churn_risk_score', 'clv_score', 'nps_last',
                'last_contact_at', 'total_interactions', 'total_orders',
                'total_spend_eur', 'avg_order_value_eur', 'open_rate_pct',
                'click_rate_pct'
            ])
        
        print()
    
    def validate_marketing_tables(self):
        """Valide les tables Marketing"""
        print("--- Validation Marketing Tables ---")
        
        # marketing_campaigns
        campaigns = self.load_csv('marketing/marketing_campaigns.csv')
        if campaigns is not None:
            self.check_columns(campaigns, 'marketing_campaigns', [
                'campaign_id', 'campaign_name', 'objective', 'start_date',
                'end_date', 'budget_eur', 'channel', 'ab_test_flag', 'status'
            ])
            
            # Vérifier format campaign_id
            sample_id = campaigns['campaign_id'].iloc[0]
            if not sample_id.startswith('CAMP_'):
                self.errors.append("marketing_campaigns.campaign_id doit être au format 'CAMP_XXX'")
        
        # marketing_sends
        sends = self.load_csv('marketing/marketing_sends.csv')
        if sends is not None:
            self.check_columns(sends, 'marketing_sends', [
                'send_id', 'campaign_id', 'asset_id', 'customer_id', 'send_at'
            ])
        
        # marketing_events (CRITIQUE pour DAX)
        events = self.load_csv('marketing/marketing_events.csv')
        if events is not None:
            self.check_columns(events, 'marketing_events', [
                'event_id', 'send_id', 'customer_id', 'event_type',
                'event_at', 'url_clicked', 'device', 'user_agent'
            ])
            
            # Vérifier event_type values (CRITIQUE)
            expected_types = {'open', 'click', 'bounce', 'unsubscribe'}
            actual_types = set(events['event_type'].unique())
            
            if expected_types != actual_types:
                self.errors.append(
                    f"marketing_events.event_type attendus: {expected_types}, "
                    f"trouvés: {actual_types}"
                )
            else:
                print(f"  ✅ marketing_events.event_type correct: {actual_types}")
        
        print()
    
    def validate_commerce_tables(self):
        """Valide les tables Commerce"""
        print("--- Validation Commerce Tables ---")
        
        # orders (CRITIQUE pour attribution)
        orders = self.load_csv('commerce/orders.csv')
        if orders is not None:
            self.check_columns(orders, 'orders', [
                'order_id', 'customer_id', 'order_at', 'channel',
                'total_amount_eur', 'promo_code', 'attributed_campaign_id', 'status'
            ])
            
            # Vérifier attributed_campaign_id (CRITIQUE)
            if 'attributed_campaign_id' not in orders.columns:
                self.errors.append(
                    "CRITIQUE: orders.attributed_campaign_id est MANQUANT ! "
                    "Cette colonne est essentielle pour les DAX queries."
                )
            else:
                print(f"  ✅ orders.attributed_campaign_id présent")
                
                # Vérifier la distribution (doit être ~91% NULL)
                null_pct = orders['attributed_campaign_id'].isna().sum() / len(orders)
                print(f"  ℹ️  Attribution: {null_pct*100:.1f}% organic (attendu: ~91%)")
                
                if null_pct < 0.85 or null_pct > 0.95:
                    self.warnings.append(
                        f"orders.attributed_campaign_id NULL rate = {null_pct*100:.1f}% "
                        f"(attendu ~91%). Vérifier la logique d'attribution."
                    )
        
        # order_lines
        lines = self.load_csv('commerce/order_lines.csv')
        if lines is not None:
            self.check_columns(lines, 'order_lines', [
                'order_line_id', 'order_id', 'product_id', 'qty',
                'unit_price_eur', 'discount_eur', 'line_total_eur'
            ])
        
        # products
        products = self.load_csv('commerce/products.csv')
        if products is not None:
            self.check_columns(products, 'products', [
                'product_id', 'product_name', 'category', 'brand',
                'price_eur', 'margin_pct', 'sku', 'in_stock'
            ])
        
        print()
    
    def validate_relationships(self):
        """Valide les relations entre tables (foreign keys)"""
        print("--- Validation Relations (Foreign Keys) ---")
        
        # Charger les tables principales
        customers = self.load_csv('crm/crm_customers.csv')
        campaigns = self.load_csv('marketing/marketing_campaigns.csv')
        orders = self.load_csv('commerce/orders.csv')
        sends = self.load_csv('marketing/marketing_sends.csv')
        
        if customers is None or campaigns is None or orders is None or sends is None:
            self.errors.append("Impossible de valider les relations: tables manquantes")
            return
        
        # Vérifier orders.customer_id → customers.customer_id
        invalid_customers = ~orders['customer_id'].isin(customers['customer_id'])
        if invalid_customers.any():
            self.errors.append(
                f"{invalid_customers.sum()} orders avec customer_id invalide"
            )
        else:
            print(f"  ✅ orders.customer_id → customers.customer_id (100% valide)")
        
        # Vérifier orders.attributed_campaign_id → campaigns.campaign_id
        # (seulement pour les non-NULL)
        attributed_orders = orders[orders['attributed_campaign_id'].notna()]
        if len(attributed_orders) > 0:
            invalid_campaigns = ~attributed_orders['attributed_campaign_id'].isin(
                campaigns['campaign_id']
            )
            if invalid_campaigns.any():
                self.errors.append(
                    f"{invalid_campaigns.sum()} orders avec attributed_campaign_id invalide"
                )
            else:
                print(f"  ✅ orders.attributed_campaign_id → campaigns.campaign_id "
                      f"({len(attributed_orders)} valides)")
        
        # Vérifier sends.customer_id → customers.customer_id
        invalid_sends_customers = ~sends['customer_id'].isin(customers['customer_id'])
        if invalid_sends_customers.any():
            self.errors.append(
                f"{invalid_sends_customers.sum()} sends avec customer_id invalide"
            )
        else:
            print(f"  ✅ sends.customer_id → customers.customer_id (100% valide)")
        
        # Vérifier sends.campaign_id → campaigns.campaign_id
        invalid_sends_campaigns = ~sends['campaign_id'].isin(campaigns['campaign_id'])
        if invalid_sends_campaigns.any():
            self.errors.append(
                f"{invalid_sends_campaigns.sum()} sends avec campaign_id invalide"
            )
        else:
            print(f"  ✅ sends.campaign_id → campaigns.campaign_id (100% valide)")
        
        print()
    
    def check_columns(self, df, table_name, expected_columns):
        """Vérifie que les colonnes attendues sont présentes"""
        missing = set(expected_columns) - set(df.columns)
        extra = set(df.columns) - set(expected_columns)
        
        if missing:
            self.errors.append(f"{table_name}: colonnes manquantes: {missing}")
        
        if extra:
            self.warnings.append(f"{table_name}: colonnes inattendues: {extra}")
        
        if not missing and not extra:
            print(f"  ✅ {table_name}: {len(expected_columns)} colonnes valides")
    
    def load_csv(self, relative_path):
        """Charge un CSV et gère les erreurs"""
        filepath = self.data_root / relative_path
        
        if not filepath.exists():
            self.errors.append(f"Fichier manquant: {filepath}")
            return None
        
        try:
            return pd.read_csv(filepath, encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Erreur lecture {filepath}: {e}")
            return None
    
    def print_summary(self):
        """Affiche le résumé des validations"""
        print("=" * 80)
        print("RÉSUMÉ DE VALIDATION")
        print("=" * 80)
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} AVERTISSEMENT(S):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} ERREUR(S):")
            for error in self.errors:
                print(f"  - {error}")
            print("\n🔧 ACTIONS REQUISES:")
            print("  1. Corriger les erreurs listées ci-dessus")
            print("  2. Régénérer les données avec generate_data.py")
            print("  3. Relancer ce script de validation")
            print("\n❌ VALIDATION ÉCHOUÉE")
        else:
            print("\n✅ VALIDATION RÉUSSIE - Tous les schémas sont corrects !")
            print("\n✅ Les DAX queries devraient fonctionner correctement.")
        
        print("=" * 80)


def main():
    """Point d'entrée principal"""
    validator = SchemaValidator()
    success = validator.validate_all()
    
    # Exit code pour CI/CD
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
