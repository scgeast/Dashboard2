# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px

# Simulasi data
df = pd.DataFrame({
    "Area": ["EAST", "WEST", "CENTRAL"] * 16,
    "Plant Name": ["PLANT A", "PLANT B", "PLANT C"] * 16,
    "Salesman": ["John", "Jane", "Doe"] * 16,
    "End Customer": ["Cust A", "Cust B", "Cust C"] * 16,
    "Tanggal": pd.date_range("2025-08-01", periods=48, freq="D"),
    "Volume": [600 + i*5 % 300 for i in range(48)],
    "Truck No": [f"A10{i%20+27}" for i in range(48)],
    "Total Ritase": [50 - i % 20 for i in range(48)],
    "Avg Volume per Ritase": [6 - (i % 20) * 0.1 for i in range(48)]
})

# Warna font sesuai tema
font_color = "white" if st.get_option("theme.base") == "dark" else "black"

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
area = st.sidebar.selectbox("Area", options=["All"] + sorted(df["Area"].unique().tolist()))
plant = st.sidebar.selectbox("Plant Name", options=["All"] + sorted(df["Plant Name"].unique().tolist()))
salesman = st.sidebar.selectbox("Salesman", options=["All"] + sorted(df["Salesman"].unique().tolist()))
customer = st.sidebar.selectbox("End Customer", options=["All"] + sorted(df["End Customer"].unique().tolist()))

# Filter Data
filtered_df = df.copy()
if area != "All":
    filtered_df = filtered_df[filtered_df["Area"] == area]
if plant != "All":
    filtered_df = filtered_df[filtered_df["Plant Name"] == plant]
if salesman != "All":
    filtered_df = filtered_df[filtered_df["Salesman"] == salesman]
if customer != "All":
    filtered_df = filtered_df[filtered_df["End Customer"] == customer]

# Export Excel
st.download_button("📥 Download data sebagai Excel", data=filtered_df.to_csv(index=False).encode("utf-8"),
                   file_name="data_filtered.csv", mime="text/csv")

# Volume PerDay
st.markdown(f"<h2 style='color:{font_color}'>📊 Volume PerDay</h2>", unsafe_allow_html=True)
volume_chart = px.line(filtered_df, x="Tanggal", y="Volume", markers=True)
volume_chart.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Volume",
    font=dict(color=font_color),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(volume_chart, use_container_width=True)

# Utilisasi Truck Mixer
st.markdown(f"<h2 style='color:{font_color}'>🚚 Utilisasi Truck Mixer</h2>", unsafe_allow_html=True)

# Total Ritase per Truck
st.markdown(f"<h4 style='color:{font_color}'>Total Ritase per Truck</h4>", unsafe_allow_html=True)
ritase_df = filtered_df.groupby("Truck No")["Total Ritase"].mean().reset_index()
ritase_chart = px.bar(ritase_df, x="Truck No", y="Total Ritase")
ritase_chart.update_layout(
    xaxis_title="Truck No",
    yaxis_title="Ritase",
    font=dict(color=font_color),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(ritase_chart, use_container_width=True)

# Average Volume per Ritase
st.markdown(f"<h4 style='color:{font_color}'>Average Volume per Ritase (Truck)</h4>", unsafe_allow_html=True)
avg_df = filtered_df.groupby("Truck No")["Avg Volume per Ritase"].mean().reset_index()
avg_chart = px.bar(avg_df, x="Truck No", y="Avg Volume per Ritase")
avg_chart.update_layout(
    xaxis_title="Truck No",
    yaxis_title="Volume",
    font=dict(color=font_color),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(avg_chart, use_container_width=True)
