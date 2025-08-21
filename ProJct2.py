# Dashboard2
# Dashboard2 Full Version
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Konfigurasi halaman
# =========================
st.set_page_config(page_title="📦 Dashboard Analyst Delivery & Sales", layout="wide")

# =========================
# Tema Futuristik
# =========================
color_palette = ["#00FFFF", "#8A2BE2", "#00FF00", "#FF00FF", "#FFD700", "#00CED1"]

# =========================
# Sidebar Tema
# =========================
st.sidebar.header("🎨 Pengaturan Tampilan")
theme = st.sidebar.radio("Pilih Tema", ["Gelap", "Terang"])
bg_color = "#0d0f15" if theme == "Gelap" else "white"
font_color = "white" if theme == "Gelap" else "black"

st.markdown(f"<h1 style='color:{font_color}'>📦 Dashboard Analyst Delivery dan Sales</h1>", unsafe_allow_html=True)

# =========================
# Upload File
# =========================
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])

# =========================
# Fungsi Styling Chart
# =========================
def styled_chart(fig, height=None, font_size=12, margin=None, text_format=".2f", text_position="outside", show_legend=False, title_font_size=18):
    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=font_color, size=font_size),
        title_font=dict(color=font_color, size=title_font_size),
        xaxis=dict(tickangle=45),
        showlegend=show_legend
    )
    if height:
        fig.update_layout(height=height)
    if margin:
        fig.update_layout(margin=margin)
    try:
        fig.update_traces(texttemplate=f"%{{text:{text_format}}}", textposition=text_position)
    except Exception:
        pass
    return fig

# =========================
# Jika File Diupload
# =========================
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Rename kolom jika perlu
    rename_map = {
        "Tanggal P": "Tanggal Pengiriman",
        "Plant Name": "Plant Name",
        "Area": "Area",
        "Ritase": "Ritase"
    }
    df.rename(columns=rename_map, inplace=True)

    # Tambahkan kolom jika tidak ada
    for col in ["Salesman", "End Customer", "Volume", "Truck No", "Distance"]:
        if col not in df.columns:
            df[col] = 1 if col in ["Volume", "Ritase", "Distance"] else "Unknown"

    df["Tanggal Pengiriman"] = pd.to_datetime(df["Tanggal Pengiriman"])

    # =========================
    # Sidebar Filter
    # =========================
    st.sidebar.header("🔎 Filter Data")
    start_date = st.sidebar.date_input("Start Date", df["Tanggal Pengiriman"].min())
    end_date = st.sidebar.date_input("End Date", df["Tanggal Pengiriman"].max())
    area = st.sidebar.multiselect("Area", options=df["Area"].dropna().unique())
    plant_options = df[df["Area"].isin(area)]["Plant Name"].dropna().unique() if area else df["Plant Name"].dropna().unique()
    plant = st.sidebar.multiselect("Plant Name", options=plant_options)
    salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
    end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())

    if st.sidebar.button("🔄 Reset Filter"):
        st.experimental_rerun()

    # =========================
    # Filter Data
    # =========================
    df_filtered = df[
        (df["Tanggal Pengiriman"] >= pd.to_datetime(start_date)) &
        (df["Tanggal Pengiriman"] <= pd.to_datetime(end_date))
    ]
    if area:
        df_filtered = df_filtered[df_filtered["Area"].isin(area)]
    if plant:
        df_filtered = df_filtered[df_filtered["Plant Name"].isin(plant)]
    if salesman:
        df_filtered = df_filtered[df_filtered["Salesman"].isin(salesman)]
    if end_customer:
        df_filtered = df_filtered[df_filtered["End Customer"].isin(end_customer)]

    # =========================
    # Dashboard Summary
    # =========================
   st.markdown(f"<h2 style='color:{font_color}'>📊 Summarize</h2>", unsafe_allow_html=True)

colA, colB, colC, colD, colE, colF = st.columns(6)

# Fungsi kotak metric
def boxed_metric(label, value):
    st.markdown(f"""
    <div style="
        border: 2px solid {font_color};
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        background-color: {'#1f1f1f' if theme=='Gelap' else '#f5f5f5'};
    ">
        <h4 style='margin:5px;color:{font_color}'>{label}</h4>
        <p style='font-size:20px;margin:0;color:{font_color}'>{value}</p>
    </div>
    """, unsafe_allow_html=True)

