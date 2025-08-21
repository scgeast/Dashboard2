# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Judul dashboard
st.title("Dashboard Analyst Delivery dan Sales")

# Upload file Excel
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])

if uploaded_file:
    # Baca file Excel
    df = pd.read_excel(uploaded_file)

    # Sidebar Filter
    st.sidebar.header("Filter Data")
    tanggal_pengiriman = st.sidebar.date_input("Tanggal Pengiriman")
    region = st.sidebar.multiselect("Region", options=df["Region"].dropna().unique())
    pabrik = st.sidebar.multiselect("Pabrik", options=df["Pabrik"].dropna().unique())
    salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
    end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())

    # Apply Filters
    if tanggal_pengiriman:
        df = df[df["Tanggal Pengiriman"] == pd.to_datetime(tanggal_pengiriman)]
    if region:
        df = df[df["Region"].isin(region)]
    if pabrik:
        df = df[df["Pabrik"].isin(pabrik)]
    if salesman:
        df = df[df["Salesman"].isin(salesman)]
    if end_customer:
        df = df[df["End Customer"].isin(end_customer)]

    # Fungsi download ke Excel
    def to_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Report')
        processed_data = output.getvalue()
        return processed_data

    # Generate Excel file for download
    excel_data = to_excel(df)

    # Tombol Download
    st.download_button(label='📥 Download data sebagai Excel', data=excel_data, file_name='report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Analisa Penjualan
    st.subheader("📊 Analisa Penjualan")
    penjualan_per_tanggal = df.groupby("Tanggal Pengiriman")["Jumlah Penjualan"].sum().reset_index()
    fig1 = px.line(penjualan_per_tanggal, x="Tanggal Pengiriman", y="Jumlah Penjualan")
    st.plotly_chart(fig1, use_container_width=True)

    # Drill Down Berdasarkan Region
    st.subheader("🔍 Filter dan Drill Down")
    region_filter = st.selectbox("Pilih Region", options=df["Region"].dropna().unique())
    df_filtered = df[df["Region"] == region_filter]
    st.dataframe(df_filtered)

    # Visualisasi Lainnya
    st.subheader("📍 Visualisasi Lainnya")

    penjualan_per_region = df.groupby("Region")["Jumlah Penjualan"].sum().reset_index()
    fig2 = px.bar(penjualan_per_region, x="Region", y="Jumlah Penjualan", title="Penjualan per Region")
    st.plotly_chart(fig2, use_container_width=True)

    penjualan_per_pabrik = df.groupby("Pabrik")["Jumlah Penjualan"].sum().reset_index()
    fig3 = px.bar(penjualan_per_pabrik, x="Pabrik", y="Jumlah Penjualan", title="Penjualan per Pabrik")
    st.plotly_chart(fig3, use_container_width=True)

    # Tracking Performa Sales
    st.subheader("👤 Tracking Performa Sales")
    performa_sales = df.groupby("Salesman")["Jumlah Penjualan"].sum().reset_index()
    fig4 = px.bar(performa_sales, x="Salesman", y="Jumlah Penjualan", title="Performa Sales")
    st.plotly_chart(fig4, use_container_width=True)

    performa_end_customer = df.groupby("End Customer")["Jumlah Penjualan"].sum().reset_index()
    fig5 = px.bar(performa_end_customer, x="End Customer", y="Jumlah Penjualan", title="Performa End Customer")
    st.plotly_chart(fig5, use_container_width=True)

    # Optimasi Logistik
    st.subheader("🚚 Optimasi Logistik")
    logistik_per_truk = df.groupby("Nomor Truk")["Jumlah Pengiriman"].sum().reset_index()
    fig6 = px.bar(logistik_per_truk, x="Nomor Truk", y="Jumlah Pengiriman", title="Logistik per Truk")
    st.plotly_chart(fig6, use_container_width=True)

    logistik_per_jadwal = df.groupby("Jadwal Kirim")["Jumlah Pengiriman"].sum().reset_index()
    fig7 = px.bar(logistik_per_jadwal, x="Jadwal Kirim", y="Jumlah Pengiriman", title="Logistik per Jadwal")
    st.plotly_chart(fig7, use_container_width=True)

    # Visualisasi Tren
    st.subheader("📈 Visualisasi Tren")
    tren_pengiriman = df.groupby("Tanggal Pengiriman")["Jumlah Pengiriman"].sum().reset_index()
    fig8 = px.line(tren_pengiriman, x="Tanggal Pengiriman", y="Jumlah Pengiriman", title="Tren Pengiriman")
    st.plotly_chart(fig8, use_container_width=True)

    tren_penjualan = df.groupby("Tanggal Pengiriman")["Jumlah Penjualan"].sum().reset_index()
    fig9 = px.line(tren_penjualan, x="Tanggal Pengiriman", y="Jumlah Penjualan", title="Tren Penjualan")
    st.plotly_chart(fig9, use_container_width=True)
