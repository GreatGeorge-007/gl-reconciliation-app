import streamlit as st
import requests
import pandas as pd
import datetime
from app.excel_export import export_excel_report

st.title("📊 GL Reconciliation Dashboard")

branch = st.selectbox("Select Branch", ['Lagos', 'Abuja', 'Kano', 'Port Harcourt', 'Enugu'])
start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
end_date = st.date_input("End Date", value=datetime.date.today())

if st.button("🔄 Reconcile"):
    with st.spinner("Reconciling data..."):
        response = requests.get("http://localhost:8000/reconcile", params={
            "branch": branch,
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        })
        data = response.json()

        summary_df = pd.DataFrame(data['summary'])
        st.subheader("✅ Reconciliation Summary")
        st.dataframe(summary_df)

        st.subheader("📑 Balance Sheet")
        st.dataframe(pd.DataFrame(data['balance_sheet']))

        st.subheader("🔍 Drill-down View")
        selected_gl = st.selectbox("Select GL", summary_df['gl_code'].unique())
        makeup_df = pd.DataFrame(data['makeup'])
        st.dataframe(makeup_df[makeup_df['gl_code'] == selected_gl])

        st.subheader("📥 Download Report")
        excel = export_excel_report(pd.DataFrame(data['balance_sheet']), summary_df, makeup_df)
        st.download_button("Download Excel Report", data=excel, file_name="gl_report.xlsx")
