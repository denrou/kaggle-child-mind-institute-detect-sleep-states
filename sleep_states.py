import streamlit as st
import polars as pl
import os
import platformdirs

DATA_PATH = os.path.join(platformdirs.user_cache_path(os.getcwd()), "data")
PROJECT_NAME = os.getcwd().split("/")[-1]

st.title("Sleep States")

st.info(DATA_PATH)

