# ============================================================
# 💳 PAYMENT RECOVERY AI
# ============================================================
#
# COMPLETE WORKFLOW
#
# Customer enters payment details
#           ↓
# REAL ML MODEL
#           ↓
# Failure Probability
#           ↓
# LOW / MEDIUM / HIGH
#           ↓
# Possible Issue Explanation
#           ↓
# Recovery Recommendation
#           ↓
# Customer clicks Recovery Button
#           ↓
# Recovery Simulation
#           ↓
# SUCCESS / FAILED
#           ↓
# BUSINESS DASHBOARD
#           ↓
# RECOVERY HISTORY
#
# BUSINESS LOGIC
#
# LOW RISK
#   → Normal payment
#   → NOT a recovery case
#   → NOT added to dashboard/history
#
# MEDIUM / HIGH RISK
#   → At-risk payment
#   → Recovery action required
#   → Added to dashboard/history ONLY after button click
#
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import random


# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Payment Recovery AI",
    page_icon="💳",
    layout="centered"
)


# ============================================================
# 3. LOAD TRAINED ML MODEL
# ============================================================
#
# payment_model.pkl = REAL trained ML model
#
# It was trained in Google Colab and downloaded into
# the razorpay folder.
#
# ============================================================

model = joblib.load("payment_model.pkl")


# ============================================================
# 4. RECOVERY SIMULATION FUNCTION
# ============================================================
#
# IMPORTANT:
# This is ONLY a simulation.
# No real money is processed.
#
# Later we can replace this with a real payment gateway API.
#
# ============================================================

def simulate_recovery(amount, risk_level):

    if risk_level == "MEDIUM":

        recovery_probability = 0.70

    elif risk_level == "HIGH":

        recovery_probability = 0.50

    else:

        recovery_probability = 0.90

    random_value = random.random()

    return random_value < recovery_probability


# ============================================================
# 5. INITIALIZE ANALYSIS SESSION STATE
# ============================================================

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


if "failure_probability" not in st.session_state:
    st.session_state.failure_probability = 0.0


if "risk_level" not in st.session_state:
    st.session_state.risk_level = ""


if "reasons" not in st.session_state:
    st.session_state.reasons = []


if "payment_amount" not in st.session_state:
    st.session_state.payment_amount = 0


if "analyzed_error_code" not in st.session_state:
    st.session_state.analyzed_error_code = "NONE"


if "analyzed_payment_method" not in st.session_state:
    st.session_state.analyzed_payment_method = ""


if "recovery_result" not in st.session_state:
    st.session_state.recovery_result = None


if "recovery_method" not in st.session_state:
    st.session_state.recovery_method = ""


# ============================================================
# 6. BUSINESS DASHBOARD STATE
# ============================================================

if "at_risk_amount" not in st.session_state:
    st.session_state.at_risk_amount = 0


if "total_recovery_attempts" not in st.session_state:
    st.session_state.total_recovery_attempts = 0


if "successful_recoveries" not in st.session_state:
    st.session_state.successful_recoveries = 0


if "total_money_recovered" not in st.session_state:
    st.session_state.total_money_recovered = 0


# ============================================================
# 7. RECOVERY HISTORY STATE
# ============================================================

if "recovery_history" not in st.session_state:
    st.session_state.recovery_history = []


# ============================================================
# 8. RECOVERY EVENT TRACKING
# ============================================================
#
# Every time a recovery button is clicked:
#
# recovery_event_id increases.
#
# This ensures that one recovery click is counted only once.
#
# ============================================================

if "recovery_event_id" not in st.session_state:
    st.session_state.recovery_event_id = 0


if "counted_event_id" not in st.session_state:
    st.session_state.counted_event_id = 0


# ============================================================
# 9. APPLICATION TITLE
# ============================================================

st.title("💳 Payment Recovery AI")

st.subheader(
    "Predict payment risk and recover failed transactions"
)

st.write(
    """
    This system analyzes a payment transaction,
    predicts its failure risk, explains the possible
    issue, and recommends a recovery action.
    """
)


# ============================================================
# 10. PAYMENT INPUTS
# ============================================================

st.header("Enter Payment Details")


# ------------------------------------------------------------
# 10.1 Payment Amount
# ------------------------------------------------------------

amount = st.number_input(
    "Payment Amount (₹)",
    min_value=100,
    max_value=100000,
    value=5000
)


