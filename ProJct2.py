# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px

# ===================== LOAD DATA =====================
# Contoh load dari CSV, bisa diganti sesuai file abang
df = pd.read_csv("data.csv")

# Pastikan kolom sesuai
df['Tanggal Pengiriman'] = pd.to_datetime(df['Tanggal Pengiriman'])
df['Truck No'] = df['Truck No'].astype(str)

# ===================== DASHBOARD =====================
st.set_page_config(page_title="Dashboard Transportasi", layout="wide")

st.title("📊 Dashboard Transportasi")

# ===================== PERFORM VOLUME PER DAY =====================
st.markdown("## 📦 Perform Volume per Day")

volume_per_day = df.groupby("Tanggal Pengiriman", as_index=False).agg({"Volume":"sum"})

fig_volume = px.line(
    volume_per_day,
    x="Tanggal Pengiriman",
    y="Volume",
    text="Volume",
    title="Perform Volume per Day"
)

fig_volume.update_traces(
    mode="lines+markers+text",
    textposition="top center"
)

fig_volume.update_layout(
    xaxis_title="Tanggal Pengiriman",
    yaxis_title="Volume",
    plot_bgcolor="#0d0f15",
    paper_bgcolor="#0d0f15",
    font=dict(color="white")
)

st.plotly_chart(fig_volume, use_container_width=True)

# ===================== RITASE PER TRUCK =====================
st.markdown("## 🚛 Ritase per Truck")

# Total & Average Ritase
ritase_per_truck = df.groupby("Truck No", as_index=False).agg({"Ritase":["sum","mean"]})
ritase_per_truck.columns = ["Truck No", "Total Ritase", "Average Ritase"]

# --- Total Ritase ---
st.markdown("### 📍 Total Ritase per Truck")

fig_total = px.bar(
    ritase_per_truck,
    x="Truck No",
    y="Total Ritase",
    text="Total Ritase",
    title="Total Ritase per Truck"
)
fig_total.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig_total.update_layout(
    xaxis=dict(tickangle=45),
    yaxis_title="Total Ritase",
    plot_bgcolor="#0d0f15",
    paper_bgcolor="#0d0f15",
    font=dict(color="white"),
    margin=dict(l=50, r=50, t=80, b=200)
)
st.plotly_chart(fig_total, use_container_width=True)

# --- Average Ritase ---
st.markdown("### 📍 Average Ritase per Truck")

# Versi 1: tampil semua truck
fig_avg = px.bar(
    ritase_per_truck,
    x="Truck No",
    y="Average Ritase",
    text="Average Ritase",
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

# Versi 2: scroll horizontal
st.markdown("### 📍 Average Ritase per Truck (Scrollable)")

fig_avg_scroll = px.bar(
    ritase_per_truck,
    x="Truck No",
    y="Average Ritase",
    text="Average Ritase",
    title="Average Ritase per Truck (Scrollable)"
)
fig_avg_scroll.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig_avg_scroll.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=ritase_per_truck['Truck No'],
        tickangle=45,
        rangeslider=dict(visible=True)
    ),
    yaxis_title="Average Ritase",
    plot_bgcolor="#0d0f15",
    paper_bgcolor="#0d0f15",
    font=dict(color="white"),
    margin=dict(l=50, r=50, t=80, b=200)
)
st.plotly_chart(fig_avg_scroll, use_container_width=True)

# ===================== PERFORM SALES =====================
st.markdown("## 💰 Perform Sales")

sales_per_day = df.groupby("Tanggal Pengiriman", as_index=False).agg({"Sales":"sum"})

fig_sales = px.line(
    sales_per_day,
    x="Tanggal Pengiriman",
    y="Sales",
    text="Sales",
    title="Perform Sales per Day"
)
fig_sales.update_traces(mode="lines+markers+text", textposition="top center")
fig_sales.update_layout(
    xaxis_title="Tanggal Pengiriman",
    yaxis_title="Sales",
    plot_bgcolor="#0d0f15",
    paper_bgcolor="#0d0f15",
    font=dict(color="white")
)
st.plotly_chart(fig_sales, use_container_width=True)

# ===================== PERFORM CUSTOMER =====================
st.markdown("## 👥 Perform Customer")

customer_per_day = df.groupby("Tanggal Pengiriman", as_index=False).agg({"Customer":"nunique"})

fig_customer = px.line(
    customer_per_day,
    x="Tanggal Pengiriman",
    y="Customer",
    text="Customer",
    title="Perform Customer per Day"
)
fig_customer.update_traces(mode="lines+markers+text", textposition="top center")
fig_customer.update_layout(
    xaxis_title="Tanggal Pengiriman",
    yaxis_title="Jumlah Customer",
    plot_bgcolor="#0d0f15",
    paper_bgcolor="#0d0f15",
    font=dict(color="white")
)
st.plotly_chart(fig_customer, use_container_width=True)
