"""Streamlit dashboard for fraud detection monitoring."""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.markdown("""
<style>
    .main-header { font-size: 3rem; font-weight: bold; color: #1f77b4; }
</style>
""", unsafe_allow_html=True)

def get_metrics():
    try:
        response = requests.get(f"{API_URL}/metrics", timeout=5)
        return response.json()
    except:
        return {"total_predictions": 0, "fraud_detected": 0, "fraud_rate": 0}

def predict_transaction(data):
    try:
        response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

st.sidebar.title("🛡️ Fraud Detection")
page = st.sidebar.radio("Navigation", [
    "Dashboard", "Transaction Prediction", "Batch Analysis",
    "Real-time Monitor", "System Health"
])

if page == "Dashboard":
    st.markdown('<p class="main-header">Fraud Detection Dashboard</p>', unsafe_allow_html=True)
    metrics = get_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Predictions", metrics.get("total_predictions", 0))
    with col2:
        st.metric("Fraud Detected", metrics.get("fraud_detected", 0))
    with col3:
        st.metric("Fraud Rate", f"{metrics.get('fraud_rate', 0)}%")
    with col4:
        st.metric("Model Version", "v1.0.0")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Fraud Distribution")
        fraud_data = pd.DataFrame({
            'Category': ['Legitimate', 'Fraudulent'],
            'Count': [
                metrics.get("total_predictions", 0) - metrics.get("fraud_detected", 0),
                metrics.get("fraud_detected", 0)
            ]
        })
        fig = px.pie(fraud_data, values='Count', names='Category',
                     color='Category', color_discrete_map={'Legitimate': '#4caf50', 'Fraudulent': '#f44336'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Risk Level Distribution")
        risk_data = pd.DataFrame({
            'Risk Level': ['Low', 'Medium', 'High', 'Critical'],
            'Count': [45, 30, 15, 10]
        })
        fig = px.bar(risk_data, x='Risk Level', y='Count',
                     color='Risk Level', color_discrete_map={
                         'Low': '#4caf50', 'Medium': '#ff9800',
                         'High': '#f44336', 'Critical': '#9c27b0'
                     })
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Transactions")
    sample_data = pd.DataFrame({
        'Transaction ID': ['txn_001', 'txn_002', 'txn_003', 'txn_004', 'txn_005'],
        'Amount': [150.00, 2500.00, 75.50, 1200.00, 45.00],
        'Type': ['purchase', 'transfer', 'purchase', 'withdrawal', 'purchase'],
        'Risk Level': ['Low', 'Critical', 'Low', 'High', 'Low'],
        'Status': ['Approved', 'Blocked', 'Approved', 'Review', 'Approved']
    })
    st.dataframe(sample_data, use_container_width=True)

elif page == "Transaction Prediction":
    st.markdown('<p class="main-header">Transaction Prediction</p>', unsafe_allow_html=True)
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        with col1:
            txn_id = st.text_input("Transaction ID", value=f"txn_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            user_id = st.text_input("User ID", value="user_123")
            amount = st.number_input("Amount ($)", min_value=0.01, value=150.00, step=10.0)
            txn_type = st.selectbox("Transaction Type", ["purchase", "transfer", "withdrawal", "deposit"])
        with col2:
            merchant_id = st.text_input("Merchant ID", value="merch_456")
            card_present = st.checkbox("Card Present", value=True)
            lat = st.number_input("Latitude", value=40.7128, format="%.4f")
            lon = st.number_input("Longitude", value=-74.0060, format="%.4f")
            device_id = st.text_input("Device ID", value="device_abc")

        submitted = st.form_submit_button("Analyze Transaction", type="primary")

    if submitted:
        with st.spinner("Analyzing transaction..."):
            data = {
                "transaction_id": txn_id,
                "user_id": user_id,
                "amount": amount,
                "transaction_type": txn_type,
                "merchant_id": merchant_id,
                "card_present": card_present,
                "latitude": lat,
                "longitude": lon,
                "device_id": device_id
            }
            result = predict_transaction(data)
            if result:
                is_fraud = result.get("is_fraud", False)
                prob = result.get("fraud_probability", 0)
                risk = result.get("risk_level", "unknown")

                if is_fraud:
                    st.error(f"FRAUD DETECTED - Risk: {risk.upper()} - Probability: {prob:.2%}")
                else:
                    st.success(f"TRANSACTION APPROVED - Risk: {risk.upper()} - Probability: {prob:.2%}")

                explanation = result.get("explanation", {})
                if explanation.get("top_risk_factors"):
                    st.subheader("Risk Factors")
                    for factor in explanation["top_risk_factors"]:
                        st.write(f"- {factor}")

                with st.expander("Raw Response"):
                    st.json(result)

elif page == "Batch Analysis":
    st.markdown('<p class="main-header">Batch Transaction Analysis</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} transactions")
        st.dataframe(df.head())

elif page == "Real-time Monitor":
    st.markdown('<p class="main-header">Real-time Monitor</p>', unsafe_allow_html=True)
    if st.button("Start Monitoring"):
        chart_placeholder = st.empty()
        data_points = []
        for i in range(30):
            new_point = {
                'time': datetime.now(),
                'amount': 100 + i * 10,
                'fraud_probability': min(0.1 + i * 0.02, 0.95),
                'is_fraud': i > 20
            }
            data_points.append(new_point)
            df = pd.DataFrame(data_points)
            with chart_placeholder.container():
                fig = px.scatter(df, x='time', y='fraud_probability',
                                color='is_fraud', size='amount',
                                color_discrete_map={True: '#f44336', False: '#4caf50'},
                                title="Real-time Fraud Probability")
                st.plotly_chart(fig, use_container_width=True)
            time.sleep(0.3)

elif page == "System Health":
    st.markdown('<p class="main-header">System Health</p>', unsafe_allow_html=True)
    try:
        health = requests.get(f"{API_URL}/health", timeout=5).json()
        if health.get("status") == "healthy":
            st.success("API is healthy")
        else:
            st.error("API is unhealthy")
        st.write(f"Version: {health.get('version')}")
        st.write(f"Timestamp: {health.get('timestamp')}")
    except Exception as e:
        st.error(f"Cannot connect to API: {e}")
