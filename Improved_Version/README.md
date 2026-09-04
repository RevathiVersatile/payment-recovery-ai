# 💳 Payment Recovery AI

### AI-Powered Payment Failure Prediction, Recovery & Business Analytics

Payment Recovery AI is an intelligent payment-risk and recovery system designed to predict the probability of payment failure and assist businesses in recovering failed payments.

The application combines **Machine Learning, Streamlit, and Razorpay Test Mode** to demonstrate an end-to-end payment recovery workflow.

> ⚠️ **Demo Mode:** This project currently uses Razorpay **Test Mode**. No real money is charged.

---

## 🚀 Project Overview

Payment failures can lead to lost revenue and frustrated customers.

This project provides an intelligent workflow:

```text
Customer Payment
       ↓
Payment Risk Prediction
       ↓
Failure Probability
       ↓
Risk Classification
       ↓
Failure Reason Analysis
       ↓
Recovery Recommendation
       ↓
Razorpay Payment Link
       ↓
Payment Status Verification
       ↓
Recovery Analytics
```

The system helps demonstrate how AI/ML can be used to identify risky transactions and support payment recovery.

---

## ✨ Key Features

### 🤖 1. Payment Failure Prediction

The Machine Learning model predicts whether a payment is likely to fail based on transaction characteristics.

Input factors include:

* Payment amount
* Payment method
* Bank
* Device
* Transaction hour
* Previous payment failures
* Attempt number
* Error code
* Customer type

---

### 📊 2. Risk Classification

The predicted failure probability is converted into three risk levels:

| Risk Level | Failure Probability |
| ---------- | ------------------: |
| 🟢 LOW     |               < 30% |
| 🟡 MEDIUM  |           30% – 69% |
| 🔴 HIGH    |               ≥ 70% |

---

### 🔍 3. Failure Reason Analysis

The application provides understandable reasons behind the predicted risk.

Examples:

* Previous payment failures
* Multiple payment attempts
* Bank-related errors
* Authentication errors
* Card declines
* Network-related issues
* High predicted failure probability

---

### 💡 4. AI-Based Recovery Recommendation

Based on the transaction risk and failure reason, the system recommends an appropriate recovery strategy.

Examples:

```text
CARD_DECLINED
      ↓
Alternative Payment Method
```

```text
NETWORK_ERROR
      ↓
Payment Retry
```

```text
AUTH_ERROR
      ↓
Authentication Retry
```

---

### 💳 5. Razorpay Payment Recovery

The application integrates with **Razorpay Test Mode** to create recovery Payment Links.

The recovery flow is:

```text
Payment Failure
      ↓
Recovery Recommendation
      ↓
Create Payment Link
      ↓
Customer Opens Link
      ↓
Test Payment
      ↓
Verify Payment Status
```

Each recovery attempt receives a unique Razorpay reference ID.

---

### ✅ 6. Payment Verification

The application verifies whether the recovery payment was actually completed.

A recovery is considered successful only when:

* Payment Link status is `paid`
* Required amount has been paid
* A captured payment is found

This prevents the dashboard from incorrectly marking unsuccessful payments as recovered.

---

### 📈 7. Recovery Analytics Dashboard

The dashboard tracks:

* At-Risk Payment Amount
* Recovery Attempts
* Successful Recoveries
* Risky Amount Recovered
* Recovery Success Rate
* Recovery History

---

## 🧠 Machine Learning

The project uses a trained Machine Learning classification model stored as:

```text
payment_model.pkl
```

The model uses transaction information to estimate payment failure risk.

The current project focuses on **payment failure prediction**, while the recovery workflow provides actionable recommendations based on the predicted risk and transaction context.

---

## 🛠️ Technology Stack

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Core programming          |
| Streamlit    | Web application           |
| Pandas       | Data processing           |
| NumPy        | Numerical operations      |
| Scikit-learn | Machine Learning          |
| Joblib       | Model loading             |
| Razorpay     | Payment integration       |
| GitHub       | Version control & hosting |

---

## 📁 Project Structure

```text
payment-recovery-ai/
│
├── app.py
├── razorpay_integration.py
├── payment_model.pkl
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml        # NOT uploaded to GitHub
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/payment-recovery-ai.git
```

Navigate into the project:

```bash
cd payment-recovery-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Razorpay Configuration

Create:

```text
.streamlit/secrets.toml
```

Add your Razorpay Test Mode credentials:

```toml
RAZORPAY_KEY_ID = "YOUR_TEST_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_TEST_KEY_SECRET"
```

### ⚠️ Security

**Never upload `secrets.toml` or Razorpay secret keys to GitHub.**

The `.gitignore` file is configured to prevent sensitive credentials from being committed.

---

## ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

## 🧪 Razorpay Test Mode

This project uses Razorpay Test Mode for safe demonstration.

Test Mode allows the complete payment workflow to be demonstrated without charging real money.

```text
Test Transaction
      ↓
Recovery Payment Link
      ↓
Test Success / Failure
      ↓
Payment Verification
      ↓
Analytics Update
```

---

## 🔮 Future Enhancement — Adaptive Recovery Engine

A planned enhancement is an **Adaptive Recovery Engine**.

Instead of repeatedly using the same recovery strategy, the system can maintain a stable transaction journey:

```text
TX2
 │
 ├── Original Payment ❌
 │
 ├── Recovery Attempt 1 — UPI ❌
 │
 ├── AI Reassessment
 │
 ├── Recovery Attempt 2 — Alternative Method
 │
 └── Final Status → RECOVERED ✅
```

The future system can:

* Maintain one transaction ID across recovery attempts
* Track recovery attempt history
* Avoid repeatedly using failed strategies
* Recommend the next-best recovery action
* Limit the number of recovery attempts
* Escalate unsuccessful transactions for manual support

> The current ML model predicts payment failure risk. The future Adaptive Recovery Engine will use transaction context and previous recovery outcomes to select the next recovery strategy.

---

## 🎯 Project Objective

The main objective of Payment Recovery AI is to demonstrate how **Machine Learning + Payment Gateway Integration + Business Analytics** can be combined to reduce payment-related revenue loss.

---

## 👩‍💻 Author

**Revathi**

B.Tech — Electronics & Communication Engineering

---

## 📌 Project Status

🟢 **Working Demo**

Current capabilities:

* Payment failure prediction
* Risk classification
* Failure reason analysis
* Recovery recommendations
* Razorpay Test Mode integration
* Payment Link generation
* Payment verification
* Recovery analytics
* Recovery history

---

## ⚠️ Disclaimer

This project is intended for **educational, research, and demonstration purposes**.

Razorpay integration is currently configured for **Test Mode** and does not process real-money transactions.
