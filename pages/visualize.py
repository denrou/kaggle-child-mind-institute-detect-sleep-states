import polars as pl
import streamlit as st
import os
import platformdirs
import plotly.express as px

DATA_PATH = os.path.join(platformdirs.user_cache_path(os.getcwd()), "data")
PROJECT_NAME = os.getcwd().split("/")[-2]
INDIVIDUAL_SERIE_PATH = os.path.join(DATA_PATH, "individual_serie")

"""
# Sleep States
"""

"""
## Data

Let's look at data for individual series.
"""

st.write(
    f"{len(os.listdir('data/individual_serie'))} individual series from training data"
)  # noqa E501

with st.sidebar:
    st.write("## Options")
    serie_name = st.selectbox(
        "Serie",
        [
            x.split(os.path.sep)[-1].split(".")[0]
            for x in os.listdir(INDIVIDUAL_SERIE_PATH)
        ],
    )
    downsampling_factor = st.selectbox(
        "Downsampling factor",
        [
            "5s",
            "10s",
            "30s",
            "1m",
            "5m",
            "10m",
            "15m",
            "30m",
            "1h",
        ],
        index=6,
    )

assert downsampling_factor is not None
serie = (
    pl.read_csv(f"data/individual_serie/{serie_name}.csv")
    .with_columns(pl.col("timestamp").str.to_datetime("%+"))
    .sort("timestamp")
    .group_by_dynamic("timestamp", every=downsampling_factor)
    .agg(pl.col("anglez").mean().alias("anglez"), pl.col("enmo").mean().alias("enmo"))
)

event = (
    pl.read_csv("data/train_events.csv")
    .filter(pl.col("series_id") == serie_name)
    .filter(pl.col("timestamp") != "")
    .with_columns(pl.col("timestamp").str.to_datetime("%+"))
)

tab1, tab2 = st.tabs(["Table", "Chart"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.write(serie)

    with col2:
        st.write(event)

with tab2:
    fig = px.line(
        serie.to_pandas(),
        x="timestamp",
        y=["anglez"],
        title=f"Anglez for serie {serie_name}",
    )
    for row in event.to_pandas().itertuples():
        fig.add_vline(x=row.timestamp, line_width=1, line_dash="dash", line_color="red")
    st.plotly_chart(fig)
    st.line_chart(serie.to_pandas(), x="timestamp", y="anglez")
    st.line_chart(serie.to_pandas(), x="timestamp", y="enmo")
# st.write(data_first_serie)
# st.line_chart(data_first_serie.to_pandas(), x="timestamp", y="anglez")
# st.line_chart(data_first_serie.to_pandas(), x="timestamp", y="enmo")
