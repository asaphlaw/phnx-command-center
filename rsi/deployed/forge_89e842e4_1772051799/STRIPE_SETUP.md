# Stripe Integration Setup

1. Install Stripe:
   pip install stripe

2. Set environment variable:
   export STRIPE_SECRET_KEY="sk_live_..."

3. Add to booking bot flow:
   - Before confirming booking
   - Generate payment URL
   - Send to client via Telegram
   - Confirm booking only after payment

4. Webhook setup (for production):
   - Configure Stripe webhook
   - Listen for payment_intent.succeeded
   - Auto-confirm booking on payment
