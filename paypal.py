import paypalrestsdk

# Set up the SDK with client ID and secret key
paypalrestsdk.configure({
    "mode": "sandbox", # or "live"
    "client_id": "PLACEHOLDER FOR THE CLIENT ID NOT PROVIDED FOR SECURITY PURPOSES",
    "client_secret": "PLACEHOLDER FOR THE CLIENT SECRET NOT PROVIDED FOR SECURITY PURPOSES"
})

# Create a payment using PayPal API
def create_paypal_payment(amount):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "USD"
            },
            "description": "Payment description"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:5000/paypal/success",
            "cancel_url": "http://localhost:5000/paypal/cancel"
        }
    })

    if payment.create():
        return payment
    else:
        return None

# Capture payment for an existing order
def capture_paypal_payment(order_id):
    payment = paypalrestsdk.Payment.find(order_id)
    if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):
        return True
    else:
        return False
