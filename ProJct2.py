# Dashboard2
# Dashboard2
import streamlit as st
import plotly.express as px

# Contoh kondisi untuk memilih tampilan chart
show_slider = True  # Ganti dengan kondisi sebenarnya sesuai kebutuhan

# ---- Average Ritase per Truck ----
if show_slider:
    fig_avg = px.bar(
        ritase_per_truck,
        x="Truck No",
        y="Average_Ritase",
        text="Average_Ritase",
        title="Average Ritase per Truck"
    )
    fig_avg.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig_avg.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=ritase_per_truck['Truck No'],
            tickangle=45,
            rangeslider=dict(visible=True)
        ),
        yaxis_title="Average Ritase",
        plot_bgcolor="#0d0f15",
        paper_bgcolor="#0d0f15",
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=80, b=200)
    )
    st.plotly_chart(fig_avg, use_container_width=True)
else:
    fig_avg = px.bar(
        ritase_per_truck,
        x="Truck No",
        y="Average_Ritase",
        text="Average_Ritase",
        title="Average Ritase per Truck"
    )
    fig_avg.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig_avg.update_layout(
        xaxis=dict(tickangle=45),
        yaxis_title="Average Ritase",
        showlegend=False,
        plot_bgcolor="#0d0f15",
        paper_bgcolor="#0d0f15",
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=80, b=200)
    )
    st.plotly_chart(fig_avg, use_container_width=True)

# ---- Average Distance ----
avg_dist_plant = filtered_df.groupby("Plant Name", as_index=False)["Distance"].mean()
avg_dist_area = filtered_df.groupby("Area", as_index=False)["Distance"].mean()

st.markdown("## 📏 Average Distance")

col1, col2 = st.columns(2)

with col1:
    fig_dist1 = px.bar(
        avg_dist_plant,
        x="Plant Name",
        y="Distance",
        text="Distance",
        title="Avg Distance per Plant"
    )
    fig_dist1.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_dist1.update_layout(
        xaxis=dict(tickangle=45),
        yaxis_title="Distance",
        showlegend=False,
        plot_bgcolor="#0d0f15",
        paper_bgcolor="#0d0f15",
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=80, b=200)
    )
    st.plotly_chart(fig_dist1, use_container_width=True)

with col2:
    fig_dist2 = px.bar(
        avg_dist_area,
        x="Area",
        y="Distance",
        text="Distance",
        title="Avg Distance per Area"
    )
    fig_dist2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_dist2.update_layout(
        xaxis=dict(tickangle=45),
        yaxis_title="Distance",
        showlegend=False,
        plot_bgcolor="#0d0f15",
        paper_bgcolor="#0d0f15",
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=80, b=200)
    )
    st.plotly_chart(fig_dist2, use_container_width=True)
