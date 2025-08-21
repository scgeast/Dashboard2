# Dashboard2
import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    df = pd.read_excel("data_penjualan.xlsx")  # ganti sesuai nama file kamu
    return df

df = load_data()

# ===============================
# Sidebar Filter
# ===============================
st.sidebar.header("🔍 Filter Data")

# Default values
default_start = df["Tanggal Pengiriman"].min()
default_end = df["Tanggal Pengiriman"].max()
default_region = []
default_pabrik = []
default_salesman = []
default_customer = []

# Tombol Reset
if st.sidebar.button("🔄 Reset Filter"):
    st.session_state["start_date"] = default_start
    st.session_state["end_date"] = default_end
    st.session_state["region"] = default_region
    st.session_state["pabrik"] = default_pabrik
    st.session_state["salesman"] = default_salesman
    st.session_state["customer"] = default_customer

# Start & End Date
start_date = st.sidebar.date_input("Start Date", 
                                   st.session_state.get("start_date", default_start), 
                                   key="start_date")
end_date = st.sidebar.date_input("End Date", 
                                 st.session_state.get("end_date", default_end), 
                                 key="end_date")

# Filter Region
region_options = df["Region"].unique().tolist()
selected_region = st.sidebar.multiselect("Region", 
                                         region_options, 
                                         default=st.session_state.get("region", default_region), 
                                         key="region")

# Filter Pabrik -> Dinamis sesuai Region
if selected_region:
    filtered_df_region = df[df["Region"].isin(selected_region)]
    pabrik_options = filtered_df_region["Pabrik"].unique().tolist()
else:
    pabrik_options = df["Pabrik"].unique().tolist()

selected_pabrik = st.sidebar.multiselect("Pabrik", 
                                         pabrik_options, 
                                         default=st.session_state.get("pabrik", default_pabrik), 
                                         key="pabrik")

# Filter Salesman & End Customer
salesman_options = df["Salesman"].unique().tolist()
selected_salesman = st.sidebar.multiselect("Salesman", 
                                           salesman_options, 
                                           default=st.session_state.get("salesman", default_salesman), 
                                           key="salesman")

customer_options = df["End Customer"].unique().tolist()
selected_customer = st.sidebar.multiselect("End Customer", 
                                           customer_options, 
                                           default=st.session_state.get("customer", default_customer), 
                                           key="customer")

# ===============================
# Apply Filter
# ===============================
filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["Tanggal Pengiriman"] >= pd.to_datetime(start_date)) &
    (filtered_df["Tanggal Pengiriman"] <= pd.to_datetime(end_date))
]

if selected_region:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_region)]
if selected_pabrik:
    filtered_df = filtered_df[filtered_df["Pabrik"].isin(selected_pabrik)]
if selected_salesman:
    filtered_df = filtered_df[filtered_df["Salesman"].isin(selected_salesman)]
if selected_customer:
    filtered_df = filtered_df[filtered_df["End Customer"].isin(selected_customer)]

# ===============================
# Output Data
# ===============================
st.subheader("📊 Data Penjualan")
st.dataframe(filtered_df, height=600)  # tabel lebih tinggi

# ===============================
# Chart Penjualan
# ===============================
st.subheader("📈 Analisa Penjualan")

if not filtered_df.empty:
    # Contoh: Penjualan per Region
    fig = px.bar(
        filtered_df.groupby("Region")["Jumlah Penjualan"].sum().reset_index(),
        x="Region",
        y="Jumlah Penjualan",
        color="Region",
        text_auto=True,
        color_discrete_sequence=px.colors.sequential.Viridis  # warna futuristik
    )

    # Perbesar Chart
    fig.update_layout(
        title="Penjualan per Region",
        xaxis_title="Region",
        yaxis_title="Jumlah Penjualan",
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Tidak ada data yang sesuai filter.")
