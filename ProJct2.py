# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(page_title="📦 Dashboard Analyst Delivery & Sales", layout="wide")

# Warna futuristik
color_palette = ["#00FFFF", "#8A2BE2", "#00FF00", "#FF00FF", "#FFD700", "#00CED1"]

# Sidebar Tema
st.sidebar.header("🎨 Pengaturan Tampilan")
theme = st.sidebar.radio("Pilih Tema", ["Gelap", "Terang"])

# Warna latar dan font
if theme == "Gelap":
    bg_color = "#0d0f15"
    font_color = "white"
else:
    bg_color = "white"
    font_color = "black"

st.markdown(f"<h1 style='color:{font_color}'>📦 Dashboard Analyst Delivery dan Sales</h1>", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    expected_columns = [
        "Tanggal Pengiriman", "Area", "Plant Name", "Salesman", "End Customer",
        "Volume", "Ritase", "Truck No", "Distance"
    ]
    missing_columns = [col for col in expected_columns if col not in df.columns]

    if missing_columns:
        st.warning(f"Kolom berikut tidak ditemukan di file Excel: {missing_columns}")
    else:
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

        # Ekspor Excel
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
        def styled_chart(fig, height=500):
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

        # 📊 Analisa Volume Penjualan
        st.subheader("📊 Analisa Volume Penjualan")
        sales_trend = df_filtered.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
        sales_trend["Volume"] = sales_trend["Volume"].round(2)
        fig_sales_trend = px.line(sales_trend, x="Tanggal Pengiriman", y="Volume", text="Volume",
                                  title="Tren Volume Penjualan")
        fig_sales_trend.update_traces(mode="lines+markers+text", textposition="top center")
        fig_sales_trend.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=font_color),
            legend=dict(orientation="h", y=-0.2),
            height=400
        )
        st.plotly_chart(fig_sales_trend, use_container_width=True)

        # 📍 Volume per Area & Plant
        col1, col2 = st.columns(2)
        with col1:
            volume_area = df_filtered.groupby("Area")["Volume"].sum().reset_index()
            volume_area["Volume"] = volume_area["Volume"].round(2)
            volume_area = volume_area.sort_values(by="Volume", ascending=False)
            fig_area = px.bar(volume_area, x="Area", y="Volume", text="Volume", color="Area",
                              title="Volume per Area", color_discrete_sequence=color_palette)
            st.plotly_chart(styled_chart(fig_area, height=500), use_container_width=True)

        with col2:
            volume_plant = df_filtered.groupby("Plant Name")["Volume"].sum().reset_index()
            volume_plant["Volume"] = volume_plant["Volume"].round(2)
            volume_plant = volume_plant.sort_values(by="Volume", ascending=False)
            fig_plant = px.bar(volume_plant, x="Plant Name", y="Volume", text="Volume", color="Plant Name",
                               title="Volume per Plant", color_discrete_sequence=color_palette)
            st.plotly_chart(styled_chart(fig_plant, height=500), use_container_width=True)

        # 👤 Performa Sales & Customer
        st.subheader("👤 Performa Sales & Customer")
        sales_perf = df_filtered.groupby("Salesman")["Volume"].sum().reset_index()
        sales_perf["Volume"] = sales_perf["Volume"].round(2)
        sales_perf = sales_perf.sort_values(by="Volume", ascending=False)
        fig_salesman = px.bar(sales_perf, x="Salesman", y="Volume", text="Volume", color="Salesman",
                              title="Performa Salesman", color_discrete_sequence=color_palette)
        st.plotly_chart(styled_chart(fig_salesman, height=600), use_container_width=True)

        cust_perf = df_filtered.groupby("End Customer")["Volume"].sum().reset_index()
        cust_perf["Volume"] = cust_perf["Volume"].round(2)
        cust_perf = cust_perf.sort_values(by="Volume", ascending=False)
        fig_customer = px.bar(cust_perf, x="End Customer", y="Volume", text="Volume", color="End Customer",
                              title="Performa End Customer", color_discrete_sequence=color_palette)
        st.plotly_chart(styled_chart(fig_customer, height=600), use_container_width=True)

        # 🚚 Optimasi Logistik
        st.subheader("🚚 Optimasi Logistik")
        col3, col4 = st.columns(2)
        with col3:
            ritase_truck = df_filtered.groupby("Truck No")["Ritase"].sum().reset_index()
            ritase_truck["Ritase"] = ritase_truck["Ritase"].round(2)
            ritase_truck = ritase_truck.sort_values(by="Ritase", ascending=False)
            fig_truck_total = px.bar(ritase_truck, x="Truck No", y="Ritase", text="Ritase", color="Truck No",
                                     title="Total Ritase per Truck", color_discrete_sequence=color_palette)
            st.plotly_chart(styled_chart(fig_truck_total, height=500), use_container_width=True)

        with col4:
            avg_vol_truck = df_filtered.groupby("Truck No")["Volume"].mean().reset_index()
            avg_vol_truck["Volume"] = avg_vol_truck["Volume"].round(2)
            avg_vol_truck = avg_vol_truck.sort_values(by="Volume", ascending=False)
            fig_truck_avg = px.bar(avg_vol_truck, x="Truck No", y="Volume", text="Volume", color="Truck No",
                                   title="Average Volume per Ritase (Truck)", color_discrete_sequence=color_palette)
            st.plotly_chart(styled_chart(fig_truck_avg, height=500), use_container_width=True)

        # 📈 Visualisasi Tren
        st.subheader("📈 Visualisasi Tren")
        trend_ritase = df_filtered.groupby("Tanggal Pengiriman")["Ritase"]
