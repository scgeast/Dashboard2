# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.title("📦 Dashboard Analyst Delivery dan Sales")

# Upload file
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])

if uploaded_file:
    # Baca data dan bersihkan nama kolom
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # Hapus spasi depan/belakang

    # Tampilkan kolom yang tersedia
    st.subheader("🧾 Kolom Ditemukan di File")
    st.write(df.columns.tolist())

    # Daftar kolom yang diperlukan (tanpa 'Jadwal Kirim')
    expected_columns = [
        "Tanggal Pengiriman", "Region", "Pabrik", "Salesman", "End Customer",
        "Jumlah Penjualan", "Jumlah Pengiriman", "Nomor Truk"
    ]
    missing_columns = [col for col in expected_columns if col not in df.columns]

    if missing_columns:
        st.warning(f"Kolom berikut tidak ditemukan di file Excel: {missing_columns}")
    else:
        # Sidebar Filter
        st.sidebar.header("🔎 Filter Data")

        tanggal_pengiriman = st.sidebar.date_input("Tanggal Pengiriman")
        region = st.sidebar.multiselect("Region", options=df["Region"].dropna().unique())
        pabrik = st.sidebar.multiselect("Pabrik", options=df["Pabrik"].dropna().unique())
        salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
        end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())

        # Terapkan Filter
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

        # Fungsi ekspor ke Excel
        def to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Report')
            return output.getvalue()

        excel_data = to_excel(df)
        st.download_button(label="📥 Download data sebagai Excel", data=excel_data, file_name='report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Analisa Penjualan
        st.subheader("📊 Analisa Penjualan")
        penjualan_per_tanggal = df.groupby("Tanggal Pengiriman")["Jumlah Penjualan"].sum().reset_index()
        fig1 = px.line(penjualan_per_tanggal, x="Tanggal Pengiriman", y="Jumlah Penjualan")
        st.plotly_chart(fig1, use_container_width=True)

        # Drill Down Region
        st.subheader("🔍 Drill Down per Region")
        region_filter = st.selectbox("Pilih Region", options=df["Region"].unique())
        df_filtered = df[df["Region"] == region_filter]
        st.dataframe(df_filtered)

        # Visualisasi
        st.subheader("📍 Visualisasi Lain")

        fig2 = px.bar(df.groupby("Region")["Jumlah Penjualan"].sum().reset_index(), x="Region", y="Jumlah Penjualan", title="Penjualan per Region")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.bar(df.groupby("Pabrik")["Jumlah Penjualan"].sum().reset_index(), x="Pabrik", y="Jumlah Penjualan", title="Penjualan per Pabrik")
        st.plotly_chart(fig3, use_container_width=True)

        # Tracking Sales
        st.subheader("👤 Performa Sales")

        fig4 = px.bar(df.groupby("Salesman")["Jumlah Penjualan"].sum().reset_index(), x="Salesman", y="Jumlah Penjualan", title="Performa Salesman")
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.bar(df.groupby("End Customer")["Jumlah Penjualan"].sum().reset_index(), x="End Customer", y="Jumlah Penjualan", title="Performa End Customer")
        st.plotly_chart(fig5, use_container_width=True)

        # Logistik
        st.subheader("🚚 Optimasi Logistik")

        fig6 = px.bar(df.groupby("Nomor Truk")["Jumlah Pengiriman"].sum().reset_index(), x="Nomor Truk", y="Jumlah Pengiriman", title="Logistik per Truk")
        st.plotly_chart(fig6, use_container_width=True)

        # Tren
        st.subheader("📈 Visualisasi Tren")

        fig8 = px.line(df.groupby("Tanggal Pengiriman")["Jumlah Pengiriman"].sum().reset_index(), x="Tanggal Pengiriman", y="Jumlah Pengiriman", title="Tren Pengiriman")
        st.plotly_chart(fig8, use_container_width=True)

        fig9 = px.line(df.groupby("Tanggal Pengiriman")["Jumlah Penjualan"].sum().reset_index(), x="Tanggal Pengiriman", y="Jumlah Penjualan", title="Tren Penjualan")
        st.plotly_chart(fig9, use_container_width=True)
