# ============================================================
# 💳 PAYMENT RECOVERY AI
# ============================================================
#
# COMPLETE BUILDATHON VERSION
#
# FLOW:
#
# Customer Payment Details
#          ↓
# ML Failure Prediction
#          ↓
# Risk Classification
#          ↓
# Issue Explanation
#          ↓
# Adaptive Recovery Strategy
#          ↓
# Razorpay TEST Payment Link
#          ↓
# Strict Payment Verification
#          ↓
# Live Recovery Analytics
#          ↓
# Portfolio Dashboard
#          ↓
# Recovery History
#
# IMPORTANT:
# - Razorpay TEST MODE only
# - No real money is charged
# - Existing razorpay_integration.py is used
# - Existing payment_model.pkl is used
# - Portfolio dashboard is DEMO analytics
# - Live Razorpay metrics remain separate
# ============================================================


# ============================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import uuid
import numpy as np


# Existing Razorpay integration
from razorpay_integration import (
    create_razorpay_order,
    verify_payment_signature,
    create_payment_link,
    fetch_payment_link
)


# ============================================================
# STEP 2: PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Payment Recovery AI",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# STEP 3: LOAD MACHINE LEARNING MODEL
# ============================================================

try:

    model = joblib.load("payment_model.pkl")

except Exception as e:

    st.error("❌ Unable to load payment_model.pkl")
    st.error(f"Error: {e}")
    st.stop()


# ============================================================
# STEP 4: SESSION STATE
# ============================================================


# ------------------------------------------------------------
# ML / ANALYSIS STATE
# ------------------------------------------------------------

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "failure_probability" not in st.session_state:
    st.session_state.failure_probability = 0.0

if "risk_level" not in st.session_state:
    st.session_state.risk_level = ""

if "reasons" not in st.session_state:
    st.session_state.reasons = []

if "payment_amount" not in st.session_state:
    st.session_state.payment_amount = 0.0

if "analyzed_error_code" not in st.session_state:
    st.session_state.analyzed_error_code = ""

if "analyzed_payment_method" not in st.session_state:
    st.session_state.analyzed_payment_method = ""


# ------------------------------------------------------------
# UNIQUE ORIGINAL TRANSACTION
# ------------------------------------------------------------

if "transaction_id" not in st.session_state:
    st.session_state.transaction_id = None


# ------------------------------------------------------------
# RECOVERY STATE
# ------------------------------------------------------------

if "recovery_result" not in st.session_state:
    st.session_state.recovery_result = None

if "recovery_method" not in st.session_state:
    st.session_state.recovery_method = ""

if "razorpay_payment_link_id" not in st.session_state:
    st.session_state.razorpay_payment_link_id = None

if "razorpay_payment_link_url" not in st.session_state:
    st.session_state.razorpay_payment_link_url = None

if "razorpay_payment_status" not in st.session_state:
    st.session_state.razorpay_payment_status = None

if "razorpay_amount_paid" not in st.session_state:
    st.session_state.razorpay_amount_paid = 0

if "razorpay_payment_id" not in st.session_state:
    st.session_state.razorpay_payment_id = None


# ------------------------------------------------------------
# LIVE DASHBOARD STATE
# ------------------------------------------------------------

if "at_risk_amount" not in st.session_state:
    st.session_state.at_risk_amount = 0.0

if "total_recovery_attempts" not in st.session_state:
    st.session_state.total_recovery_attempts = 0

if "successful_recoveries" not in st.session_state:
    st.session_state.successful_recoveries = 0

if "total_money_recovered" not in st.session_state:
    st.session_state.total_money_recovered = 0.0


# ------------------------------------------------------------
# RECOVERY HISTORY
# ------------------------------------------------------------

if "recovery_history" not in st.session_state:
    st.session_state.recovery_history = []


# ------------------------------------------------------------
# UNIQUE TRANSACTIONS ENTERING RECOVERY
# ------------------------------------------------------------

if "at_risk_transaction_ids" not in st.session_state:
    st.session_state.at_risk_transaction_ids = set()


# ------------------------------------------------------------
# PORTFOLIO ANALYTICS STATE
# ------------------------------------------------------------

if "demo_transaction_count" not in st.session_state:
    st.session_state.demo_transaction_count = 2000

if "demo_portfolio" not in st.session_state:
    st.session_state.demo_portfolio = None


# ============================================================
# STEP 5: DEMO PORTFOLIO BUILDER
# ============================================================

