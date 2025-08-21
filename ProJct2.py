# Dashboard2
# Dashboard2 Futuristik Dark Theme + Grid Layout
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="🚀 Futuristic Dashboard", layout="wide")

# CSS Custom buat tema dark neon
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    .stSidebar {
        background-color: #1C1C1C !important;
    }
    h1, h2, h3, h4 {
        color: #00E5FF !important;
        font-weight: 700 !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #00E5FF, #7C4DFF);
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Dashboard Delivery & Sales ")

# Upload file
uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    expected_columns = [
        "Tanggal Pengiriman", "Area", "Plant Name", "Salesman", "End Customer",
        "Volume", "Ritase", "Truck No", "Distance"
    ]
    missing_columns = [col for col in expected_columns if col not in df.columns]

    if missing_columns:
        st.warning(f"⚠️ Kolom berikut tidak ada di file: {missing_columns}")
    else:
        # Sidebar Filter
        st.sidebar.header("🎛 Filter Data")

        if st.sidebar.button("🔄 Reset Filter"):
            st.experimental_rerun()

        start_date = st.sidebar.date_input("Start Date")
        end_date = st.sidebar.date_input("End Date")

        area = st.sidebar.multiselect("Area", options=df["Area"].dropna().unique())
        plant_options = df[df["Area"].isin(area)]["Plant Name"].dropna().unique() if area else df["Plant Name"].dropna().unique()
        plant = st.sidebar.multiselect("Plant Name", options=plant_options)
        salesman = st.sidebar.multiselect("Salesman", options=df["Salesman"].dropna().unique())
        end_customer = st.sidebar.multiselect("End Customer", options=df["End Customer"].dropna().unique())
        truck = st.sidebar.multiselect("Truck No", options=df["Truck No"].dropna().unique())

        if start_date and end_date:
            df = df[(df["Tanggal Pengiriman"] >= pd.to_datetime(start_date)) &
                    (df["Tanggal Pengiriman"] <= pd.to_datetime(end_date))]
        if area:
            df = df[df["Area"].isin(area)]
        if plant:
            df = df[df["Plant Name"].isin(plant)]
        if salesman:
            df = df[df["Salesman"].isin(salesman)]
        if end_customer:
            df = df[df["End Customer"].isin(end_customer)]
        if truck:
            df = df[df["Truck No"].isin(truck)]

        # Fungsi export
        def to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Report')
            return output.getvalue()

        st.download_button(
            label="📥 Download Excel",
            data=to_excel(df),
            file_name='report.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # 🎨 Warna Neon untuk Chart
        neon_colors = ["#00E5FF", "#FF4081", "#7C4DFF", "#76FF03", "#FFEA00"]

        # 📊 Volume Trend (Full Width)
        st.subheader("📊 Volume Trend")
        vol_per_tanggal = df.groupby("Tanggal Pengiriman")["Volume"].sum().reset_index()
        fig1 = px.line(vol_per_tanggal, x="Tanggal Pengiriman", y="Volume", markers=True,
                       title="Trend Volume", color_discrete_sequence=[neon_colors[0]])
        fig1.update_traces(line_width=3, marker=dict(size=10),
                           text=vol_per_tanggal["Volume"], textposition="top center")
        fig1.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                           font=dict(color="white"))
        st.plotly_chart(fig1, use_container_width=True)

        # 📍 Volume per Area & Plant (Grid)
        st.subheader("📍 Volume per Area & Plant")
        col1, col2 = st.columns(2)

        with col1:
            fig2 = px.bar(df.groupby("Area")["Volume"].sum().reset_index(),
                          x="Area", y="Volume", title="Volume per Area",
                          color="Area", color_discrete_sequence=neon_colors)
            fig2.update_traces(texttemplate='%{y}', textposition='outside')
            fig2.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            fig3 = px.bar(df.groupby("Plant Name")["Volume"].sum().reset_index(),
                          x="Plant Name", y="Volume", title="Volume per Plant",
                          color="Plant Name", color_discrete_sequence=neon_colors)
            fig3.update_traces(texttemplate='%{y}', textposition='outside')
            fig3.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig3, use_container_width=True)

        # 👤 Performa Sales & Customer (Grid)
        st.subheader("👤 Performa Sales & Customer")
        col3, col4 = st.columns(2)

        with col3:
            fig4 = px.bar(df.groupby("Salesman")["Volume"].sum().reset_index(),
                          x="Salesman", y="Volume", title="Salesman Performance",
                          color="Salesman", color_discrete_sequence=neon_colors)
            fig4.update_traces(texttemplate='%{y}', textposition='outside')
            fig4.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig4, use_container_width=True)

        with col4:
            fig5 = px.bar(df.groupby("End Customer")["Volume"].sum().reset_index(),
                          x="End Customer", y="Volume", title="End Customer Performance",
                          color="End Customer", color_discrete_sequence=neon_colors)
            fig5.update_traces(texttemplate='%{y}', textposition='outside')
            fig5.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig5, use_container_width=True)

        # 🚚 Logistik (Grid)
        st.subheader("🚚 Ritase per Truck")
        col5, col6 = st.columns(2)

        with col5:
            fig6_sum = px.bar(df.groupby("Truck No")["Ritase"].sum().reset_index(),
                              x="Truck No", y="Ritase", title="Total Ritase per Truck",
                              color="Truck No", color_discrete_sequence=neon_colors)
            fig6_sum.update_traces(texttemplate='%{y}', textposition='outside')
            fig6_sum.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig6_sum, use_container_width=True)

        with col6:
            fig6_avg = px.bar(df.groupby("Truck No")["Ritase"].mean().reset_index(),
                              x="Truck No", y="Ritase", title="Average Ritase per Truck",
                              color="Truck No", color_discrete_sequence=neon_colors)
            fig6_avg.update_traces(texttemplate='%{y:.2f}', textposition='outside')
            fig6_avg.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig6_avg, use_container_width=True)

        # 📏 Distance (Grid)
        st.subheader("📏 Distance Analysis")
        col7, col8 = st.columns(2)

        with col7:
            fig_dist_plant = px.bar(df.groupby("Plant Name")["Distance"].mean().reset_index(),
                                    x="Plant Name", y="Distance", title="Avg Distance per Plant",
                                    color="Plant Name", color_discrete_sequence=neon_colors)
            fig_dist_plant.update_traces(texttemplate='%{y:.2f}', textposition='outside')
            fig_dist_plant.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig_dist_plant, use_container_width=True)

        with col8:
            fig_dist_area = px.bar(df.groupby("Area")["Distance"].mean().reset_index(),
                                   x="Area", y="Distance", title="Avg Distance per Area",
                                   color="Area", color_discrete_sequence=neon_colors)
            fig_dist_area.update_traces(texttemplate='%{y:.2f}', textposition='outside')
            fig_dist_area.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
            st.plotly_chart(fig_dist_area, use_container_width=True)

        # 📈 Trend Ritase (Full Width)
        st.subheader("📈 Trend Ritase")
        fig8 = px.line(df.groupby("Tanggal Pengiriman")["Ritase"].sum().reset_index(),
                       x="Tanggal Pengiriman", y="Ritase", markers=True,
                       title="Trend Ritase", color_discrete_sequence=[neon_colors[1]])
        fig8.update_traces(line_width=3, marker=dict(size=10))
        fig8.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig8, use_container_width=True)