boxed_metric("Total Area", f"{df_filtered['Area'].nunique()}")
boxed_metric("Total Plant", f"{df_filtered['Plant Name'].nunique()}")
boxed_metric("Total Volume", f"{df_filtered['Volume'].sum():,.2f}")
boxed_metric("Total Ritase", f"{df_filtered['Ritase'].sum():,.2f}")
boxed_metric("Total End Customer", f"{df_filtered['End Customer'].nunique()}")
boxed_metric("Total Truck Mixer", f"{df_filtered['Truck No'].nunique()}")


    # =========================
    # Volume Per Day
    # =========================
    st.markdown(f"<h2 style='color:{font_color}'>📈 Volume Per Day</h2>", unsafe_allow_html=True)
    sales_trend = df_filtered.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
    sales_trend["Volume"] = sales_trend["Volume"].round(2)
    fig_sales_trend = px.line(sales_trend, x="Tanggal Pengiriman", y="Volume", markers=True, text="Volume", title="Volume Per Day")
    st.plotly_chart(styled_chart(fig_sales_trend, height=400, font_size=13, text_position="top center"), use_container_width=True)

    # =========================
    # Perform Delivery per Area & Plant
    # =========================
    col1, col2 = st.columns(2)
    with col1:
        volume_area = df_filtered.groupby("Area")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
        fig_area = px.bar(volume_area, x="Area", y="Volume", text="Volume", color="Area",
                          title="Perform Delivery per Area", color_discrete_sequence=color_palette)
        st.plotly_chart(styled_chart(fig_area), use_container_width=True)

    with col2:
        volume_plant = df_filtered.groupby("Plant Name")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
        fig_plant = px.bar(volume_plant, x="Plant Name", y="Volume", text="Volume", color="Plant Name",
                           title="Perform Delivery per Plant", color_discrete_sequence=color_palette)
        st.plotly_chart(styled_chart(fig_plant), use_container_width=True)

    # =========================
    # Performa Sales & Customer
    # =========================
    st.markdown(f"<h2 style='color:{font_color}'>👤 Performa Sales & Customer</h2>", unsafe_allow_html=True)
    sales_perf = df_filtered.groupby("Salesman")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
    fig_salesman = px.bar(sales_perf, x="Salesman", y="Volume", text="Volume", color="Salesman",
                          title="Performa Salesman", color_discrete_sequence=color_palette)
    st.plotly_chart(styled_chart(fig_salesman, height=600), use_container_width=True)

    cust_perf = df_filtered.groupby("End Customer")["Volume"].sum().reset_index().sort_values(by="Volume", ascending=False)
    fig_customer = px.bar(cust_perf, x="End Customer", y="Volume", text="Volume", color="End Customer",
                          title="Performa End Customer", color_discrete_sequence=color_palette)
    st.plotly_chart(styled_chart(fig_customer, height=600), use_container_width=True)

    # =========================
    # Utilisasi Truck Mixer
    # =========================
    st.markdown(f"<h2 style='color:{font_color}'>🚚 Utilisasi Truck Mixer</h2>", unsafe_allow_html=True)
    ritase_truck = df_filtered.groupby("Truck No")["Ritase"].sum().reset_index().sort_values(by="Ritase", ascending=False)
    fig_truck_total = px.bar(ritase_truck, x="Truck No", y="Ritase", text="Ritase", color="Truck No",
                             title="Total Ritase per Truck", color_discrete_sequence=color_palette)
    st.plotly_chart(styled_chart(fig_truck_total), use_container_width=True)

    volume_avg = df_filtered.groupby("Truck No")["Volume"].mean().reset_index().sort_values(by="Volume", ascending=False)
    fig_truck_avg = px.bar(volume_avg, x="Truck No", y="Volume", text="Volume", color="Truck No",
                           title="Average Volume per Ritase (Truck)", color_discrete_sequence=color_palette)
    st.plotly_chart(styled_chart(fig_truck_avg), use_container_width=True)

    # =========================
    # 📈 Visualisasi Tren & 📍 Analisa Jarak Tempuh (Paling Bawah)
    # =========================
    st.markdown("---")  # garis pemisah

    st.subheader("📈 Visualisasi Tren")
    trend_ritase = df_filtered.groupby("Tanggal Pengiriman")["Ritase"].sum().reset_index()
    trend_ritase["Ritase"] = trend_ritase["Ritase"].round(2)
    fig_trend_ritase = px.line(trend_ritase, x="Tanggal Pengiriman", y="Ritase", markers=True, text="Ritase", title="Tren Ritase")
    st.plotly_chart(styled_chart(fig_trend_ritase, height=400, text_position="top center"), use_container_width=True)

    trend_volume = df_filtered.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
    trend_volume["Volume"] = trend_volume["Volume"].round(2)
    fig_trend_volume = px.line(trend_volume, x="Tanggal Pengiriman", y="Volume", markers=True, text="Volume", title="Tren Volume")
    st.plotly_chart(styled_chart(fig_trend_volume, height=400, text_position="top center"), use_container_width=True)

    st.subheader("📍 Analisa Jarak Tempuh")
    col5, col6 = st.columns(2)
    with col5:
        avg_dist_plant = df_filtered.groupby("Plant Name")["Distance"].mean().reset_index()
        avg_dist_plant["Distance"] = avg_dist_plant["Distance"].round(2)
        fig_avg_dist_plant = px.bar(avg_dist_plant, x="Plant Name", y="Distance", text="Distance", title="Average Distance per Plant")
        st.plotly_chart(styled_chart(fig_avg_dist_plant), use_container_width=True)

    with col6:
        avg_dist_area = df_filtered.groupby("Area")["Distance"].mean().reset_index()
        avg_dist_area["Distance"] = avg_dist_area["Distance"].round(2)
        fig_avg_dist_area = px.bar(avg_dist_area, x="Area", y="Distance", text="Distance", title="Average Distance per Area")
        st.plotly_chart(styled_chart(fig_avg_dist_area), use_container_width=True)
