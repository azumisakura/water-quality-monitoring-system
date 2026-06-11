import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt
import base64
import os
from utils.prepare_data import prepare_display_data
from utils.load_records import load_records
from components.filter import show_filters
from components.table import show_table
from utils.quality_score import compute_quality_score
from io import BytesIO
from components.navbar import show_navbar

# ✅ Page config dapat nasa taas
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Navbar
show_navbar()

def get_base64_img(image_path):
    """Safely converts local image to base64 string."""
    # Fallback placeholder if the file is completely missing
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
img_base64 = get_base64_img("static/water-bg.jpg")
if img_base64:
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
else:
    st.error(
        "Error: Could not find 'water-bg.jpg'. Place it next to your python script."
    )

# ✅ Hide sidebar controls
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
</style>
""", unsafe_allow_html=True)

with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center;'>📈 Data Visualization</h1>", unsafe_allow_html=True)
st.html(
    """
    <div style="
        background-color: #2563eb; 
        color: white !important; 
        width: 100%; 
        border-radius: 8px; 
        padding: 12px 20px; 
        font-size: 24px; 
        font-weight: 600; 
        display: flex; 
        align-items: center; 
        gap: 8px;
        box-sizing: border-box;
        margin-bottom: 1rem;
    ">
        Visualize existing records and understand the water quality trends:
    </div>
    """
)

records_df = load_records()

if records_df.empty:
    st.info("No records available for visualization.")
else:
    selected_parameter, station_selection, month_selection, parameter_labels = show_filters(records_df)

    filtered_df = records_df.copy()
    if station_selection:
        filtered_df = filtered_df[filtered_df["location"].isin(station_selection)]
    if month_selection and "month" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["month"].astype(str).isin(month_selection)]

    if filtered_df.empty:
        st.warning("No records match the selected filters.")
    else:
        filtered_df, display_df = prepare_display_data(filtered_df)

        # 📋 All Records
        st.html(
            """
            <div style="
                background-color: #2563eb; 
                color: white !important; 
                width: 100%; 
                border-radius: 8px; 
                padding: 12px 20px; 
                font-size: 24px; 
                font-weight: 600; 
                display: flex; 
                align-items: center; 
                gap: 8px;
                box-sizing: border-box;
                margin-bottom: 1rem;
            ">
                Filtered records
            </div>
            """
        )
        show_table(display_df)

        # 🥧 Compliance Distribution
        if "classification" in filtered_df.columns:
            pie_data = filtered_df["classification"].value_counts().reset_index()
            pie_data.columns = ["Classification", "Count"]
            fig = px.pie(pie_data, names="Classification", values="Count", hole=0.4)
            st.html(
                    """
                    <div style="
                        background-color: #2563eb; 
                        color: white !important; 
                        width: 100%; 
                        border-radius: 8px; 
                        padding: 12px 20px; 
                        font-size: 24px; 
                        font-weight: 600; 
                        display: flex; 
                        align-items: center; 
                        gap: 8px;
                        box-sizing: border-box;
                        margin-bottom: 1rem;
                    ">
                        🥧 Compliance Distribution
                    </div>
                    """
                )
            st.plotly_chart(fig, use_container_width=True)

        # 📈 Monthly Sample Distribution
        if "month" in filtered_df.columns:
            month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]
            month_counts = filtered_df["month"].value_counts().reindex(month_order, fill_value=0).reset_index()
            month_counts.columns = ["Month", "Samples"]
            fig = px.bar(month_counts, x="Month", y="Samples")
            st.html(
                """
                <div style="
                    background-color: #2563eb; 
                    color: white !important; 
                    width: 100%; 
                    border-radius: 8px; 
                    padding: 12px 20px; 
                    font-size: 24px; 
                    font-weight: 600; 
                    display: flex; 
                    align-items: center; 
                    gap: 8px;
                    box-sizing: border-box;
                    margin-bottom: 1rem;
                ">
                    📈 Monthly Sample Distribution
                </div>
                """
            )
            st.plotly_chart(fig, use_container_width=True)

        # 🌍 Monitoring Station Distribution
        if "location" in filtered_df.columns:
            station_counts = filtered_df["location"].value_counts().reset_index()
            station_counts.columns = ["Station", "Samples"]
            fig = px.bar(station_counts, x="Station", y="Samples", color="Samples")
            st.html(
                """
                <div style="
                    background-color: #2563eb; 
                    color: white !important; 
                    width: 100%; 
                    border-radius: 8px; 
                    padding: 12px 20px; 
                    font-size: 24px; 
                    font-weight: 600; 
                    display: flex; 
                    align-items: center; 
                    gap: 8px;
                    box-sizing: border-box;
                    margin-bottom: 1rem;
                ">
                    🌍 Monitoring Station Distribution
                </div>
                """
            )
            st.plotly_chart(fig, use_container_width=True)

        # ⭐ Top Stations by Average Quality Score
        score_df = filtered_df.copy()
        score_df["quality_score"] = compute_quality_score(score_df)
        if "location" in score_df.columns:
            top_stations = score_df.groupby("location")["quality_score"].mean().reset_index().sort_values(by="quality_score", ascending=False)
            fig = px.bar(top_stations, x="location", y="quality_score", color="quality_score")
            fig.update_layout(xaxis_title="Monitoring Station", yaxis_title="Average Quality Score")
            st.html(
                """
                <div style="
                    background-color: #2563eb; 
                    color: white !important; 
                    width: 100%; 
                    border-radius: 8px; 
                    padding: 12px 20px; 
                    font-size: 24px; 
                    font-weight: 600; 
                    display: flex; 
                    align-items: center; 
                    gap: 8px;
                    box-sizing: border-box;
                    margin-bottom: 1rem;
                ">
                    ⭐ Top Stations by Average Quality Score
                </div>
                """
            )
            st.plotly_chart(fig, use_container_width=True)

        # 📉 Line Graph of Selected Parameter over Time (Altair)
        if selected_parameter in filtered_df.columns:
            st.html(
                f"""
                <div style="
                    background-color: #2563eb; 
                    color: white !important; 
                    width: 100%; 
                    border-radius: 8px; 
                    padding: 12px 20px; 
                    font-size: 24px; 
                    font-weight: 600; 
                    display: flex; 
                    align-items: center; 
                    gap: 8px;
                    box-sizing: border-box;
                    margin-bottom: 1rem;
                ">
                    {parameter_labels[selected_parameter]} over time
                </div>
                """
            )
            chart_df = filtered_df.copy()
            if "month" in chart_df.columns:
                month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]
                chart_df["month"] = chart_df["month"].astype(str).str.strip().str.capitalize()
                chart_df["month_cat"] = pd.Categorical(chart_df["month"], categories=month_order, ordered=True)
                chart_df = chart_df.sort_values("month_cat")
            elif "year" in chart_df.columns:
                chart_df["year"] = chart_df["year"].astype(str)

            base = alt.Chart(chart_df).mark_line(point=True)
            x_axis = alt.X("month_cat:N" if "month_cat" in chart_df.columns else ("year:N" if "year" in chart_df.columns else "index:O"),
                           title="Month" if "month_cat" in chart_df.columns else ("Year" if "year" in chart_df.columns else "Record"),
                           axis=alt.Axis(labelAngle=0))
            if "location" in chart_df.columns:
                chart = base.encode(
                    x=x_axis,
                    y=alt.Y(f"{selected_parameter}:Q", title=parameter_labels[selected_parameter]),
                    color=alt.Color("location:N", title="Station"),
                    tooltip=["month", selected_parameter, "location"] if "month" in chart_df.columns else ["year", selected_parameter, "location"]
                )
            else:
                chart = base.encode(
                    x=x_axis,
                    y=alt.Y(f"{selected_parameter}:Q", title=parameter_labels[selected_parameter]),
                    tooltip=["month", selected_parameter] if "month" in chart_df.columns else ["year", selected_parameter]
                )
            chart = chart.properties(width=700, height=400)
            st.altair_chart(chart, use_container_width=True)

            # Average parameter by station
            if "location" in filtered_df.columns:
                st.html(
                    f"""
                    <div style="
                        background-color: #2563eb; 
                        color: white !important; 
                        width: 100%; 
                        border-radius: 8px; 
                        padding: 12px 20px; 
                        font-size: 24px; 
                        font-weight: 600; 
                        display: flex; 
                        align-items: center; 
                        gap: 8px;
                        box-sizing: border-box;
                        margin-bottom: 1rem;
                    ">
                        Average {parameter_labels[selected_parameter]} by station
                    </div>
                    """
                )
                avg_by_station = filtered_df.groupby("location")[selected_parameter].mean().reset_index()
                avg_chart = alt.Chart(avg_by_station).mark_bar().encode(
                    x=alt.X(f"{selected_parameter}:Q", title=parameter_labels[selected_parameter]),
                    y=alt.Y("location:N", title="Station", sort="-x"),
                    tooltip=["location", alt.Tooltip(f"{selected_parameter}:Q", title=parameter_labels[selected_parameter])]
                ).properties(width=700, height=400)
                st.altair_chart(avg_chart, use_container_width=True)

            # Average quality score by station
            if "location" in filtered_df.columns:
                station_score = score_df.groupby("location")["quality_score"].mean().reset_index()
                st.html(
                    """
                    <div style="
                        background-color: #2563eb; 
                        color: white !important; 
                        width: 100%; 
                        border-radius: 8px; 
                        padding: 12px 20px; 
                        font-size: 24px; 
                        font-weight: 600; 
                        display: flex; 
                        align-items: center; 
                        gap: 8px;
                        box-sizing: border-box;
                        margin-bottom: 1rem;
                    ">
                        Average Quality Score by station
                    </div>
                    """
                )
                score_chart = alt.Chart(station_score).mark_bar().encode(
                    x=alt.X("quality_score:Q", title="Quality Score"),
                    y=alt.Y("location:N", title="Station", sort="-x"),
                    tooltip=["location", alt.Tooltip("quality_score:Q", title="Quality Score")]
                ).properties(width=700, height=400)
                st.altair_chart(score_chart, use_container_width=True)

        # 🏆 Best and Worst Monitoring Stations
        station_scores = score_df.groupby("location")["quality_score"].mean().reset_index()
        if not station_scores.empty:
            best_station = station_scores.loc[station_scores["quality_score"].idxmax()]
            worst_station = station_scores.loc[station_scores["quality_score"].idxmin()]
            col1, col2 = st.columns(2)
            with col1: st.success(f"🏆 Best Monitoring Station\n\n{best_station['location']}\n\nAverage Quality Score: {round(best_station['quality_score'],2)}")
            with col2: st.error(f"⚠️ Worst Monitoring Station\n\n{worst_station['location']}\n\nAverage Quality Score: {round(worst_station['quality_score'],2)}")

        # 📊 Monitoring Station Rankings
        station_ranking = score_df.groupby("location")["quality_score"].mean().reset_index().sort_values(by="quality_score", ascending=False)
        station_ranking["Rank"] = range(1, len(station_ranking)+1)
        station_ranking = station_ranking[["Rank","location","quality_score"]]
        station_ranking.columns = ["Rank","Monitoring Station","Average Quality Score"]
        station_ranking["Average Quality Score"] = station_ranking["Average Quality Score"].round(2)
        st.html(
            """
            <div style="
                background-color: #2563eb; 
                color: white !important; 
                width: 100%; 
                border-radius: 8px; 
                padding: 12px 20px; 
                font-size: 24px; 
                font-weight: 600; 
                display: flex; 
                align-items: center; 
                gap: 8px;
                box-sizing: border-box;
                margin-bottom: 1rem;
            ">
                📊 Monitoring Station Rankings
            </div>
            """
        )
        st.dataframe(station_ranking, use_container_width=True)

        # 📥 Export Records
        st.html(
            """
            <div style="
                background-color: #2563eb; 
                color: white !important; 
                width: 100%; 
                border-radius: 8px; 
                padding: 12px 20px; 
                font-size: 24px; 
                font-weight: 600; 
                display: flex; 
                align-items: center; 
                gap: 8px;
                box-sizing: border-box;
                margin-bottom: 1rem;
            ">
                📥 Export Records
            </div>
            """
        )
        st.write("You can download the filtered records as a CSV or Excel file:")
        csv = filtered_df.to_csv(index=False)
        st.download_button("📄 Download CSV", csv, "water_quality_records.csv", "text/csv")

        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            filtered_df.to_excel(writer, index=False, sheet_name="Water Quality Records")
        excel_data = excel_buffer.getvalue()
        st.download_button("📊 Download Excel", excel_data, "water_quality_records.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