def build_demo_portfolio(
    loaded_model,
    transaction_count=2000
):
    """
    Creates a deterministic synthetic transaction portfolio.

    IMPORTANT:
    This is only for Buildathon / business dashboard
    demonstration.

    It does NOT represent real Razorpay transactions.
    """

    transaction_count = int(transaction_count)

    rng = np.random.default_rng(20260905)


    # --------------------------------------------------------
    # SYNTHETIC TRANSACTIONS
    # --------------------------------------------------------

    portfolio = pd.DataFrame({

        "amount":
            rng.integers(
                1000,
                8001,
                transaction_count
            ).astype(float),

        "payment_method":
            rng.choice(
                [
                    "UPI",
                    "CARD",
                    "NET_BANKING"
                ],
                transaction_count,
                p=[
                    0.50,
                    0.35,
                    0.15
                ]
            ),

        "bank":
            rng.choice(
                [
                    "Bank_A",
                    "Bank_B",
                    "Bank_C",
                    "Bank_D"
                ],
                transaction_count
            ),

        "device":
            rng.choice(
                [
                    "Android",
                    "iOS",
                    "Desktop"
                ],
                transaction_count,
                p=[
                    0.55,
                    0.20,
                    0.25
                ]
            ),

        "hour":
            rng.integers(
                0,
                24,
                transaction_count
            ),

        "previous_failures":
            rng.choice(
                [
                    0,
                    1,
                    2,
                    3,
                    4
                ],
                transaction_count,
                p=[
                    0.62,
                    0.20,
                    0.10,
                    0.05,
                    0.03
                ]
            ),

        "attempt_number":
            rng.choice(
                [
                    1,
                    2,
                    3,
                    4
                ],
                transaction_count,
                p=[
                    0.72,
                    0.18,
                    0.07,
                    0.03
                ]
            ),

        "error_code":
            rng.choice(
                [
                    "NONE",
                    "AUTH_ERROR",
                    "BANK_ERROR",
                    "CARD_DECLINED",
                    "NETWORK_ERROR"
                ],
                transaction_count,
                p=[
                    0.56,
                    0.10,
                    0.12,
                    0.12,
                    0.10
                ]
            ),

        "customer_type":
            rng.choice(
                [
                    "NEW",
                    "RETURNING"
                ],
                transaction_count,
                p=[
                    0.40,
                    0.60
                ]
            )
    })


    # --------------------------------------------------------
    # RUN SAME ML MODEL
    # --------------------------------------------------------

    try:

        probabilities = loaded_model.predict_proba(
            portfolio
        )

        classes = list(
            loaded_model.classes_
        )


        if "FAILED" in classes:

            failed_index = classes.index(
                "FAILED"
            )

            portfolio[
                "failure_probability"
            ] = (
                probabilities[
                    :,
                    failed_index
                ] * 100
            )

        else:

            portfolio[
                "failure_probability"
            ] = (
                np.max(
                    probabilities,
                    axis=1
                ) * 100
            )


    except Exception:

        # Fallback keeps the portfolio dashboard
        # operational if model schema differs.

        portfolio[
            "failure_probability"
        ] = 0.0


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    portfolio["risk_level"] = pd.cut(
        portfolio[
            "failure_probability"
        ],

        bins=[
            -np.inf,
            30,
            70,
            np.inf
        ],

        labels=[
            "LOW",
            "MEDIUM",
            "HIGH"
        ],

        right=False
    ).astype(str)


    # --------------------------------------------------------
    # PRIMARY SCREENING
    #
    # >= 50% = primary failure
    # --------------------------------------------------------

    portfolio[
        "primary_failed"
    ] = (
        portfolio[
            "failure_probability"
        ] >= 50.0
    )


    # --------------------------------------------------------
    # SAFETY RULE
    #
    # Stop recovery if:
    #
    # previous failures >= 3
    # OR
    # attempt number >= 3
    # --------------------------------------------------------

    portfolio[
        "safety_blocked"
    ] = (

        portfolio[
            "primary_failed"
        ]

        &

        (
            (
                portfolio[
                    "previous_failures"
                ] >= 3
            )

            |

            (
                portfolio[
                    "attempt_number"
                ] >= 3
            )
        )
    )


    # --------------------------------------------------------
    # RECOVERY ELIGIBILITY
    # --------------------------------------------------------

    portfolio[
        "recovery_eligible"
    ] = (

        portfolio[
            "primary_failed"
        ]

        &

        portfolio[
            "risk_level"
        ].isin(
            [
                "MEDIUM",
                "HIGH"
            ]
        )

        &

        ~portfolio[
            "safety_blocked"
        ]
    )


    # --------------------------------------------------------
    # UNIQUE DEMO TRANSACTION IDs
    # --------------------------------------------------------

    portfolio[
        "transaction_id"
    ] = [
        f"DEMO-TXN-{i:05d}"
        for i in range(
            1,
            transaction_count + 1
        )
    ]


    # --------------------------------------------------------
    # ADAPTIVE STRATEGY SCORE
    # --------------------------------------------------------

    strategy_score = np.select(

        [

            portfolio[
                "error_code"
            ].eq(
                "NETWORK_ERROR"
            ),

            portfolio[
                "error_code"
            ].eq(
                "AUTH_ERROR"
            ),

            portfolio[
                "error_code"
            ].isin(
                [
                    "CARD_DECLINED",
                    "BANK_ERROR"
                ]
            )
        ],

        [
            0.48,
            0.42,
            0.38
        ],

        default=0.40
    )


    # --------------------------------------------------------
    # SIMULATED DEMO RECOVERY
    # --------------------------------------------------------

    recovery_draw = rng.random(
        transaction_count
    )

    portfolio[
        "demo_recovered"
    ] = (

        portfolio[
            "recovery_eligible"
        ]

        &

        (
            recovery_draw
            < strategy_score
        )
    )


    return portfolio


# ============================================================
# STEP 6: CREATE INITIAL DEMO PORTFOLIO
# ============================================================

if (
    st.session_state.demo_portfolio
    is None
):

    st.session_state.demo_portfolio = (
        build_demo_portfolio(
            model,
            st.session_state.demo_transaction_count
        )
    )


# ============================================================
# STEP 7: APPLICATION HEADER
# ============================================================

st.title(
    "💳 Payment Recovery AI"
)

st.subheader(
    "AI-Powered Payment Failure Prediction, "
    "Payment Recovery & Business Analytics"
)

st.info(
    "🧪 TEST MODE — Razorpay test transactions only. "
    "No real money will be charged."
)


# ============================================================
# STEP 8: PAYMENT INPUT
# ============================================================

st.header(
    "💳 Payment & Technical Risk Details"
)


payment_amount = st.number_input(
    "Payment Amount (₹)",
    min_value=100.0,
    max_value=100000.0,
    value=5000.0,
    step=100.0
)


