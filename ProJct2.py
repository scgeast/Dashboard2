# Dashboard2
import streamlit as st
import plotly.express as px
import pandas as pd
import io
import pdfkit

# --- Simulasi Data (ganti dengan data asli kamu) ---
data = {
    "Truck No": ["T01", "T02", "T03", "T04"],
    "Ritase": [10, 15, 12, 18],
    "Distance": [25.5, 30.2, 28.0, 35.1],
    "Plant Name": ["Plant A", "Plant B", "Plant A", "Plant C"],
    "Area": ["North", "South", "North", "East"]
}
df = pd.DataFrame(data)

# --- Sidebar Filter ---
st.sidebar.header("🔍 Filter Data")
selected_area = st.sidebar.multiselect("Pilih Area", df["Area"].unique(), default=df["Area"].unique())
selected_plant = st.sidebar.multiselect("Pilih Plant", df["Plant Name"].unique(), default=df["Plant Name"].unique())

filtered_df = df[(df["Area"].isin(selected_area)) & (df["Plant Name"].isin(selected_plant))]

# --- Average Ritase per Truck ---
ritase_per_truck = filtered_df.groupby("Truck No", as_index=False)["Ritase"].mean()
ritase_per_truck.rename(columns={"Ritase": "Average_Ritase"}, inplace=True)

st.markdown("## 🚚 Average Ritase per Truck")
fig_avg = px.bar(
    ritase_per_truck,
    x="Truck No",
    y="Average_Ritase",
    text="Average_Ritase",
    title="Average Ritase per Truck"
)
fig_avg.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig_avg.update_layout(
    xaxis=dict(tickangle=45),
    yaxis_title="Average Ritase",
    plot_bgcolor="#0d0f15",
    paper_bgcolor="#0d0f15",
    font=dict(color="white"),
    margin=dict(l=50, r=50, t=80, b=200)
)
st.plotly_chart(fig_avg, use_container_width=True)

# --- Average Distance ---
avg_dist_plant = filtered_df.groupby("Plant Name", as_index=False)["Distance"].mean()
avg_dist_area = filtered_df.groupby("Area", as_index=False)["Distance"].mean()

st.markdown("## 📏 Average Distance")
col1, col2 = st.columns(2)

with col1:
    fig_dist1 = px.bar(
        avg_dist_plant,
        x="Plant Name",
        y="Distance",
        text="Distance",
        title="Avg Distance per Plant"
    )
    fig_dist1.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_dist1.update_layout(
        xaxis=dict(tickangle=45),
        yaxis_title="Distance",
        plot_bgcolor="#0d0f15",
        paper_bgcolor="#0d0f15",
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=80, b=200)
    )
    st.plotly_chart(fig_dist1, use_container_width=True)

with col2:
    fig_dist2 = px.bar(
        avg_dist_area,
        x="Area",
        y="Distance",
        text="Distance",
        title="Avg Distance per Area"
    )
    fig_dist2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_dist2.update_layout(
        xaxis=dict(tickangle=45),
        yaxis_title="Distance",
        plot_bgcolor="#0d0f15",
        paper_bgcolor="#0d0f15",
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=80, b=200)
    )
    st.plotly_chart(fig_dist2, use_container_width=True)

# --- Export Section ---
st.markdown("## 📤 Export Data")

# Export to Excel
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Filtered Data')
    writer.save()

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer.getvalue(),
    file_name="filtered_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

