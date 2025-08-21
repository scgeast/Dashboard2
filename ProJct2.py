# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(page_title="📦 Dashboard Analyst Delivery & Sales", layout="wide")

# Tema & Warna
st.sidebar.header("🎨 Pengaturan Tampilan")
theme = st.sidebar.radio("Pilih Tema", ["Gelap", "Terang"])
bg_color = "#0d0f15" if theme == "Gelap" else "white"
font_color = "white" if theme == "Gelap" else "black"
color_palette = ["#00FFFF", "#8A2BE2", "#00FF00", "#FF00FF", "#FFD700", "#00CED1"]
default_chart_args = dict(color_discrete_sequence=color_palette)
default_height = 500

# Judul
st.markdown(f"<h1 style='color:{font_color}'>📦 Dashboard Analyst Delivery dan Sales</h1>", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])
if not uploaded_file:
    st.stop()

df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip()

expected_columns = [
    "Tanggal Pengiriman", "Area", "Plant Name", "Salesman", "End Customer"
    "Volume", "Ritase", "Truck No", "Distance"
]
if not set(expected_columns).issubset(df.columns):
    st.warning("File tidak sesuai format. Harap gunakan template yang benar.")
    st.stop()

df["Tanggal Pengiriman"] = pd.to_datetime(df["Tanggal Pengiriman"])

# Sidebar Filter
st.sidebar.header("🔎 Filter Data")
start_date = st.sidebar.date_input("Start Date", df["Tanggal Pengiriman"].min())
end_date = st.sidebar.date_input("End Date", df["Tanggal Pengiriman"].max())
area = st.sidebar.multiselect("Area", options=df["Area"].dropna().unique())
plant_options = df[df["Area"].isin(area)]["Plant Name"].dropna().unique() if area else df["Plant Name"].dropna().unique()
plant = st.sidebar.multiselect("Plant Name", options=plant_options)
salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())

# Tombol Reset
if st.sidebar.button("🔄 Reset Filter"):
    st.experimental_rerun()

# Filter Data
df_filtered = df.copy()
df_filtered = df_filtered[
    (df_filtered["Tanggal Pengiriman"] >= pd.to_datetime(start_date)) &
    (df_filtered["Tanggal Pengiriman"] <= pd.to_datetime(end_date))
]
if area:
    df_filtered = df_filtered[df_filtered["Area"].isin(area)]
if plant:
    df_filtered = df_filtered[df_filtered["Plant Name"].isin(plant)]
if salesman:
    df_filtered = df_filtered[df_filtered["Salesman"].isin(salesman)]
if end_customer:
    df_filtered = df_filtered[df_filtered["End Customer"].isin(end_customer)]

# Export Excel
def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Report")
    output.seek(0)
    return output.getvalue()

excel_data = to_excel(df_filtered)
st.download_button("📥 Download data sebagai Excel", excel_data, "report.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Fungsi bantu chart
def styled_chart(fig, height=default_height):
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=font_color),
        title_font=dict(size=18),
        xaxis=dict(tickangle=45),
        showlegend=False,
        height=height
    )
    return fig

def create_chart(df, x, y, title, chart_type="bar", height=default_height):
    if chart_type == "bar":
        fig = px.bar(df, x=x, y=y, text=y, title=title, **default_chart_args)
    else:
        fig = px.line(df, x=x, y=y, text=y, title=title)
        fig.update_traces(mode="lines+markers+text", textposition="top center")
    return styled_chart(fig, height=height)

# 📊 Ringkasan Dashboard
st.markdown(f"<h2 style='color:{font_color}'>📊 Ringkasan Data</h2>", unsafe_allow_html=True)
summary_style = f"""
<style>
.card {{
    background-color: {bg_color};
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444;
    text-align: center;
    color: {font_color};
    font-size: 20px;
    box-shadow: 0 0 10px rgba(0,255,255,0.2);
}}
.card-title {{
    font-size: 14px;
    margin-bottom: 5px;
    color: {font_color};
}}
</style>
"""
st.markdown(summary_style, unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown(f"<div class='card'><div class='card-title'>Total Area</div>{df_filtered['Area'].nunique()}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card'><div class='card-title'>Total Plant</div>{df_filtered['Plant Name'].nunique()}</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='card'><div class='card-title'>Total Volume</div>{df_filtered['Volume'].sum():,.2f}</div>", unsafe_allow_html=True)
with col4:
    ritase_total = df_filtered['Ritase'].sum()
    st.markdown(f"<div class='card'><div class='card-title'>Total Ritase</div>{ritase_total:,.2f}</div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='card'><div class='card-title'>Total Truck</div>{df_filtered['Truck No'].nunique()}</div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div class='card'><div class='card-title'>Total End Customer</div>{df_filtered['End Customer'].nunique()}</div>", unsafe_allow_html=True)

# 📊 Volume PerDay
st.markdown(f"<h2 style='color:{font_color}'>📊 Volume PerDay</h2>", unsafe_allow_html=True)
chart_type = st.radio("Pilih Jenis Grafik", ["Line", "Bar"], horizontal=True)
sales_trend = df_filtered.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
sales_trend["Volume"] = sales_trend["Volume"].round(2)
st.plotly_chart(create_chart(sales_trend, "Tanggal Pengiriman", "Volume", "Tren Volume PerDay", chart_type), use_container_width=True)

# 📍 Volume per Area & Plant
colA, colB = st.columns(2)
with colA:
    area_df = df_filtered.groupby("Area")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
    area_df["Volume"] = area_df["Volume"].round(2)
    st.plotly_chart(create_chart(area_df, "Area", "Volume", "Volume per Area"), use_container_width=True)
with colB:
    plant_df = df_filtered.groupby("Plant Name")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
    plant_df["Volume"] = plant_df["Volume"].round(2)
    st.plotly_chart(create_chart(plant_df, "Plant Name", "Volume", "Volume per Plant"), use_container_width=True)

# 👤 Performa Sales & Customer
st.markdown(f"<h2 style='color:{font_color}'>👤 Performa Sales & Customer</h2>", unsafe_allow_html=True)
sales_df = df_filtered.groupby("Salesman")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
sales_df["Volume"] = sales_df["Volume"].round(2)
st.plotly_chart(create_chart(sales_df, "Salesman", "Volume", "Performa Salesman", "bar", 600), use_container_width=True)

cust_df = df_filtered.groupby("End Customer")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
cust_df["Volume"] = cust_df["Volume"].round(2)
st.plotly_chart(create_chart(cust_df, "End Customer", "Volume", "Performa End Customer",
