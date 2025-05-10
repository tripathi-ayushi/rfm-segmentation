import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# --- Path Setup ---
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / 'outputs' / 'reports' / 'final_campaign_actions.csv'
MODEL_PATH = BASE_DIR.parent / 'outputs' / 'models' / 'xgb_churn_model.joblib'

# --- Load Model ---
@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error(f"Model file not found at: {MODEL_PATH}")
        st.stop()
    return joblib.load(MODEL_PATH)

# --- Load Data ---
@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        st.error(f"Data file not found at: {DATA_PATH}")
        st.stop()
    return pd.read_csv(DATA_PATH)

# --- Streamlit Config ---
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("Customer Segmentation & Churn Dashboard")

# --- Load the dataset
rfm = load_data()

# --- Summary Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(rfm):,}")
col2.metric("At-Risk Customers", f"{rfm['churn_prediction'].sum():,}")
col3.metric("Unique Segments", rfm['Segment'].nunique())

st.markdown("---")

# --- Segment Filter ---
segments = rfm['Segment'].unique().tolist()
selected_segment = st.selectbox("Select Segment to Explore:", ["All"] + segments)

if selected_segment != "All":
    filtered = rfm[rfm['Segment'] == selected_segment]
else:
    filtered = rfm.copy()

st.subheader(f"Segment: {selected_segment} ({len(filtered)} customers)")
st.dataframe(filtered[['CustomerID', 'Segment', 'churn_prediction', 'marketing_action']])

# --- Marketing Action Breakdown ---
st.markdown("### Marketing Actions Distribution")
action_counts = filtered['marketing_action'].value_counts()
st.bar_chart(action_counts)

# --- Upload CSV for Future Prediction Integration ---
st.markdown("---")
st.markdown("### Upload New Customer RFM Data")
uploaded = st.file_uploader("Upload a CSV with Recency, Frequency, Monetary", type="csv")

if uploaded:
    new_data = pd.read_csv(uploaded)
    st.write("Preview of Uploaded Data:", new_data.head())

    # Load model
    model = load_model()

    # Check for required columns
    required_cols = {'Recency', 'Frequency', 'Monetary'}
    if required_cols.issubset(set(new_data.columns)):
        # Predict churn
        new_data['churn_prediction'] = model.predict(new_data[['Recency', 'Frequency', 'Monetary']])
        
        # Show predictions
        st.success("Churn predictions added!")
        st.dataframe(new_data[['Recency', 'Frequency', 'Monetary', 'churn_prediction']])
    else:
        st.error("Uploaded file must contain: Recency, Frequency, Monetary columns.")
