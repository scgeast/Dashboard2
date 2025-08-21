# Dashboard2
# Dashboard Analyst Delivery & Sales 🚀 Futuristic Style
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard Analyst", layout="wide")

st.title("📦 Dashboard Analyst Delivery & Sales")

# 🎨 Warna Futuristik
neon_colors = px.colors.qualitative.Prism

# Upload file Excel
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Rename kolom sesuai request
    df.rename(columns={
        "Jumlah Penjualan": "Volume",
        "Jumlah Pengiriman": "Ritase",
        "Pabrik": "Plant Name",
        "Region": "Area",
        "Nomor Truk": "Truck No"
    }, inplace=True)

    # Tampilkan kolom
    st.subheader("🧾 Kolom Ditemukan di File")
    st.write(df.columns.tolist())

    # Expected columns
    expected_columns = [
        "Tanggal Pengiriman", "Area", "Plant Name", "Salesman", "End Customer",
        "Volume", "Ritase", "Truck No", "Distance"
    ]
    missing_columns = [col for col in expected_columns if col not in df.columns]

    if missing_columns:
        st.warning(f"Kolom berikut tidak ditemukan di file Excel: {missing_columns}")
    else:
        # Sidebar Filter
        st.sidebar.header("🔎 Filter Data")

        # Filter tanggal dengan start & end date
        start_date = st.sidebar.date_input("Start Date")
        end_date = st.sidebar.date_input("End Date")

        area = st.sidebar.multiselect("Area", options=df["Area"].dropna().unique())

        # Plant filter mengikuti Area
        if area:
            plant_options = df[df["Area"].isin(area)]["Plant Name"].dropna().unique()
        else:
            plant_options = df["Plant Name"].dropna().unique()
        plant_name = st.sidebar.multiselect("Plant Name", options=plant_options)

        salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
        end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())

        # Tombol reset filter
        if st.sidebar.button("🔄 Reset Filter"):
            start_date, end_date, area, plant_name, salesman, end_customer = None, None, [], [], [], []

        # Apply filter
        if start_date and end_date:
            df = df[(df["Tanggal Pengiriman"] >= pd.to_datetime(start_date)) &
                    (df["Tanggal Pengiriman"] <= pd.to_datetime(end_date))]
        if area:
            df = df[df["Area"].isin(area)]
        if plant_name:
            df = df[df["Plant Name"].isin(plant_name)]
        if salesman:
            df = df[df["Salesman"].isin(salesman)]
        if end_customer:
            df = df[df["End Customer"].isin(end_customer)]

        # Download data
        def to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Report")
            return output.getvalue()

        excel_data = to_excel(df)
        st.download_button(label="📥 Download data sebagai Excel",
                           data=excel_data,
                           file_name="report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 📊 Analisa Volume
        st.subheader("📊 Analisa Volume")
        penjualan_per_tanggal = df.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
        fig1 = px.line(penjualan_per_tanggal, x="Tanggal Pengiriman", y="Volume",
                       title="Trend Volume")
        fig1.update_traces(mode="lines+markers")
        fig1.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                           font=dict(color="white"))
        st.plotly_chart(fig1, use_container_width=True)

        # 🔍 Drill Down Area
        st.subheader("🔍 Drill Down per Area")
        area_filter = st.selectbox("Pilih Area", options=df["Area"].unique())
        df_filtered = df[df["Area"] == area_filter]
        st.dataframe(df_filtered)

        # 📍 Visualisasi per Area & Plant
        st.subheader("📍 Visualisasi Lain")

        fig2 = px.bar(df.groupby("Area")["Volume"].sum().reset_index(),
                      x="Area", y="Volume", title="Volume per Area",
                      color="Area", color_discrete_sequence=neon_colors)
        fig2.update_traces(texttemplate='%{y}', textposition="outside")
        fig2.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                           paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.bar(df.groupby("Plant Name")["Volume"].sum().reset_index(),
                      x="Plant Name", y="Volume", title="Volume per Plant",
                      color="Plant Name", color_discrete_sequence=neon_colors)
        fig3.update_traces(texttemplate='%{y}', textposition="outside")
        fig3.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                           paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig3, use_container_width=True)

        # 👤 Performa Sales & Customer
        st.subheader("👤 Performa Sales")

        fig4 = px.bar(df.groupby("Salesman")["Volume"].sum().reset_index(),
                      x="Salesman", y="Volume", title="Performa Salesman",
                      color="Salesman", color_discrete_sequence=neon_colors)
        fig4.update_traces(texttemplate='%{y}', textposition="outside")
        fig4.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                           paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.bar(df.groupby("End Customer")["Volume"].sum().reset_index(),
                      x="End Customer", y="Volume", title="Performa End Customer",
                      color="End Customer", color_discrete_sequence=neon_colors)
        fig5.update_traces(texttemplate='%{y}', textposition="outside")
        fig5.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                           paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig5, use_container_width=True)

        # 🚚 Ritase per Truck (Total & Average)
        st.subheader("🚚 Ritase per Truck")

        fig6_sum = px.bar(df.groupby("Truck No")["Ritase"].sum().reset_index(),
                          x="Truck No", y="Ritase", title="Total Ritase per Truck",
                          color="Truck No", color_discrete_sequence=neon_colors)
        fig6_sum.update_traces(texttemplate='%{y}', textposition="outside")
        fig6_sum.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                               paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig6_sum, use_container_width=True)

        fig6_avg = px.bar(df.groupby("Truck No")["Ritase"].mean().reset_index(),
                          x="Truck No", y="Ritase", title="Average Ritase per Truck",
                          color="Truck No", color_discrete_sequence=neon_colors)
        fig6_avg.update_traces(texttemplate='%{y:.2f}', textposition="outside")
        fig6_avg.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                               paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig6_avg, use_container_width=True)

        # 📏 Analisa Distance
        st.subheader("📏 Analisa Distance")

        avg_distance_plant = df.groupby("Plant Name")["Distance"].mean().reset_index()
        fig7 = px.bar(avg_distance_plant, x="Plant Name", y="Distance",
                      title="Average Distance per Plant",
                      color="Plant Name", color_discrete_sequence=neon_colors)
        fig7.update_traces(texttemplate='%{y:.2f}', textposition="outside")
        fig7.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                           paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig7, use_container_width=True)

        avg_distance_area = df.groupby("Area")["Distance"].mean().reset_index()
        fig8 = px.bar(avg_distance_area, x="Area", y="Distance",
                      title="Average Distance per Area",
                      color="Area", color_discrete_sequence=neon_colors)
        fig8.update_traces(texttemplate='%{y:.2f}', textposition="outside")
        fig8.update_layout(showlegend=False, plot_bgcolor="#0E1117",
                           paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig8, use_container_width=True)

        # 📈 Tren Volume & Ritase
        st.subheader("📈 Visualisasi Tren")

        fig9 = px.line(df.groupby("Tanggal Pengiriman")["Ritase"].sum().reset_index(),
                       x="Tanggal Pengiriman", y="Ritase", title="Trend Ritase")
        fig9.update_traces(mode="lines+markers")
        fig9.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                           font=dict(color="white"))
        st.plotly_chart(fig9, use_container_width=True)

        fig10 = px.line(df.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index(),
                        x="Tanggal Pengiriman", y="Volume", title="Trend Volume")
        fig10.update_traces(mode="lines+markers")
        fig10.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                            font=dict(color="white"))
        st.plotly_chart(fig10, use_container_width=True)
