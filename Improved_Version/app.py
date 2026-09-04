# ============================================================
# PAYMENT RECOVERY AI
# ============================================================
# STEP 1  : Imports
# STEP 2  : Page configuration
# STEP 3  : Load ML model
# STEP 4  : Initialize session state
# STEP 5  : Payment input section
# STEP 6  : ML prediction
# STEP 7  : Risk analysis
# STEP 8  : Recovery recommendation
# STEP 9  : Razorpay Test Mode Payment Link
# STEP 10 : STRICT Razorpay payment verification
# STEP 11 : Correct recovery analytics
# STEP 12 : Recovery history
# ============================================================


# ============================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import uuid

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
    layout="centered"
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
# STEP 4: INITIALIZE SESSION STATE
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
# ORIGINAL TRANSACTION STATE
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
# DASHBOARD STATE
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
# UNIQUE ORIGINAL TRANSACTIONS ENTERING RECOVERY
# ------------------------------------------------------------

if "at_risk_transaction_ids" not in st.session_state:
    st.session_state.at_risk_transaction_ids = set()


# ============================================================
# STEP 5: APPLICATION HEADER
# ============================================================

st.title("💳 Payment Recovery AI")

st.subheader(
    "AI-Powered Payment Failure Prediction, "
    "Payment Recovery & Business Analytics"
)

st.info(
    "🧪 TEST MODE — Razorpay test transactions only. "
    "No real money will be charged."
)


# ============================================================
# STEP 6: PAYMENT INPUT SECTION
# ============================================================

st.header("💳 Payment & Technical Risk Details")


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
# STEP 7: ANALYZE PAYMENT
# ============================================================

