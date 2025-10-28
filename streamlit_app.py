import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Audit Pack Collector", layout="wide")

st.title("📦 Audit Pack Collector (Demo)")

# --- Dummy Audit Checklist ---
if "audit_items" not in st.session_state:
    st.session_state.audit_items = pd.DataFrame({
        "Department": ["HR", "Finance", "IT", "Operations"],
        "Document": ["Training Records", "Payroll Compliance", "System Access Logs", "Safety Certificates"],
        "Status": ["Pending", "Pending", "Pending", "Pending"],
        "Last Updated": ["", "", "", ""],
    })

# Display dashboard
st.subheader("📋 Audit Checklist Progress")

progress = (st.session_state.audit_items["Status"].eq("Completed").sum() /
            len(st.session_state.audit_items)) * 100
st.progress(progress / 100)
st.caption(f"✅ {progress:.0f}% of audit items completed")

st.dataframe(st.session_state.audit_items, use_container_width=True)

# --- Upload Section ---
st.subheader("📁 Upload Audit Evidence")

dept = st.selectbox("Select Department", st.session_state.audit_items["Department"])
doc_type = st.selectbox("Select Document Type", st.session_state.audit_items.query("Department == @dept")["Document"])
uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx", "jpg", "png"])

if uploaded_file:
    st.success(f"✅ File '{uploaded_file.name}' uploaded for {dept} - {doc_type}")
    idx = st.session_state.audit_items.query("Department == @dept and Document == @doc_type").index[0]
    st.session_state.audit_items.loc[idx, "Status"] = "Completed"
    st.session_state.audit_items.loc[idx, "Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

# --- Summary Section ---
st.divider()
st.subheader("📊 Summary Insights")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Departments", st.session_state.audit_items["Department"].nunique())
with col2:
    st.metric("Total Items", len(st.session_state.audit_items))
with col3:
    st.metric("Completed", st.session_state.audit_items["Status"].eq("Completed").sum())

st.caption("💡 Tip: This is a demo. In a real app, files would be stored in Supabase Storage and audit data in Supabase Database.")
