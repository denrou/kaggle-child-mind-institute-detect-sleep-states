import streamlit as st
import os
import polars as pl
import platformdirs

DATA_PATH = os.path.join(platformdirs.user_cache_path(os.getcwd()), "data")
PROJECT_NAME = os.getcwd().split("/")[-2]
INDIVIDUAL_SERIE_PATH = os.path.join(DATA_PATH, "individual_serie")
upload_file = None
data = None

if not os.path.exists(DATA_PATH):
    st.info(f"Creating data folder at {DATA_PATH}")
    os.makedirs(DATA_PATH)
if "train_series.parquet" not in os.listdir(DATA_PATH): 
    upload_file = st.file_uploader("Locate data", type=["zip"])
if upload_file is not None:
    st.info("Unzipping data")
    os.system(f"unzip {upload_file.name} -d {DATA_PATH}")
    st.success("Data unzipped")
if "individual_serie" not in os.listdir(DATA_PATH):
    st.info("Creating individual serie folder")
    os.makedirs(INDIVIDUAL_SERIE_PATH)
    st.success("Individual serie folder created")
if len(os.listdir(INDIVIDUAL_SERIE_PATH)) == 0:
    st.info("Reading training data")
    data = pl.read_parquet(os.path.join(DATA_PATH, "train_series.parquet"))
    st.success("Training data read")
    st.info("Create individual csv files for each patient")
    progress_text = "Saving individual csv files"
    progress_bar = st.progress(0)
    series_ids = data.get_column("series_id").unique().to_list()
    for i, series_id in enumerate(series_ids):
        progress_bar.progress(i / (len(series_ids) - 1), progress_text)
        data.filter(pl.col("series_id") == series_id).write_csv(
                os.path.join(INDIVIDUAL_SERIE_PATH, f"{series_id}.csv")
        )
    st.success("Individual csv files created")