if st.button(
    "🔍 Analyze Payment",
    use_container_width=True
):

    # --------------------------------------------------------
    # CREATE NEW UNIQUE TRANSACTION ID
    # --------------------------------------------------------

    new_transaction_id = (
        f"TXN-{uuid.uuid4().hex[:10].upper()}"
    )

    st.session_state.transaction_id = new_transaction_id


    # --------------------------------------------------------
    # CREATE INPUT DATA
    # --------------------------------------------------------

    input_data = pd.DataFrame(
        [{
            "amount": payment_amount,
            "payment_method": payment_method,
            "bank": bank,
            "device": device,
            "hour": hour,
            "previous_failures": previous_failures,
            "attempt_number": attempt_number,
            "error_code": error_code,
            "customer_type": customer_type
        }]
    )


    # --------------------------------------------------------
    # MACHINE LEARNING PREDICTION
    # --------------------------------------------------------

    try:

        probabilities = model.predict_proba(
            input_data
        )[0]

        classes = list(model.classes_)


        if "FAILED" in classes:

            failed_index = classes.index("FAILED")

            failure_probability = (
                probabilities[failed_index] * 100
            )

        else:

            prediction = model.predict(
                input_data
            )[0]

            failure_probability = (
                100.0 if prediction == 1 else 0.0
            )


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
            f"Customer has {previous_failures} previous "
            f"payment failure(s)."
        )


    if attempt_number > 1:

        reasons.append(
            f"This is payment attempt #{attempt_number}."
        )


    if error_code != "NONE":

        reasons.append(
            f"Technical error detected: {error_code}."
        )


    if payment_method == "CARD":

        reasons.append(
            "Card payments may be affected by issuer "
            "or authentication failures."
        )


    if payment_method == "UPI":

        reasons.append(
            "UPI payments can be affected by bank/network "
            "availability."
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
    # SAVE ANALYSIS
    # --------------------------------------------------------

    st.session_state.analyzed = True

    st.session_state.failure_probability = (
        failure_probability
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


    # --------------------------------------------------------
    # RESET OLD RECOVERY STATE
    # --------------------------------------------------------

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
# STEP 8: DISPLAY ANALYSIS RESULT
# ============================================================

if st.session_state.analyzed:

    st.header(
        "📊 AI Payment Risk Analysis"
    )


    # --------------------------------------------------------
    # TRANSACTION ID
    # --------------------------------------------------------

    st.caption(
        f"Transaction ID: "
        f"{st.session_state.transaction_id}"
    )


    # --------------------------------------------------------
    # FAILURE PROBABILITY
    # --------------------------------------------------------

    probability = (
        st.session_state.failure_probability
    )

    risk = (
        st.session_state.risk_level
    )


    if risk == "HIGH":

        st.error(
            f"🔴 HIGH RISK — Failure Probability: "
            f"{probability:.2f}%"
        )

    elif risk == "MEDIUM":

        st.warning(
            f"🟠 MEDIUM RISK — Failure Probability: "
            f"{probability:.2f}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — Failure Probability: "
            f"{probability:.2f}%"
        )


    # --------------------------------------------------------
    # RISK FACTORS
    # --------------------------------------------------------

    st.subheader(
        "🔎 Risk Factors"
    )


    for reason in st.session_state.reasons:

        st.write(
            f"• {reason}"
        )


# ============================================================
# STEP 9: RECOVERY STRATEGY
# ============================================================

if (
    st.session_state.analyzed
    and st.session_state.risk_level
    in ["MEDIUM", "HIGH"]
):

    error_code = (
        st.session_state.analyzed_error_code
    )

    risk_level = (
        st.session_state.risk_level
    )


    # --------------------------------------------------------
    # DETERMINE RECOVERY METHOD
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
    # CREATE RECOVERY PAYMENT
    # ========================================================

    if st.button(
        "💳 Create Recovery Payment",
        use_container_width=True
    ):

        try:

            # ------------------------------------------------
            # COUNT PREVIOUS ATTEMPTS FOR THIS TRANSACTION
            # ------------------------------------------------

            existing_attempts = 0


            for record in (
                st.session_state.recovery_history
            ):

                if (
                    record.get("Transaction ID")
                    == st.session_state.transaction_id
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
            # CREATE RAZORPAY PAYMENT LINK
            # ------------------------------------------------

            payment_link = create_payment_link(

                st.session_state.payment_amount,

                "Payment Recovery AI - Recovery Payment",

                internal_reference_id
            )


            # ------------------------------------------------
            # READ RESPONSE
            # ------------------------------------------------

            payment_link_id = (
                payment_link.get("id")
            )

            payment_link_url = (
                payment_link.get("short_url")
            )

            payment_link_status = (
                payment_link.get(
                    "status",
                    "created"
                )
            )


            # ------------------------------------------------
            # VALIDATE PAYMENT LINK
            # ------------------------------------------------

            if not payment_link_id:

                st.error(
                    "❌ Razorpay did not return "
                    "a Payment Link ID."
                )

                st.stop()


            # ------------------------------------------------
            # SAVE ACTIVE PAYMENT LINK
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


            # =================================================
            # ANALYTICS
            # =================================================

            # Creating a NEW Payment Link = ONE attempt.

            st.session_state.total_recovery_attempts += 1


            # ------------------------------------------------
            # AT-RISK AMOUNT
            # ------------------------------------------------

            current_transaction_id = (
                st.session_state.transaction_id
            )


            if (
                current_transaction_id
                not in st.session_state.at_risk_transaction_ids
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
            # DISPLAY
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
                "⚠️ For testing FAILURE, use a fresh "
                "Payment Link. Do not reuse a Payment Link "
                "that was already successfully paid."
            )


            st.caption(
                "🧪 Razorpay Test Mode — no real money will be charged."
            )


        except Exception as e:

            st.error(
                "❌ Failed to create Razorpay Payment Link."
            )

            st.exception(e)


# ============================================================
# STEP 10: STRICT RAZORPAY PAYMENT VERIFICATION
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
            # GET PAYMENT LINK STATUS
            # ------------------------------------------------

            latest_status = (
                str(
                    latest_payment.get(
                        "status",
                        "unknown"
                    )
                ).lower()
            )


            # ------------------------------------------------
            # GET AMOUNT
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
            # GET PAYMENTS ARRAY
            # ------------------------------------------------

            payments = (
                latest_payment.get(
                    "payments"
                )
            )


            # ------------------------------------------------
            # DETERMINE WHETHER A CAPTURED PAYMENT EXISTS
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
            # STORE RAZORPAY INFORMATION
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
                    record.get("Payment Link ID")
                    == active_payment_link_id
                ):

                    history_index = index

                    break


            # =================================================
            # STRICT SUCCESS CHECK
            # =================================================
            #
            # Recovery is SUCCESSFUL only when ALL required
            # evidence is present:
            #
            # 1. Payment Link status = paid
            # 2. amount_paid >= required amount
            # 3. payments array contains captured payment
            #
            # This prevents our application from blindly
            # trusting only the "paid" string.
            # =================================================

            required_amount_paise = (
                amount_paise
            )


            payment_is_really_paid = (

                latest_status == "paid"

                and

                amount_paid_paise
                >= required_amount_paise

                and

                captured_payment is not None
            )


            # =================================================
            # CASE 1: VERIFIED SUCCESS
            # =================================================

            if payment_is_really_paid:

                st.session_state.recovery_result = True


                # ------------------------------------------------
                # CHECK WHETHER ORIGINAL TRANSACTION WAS ALREADY
                # RECOVERED
                # ------------------------------------------------

                transaction_already_recovered = False


                for record in (
                    st.session_state.recovery_history
                ):

                    if (

                        record.get("Transaction ID")
                        == st.session_state.transaction_id

                        and

                        record.get("Result")
                        == "✅ RECOVERED"

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
                    ]["Razorpay Status"] = (
                        latest_status
                    )

                    st.session_state.recovery_history[
                        history_index
                    ]["Amount Paid"] = (
                        f"₹{amount_paid_rupees:,.2f}"
                    )

                    st.session_state.recovery_history[
                        history_index
                    ]["Payment ID"] = (
                        st.session_state.razorpay_payment_id
                        or "-"
                    )

                    st.session_state.recovery_history[
                        history_index
                    ]["Result"] = (
                        "✅ RECOVERED"
                    )


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
            # CASE 2: NOT PAID
            # =================================================

            else:

                # ------------------------------------------------
                # NEVER MARK AS RECOVERED
                # ------------------------------------------------

                st.session_state.recovery_result = False


                # ------------------------------------------------
                # IF PAYMENT LINK IS STILL ACTIVE
                # ------------------------------------------------

                if latest_status in [
                    "created",
                    "issued",
                    "partially_paid"
                ]:

                    if history_index is not None:

                        st.session_state.recovery_history[
                            history_index
                        ]["Razorpay Status"] = (
                            latest_status
                        )

                        st.session_state.recovery_history[
                            history_index
                        ]["Amount Paid"] = (
                            f"₹{amount_paid_rupees:,.2f}"
                        )

                        st.session_state.recovery_history[
                            history_index
                        ]["Result"] = (
                            "❌ NOT RECOVERED"
                        )


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
                # EXPIRED / CANCELLED
                # ------------------------------------------------

                else:

                    if history_index is not None:

                        st.session_state.recovery_history[
                            history_index
                        ]["Razorpay Status"] = (
                            latest_status
                        )

                        st.session_state.recovery_history[
                            history_index
                        ]["Amount Paid"] = (
                            f"₹{amount_paid_rupees:,.2f}"
                        )

                        st.session_state.recovery_history[
                            history_index
                        ]["Result"] = (
                            "❌ FAILED"
                        )


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
            # DEBUG INFORMATION
            # =================================================
            #
            # This is useful during your demo/testing.
            # It lets you see exactly what Razorpay returned.
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
                    "YES" if captured_payment else "NO"
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


            # ------------------------------------------------
            # IMPORTANT MESSAGE
            # ------------------------------------------------

            st.caption(
                "ℹ️ Checking status does not create a new "
                "recovery attempt."
            )


        except Exception as e:

            st.error(
                "❌ Unable to fetch Razorpay payment status."
            )

            st.exception(e)


# ============================================================
# STEP 11: CURRENT RECOVERY RESULT
# ============================================================

if (
    st.session_state.razorpay_payment_link_id
    and
    st.session_state.recovery_result is not None
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
# STEP 12: BUSINESS ANALYTICS DASHBOARD
# ============================================================

st.divider()

st.header(
    "📈 Payment Recovery Dashboard"
)


# ------------------------------------------------------------
# SUCCESS RATE
# ------------------------------------------------------------

if (
    st.session_state.total_recovery_attempts > 0
):

    recovery_success_rate = (

        st.session_state.successful_recoveries

        /

        st.session_state.total_recovery_attempts

        *

        100
    )

else:

    recovery_success_rate = 0.0


# ------------------------------------------------------------
# DASHBOARD METRICS
# ------------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "At-Risk Payment Amount",
        f"₹{st.session_state.at_risk_amount:,.2f}"
    )


with col2:

    st.metric(
        "Recovery Attempts",
        st.session_state.total_recovery_attempts
    )


col3, col4 = st.columns(2)


with col3:

    st.metric(
        "Successful Recoveries",
        st.session_state.successful_recoveries
    )


with col4:

    st.metric(
        "Risky Amount Recovered",
        f"₹{st.session_state.total_money_recovered:,.2f}"
    )


st.metric(
    "Recovery Success Rate",
    f"{recovery_success_rate:.1f}%"
)


# ------------------------------------------------------------
# DASHBOARD DEFINITIONS
# ------------------------------------------------------------

st.caption(
    "Recovery Attempts = number of unique recovery "
    "Payment Links created."
)


st.caption(
    "Successful Recoveries = unique original transactions "
    "with a verified captured payment."
)


st.caption(
    "At-Risk Payment Amount = unique original transactions "
    "that entered the recovery process."
)


# ============================================================
# STEP 13: RECOVERY HISTORY
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


    # --------------------------------------------------------
    # COLUMN ORDER
    # --------------------------------------------------------

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
# STEP 14: SYSTEM LOGIC
# ============================================================

with st.expander(
    "ℹ️ How Payment Recovery AI works"
):

    st.markdown(
        """
### 1️⃣ Payment Analysis

The ML model analyzes the transaction and predicts
the probability of payment failure.

### 2️⃣ Risk Classification

- 🟢 LOW: Failure probability below 30%
- 🟠 MEDIUM: Failure probability from 30% to below 70%
- 🔴 HIGH: Failure probability 70% or above

### 3️⃣ Recovery Recommendation

The system recommends a recovery strategy based on
the detected error and risk level.

### 4️⃣ Razorpay Test Mode

For MEDIUM/HIGH risk payments, the application
creates a Razorpay Test Mode Payment Link.

### 5️⃣ Recovery Attempt

Creating one Payment Link = one recovery attempt.

Checking its status multiple times does NOT create
additional recovery attempts.

### 6️⃣ Strict Payment Verification

The application does NOT mark a payment as recovered
just because a status value says "paid".

It verifies:

- Payment Link status
- Amount paid
- Captured payment information

### 7️⃣ Failed Payment

If the payment is not successfully captured,
the application shows:

❌ RECOVERY NOT SUCCESSFUL

and does NOT increment Successful Recoveries.

### 8️⃣ Unique Transaction Tracking

Every new analysis receives a unique Transaction ID.

Two transactions with the same amount are still treated
as different transactions.

### 9️⃣ Duplicate Status Checks

Checking the same Payment Link repeatedly updates the
same history record.

It does NOT create duplicate recovery attempts.

### 🔟 Successful Recovery

A successful original transaction is counted only once,
even if its status is checked multiple times.
"""
    )


# ============================================================
# END OF PAYMENT RECOVERY AI
# ============================================================