# ------------------------------------------------------------
# 10.2 Payment Method
# ------------------------------------------------------------

payment_method = st.selectbox(
    "Payment Method",
    [
        "UPI",
        "CARD",
        "NET_BANKING"
    ]
)


# ------------------------------------------------------------
# 10.3 Bank
# ------------------------------------------------------------

bank = st.selectbox(
    "Bank",
    [
        "Bank_A",
        "Bank_B",
        "Bank_C",
        "Bank_D"
    ]
)


# ------------------------------------------------------------
# 10.4 Device
# ------------------------------------------------------------

device = st.selectbox(
    "Device",
    [
        "Android",
        "iOS",
        "Desktop"
    ]
)


# ------------------------------------------------------------
# 10.5 Payment Hour
# ------------------------------------------------------------

hour = st.slider(
    "Payment Hour",
    min_value=0,
    max_value=23,
    value=12
)


# ------------------------------------------------------------
# 10.6 Previous Payment Failures
# ------------------------------------------------------------

previous_failures = st.number_input(
    "Previous Payment Failures",
    min_value=0,
    max_value=10,
    value=0
)


# ------------------------------------------------------------
# 10.7 Current Attempt Number
# ------------------------------------------------------------

attempt_number = st.number_input(
    "Current Attempt Number",
    min_value=1,
    max_value=10,
    value=1
)


# ------------------------------------------------------------
# 10.8 Payment Error
# ------------------------------------------------------------

error_code = st.selectbox(
    "Payment Error",
    [
        "NONE",
        "AUTH_ERROR",
        "BANK_ERROR",
        "CARD_DECLINED",
        "NETWORK_ERROR"
    ]
)


# ------------------------------------------------------------
# 10.9 Customer Type
# ------------------------------------------------------------

customer_type = st.selectbox(
    "Customer Type",
    [
        "NEW",
        "RETURNING"
    ]
)


# ============================================================
# 11. ANALYZE PAYMENT
# ============================================================

if st.button(
    "🔍 Analyze Payment",
    use_container_width=True
):

    # --------------------------------------------------------
    # 11.1 Create transaction
    # --------------------------------------------------------

    transaction = pd.DataFrame({

        "amount": [amount],

        "payment_method": [payment_method],

        "bank": [bank],

        "device": [device],

        "hour": [hour],

        "previous_failures": [previous_failures],

        "attempt_number": [attempt_number],

        "error_code": [error_code],

        "customer_type": [customer_type]

    })


    # --------------------------------------------------------
    # 11.2 REAL ML MODEL PREDICTION
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        transaction
    )


    # --------------------------------------------------------
    # 11.3 Find FAILED class
    # --------------------------------------------------------

    failed_index = list(
        model.classes_
    ).index("FAILED")


    # --------------------------------------------------------
    # 11.4 Calculate Failure Probability
    # --------------------------------------------------------

    failure_probability = (
        probabilities[0][failed_index] * 100
    )


    # --------------------------------------------------------
    # 11.5 Determine Risk Level
    # --------------------------------------------------------

    if failure_probability < 30:

        risk_level = "LOW"

    elif failure_probability < 70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    # ========================================================
    # 11.6 CREATE ISSUE EXPLANATION
    # ========================================================

    reasons = []


    # Previous failures

    if previous_failures >= 2:

        reasons.append(
            f"{previous_failures} previous payment failures"
        )

    elif previous_failures == 1:

        reasons.append(
            "1 previous payment failure"
        )


    # Attempt number

    if attempt_number >= 3:

        reasons.append(
            f"Payment attempt #{attempt_number}"
        )


    # Payment error

    if error_code != "NONE":

        reasons.append(
            f"Payment error: {error_code}"
        )


    # High amount

    if amount > 15000:

        reasons.append(
            "High transaction amount"
        )


    # No warning

    if len(reasons) == 0:

        reasons.append(
            "No major warning signal detected"
        )


    # ========================================================
    # 11.7 SAVE ANALYSIS RESULT
    # ========================================================

    st.session_state.analyzed = True

    st.session_state.failure_probability = (
        failure_probability
    )

    st.session_state.risk_level = risk_level

    st.session_state.reasons = reasons

    st.session_state.payment_amount = amount

    st.session_state.analyzed_error_code = (
        error_code
    )

    st.session_state.analyzed_payment_method = (
        payment_method
    )


    # --------------------------------------------------------
    # Reset old recovery result
    # --------------------------------------------------------

    st.session_state.recovery_result = None

    st.session_state.recovery_method = ""


