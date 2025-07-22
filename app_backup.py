import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="CDP AI NQ Prototype", layout="wide")

html_code = Path("aiq-re.html").read_text("utf-8")

components.html(html_code, height=1100, scrolling=True)