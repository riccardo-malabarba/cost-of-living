import streamlit as st

overview = st.Page("pages/overview.py", title="Overview", icon=":material/travel_explore:")
budget_simulator = st.Page("pages/page_1.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([overview, budget_simulator])
st.set_page_config(
    page_title="EuroNomad Navigator",
    page_icon="🗺️",
    layout="wide"
    )
pg.run()