# ============================================================
# 12. DISPLAY ML RESULT
# ============================================================

if st.session_state.analyzed:

    st.divider()

    st.header("🔎 Payment Risk Result")


    # --------------------------------------------------------
    # 12.1 Failure Probability
    # --------------------------------------------------------

    st.metric(
        "Failure Probability",
        f"{st.session_state.failure_probability:.2f}%"
    )


    # --------------------------------------------------------
    # 12.2 Risk Level
    # --------------------------------------------------------

    if st.session_state.risk_level == "HIGH":

        st.error(
            f"🔴 Risk Level: {st.session_state.risk_level}"
        )

    elif st.session_state.risk_level == "MEDIUM":

        st.warning(
            f"🟡 Risk Level: {st.session_state.risk_level}"
        )

    else:

        st.success(
            f"🟢 Risk Level: {st.session_state.risk_level}"
        )


    # ========================================================
    # 13. POSSIBLE ISSUE EXPLANATION
    # ========================================================

    st.header("🔎 Possible Issue")


    for reason in st.session_state.reasons:

        st.write(
            "•",
            reason
        )


    # ========================================================
    # 14. RECOMMENDED RECOVERY ACTION
    # ========================================================

    st.header("🧠 Recommended Recovery Action")


    analyzed_error = (
        st.session_state.analyzed_error_code
    )

    current_risk = (
        st.session_state.risk_level
    )


    # ========================================================
    # 14.1 LOW RISK
    # ========================================================
    #
    # LOW risk is NOT a recovery case.
    #
    # No recovery button.
    # No dashboard entry.
    # No history entry.
    #
    # ========================================================

    if current_risk == "LOW":

        st.success(
            "🟢 Low risk detected. "
            "No recovery action is required."
        )

        st.info(
            "💰 This payment is expected to proceed normally."
        )


    # ========================================================
    # 14.2 AUTHENTICATION ERROR
    # ========================================================

    elif analyzed_error == "AUTH_ERROR":

        st.info(
            "🔐 Complete authentication and retry the payment."
        )


        if st.button(
            "🔄 Complete Authentication & Retry",
            key="auth_retry",
            use_container_width=True
        ):

            st.session_state.recovery_method = (
                "Authentication Retry"
            )

            st.session_state.recovery_result = (
                simulate_recovery(
                    st.session_state.payment_amount,
                    current_risk
                )
            )

            st.session_state.recovery_event_id += 1


    # ========================================================
    # 14.3 CARD DECLINED
    # ========================================================

    elif analyzed_error == "CARD_DECLINED":

        st.info(
            "💳 Card was declined. "
            "Try another payment method."
        )


        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # Try UPI
        # ----------------------------------------------------

        with col1:

            if st.button(
                "📱 Try UPI",
                key="try_upi",
                use_container_width=True
            ):

                st.session_state.recovery_method = "UPI"

                st.session_state.recovery_result = (
                    simulate_recovery(
                        st.session_state.payment_amount,
                        current_risk
                    )
                )

                st.session_state.recovery_event_id += 1


        # ----------------------------------------------------
        # Try Net Banking
        # ----------------------------------------------------

        with col2:

            if st.button(
                "🏦 Try Net Banking",
                key="try_netbanking",
                use_container_width=True
            ):

                st.session_state.recovery_method = (
                    "Net Banking"
                )

                st.session_state.recovery_result = (
                    simulate_recovery(
                        st.session_state.payment_amount,
                        current_risk
                    )
                )

                st.session_state.recovery_event_id += 1


    # ========================================================
    # 14.4 BANK ERROR
    # ========================================================

    elif analyzed_error == "BANK_ERROR":

        st.info(
            "🏦 Bank issue detected. "
            "Try another bank or payment method."
        )


        if st.button(
            "💳 Choose Another Payment Method",
            key="another_payment_method",
            use_container_width=True
        ):

            st.session_state.recovery_method = (
                "Alternative Payment Method"
            )

            st.session_state.recovery_result = (
                simulate_recovery(
                    st.session_state.payment_amount,
                    current_risk
                )
            )

            st.session_state.recovery_event_id += 1


    # ========================================================
    # 14.5 NETWORK ERROR
    # ========================================================

    elif analyzed_error == "NETWORK_ERROR":

        st.info(
            "🌐 Network problem detected. "
            "Retry after a short delay."
        )


        if st.button(
            "🔄 Retry Payment",
            key="retry_payment",
            use_container_width=True
        ):

            st.session_state.recovery_method = (
                "Payment Retry"
            )

            st.session_state.recovery_result = (
                simulate_recovery(
                    st.session_state.payment_amount,
                    current_risk
                )
            )

            st.session_state.recovery_event_id += 1


    # ========================================================
    # 14.6 HIGH RISK
    # ========================================================

    elif current_risk == "HIGH":

        st.warning(
            "⚠️ High payment failure risk detected."
        )


        if st.button(
            "💳 Try Alternative Payment Method",
            key="high_risk_alternative",
            use_container_width=True
        ):

            st.session_state.recovery_method = (
                "Alternative Payment Method"
            )

            st.session_state.recovery_result = (
                simulate_recovery(
                    st.session_state.payment_amount,
                    current_risk
                )
            )

            st.session_state.recovery_event_id += 1


    # ========================================================
    # 14.7 MEDIUM RISK
    # ========================================================

    elif current_risk == "MEDIUM":

        st.info(
            "🟡 Medium risk detected. "
            "You can continue or use another payment method."
        )


        col1, col2 = st.columns(2)


        with col1:

            if st.button(
                "🔄 Continue Payment",
                key="continue_payment",
                use_container_width=True
            ):

                st.session_state.recovery_method = (
                    "Continue Payment"
                )

                st.session_state.recovery_result = (
                    simulate_recovery(
                        st.session_state.payment_amount,
                        current_risk
                    )
                )

                st.session_state.recovery_event_id += 1


        with col2:

            if st.button(
                "💳 Use Another Method",
                key="medium_alternative",
                use_container_width=True
            ):

                st.session_state.recovery_method = (
                    "Alternative Payment Method"
                )

                st.session_state.recovery_result = (
                    simulate_recovery(
                        st.session_state.payment_amount,
                        current_risk
                    )
                )

                st.session_state.recovery_event_id += 1


    # ========================================================
    # 15. RECOVERY RESULT
    # ========================================================

    if st.session_state.recovery_result is not None:

        st.divider()

        st.header("🔄 Recovery Result")


        # ----------------------------------------------------
        # 15.1 SUCCESS
        # ----------------------------------------------------

        if st.session_state.recovery_result:

            st.success(
                "🎉 Payment recovered successfully!"
            )


            st.metric(
                "💰 Recovered Amount",
                f"₹{st.session_state.payment_amount:,.2f}"
            )


            st.write(
                f"Recovery method: "
                f"**{st.session_state.recovery_method}**"
            )


            st.info(
                "✅ This transaction was at risk, "
                "but the recovery action successfully "
                "retained the payment."
            )


        # ----------------------------------------------------
        # 15.2 FAILURE
        # ----------------------------------------------------

        else:

            st.error(
                "❌ Recovery attempt failed."
            )


            st.write(
                f"Recovery method tried: "
                f"**{st.session_state.recovery_method}**"
            )


            st.warning(
                "The customer can try another recovery method."
            )



