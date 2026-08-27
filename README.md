# 💳 Payment Recovery AI

### AI-powered payment failure risk prediction and revenue recovery prototype

Payment Recovery AI is an AI/ML-based prototype designed to identify risky failed payments and simulate intelligent recovery actions to reduce potentially lost payment revenue.

The system combines **machine learning, risk classification, recovery decision logic, recovery simulation, business metrics, auditability, and stopping rules** into one end-to-end workflow.

---

## 🎯 Problem

Failed payments can result in lost revenue and frustrated customers.

Traditional payment systems may simply report that a payment failed. This project goes one step further by asking:

* How risky is this payment?
* Why might the payment fail?
* Should recovery action be attempted?
* Which recovery action should be recommended?
* Was the payment successfully recovered?
* How much payment value was recovered?
* When should the system stop retrying?

---

## 💡 Solution

Payment Recovery AI uses a trained machine learning model to predict payment failure probability.

Based on the predicted probability, payments are classified into:

* 🟢 **LOW Risk**
* 🟡 **MEDIUM Risk**
* 🔴 **HIGH Risk**

MEDIUM and HIGH risk payments can enter the recovery workflow.

The system then simulates a recovery action and calculates the resulting business impact.

---

## 🔄 End-to-End Workflow

```text
Failed Payment
      ↓
AI Failure Risk Prediction
      ↓
Failure Probability
      ↓
LOW / MEDIUM / HIGH Risk
      ↓
Possible Issue Explanation
      ↓
Recovery Action Recommendation
      ↓
Recovery Simulation
      ↓
RECOVERED / UNRECOVERED
      ↓
Recovery Metrics
      ↓
Business Impact
      ↓
Audit Log
      ↓
Stopping Rule
```

---

## 🤖 Machine Learning

The trained model uses payment transaction features including:

* Payment amount
* Payment method
* Bank
* Device
* Payment hour
* Previous payment failures
* Attempt number
* Payment error
* Customer type

The model outputs the probability that a transaction belongs to the **FAILED** class.

---

## 🧠 Risk Classification

| Failure Probability | Risk Level | Recovery Decision           |
| ------------------- | ---------- | --------------------------- |
| < 30%               | 🟢 LOW     | No recovery required        |
| 30% – <70%          | 🟡 MEDIUM  | Recovery action allowed     |
| ≥ 70%               | 🔴 HIGH    | Recovery action recommended |

---

## 🔄 Recovery Simulation

The prototype simulates recovery actions instead of processing real payments.

Examples include:

* Payment retry
* Authentication retry
* Alternative payment method
* UPI
* Net Banking

The simulation produces:

```text
RECOVERED
```

or

```text
FAILED
```

No real money is processed by this prototype.

---

## 🛑 Recovery Control

The system includes a stopping rule:

> **Maximum 2 recovery attempts per transaction.**

This prevents unlimited retry behavior and demonstrates controlled recovery rather than blindly retrying failed payments.

---

## 💰 Transaction-Level Money Protection

A key business rule is implemented:

> **One transaction amount can be recovered only once.**

Multiple recovery attempts for the same transaction must not artificially increase the recovered payment value.

This prevents double-counting of recovered revenue.

---

## 📊 Prototype Validation Results

The prototype was validated using failed transactions from the dataset.

### Validation

* Total failed payment value: **₹127,149**
* AI identified at-risk value: **₹118,383**
* At-risk value identified: **93.11%**
* Recovered payment value: **₹56,068**
* Unrecovered payment value: **₹62,315**
* Recovery rate by at-risk value: **47.36%**
* Overall failed-value recovery: **44.10%**

These values represent the prototype's validation/simulation results, not real Razorpay payment data or real financial transactions.

---

## 📋 Auditability

The system records important recovery decisions including:

* Transaction ID
* Payment amount
* Actual payment status
* AI failure probability
* Risk level
* Payment error
* Recovery action
* Recovery result
* Recovered amount
* Unrecovered amount
* Final recovery outcome

This makes the recovery process easier to inspect and explain.

---

## 🖥️ Application

The project includes a Streamlit application that allows users to:

1. Enter payment details
2. Analyze payment risk
3. View failure probability
4. View risk level
5. Understand possible payment issues
6. Receive a recovery recommendation
7. Simulate recovery
8. View recovered amount
9. View business recovery metrics
10. Review recovery history

---

## 🛠️ Technologies

* Python
* Pandas
* Scikit-learn
* Joblib
* Streamlit
* Google Colab
* Jupyter Notebook
* GitHub

---

## 📁 Project Structure

```text
payment-recovery-ai/
│
├── app.py
├── Payment_Recovery_AI_Final.ipynb
├── payment_model.pkl
├── payment_recovery_results.csv
├── payment_transactions_realistic (1).csv
│
└── proof_images/
```

---

## ▶️ How to Run

Install the required Python packages:

```bash
pip install streamlit pandas scikit-learn joblib
```

Then run:

```bash
streamlit run app.py
```

The application will open in the browser.

---

## ⚠️ Important Note

This is a **prototype and simulation system** developed for the Razorpay AI Buildathon.

The recovery process does not process real payments and does not connect to a live payment gateway.

Recovery probabilities and recovery results are simulated for demonstrating the AI-driven recovery workflow.

---

## 🚀 Future Scope

Possible future improvements include:

* Integration with a real payment gateway
* Real-time payment failure detection
* More advanced recovery policies
* Customer-specific recovery strategies
* Reinforcement learning for recovery optimization
* Real-time monitoring dashboards
* Production-grade audit and compliance systems
* Integration with payment gateway webhooks

---

## 👩‍💻 Project

**Payment Recovery AI**

Built as an AI/ML prototype focused on **payment risk prediction and revenue recovery**.