payment_method = st.selectbox(
    "Payment Method",
    [
        "UPI",
        "CARD",
        "NET_BANKING"
    ]
)


bank = st.selectbox(
    "Bank",
    [
        "Bank_A",
        "Bank_B",
        "Bank_C",
        "Bank_D"
    ]
)


device = st.selectbox(
    "Device",
    [
        "Android",
        "iOS",
        "Desktop"
    ]
)


hour = st.number_input(
    "Transaction Hour",
    min_value=0,
    max_value=23,
    value=12,
    step=1
)


previous_failures = st.number_input(
    "Previous Payment Failures",
    min_value=0,
    max_value=10,
    value=0,
    step=1
)


attempt_number = st.number_input(
    "Payment Attempt Number",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)


error_code = st.selectbox(
    "Error Code",
    [
        "NONE",
        "AUTH_ERROR",
        "BANK_ERROR",
        "CARD_DECLINED",
        "NETWORK_ERROR"
    ]
)


customer_type = st.selectbox(
    "Customer Type",
    [
        "NEW",
        "RETURNING"
    ]
)


# ============================================================
# STEP 9: ANALYZE PAYMENT
# ============================================================

if st.button(
    "🔍 Analyze Payment",
    use_container_width=True
):

    # --------------------------------------------------------
    # UNIQUE TRANSACTION ID
    # --------------------------------------------------------

    new_transaction_id = (
        f"TXN-{uuid.uuid4().hex[:10].upper()}"
    )

    st.session_state.transaction_id = (
        new_transaction_id
    )


    # --------------------------------------------------------
    # INPUT DATA
    # --------------------------------------------------------

    input_data = pd.DataFrame(
        [
            {
                "amount":
                    payment_amount,

                "payment_method":
                    payment_method,

                "bank":
                    bank,

                "device":
                    device,

                "hour":
                    hour,

                "previous_failures":
                    previous_failures,

                "attempt_number":
                    attempt_number,

                "error_code":
                    error_code,

                "customer_type":
                    customer_type
            }
        ]
    )


    # --------------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------------

    try:

        probabilities = (
            model.predict_proba(
                input_data
            )[0]
        )

        classes = list(
            model.classes_
        )


        if "FAILED" in classes:

            failed_index = (
                classes.index(
                    "FAILED"
                )
            )

            failure_probability = (
                probabilities[
                    failed_index
                ] * 100
            )

        else:

            prediction = (
                model.predict(
                    input_data
                )[0]
            )

            if prediction == 1:

                failure_probability = 100.0

            else:

                failure_probability = 0.0


    except Exception as e:

        st.error(
            "❌ Error while running the ML model."
        )

        st.error(
            f"Model error: {e}"
        )

        st.stop()


    # --------------------------------------------------------
    # RISK CLASSIFICATION
    # --------------------------------------------------------

    if failure_probability < 30:

        risk_level = "LOW"

    elif failure_probability < 70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    # --------------------------------------------------------
    # RISK REASONS
    # --------------------------------------------------------

    reasons = []


    if previous_failures > 0:

        reasons.append(
            f"Customer has {previous_failures} "
            f"previous payment failure(s)."
        )


    if attempt_number > 1:

        reasons.append(
            f"This is payment attempt "
            f"#{attempt_number}."
        )


    if error_code != "NONE":

        reasons.append(
            f"Technical error detected: "
            f"{error_code}."
        )


    if payment_method == "CARD":

        reasons.append(
            "Card payments may be affected by "
            "issuer or authentication failures."
        )


    if payment_method == "UPI":

        reasons.append(
            "UPI payments can be affected by "
            "bank/network availability."
        )


    if hour < 6 or hour > 22:

        reasons.append(
            "Transaction occurred during an unusual hour."
        )


    if risk_level == "HIGH":

        reasons.append(
            "ML model indicates a high probability "
            "of payment failure."
        )

    elif risk_level == "MEDIUM":

        reasons.append(
            "ML model indicates a moderate probability "
            "of payment failure."
        )

    else:

        reasons.append(
            "ML model indicates a low probability "
            "of payment failure."
        )


    # --------------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------------

    st.session_state.analyzed = True

    st.session_state.failure_probability = (
        float(failure_probability)
    )

    st.session_state.risk_level = (
        risk_level
    )

    st.session_state.reasons = (
        reasons
    )

    st.session_state.payment_amount = (
        float(payment_amount)
    )

    st.session_state.analyzed_error_code = (
        error_code
    )

    st.session_state.analyzed_payment_method = (
        payment_method
    )


    # Reset previous recovery result
    st.session_state.recovery_result = None

    st.session_state.recovery_method = ""

    st.session_state.razorpay_payment_link_id = None

    st.session_state.razorpay_payment_link_url = None

    st.session_state.razorpay_payment_status = None

    st.session_state.razorpay_amount_paid = 0

    st.session_state.razorpay_payment_id = None


    st.success(
        "✅ Payment analysis completed successfully."
    )


# ============================================================
# STEP 10: DISPLAY AI RESULT
# ============================================================

if st.session_state.analyzed:

    st.header(
        "📊 AI Payment Risk Analysis"
    )


    st.caption(
        f"Transaction ID: "
        f"{st.session_state.transaction_id}"
    )


    probability = (
        st.session_state.failure_probability
    )

    risk = (
        st.session_state.risk_level
    )


    if risk == "HIGH":

        st.error(
            f"🔴 HIGH RISK — "
            f"Failure Probability: "
            f"{probability:.2f}%"
        )

    elif risk == "MEDIUM":

        st.warning(
            f"🟠 MEDIUM RISK — "
            f"Failure Probability: "
            f"{probability:.2f}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — "
            f"Failure Probability: "
            f"{probability:.2f}%"
        )


    st.subheader(
        "🔎 Risk Factors"
    )


    for reason in (
        st.session_state.reasons
    ):

        st.write(
            f"• {reason}"
        )


