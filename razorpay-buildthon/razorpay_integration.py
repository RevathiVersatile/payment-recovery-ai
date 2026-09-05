# ============================================================
# STEP 8 + STEP 12: RAZORPAY INTEGRATION
# ============================================================
# This file handles:
# 1. Razorpay client creation
# 2. Creating a Razorpay Test Mode order
# 3. Verifying payment signature
# 4. Creating unique Razorpay Test Mode Payment Links
# 5. Fetching Payment Link status
# ============================================================

import razorpay
import hmac
import hashlib
import uuid
import streamlit as st


# ------------------------------------------------------------
# 1. CREATE RAZORPAY CLIENT
# ------------------------------------------------------------

def get_razorpay_client():
    """
    Creates and returns a Razorpay client using
    the credentials stored in Streamlit secrets.
    """

    key_id = st.secrets["RAZORPAY_KEY_ID"]
    key_secret = st.secrets["RAZORPAY_KEY_SECRET"]

    client = razorpay.Client(
        auth=(key_id, key_secret)
    )

    return client


# ------------------------------------------------------------
# 2. CREATE RAZORPAY ORDER
# ------------------------------------------------------------

def create_razorpay_order(amount, receipt_id):
    """
    Creates a Razorpay Test Mode order.

    amount:
        Payment amount in INR.

    receipt_id:
        Unique ID for our transaction.
    """

    client = get_razorpay_client()

    # Razorpay expects amount in paise.
    amount_paise = int(float(amount) * 100)

    order_data = {
        "amount": amount_paise,
        "currency": "INR",
        "receipt": receipt_id,
        "payment_capture": 1
    }

    order = client.order.create(
        data=order_data
    )

    return order


# ------------------------------------------------------------
# 3. VERIFY PAYMENT SIGNATURE
# ------------------------------------------------------------

def verify_payment_signature(
    order_id,
    payment_id,
    signature
):
    """
    Verifies that the payment response actually came
    from Razorpay and was not modified.
    """

    key_secret = st.secrets["RAZORPAY_KEY_SECRET"]

    message = f"{order_id}|{payment_id}"

    generated_signature = hmac.new(
        key_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        generated_signature,
        signature
    )


# ============================================================
# STEP 12: CREATE RAZORPAY PAYMENT LINK
# ============================================================

def create_payment_link(amount, description, reference_id):
    """
    Creates a Razorpay Test Mode Payment Link.

    IMPORTANT:
    Razorpay requires reference_id to be unique.
    Therefore, we generate a new unique reference ID
    for every recovery attempt.

    The reference_id supplied by app.py is intentionally
    not reused because it may be something like RECOVERY-1,
    which can already exist in Razorpay.
    """

    client = get_razorpay_client()

    # Razorpay expects amount in paise.
    amount_paise = int(float(amount) * 100)

    # --------------------------------------------------------
    # Generate a UNIQUE reference ID
    # --------------------------------------------------------
    unique_reference_id = (
        f"RECOVERY-{uuid.uuid4().hex[:12].upper()}"
    )

    payment_link_data = {
        "amount": amount_paise,
        "currency": "INR",
        "description": description,
        "reference_id": unique_reference_id,
        "accept_partial": False,
        "reminder_enable": False
    }

    # Create Payment Link in Razorpay Test Mode
    payment_link = client.payment_link.create(
        data=payment_link_data
    )

    return payment_link


# ============================================================
# FETCH RAZORPAY PAYMENT LINK STATUS
# ============================================================

def fetch_payment_link(payment_link_id):
    """
    Fetches the latest status of a Razorpay Payment Link.
    """

    client = get_razorpay_client()

    payment_link = client.payment_link.fetch(
        payment_link_id
    )

    return payment_link

