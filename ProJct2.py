# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(page_title="📦 Dashboard Analyst Delivery & Sales", layout="wide")

# Tema futuristik
color_palette = ["#00FFFF", "#8A2BE2", "#00FF00", "#FF00FF", "#FFD700", "#00CED1"]

# Sidebar Tema
st.sidebar.header("🎨 Pengaturan Tampilan")
theme = st.sidebar.radio("Pilih Tema", ["Gelap", "Terang"])
bg_color = "#0d0f15" if theme == "Gelap" else "white"
font_color = "white" if theme == "Gelap" else "black"

st.markdown(f"<h1 style='color:{font_color}'>📦 Dashboard Analyst Delivery dan Sales</h1>", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Upload file Excel (5MB–30MB)", type=["xlsx", "xls"])
# 🎨 Modular Styling Function
def styled_chart(fig, height=None, font_size=12, margin=None, text_format=".2f", text_position="outside", show_legend=False, title_font_size=18):
    """
    Menata chart Plotly agar tampil profesional dan fleksibel.

    Parameters:
    - fig: objek figure dari Plotly
    - height: tinggi chart (int)
    - font_size: ukuran font umum (int)
    - margin: dict margin seperti {'t':40, 'b':40}
    - text_format: format angka pada label teks (str)
    - text_position: posisi teks seperti 'outside', 'top center'
    - show_legend: apakah legend ditampilkan (bool)
    - title_font_size: ukuran font judul (int)

    Returns:
    - fig yang sudah diupdate
    """
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

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Penyesuaian kolom agar fleksibel
    df.rename(columns={
        "Tanggal P": "Tanggal Pengiriman",
        "Plant Name": "Plant Name",
        "Area": "Area",
        "Ritase": "Ritase"
    }, inplace=True)

    for col in ["Salesman", "End Customer", "Volume", "Truck No", "Distance"]:
        if col not in df.columns:
            df[col] = 1 if col in ["Volume", "Ritase", "Distance"] else "Unknown"

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

    # Fungsi styling chart
    def styled_chart(fig, height=500):
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=font_color),
            title_font=dict(color=font_color, size=18),
            xaxis=dict(tickangle=45),
            showlegend=False,
            height=height
        )
        return fig

    # Dashboard Summary
    st.markdown(f"<h2 style='color:{font_color}'>📊 Dashboard Summary</h2>", unsafe_allow_html=True)
    colA, colB, colC, colD, colE, colF = st.columns(6)
    colA.metric("Total Area", f"{df_filtered['Area'].nunique()}")
    colB.metric("Total Plant", f"{df_filtered['Plant Name'].nunique()}")
    colC.metric("Total Volume", f"{df_filtered['Volume'].sum():,.2f}")
    colD.metric("Total Ritase", f"{df_filtered['Ritase'].sum():,.2f}")
    colE.metric("Total End Customer", f"{df_filtered['End Customer'].nunique()}")
    colF.metric("Total Truck Mixer", f"{df_filtered['Truck No'].nunique()}")

    # Volume Per Day
    st.markdown(f"<h2 style='color:{font_color}'>📈 Volume Per Day</h2>", unsafe_allow_html=True)
    sales_trend = df_filtered.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
    sales_trend["Volume"] = sales_trend["Volume"].round(2)
    fig_sales_trend = px.line(sales_trend, x="Tanggal Pengiriman", y="Volume", markers=True,
                              title="Volume Per Day", text="Volume")
    fig_sales_trend.update_traces(textposition="top center")
    st.plotly_chart(
    styled_chart(fig_sales_trend, height=400, font_size=13, text_position="top center"),
    use_container_width=True
)

    # Perform Delivery per Area & Plant
    col1, col2 = st.columns(2)
    with col1:
        volume_area = df_filtered.groupby("Area")["Volume"].sum().reset_index()
        volume_area["Volume"] = volume_area["Volume"].round(2)
        volume_area = volume_area.sort_values(by="Volume", ascending=False)
        fig_area = px.bar(volume_area, x="Area", y="Volume", text="Volume", color="Area",
                          title="Perform Delivery per Area", color_discrete_sequence=color_palette)
        st.plotly_chart(styled_chart(fig_area), use_container_width=True)

    with col2:
        volume_plant = df_filtered.groupby("Plant Name")["Volume"].sum().reset_index()
        volume_plant["Volume"] = volume_plant["Volume"].round(2)
        volume_plant = volume_plant.sort_values(by="Volume", ascending=False)
        fig_plant = px.bar(volume_plant, x="Plant Name", y="Volume", text="Volume", color="Plant Name",
                           title="Perform Delivery per Plant", color_discrete_sequence=color_palette)
        st.plotly_chart(styled_chart(fig_plant), use_container_width=True)

    # Performa Sales & Customer
    st.markdown(f"<h2 style='color:{font_color}'>👤 Performa Sales & Customer</h2>", unsafe_allow_html=True)
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

    # Utilisasi Truck Mixer
    st.markdown(f"<h2 style='color:{font_color}'>🚚 Utilisasi Truck Mixer</h2>", unsafe_allow_html=True)
    ritase_truck = df_filtered.groupby("Truck No")["Ritase"].sum().reset_index()
    ritase_truck["Ritase"] = ritase_truck["Ritase"].round(2)
    ritase_truck = ritase_truck.sort_values(by="Ritase", ascending=False)
    fig_truck_total = px.bar(ritase_truck, x="Truck No", y="Ritase", text="Ritase", color="Truck No",
                             title="Total Ritase per Truck", color_discrete_sequence=color_palette)
    st.plotly_chart(styled_chart(fig_truck_total), use_container_width=True)

    volume_avg = df_filtered.groupby("Truck No")["Volume"].mean().reset_index()
    volume_avg["Volume"] = volume_avg["Volume"].round(2)
    volume_avg = volume_avg.sort_values(by="Volume", ascending=False)
    fig_truck_avg = px.bar(volume_avg, x="Truck No", y="Volume", text="Volume", color="Truck No",
                       title="Average Volume per Ritase (Truck)", color_discrete_sequence=color_palette)
    st.plotly_chart(styled_chart(fig_truck_avg), use_container_width=True)

        """
    if height:
        fig.update_layout(height=height)

    if margin:
        fig.update_layout(margin=margin)

    fig.update_layout(
        font=dict(size=font_size),
        title_font=dict(size=title_font_size),
        showlegend=show_legend
    )

    try:
        fig.update_traces(texttemplate=f"%{{text:{text_format}}}", textposition=text_position)
    except Exception:
        pass  # Abaikan jika trace tidak mendukung texttemplate

    return fig

# 📥 Load & Filter Data
df = pd.read_excel("data.xlsx")  # Ganti dengan sumber data kamu
df_filtered = df[df["Date"] >= "2023-01-01"]  # Contoh filter

# 🎯 Summary Metrics (opsional)
total_volume = df_filtered["Volume"].sum()
total_sales = df_filtered["Sales"].sum()
st.metric("Total Volume", f"{total_volume:,.2f}")
st.metric("Total Sales", f"{total_sales:,.0f}")

# 📊 Chart 1: Bar Chart - Volume per Truck
volume_avg = df_filtered.groupby("Truck No")["Volume"].mean().reset_index()
volume_avg["Volume"] = volume_avg["Volume"].round(2)
volume_avg = volume_avg.sort_values(by="Volume", ascending=False)

fig_truck_avg = px.bar(volume_avg, x="Truck No", y="Volume", text="Volume", color="Truck No",
                       title="Average Volume per Ritase (Truck)", color_discrete_sequence=px.colors.qualitative.Set2)

st.plotly_chart(
    styled_chart(fig_truck_avg, height=500, margin=dict(t=40, b=40)),
    use_container_width=True
)

# 📈 Chart 2: Line Chart - Sales Trend
df_sales = df_filtered.groupby("Date")["Sales"].sum().reset_index()
fig_sales_trend = px.line(df_sales, x="Date", y="Sales", markers=True, title="Sales Trend Over Time")
fig_sales_trend.update_traces(text=df_sales["Sales"].round(2).astype(str))

st.plotly_chart(
    styled_chart(fig_sales_trend, height=400, font_size=13, text_position="top center"),
    use_container_width=True
"""