# ============================================================
# STEP 11: RECOVERY STRATEGY
# ============================================================

if (
    st.session_state.analyzed

    and

    st.session_state.risk_level
    in [
        "MEDIUM",
        "HIGH"
    ]
):

    error_code = (
        st.session_state.analyzed_error_code
    )

    risk_level = (
        st.session_state.risk_level
    )


    # --------------------------------------------------------
    # ADAPTIVE RECOVERY STRATEGY
    # --------------------------------------------------------

    if error_code == "AUTH_ERROR":

        recovery_description = (
            "Authentication Retry"
        )

    elif error_code == "CARD_DECLINED":

        recovery_description = (
            "Alternative Payment Method"
        )

    elif error_code == "BANK_ERROR":

        recovery_description = (
            "Alternative Payment Method"
        )

    elif error_code == "NETWORK_ERROR":

        recovery_description = (
            "Payment Retry"
        )

    elif risk_level == "HIGH":

        recovery_description = (
            "Alternative Payment Method"
        )

    else:

        recovery_description = (
            "Payment Retry"
        )


    st.header(
        "🔄 Payment Recovery"
    )


    st.write(
        f"**Recommended Recovery Strategy:** "
        f"{recovery_description}"
    )


    # ========================================================
    # CREATE RAZORPAY PAYMENT LINK
    # ========================================================

    if st.button(
        "💳 Create Recovery Payment",
        use_container_width=True
    ):

        try:

            # ------------------------------------------------
            # COUNT EXISTING ATTEMPTS FOR SAME TRANSACTION
            # ------------------------------------------------

            existing_attempts = 0

            for record in (
                st.session_state.recovery_history
            ):

                if (
                    record.get(
                        "Transaction ID"
                    )
                    ==
                    st.session_state.transaction_id
                ):

                    existing_attempts += 1


            # ------------------------------------------------
            # INTERNAL REFERENCE
            # ------------------------------------------------

            internal_reference_id = (
                f"{st.session_state.transaction_id}-"
                f"{existing_attempts + 1}"
            )


            # ------------------------------------------------
            # CREATE PAYMENT LINK
            # ------------------------------------------------

            payment_link = create_payment_link(

                st.session_state.payment_amount,

                "Payment Recovery AI - Recovery Payment",

                internal_reference_id
            )


            payment_link_id = (
                payment_link.get(
                    "id"
                )
            )

            payment_link_url = (
                payment_link.get(
                    "short_url"
                )
            )

            payment_link_status = (
                payment_link.get(
                    "status",
                    "created"
                )
            )


            # ------------------------------------------------
            # VALIDATE
            # ------------------------------------------------

            if not payment_link_id:

                st.error(
                    "❌ Razorpay did not return "
                    "a Payment Link ID."
                )

                st.stop()


            # ------------------------------------------------
            # SAVE PAYMENT LINK
            # ------------------------------------------------

            st.session_state.razorpay_payment_link_id = (
                payment_link_id
            )

            st.session_state.razorpay_payment_link_url = (
                payment_link_url
            )

            st.session_state.razorpay_payment_status = (
                payment_link_status
            )

            st.session_state.recovery_method = (
                recovery_description
            )

            st.session_state.recovery_result = None

            st.session_state.razorpay_amount_paid = 0

            st.session_state.razorpay_payment_id = None


            # ------------------------------------------------
            # ONE PAYMENT LINK = ONE RECOVERY ATTEMPT
            # ------------------------------------------------

            st.session_state.total_recovery_attempts += 1


            # ------------------------------------------------
            # AT-RISK AMOUNT COUNTED ONCE PER TRANSACTION
            # ------------------------------------------------

            current_transaction_id = (
                st.session_state.transaction_id
            )


            if (
                current_transaction_id
                not in
                st.session_state.at_risk_transaction_ids
            ):

                st.session_state.at_risk_transaction_ids.add(
                    current_transaction_id
                )

                st.session_state.at_risk_amount += (
                    st.session_state.payment_amount
                )


            # ------------------------------------------------
            # HISTORY RECORD
            # ------------------------------------------------

            recovery_record = {

                "Transaction ID":
                    current_transaction_id,

                "Payment Link ID":
                    payment_link_id,

                "Transaction Amount":
                    st.session_state.payment_amount,

                "Amount (₹)":
                    st.session_state.payment_amount,

                "Risk Level":
                    st.session_state.risk_level,

                "Failure Probability":
                    f"{st.session_state.failure_probability:.2f}%",

                "Recovery Method":
                    recovery_description,

                "Razorpay Status":
                    payment_link_status,

                "Amount Paid":
                    "₹0.00",

                "Payment ID":
                    "-",

                "Result":
                    "⏳ PENDING"
            }


            st.session_state.recovery_history.append(
                recovery_record
            )


            # ------------------------------------------------
            # DISPLAY PAYMENT LINK
            # ------------------------------------------------

            st.success(
                "✅ Recovery Payment Link created successfully!"
            )


            st.write(
                f"**Recovery Attempt:** "
                f"#{st.session_state.total_recovery_attempts}"
            )


            st.write(
                f"**Payment Link ID:** "
                f"`{payment_link_id}`"
            )


            st.write(
                f"**Razorpay Status:** "
                f"`{payment_link_status}`"
            )


            if payment_link_url:

                st.link_button(
                    "💰 Pay Now with Razorpay",
                    payment_link_url,
                    use_container_width=True
                )


            st.warning(
                "⚠️ For testing failure, use a fresh "
                "Payment Link. Do not reuse a Payment Link "
                "that was already successfully paid."
            )


            st.caption(
                "🧪 Razorpay Test Mode — "
                "no real money will be charged."
            )


        except Exception as e:

            st.error(
                "❌ Failed to create Razorpay Payment Link."
            )

            st.exception(e)


