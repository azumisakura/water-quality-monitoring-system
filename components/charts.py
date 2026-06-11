import altair as alt
import pandas as pd
import streamlit as st

from utils.quality_score import compute_quality_score


def show_charts(filtered_df, selected_parameter, parameter_labels):

    if selected_parameter in filtered_df.columns:

        st.subheader(f"{parameter_labels[selected_parameter]} over time")

        chart_df = filtered_df.copy()

        if "month" in chart_df.columns:

            month_order = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]

            chart_df["month"] = (
                chart_df["month"]
                .astype(str)
                .str.strip()
                .str.capitalize()
            )

            chart_df["month_cat"] = pd.Categorical(
                chart_df["month"],
                categories=month_order,
                ordered=True
            )

            chart_df = chart_df.sort_values("month_cat")

            chart_df.index = chart_df["month_cat"]

        elif "year" in chart_df.columns:

            chart_df.index = chart_df["year"].astype(str)

        else:

            chart_df.index = chart_df.index.astype(str)

        x_field = (
            "month_cat:N"
            if "month_cat" in chart_df.columns
            else (
                "year:N"
                if "year" in chart_df.columns
                else "record:O"
            )
        )

        x_title = (
            "Month"
            if "month_cat" in chart_df.columns
            else (
                "Year"
                if "year" in chart_df.columns
                else "Record"
            )
        )

        if x_field == "record:O":

            chart_df = (
                chart_df
                .reset_index()
                .rename(columns={"index": "record"})
            )

        else:

            chart_df = chart_df.reset_index(drop=True)

        base = alt.Chart(chart_df).mark_line(point=True)

        x_axis = alt.X(
            x_field,
            title=x_title,
            axis=alt.Axis(labelAngle=0),
            sort=month_order if x_field == "month_cat:N" else None
        )

        if "location" in chart_df.columns:

            chart = base.encode(
                x=x_axis,
                y=alt.Y(
                    f"{selected_parameter}:Q",
                    title=parameter_labels[selected_parameter]
                ),
                color=alt.Color(
                    "location:N",
                    title="Station"
                ),
                tooltip=[
                    "month",
                    selected_parameter,
                    "location"
                ] if "month" in chart_df.columns else [
                    "year",
                    selected_parameter,
                    "location"
                ]
            )

        else:

            chart = base.encode(
                x=x_axis,
                y=alt.Y(
                    f"{selected_parameter}:Q",
                    title=parameter_labels[selected_parameter]
                ),
                tooltip=[
                    "month",
                    selected_parameter
                ] if "month" in chart_df.columns else [
                    "year",
                    selected_parameter
                ]
            )

        chart = (
            chart
            .properties(
                width=700,
                height=400,
                background="white"
            )
            .configure_axis(
                labelColor="black",
                titleColor="black"
            )
            .configure_title(
                color="black"
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

        if "location" in filtered_df.columns:

            st.subheader(
                f"Average {parameter_labels[selected_parameter]} by station"
            )

            avg_by_station = (
                filtered_df
                .groupby("location")[selected_parameter]
                .mean()
                .reset_index()
            )

            avg_chart = (
                alt.Chart(avg_by_station)
                .mark_bar()
                .encode(
                    x=alt.X(
                        f"{selected_parameter}:Q",
                        title=parameter_labels[selected_parameter]
                    ),
                    y=alt.Y(
                        "location:N",
                        title="Station",
                        sort="-x"
                    ),
                    tooltip=[
                        "location",
                        alt.Tooltip(
                            f"{selected_parameter}:Q",
                            title=parameter_labels[selected_parameter]
                        )
                    ]
                )
                .properties(
                    width=700,
                    height=400,
                    background="white"
                )
                .configure_axis(
                    labelColor="black",
                    titleColor="black"
                )
                .configure_title(
                    color="black"
                )
            )

            st.altair_chart(
                avg_chart,
                use_container_width=True
            )

            score_df = chart_df.copy()

            score_df["quality_score"] = compute_quality_score(
                score_df
            )

            station_score = (
                score_df
                .groupby("location")["quality_score"]
                .mean()
                .reset_index()
            )

            st.subheader(
                "Average quality score by station"
            )

            score_chart = (
                alt.Chart(station_score)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "quality_score:Q",
                        title="Quality Score"
                    ),
                    y=alt.Y(
                        "location:N",
                        title="Station",
                        sort="-x"
                    ),
                    tooltip=[
                        "location",
                        alt.Tooltip(
                            "quality_score:Q",
                            title="Quality Score"
                        )
                    ]
                )
                .properties(
                    width=700,
                    height=400,
                    background="white"
                )
                .configure_axis(
                    labelColor="black",
                    titleColor="black"
                )
                .configure_title(
                    color="black"
                )
            )

            st.altair_chart(
                score_chart,
                use_container_width=True
            )

    else:

        st.warning(
            f"The selected parameter '{selected_parameter}' is not available in the current data."
        )