import streamlit as st

overview = st.Page("pages/overview.py", title="Overview", icon=":material/travel_explore:")
simulator = st.Page("pages/simulator.py", title="Budget Simulator", icon=":material/attach_money:")

pg = st.navigation([overview, simulator])
st.set_page_config(
    page_title="EuroNomad Navigator",
    page_icon="🗺️",
    layout="wide"
    )
pg.run()