# ============================================================
# STEP 12: STRICT RAZORPAY PAYMENT VERIFICATION
# ============================================================

if (
    st.session_state.razorpay_payment_link_id
):

    st.divider()

    st.subheader(
        "🔎 Check Recovery Payment Status"
    )


    st.write(
        f"**Active Payment Link:** "
        f"`{st.session_state.razorpay_payment_link_id}`"
    )


    if st.button(
        "🔄 Check Payment Status",
        use_container_width=True
    ):

        try:

            # ------------------------------------------------
            # FETCH PAYMENT LINK
            # ------------------------------------------------

            latest_payment = fetch_payment_link(
                st.session_state.razorpay_payment_link_id
            )


            # ------------------------------------------------
            # PAYMENT LINK STATUS
            # ------------------------------------------------

            latest_status = str(
                latest_payment.get(
                    "status",
                    "unknown"
                )
            ).lower()


            # ------------------------------------------------
            # REQUIRED AMOUNT
            # ------------------------------------------------

            amount_paise = int(
                latest_payment.get(
                    "amount",
                    int(
                        st.session_state.payment_amount
                        * 100
                    )
                )
            )


            # ------------------------------------------------
            # AMOUNT PAID
            # ------------------------------------------------

            amount_paid_paise = int(
                latest_payment.get(
                    "amount_paid",
                    0
                )
            )


            amount_paid_rupees = (
                amount_paid_paise / 100
            )


            # ------------------------------------------------
            # PAYMENTS ARRAY
            # ------------------------------------------------

            payments = latest_payment.get(
                "payments"
            )


            # ------------------------------------------------
            # FIND CAPTURED PAYMENT
            # ------------------------------------------------

            captured_payment = None


            if isinstance(
                payments,
                list
            ):

                for payment in payments:

                    if not isinstance(
                        payment,
                        dict
                    ):

                        continue


                    payment_status = str(
                        payment.get(
                            "status",
                            ""
                        )
                    ).lower()


                    if payment_status == "captured":

                        captured_payment = payment

                        break


            # ------------------------------------------------
            # SAVE RAZORPAY DATA
            # ------------------------------------------------

            st.session_state.razorpay_payment_status = (
                latest_status
            )

            st.session_state.razorpay_amount_paid = (
                amount_paid_paise
            )


            if captured_payment:

                st.session_state.razorpay_payment_id = (
                    captured_payment.get(
                        "payment_id"
                    )
                )


            # ------------------------------------------------
            # FIND HISTORY RECORD
            # ------------------------------------------------

            active_payment_link_id = (
                st.session_state.razorpay_payment_link_id
            )

            history_index = None


            for index, record in enumerate(
                st.session_state.recovery_history
            ):

                if (
                    record.get(
                        "Payment Link ID"
                    )
                    ==
                    active_payment_link_id
                ):

                    history_index = index

                    break


            # =================================================
            # STRICT SUCCESS CHECK
            # =================================================
            #
            # SUCCESS ONLY WHEN:
            #
            # 1. status = paid
            # 2. amount_paid >= required amount
            # 3. captured payment exists
            #
            # =================================================

            required_amount_paise = (
                amount_paise
            )


            payment_is_really_paid = (

                latest_status == "paid"

                and

                amount_paid_paise
                >=
                required_amount_paise

                and

                captured_payment
                is not None
            )


            # =================================================
            # SUCCESS
            # =================================================

            if payment_is_really_paid:

                st.session_state.recovery_result = True


                # ------------------------------------------------
                # CHECK DUPLICATE SUCCESS
                # ------------------------------------------------

                transaction_already_recovered = False


                for record in (
                    st.session_state.recovery_history
                ):

                    if (

                        record.get(
                            "Transaction ID"
                        )
                        ==
                        st.session_state.transaction_id

                        and

                        record.get(
                            "Result"
                        )
                        ==
                        "✅ RECOVERED"
                    ):

                        transaction_already_recovered = True

                        break


                # ------------------------------------------------
                # COUNT SUCCESS ONLY ONCE
                # ------------------------------------------------

                if not transaction_already_recovered:

                    st.session_state.successful_recoveries += 1

                    st.session_state.total_money_recovered += (
                        st.session_state.payment_amount
                    )


                # ------------------------------------------------
                # UPDATE HISTORY
                # ------------------------------------------------

                if history_index is not None:

                    st.session_state.recovery_history[
                        history_index
                    ][
                        "Razorpay Status"
                    ] = latest_status


                    st.session_state.recovery_history[
                        history_index
                    ][
                        "Amount Paid"
                    ] = (
                        f"₹{amount_paid_rupees:,.2f}"
                    )


                    st.session_state.recovery_history[
                        history_index
                    ][
                        "Payment ID"
                    ] = (
                        st.session_state.razorpay_payment_id
                        or "-"
                    )


                    st.session_state.recovery_history[
                        history_index
                    ][
                        "Result"
                    ] = "✅ RECOVERED"


                st.success(
                    "🎉 PAYMENT SUCCESSFULLY RECOVERED"
                )


                st.write(
                    f"**Amount Paid:** "
                    f"₹{amount_paid_rupees:,.2f}"
                )


                if st.session_state.razorpay_payment_id:

                    st.write(
                        f"**Captured Payment ID:** "
                        f"`{st.session_state.razorpay_payment_id}`"
                    )


            # =================================================
            # NOT SUCCESSFULLY PAID
            # =================================================

            else:

                st.session_state.recovery_result = False


                # ------------------------------------------------
                # STILL ACTIVE
                # ------------------------------------------------

                if latest_status in [
                    "created",
                    "issued",
                    "partially_paid"
                ]:

                    if history_index is not None:

                        st.session_state.recovery_history[
                            history_index
                        ][
                            "Razorpay Status"
                        ] = latest_status


                        st.session_state.recovery_history[
                            history_index
                        ][
                            "Amount Paid"
                        ] = (
                            f"₹{amount_paid_rupees:,.2f}"
                        )


                        st.session_state.recovery_history[
                            history_index
                        ][
                            "Result"
                        ] = "❌ NOT RECOVERED"


                    st.warning(
                        "❌ PAYMENT NOT RECOVERED"
                    )


                    st.write(
                        f"Razorpay Payment Link Status: "
                        f"`{latest_status}`"
                    )


                    st.write(
                        f"Amount Paid: "
                        f"₹{amount_paid_rupees:,.2f}"
                    )


                    st.info(
                        "The customer has not completed "
                        "a successfully captured payment."
                    )


                # ------------------------------------------------
                # EXPIRED / CANCELLED / OTHER
                # ------------------------------------------------

                else:

                    if history_index is not None:

                        st.session_state.recovery_history[
                            history_index
                        ][
                            "Razorpay Status"
                        ] = latest_status


                        st.session_state.recovery_history[
                            history_index
                        ][
                            "Amount Paid"
                        ] = (
                            f"₹{amount_paid_rupees:,.2f}"
                        )


                        st.session_state.recovery_history[
                            history_index
                        ][
                            "Result"
                        ] = "❌ FAILED"


                    st.error(
                        "❌ RECOVERY FAILED / NOT COMPLETED"
                    )


                    st.write(
                        f"Razorpay Status: "
                        f"`{latest_status}`"
                    )


                    st.write(
                        f"Amount Paid: "
                        f"₹{amount_paid_rupees:,.2f}"
                    )


            # =================================================
            # VERIFICATION DETAILS
            # =================================================

            with st.expander(
                "🔧 Razorpay Verification Details"
            ):

                st.write(
                    "**Payment Link Status:**",
                    latest_status
                )


                st.write(
                    "**Required Amount:**",
                    f"₹{amount_paise / 100:,.2f}"
                )


                st.write(
                    "**Amount Paid:**",
                    f"₹{amount_paid_rupees:,.2f}"
                )


                st.write(
                    "**Captured Payment Found:**",
                    "YES"
                    if captured_payment
                    else "NO"
                )


                if captured_payment:

                    st.write(
                        "**Captured Payment ID:**",
                        captured_payment.get(
                            "payment_id",
                            "-"
                        )
                    )


                    st.write(
                        "**Captured Payment Status:**",
                        captured_payment.get(
                            "status",
                            "-"
                        )
                    )


                else:

                    st.write(
                        "**Payment ID:**",
                        "-"
                    )


            st.caption(
                "ℹ️ Checking status does not create "
                "a new recovery attempt."
            )


        except Exception as e:

            st.error(
                "❌ Unable to fetch Razorpay payment status."
            )

            st.exception(e)


