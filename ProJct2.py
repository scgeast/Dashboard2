# Dashboard2
# Dashboard2 - versi Futuristik
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
    df.columns = df.columns.str.strip()

    # Konversi tipe data
    if "Tanggal Pengiriman" in df.columns:
        df["Tanggal Pengiriman"] = pd.to_datetime(df["Tanggal Pengiriman"], errors="coerce")
    if "Jumlah Penjualan" in df.columns:
        df["Jumlah Penjualan"] = pd.to_numeric(df["Jumlah Penjualan"], errors="coerce").fillna(0)
    if "Jumlah Pengiriman" in df.columns:
        df["Jumlah Pengiriman"] = pd.to_numeric(df["Jumlah Pengiriman"], errors="coerce").fillna(0)

    # Style Futuristik
    layout_style = dict(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="#E0E0E0"),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#333333"),
    )

    # Tampilkan kolom yang tersedia
    st.subheader("🧾 Kolom Ditemukan di File")
    st.write(df.columns.tolist())

    # Daftar kolom yang diperlukan
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

        # Rentang tanggal
        min_date = df["Tanggal Pengiriman"].min().date()
        max_date = df["Tanggal Pengiriman"].max().date()

        start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

        region = st.sidebar.multiselect("Region", options=df["Region"].dropna().unique())
        pabrik = st.sidebar.multiselect("Pabrik", options=df["Pabrik"].dropna().unique())
        salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
        end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())

        # Terapkan Filter
        if start_date and end_date:
            df = df[(df["Tanggal Pengiriman"].dt.date >= start_date) & (df["Tanggal Pengiriman"].dt.date <= end_date)]
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
        st.download_button(
            label="📥 Download data sebagai Excel",
            data=excel_data,
            file_name='report.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # ------------------ 📊 Analisa Penjualan ------------------
        st.subheader("📊 Analisa Penjualan")
        penjualan_per_tanggal = (
            df.groupby(df["Tanggal Pengiriman"].dt.date)["Jumlah Penjualan"]
            .sum()
            .reset_index()
            .rename(columns={"Tanggal Pengiriman": "Tanggal"})
        )
        fig1 = px.line(
            penjualan_per_tanggal, x="Tanggal", y="Jumlah Penjualan",
            markers=True, title="Trend Penjualan",
            color_discrete_sequence=["#00F5FF"]
        )
        fig1.update_traces(text=penjualan_per_tanggal["Jumlah Penjualan"], textposition="top center")
        fig1.update_layout(**layout_style)
        st.plotly_chart(fig1, use_container_width=True)

        # ------------------ 🔍 Drill Down per Region ------------------
        st.subheader("🔍 Drill Down per Region")
        if not df["Region"].dropna().empty:
            region_filter = st.selectbox("Pilih Region", options=df["Region"].dropna().unique())
            df_filtered = df[df["Region"] == region_filter]
            st.dataframe(df_filtered)

        # ------------------ 📍 Visualisasi Lain ------------------
        st.subheader("📍 Visualisasi Lain")

        fig2 = px.bar(
            df.groupby("Region")["Jumlah Penjualan"].sum().reset_index(),
            x="Region", y="Jumlah Penjualan",
            title="Penjualan per Region",
            color="Region", color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig2.update_traces(texttemplate="%{y}", textposition="outside")
        fig2.update_layout(**layout_style)
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.bar(
            df.groupby("Pabrik")["Jumlah Penjualan"].sum().reset_index(),
            x="Pabrik", y="Jumlah Penjualan",
            title="Penjualan per Pabrik",
            color="Pabrik", color_discrete_sequence=px.colors.sequential.Magenta
        )
        fig3.update_traces(texttemplate="%{y}", textposition="outside")
        fig3.update_layout(**layout_style)
        st.plotly_chart(fig3, use_container_width=True)

        # ------------------ 👤 Performa Sales ------------------
        st.subheader("👤 Performa Sales")
        fig4 = px.bar(
            df.groupby("Salesman")["Jumlah Penjualan"].sum().reset_index(),
            x="Salesman", y="Jumlah Penjualan",
            title="Performa Salesman",
            color="Jumlah Penjualan",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        fig4.update_traces(texttemplate="%{y}", textposition="outside")
        fig4.update_layout(**layout_style, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

        top_customer = df.groupby("End Customer")["Jumlah Penjualan"].sum().nlargest(10).reset_index()
        fig5 = px.bar(
            top_customer, x="End Customer", y="Jumlah Penjualan",
            title="Top 10 End Customer",
            color="Jumlah Penjualan",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig5.update_traces(texttemplate="%{y}", textposition="outside")
        fig5.update_layout(**layout_style, coloraxis_showscale=False)
        st.plotly_chart(fig5, use_container_width=True)

        # ------------------ 🚚 Optimasi Logistik ------------------
        st.subheader("🚚 Optimasi Logistik")
        fig6 = px.bar(
            df.groupby("Nomor Truk")["Jumlah Pengiriman"].sum().reset_index(),
            x="Nomor Truk", y="Jumlah Pengiriman",
            title="Logistik per Truk",
            color="Jumlah Pengiriman",
            color_continuous_scale=px.colors.sequential.Cividis
        )
        fig6.update_traces(texttemplate="%{y}", textposition="outside")
        fig6.update_layout(**layout_style, coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

        # ------------------ 📈 Visualisasi Tren ------------------
        st.subheader("📈 Visualisasi Tren")
        tren_pengiriman = df.groupby(df["Tanggal Pengiriman"].dt.date)["Jumlah Pengiriman"].sum().reset_index()
        fig8 = px.line(
            tren_pengiriman, x="Tanggal Pengiriman", y="Jumlah Pengiriman",
            title="Tren Pengiriman", markers=True,
            color_discrete_sequence=["#FF00FF"]
        )
        fig8.update_traces(text=tren_pengiriman["Jumlah Pengiriman"], textposition="top center")
        fig8.update_layout(**layout_style)
        st.plotly_chart(fig8, use_container_width=True)

        tren_penjualan = df.groupby(df["Tanggal Pengiriman"].dt.date)["Jumlah Penjualan"].sum().reset_index()
        fig9 = px.line(
            tren_penjualan, x="Tanggal Pengiriman", y="Jumlah Penjualan",
            title="Tren Penjualan", markers=True,
            color_discrete_sequence=["#00FF85"]
        )
        fig9.update_traces(text=tren_penjualan["Jumlah Penjualan"], textposition="top center")
        fig9.update_layout(**layout_style)
        st.plotly_chart(fig9, use_container_width=True)