# ============================================================
# 16. UPDATE BUSINESS DASHBOARD
# ============================================================
#
# IMPORTANT BUSINESS RULE:
#
# Recovery attempts may happen multiple times for the same
# transaction, but the transaction amount can be recovered
# ONLY ONCE.
#
# Example:
# Payment = ₹5,000
# Attempt 1 = FAILED      → Recovered ₹0
# Attempt 2 = SUCCESS     → Recovered ₹5,000
# Attempt 3 = SUCCESS     → Still ₹5,000 (NOT ₹10,000)
#
# ============================================================

if (
    st.session_state.recovery_event_id
    != st.session_state.counted_event_id
):

    # --------------------------------------------------------
    # 16.1 Count recovery attempt
    # --------------------------------------------------------

    st.session_state.total_recovery_attempts += 1


    # --------------------------------------------------------
    # 16.2 Add payment to AT-RISK amount only once
    # --------------------------------------------------------

    # Check whether this transaction amount has already
    # entered the dashboard.

    transaction_already_counted = any(
        record.get("Transaction Amount") ==
        st.session_state.payment_amount
        for record in st.session_state.recovery_history
    )


    if not transaction_already_counted:

        st.session_state.at_risk_amount += (
            st.session_state.payment_amount
        )


    # --------------------------------------------------------
    # 16.3 Count successful recovery
    # --------------------------------------------------------

    if st.session_state.recovery_result:

        # Only count money if this transaction has NOT
        # already been successfully recovered.

        transaction_already_recovered = any(
            record.get("Transaction Amount") ==
            st.session_state.payment_amount
            and record.get("Result") == "✅ RECOVERED"
            for record in st.session_state.recovery_history
        )


        if not transaction_already_recovered:

            st.session_state.successful_recoveries += 1

            st.session_state.total_money_recovered += (
                st.session_state.payment_amount
            )


    # --------------------------------------------------------
    # 16.4 Mark event as counted
    # --------------------------------------------------------

    st.session_state.counted_event_id = (
        st.session_state.recovery_event_id
    )


    # ========================================================
    # 16.5 SAVE RECOVERY TO HISTORY
    # ========================================================

    recovery_record = {

        "Transaction Amount":
            st.session_state.payment_amount,

        "Amount (₹)":
            st.session_state.payment_amount,

        "Risk Level":
            st.session_state.risk_level,

        "Failure Probability":
            f"{st.session_state.failure_probability:.2f}%",

        "Recovery Method":
            st.session_state.recovery_method,

        "Result":
            (
                "✅ RECOVERED"
                if st.session_state.recovery_result
                else "❌ FAILED"
            )
    }


    st.session_state.recovery_history.append(
        recovery_record
    )