# ============================================================
# STEP 13: CURRENT RECOVERY RESULT
# ============================================================

if (
    st.session_state.razorpay_payment_link_id

    and

    st.session_state.recovery_result
    is not None
):

    st.divider()

    st.subheader(
        "📌 Current Recovery Result"
    )


    if st.session_state.recovery_result is True:

        st.success(
            "✅ RECOVERY SUCCESSFUL"
        )


        st.write(
            f"₹{st.session_state.payment_amount:,.2f} "
            "successfully recovered."
        )


    elif st.session_state.recovery_result is False:

        st.error(
            "❌ RECOVERY NOT SUCCESSFUL"
        )


        st.write(
            "No successfully captured payment was "
            "verified for this recovery attempt."
        )


# ============================================================
# STEP 14: BUSINESS ANALYTICS DASHBOARD
# ============================================================

st.divider()

st.header(
    "📈 Payment Recovery Operations Dashboard"
)


# ============================================================
# PORTFOLIO ANALYSIS CONFIGURATION
# ============================================================

st.subheader(
    "📊 Portfolio Analysis Configuration"
)


selected_transaction_count = st.number_input(
    "Transactions to Analyze",

    min_value=100,

    max_value=100000,

    value=int(
        st.session_state.demo_transaction_count
    ),

    step=100,

    help=(
        "Choose how many synthetic transactions "
        "the AI portfolio dashboard should analyze."
    )
)


# ------------------------------------------------------------
# REBUILD PORTFOLIO WHEN COUNT CHANGES
# ------------------------------------------------------------

if (
    selected_transaction_count
    !=
    st.session_state.demo_transaction_count
):

    st.session_state.demo_transaction_count = (
        int(selected_transaction_count)
    )

    st.session_state.demo_portfolio = (
        build_demo_portfolio(
            model,
            int(selected_transaction_count)
        )
    )


portfolio = (
    st.session_state.demo_portfolio
)


# ============================================================
# PORTFOLIO METRICS
# ============================================================

transactions_analyzed = int(
    len(portfolio)
)


failed_payments = int(
    portfolio[
        "primary_failed"
    ].sum()
)


