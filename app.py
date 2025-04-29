import streamlit as st

create_page = st.Page("pages/cost_of_living_map.py", title="Cost of Living Map", icon=":material/map:")
# delete_page = st.Page("pages/page_1.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([create_page])
st.set_page_config(
    page_title="EU Livestyle",
    page_icon="🗺️",
    layout="wide"
    )
pg.run()