# ============================================================
# 17. RECOVERY BUSINESS DASHBOARD
# ============================================================

st.divider()

st.header("📊 Recovery Business Dashboard")


# ------------------------------------------------------------
# 17.1 Calculate Recovery Success Rate
# ------------------------------------------------------------

if st.session_state.total_recovery_attempts > 0:

    recovery_rate = (
        st.session_state.successful_recoveries
        /
        st.session_state.total_recovery_attempts
    ) * 100

else:

    recovery_rate = 0


# ============================================================
# 17.2 AT-RISK PAYMENT AMOUNT
# ============================================================

st.metric(
    "⚠️ At-Risk Payment Amount",
    f"₹{st.session_state.at_risk_amount:,.2f}"
)


# ============================================================
# 17.3 RECOVERY ATTEMPTS + SUCCESSFUL RECOVERIES
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "🔄 Recovery Attempts",
        st.session_state.total_recovery_attempts
    )


with col2:

    st.metric(
        "✅ Successful Recoveries",
        st.session_state.successful_recoveries
    )


# ============================================================
# 17.4 RISKY AMOUNT RECOVERED + SUCCESS RATE
# ============================================================

col3, col4 = st.columns(2)


with col3:

    st.metric(
        "💰 Risky Amount Recovered",
        f"₹{st.session_state.total_money_recovered:,.2f}"
    )


with col4:

    st.metric(
        "📈 Recovery Success Rate",
        f"{recovery_rate:.1f}%"
    )


# ============================================================
# 17.5 BUSINESS IMPACT
# ============================================================

if st.session_state.total_recovery_attempts > 0:

    st.success(
        f"""
        💰 Business Impact

        The AI identified payment attempts worth
        ₹{st.session_state.at_risk_amount:,.2f}
        as recovery cases.

        The recovery system successfully retained
        ₹{st.session_state.total_money_recovered:,.2f}
        of that potentially lost payment value.
        """
    )

else:

    st.info(
        "No at-risk payments have entered recovery yet. "
        "Analyze a MEDIUM or HIGH risk payment and try "
        "a recovery action."
    )


# ============================================================
# 18. RECOVERY HISTORY
# ============================================================

st.divider()

st.header("📋 Recovery History")


# ------------------------------------------------------------
# 18.1 Display recovery history
# ------------------------------------------------------------

if len(st.session_state.recovery_history) > 0:

    history_df = pd.DataFrame(
        st.session_state.recovery_history
    )


    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No recovery transactions yet. "
        "Only MEDIUM and HIGH risk payments that "
        "trigger a recovery action appear here."
    )


# ============================================================
# 19. END OF APPLICATION
# ============================================================