recovery_eligible_count = int(
    portfolio[
        "recovery_eligible"
    ].sum()
)


safety_prevented = int(
    portfolio[
        "safety_blocked"
    ].sum()
)


# ------------------------------------------------------------
# REVENUE AT RISK
# ------------------------------------------------------------

revenue_at_risk = float(
    portfolio.loc[
        portfolio[
            "primary_failed"
        ],
        "amount"
    ].sum()
)


# ------------------------------------------------------------
# DEMO RECOVERED AMOUNT
# ------------------------------------------------------------

demo_recovered_amount = float(
    portfolio.loc[
        portfolio[
            "demo_recovered"
        ],
        "amount"
    ].sum()
)


# ------------------------------------------------------------
# DEMO RECOVERY RATE
# ------------------------------------------------------------

demo_recovery_rate = (

    demo_recovered_amount
    /
    revenue_at_risk
    *
    100

    if revenue_at_risk > 0

    else 0.0
)


# ============================================================
# KPI ROW 1
# ============================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "Transactions Analyzed",
        f"{transactions_analyzed:,}"
    )


with k2:

    st.metric(
        "Failed Payments",
        f"{failed_payments:,}"
    )


with k3:

    st.metric(
        "Recovery Eligible",
        f"{recovery_eligible_count:,}"
    )


with k4:

    st.metric(
        "Successfully Recovered",
        f"₹{demo_recovered_amount / 100000:.2f} L"
    )


# ============================================================
# KPI ROW 2
# ============================================================

k5, k6, k7 = st.columns(3)


with k5:

    st.metric(
        "Revenue at Risk",
        f"₹{revenue_at_risk / 100000:.2f} L"
    )


with k6:

    st.metric(
        "Recovery Rate",
        f"{demo_recovery_rate:.1f}%"
    )


with k7:

    st.metric(
        "Safety Actions Prevented",
        f"{safety_prevented:,}"
    )


st.caption(
    f"DEMO PORTFOLIO: {transactions_analyzed:,} "
    "synthetic transactions are analyzed using the "
    "loaded ML model. Portfolio recovery outcomes are "
    "simulated for Buildathon demonstration. "
    "Razorpay payments remain in TEST mode."
)


# ============================================================
# PRIMARY → ELIGIBILITY PIPELINE
# ============================================================

st.subheader(
    "🔎 Primary Screening → Recovery Eligibility"
)


pipeline_col1, pipeline_col2, pipeline_col3, pipeline_col4 = (
    st.columns(4)
)


with pipeline_col1:

    st.metric(
        "1. Transactions Analyzed",
        f"{transactions_analyzed:,}"
    )


with pipeline_col2:

    st.metric(
        "2. Failed at Primary Level",
        f"{failed_payments:,}"
    )


with pipeline_col3:

    st.metric(
        "3. Recovery Eligible",
        f"{recovery_eligible_count:,}"
    )


with pipeline_col4:

    st.metric(
        "4. Safety Blocked",
        f"{safety_prevented:,}"
    )


st.markdown(
    "**Decision flow:** "
    "`All Transactions → Primary YES/NO → "
    "Recovery Eligibility → Safety Rules → "
    "Next-Best Recovery Action → Verified Result`"
)


# ============================================================
# DECISION BREAKDOWN
# ============================================================

primary_success_count = (
    transactions_analyzed
    -
    failed_payments
)


not_eligible_count = (
    failed_payments
    -
    recovery_eligible_count
)


breakdown_df = pd.DataFrame({

    "Decision Stage": [

        "Transactions analyzed",

        "Primary YES — failed",

        "Primary NO — no recovery required",

        "Recovery eligible",

        "Not eligible / stopped"
    ],

    "Transactions": [

        transactions_analyzed,

        failed_payments,

        primary_success_count,

        recovery_eligible_count,

        not_eligible_count
    ]
})


