-- =====================================================
-- STRIPE BILLING SUPPORT
-- =====================================================

ALTER TABLE businesses ADD COLUMN stripe_customer_id TEXT;

ALTER TABLE businesses ADD COLUMN subscription_status TEXT DEFAULT 'free';

ALTER TABLE businesses ADD COLUMN plan TEXT DEFAULT 'starter';