st.dataframe(
    breakdown_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# RECOVERY ECONOMICS
# ============================================================

st.subheader(
    "💰 Recovery Economics"
)


econ_col1, econ_col2, econ_col3 = (
    st.columns(3)
)


remaining_risk = max(
    revenue_at_risk
    -
    demo_recovered_amount,
    0.0
)


with econ_col1:

    st.metric(
        "Revenue at Risk",
        f"₹{revenue_at_risk / 100000:.2f} L"
    )


with econ_col2:

    st.metric(
        "Recovered",
        f"₹{demo_recovered_amount / 100000:.2f} L"
    )


with econ_col3:

    st.metric(
        "Remaining Risk",
        f"₹{remaining_risk / 100000:.2f} L"
    )


# ============================================================
# LIVE RAZORPAY METRICS
# ============================================================

st.subheader(
    "🧪 Live Razorpay Test Recovery Metrics"
)


live_rate = (

    st.session_state.successful_recoveries

    /

    st.session_state.total_recovery_attempts

    *

    100

    if st.session_state.total_recovery_attempts > 0

    else 0.0
)


live1, live2, live3, live4 = (
    st.columns(4)
)


with live1:

    st.metric(
        "Live Recovery Attempts",
        f"{st.session_state.total_recovery_attempts:,}"
    )


with live2:

    st.metric(
        "Live Successful Recoveries",
        f"{st.session_state.successful_recoveries:,}"
    )


with live3:

    st.metric(
        "Live Amount Recovered",
        f"₹{st.session_state.total_money_recovered:,.2f}"
    )


with live4:

    st.metric(
        "Live Recovery Rate",
        f"{live_rate:.1f}%"
    )


st.caption(
    "Live metrics are updated only after a "
    "Razorpay TEST payment is strictly verified "
    "as captured."
)


# ============================================================
# PORTFOLIO DECISION LOG
# ============================================================

st.subheader(
    "📋 Portfolio Decision Log"
)


preview = portfolio.head(
    12
).copy()


preview[
    "Primary Decision"
] = np.where(

    preview[
        "primary_failed"
    ],

    "YES — FAILED",

    "NO — SUCCESS"
)


preview[
    "Recovery Eligible"
] = np.where(

    preview[
        "recovery_eligible"
    ],

    "YES",

    "NO"
)


preview[
    "Safety Check"
] = np.where(

    preview[
        "safety_blocked"
    ],

    "BLOCKED",

    "CLEAR"
)


preview[
    "Demo Result"
] = np.where(

    preview[
        "demo_recovered"
    ],

    "RECOVERED",

    "NOT RECOVERED"
)


preview_display = preview[
    [
        "transaction_id",

        "amount",

        "risk_level",

        "failure_probability",

        "Primary Decision",

        "Recovery Eligible",

        "Safety Check",

        "Demo Result"
    ]
].rename(

    columns={

        "transaction_id":
            "Transaction ID",

        "amount":
            "Amount (₹)",

        "risk_level":
            "Risk Level",

        "failure_probability":
            "Failure Probability (%)"
    }
)


st.dataframe(
    preview_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DASHBOARD DEFINITIONS
# ============================================================

with st.expander(
    "📖 Dashboard Definitions"
):

    st.markdown(
        """
### Transactions Analyzed
Number of synthetic transactions selected for
the portfolio demonstration.

### Failed Payments
Transactions whose ML failure probability is
50% or higher at the primary screening level.

### Recovery Eligible
Failed transactions that are MEDIUM/HIGH risk
and pass the safety rules.

### Safety Actions Prevented
Transactions blocked from additional recovery
because repeated failures or attempts indicate
that another recovery action should not be attempted.

### Revenue at Risk
Total value of transactions classified as failed
at the primary screening level.

### Successfully Recovered
Synthetic recovery amount used only for
portfolio demonstration.

### Live Razorpay Metrics
Actual Razorpay TEST MODE recovery information.
These metrics are separate from the synthetic
portfolio dashboard.

### Recovery Attempts
Number of unique Razorpay Payment Links created.

### Successful Recoveries
Unique original transactions with a strictly
verified captured payment.
"""
    )


# ============================================================
# STEP 15: RECOVERY HISTORY
# ============================================================

st.divider()

st.header(
    "📜 Recovery History"
)


if len(
    st.session_state.recovery_history
) > 0:

    history_df = pd.DataFrame(
        st.session_state.recovery_history
    )


    preferred_columns = [

        "Transaction ID",

        "Payment Link ID",

        "Transaction Amount",

        "Amount (₹)",

        "Risk Level",

        "Failure Probability",

        "Recovery Method",

        "Razorpay Status",

        "Amount Paid",

        "Payment ID",

        "Result"
    ]


    existing_columns = [

        column

        for column in preferred_columns

        if column in history_df.columns
    ]


    history_df = history_df[
        existing_columns
    ]


    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No recovery attempts yet."
    )


# ============================================================
# STEP 16: HOW PAYMENT RECOVERY AI WORKS
# ============================================================

with st.expander(
    "ℹ️ How Payment Recovery AI works"
):

    st.markdown(
        """
### 1️⃣ Payment Analysis

The ML model analyzes the transaction details
and predicts the probability of payment failure.

### 2️⃣ Risk Classification

- 🟢 LOW: Failure probability below 30%
- 🟠 MEDIUM: Failure probability from 30% to below 70%
- 🔴 HIGH: Failure probability 70% or above

### 3️⃣ Primary Screening

The application uses a 50% failure-probability
threshold for primary failure classification.

### 4️⃣ Recovery Eligibility

Only MEDIUM/HIGH-risk failed transactions
that pass safety rules become recovery eligible.

### 5️⃣ Adaptive Recovery Strategy

The recovery strategy changes based on the
detected issue:

- AUTH_ERROR → Authentication Retry
- CARD_DECLINED → Alternative Payment Method
- BANK_ERROR → Alternative Payment Method
- NETWORK_ERROR → Payment Retry
- HIGH risk → Alternative Payment Method
- Otherwise → Payment Retry

### 6️⃣ Safety Rules

The system prevents unnecessary repeated
recovery attempts when:

- Previous failures >= 3
- OR payment attempt number >= 3

### 7️⃣ Razorpay Test Mode

Recovery uses Razorpay TEST MODE Payment Links.

No real money is charged.

### 8️⃣ Recovery Attempt

Creating one new Payment Link equals one
recovery attempt.

Checking the status of the same Payment Link
does NOT create another recovery attempt.

### 9️⃣ Strict Verification

A payment is considered recovered only when:

- Payment Link status is `paid`
- Amount paid is at least the required amount
- A captured payment exists

### 🔟 Unique Transaction Tracking

Every new payment analysis receives a unique
Transaction ID.

Two transactions with the same amount are still
treated as different transactions.

### 1️⃣1️⃣ Portfolio Analytics

The dashboard can analyze:

100, 200, 500, 1,000, 2,000,
5,000, 10,000 and larger synthetic portfolios.

The selected transaction count dynamically
changes all portfolio metrics.

### 1️⃣2️⃣ Live vs Demo Data

The portfolio dashboard is synthetic demonstration
data.

The Live Razorpay section contains actual TEST MODE
recovery information.

These two data sources are intentionally kept
separate.
"""
    )


# ============================================================
# END OF PAYMENT RECOVERY AI
# ============================================================
