import pandas as pd
import streamlit as st
import plotly.express as px

from dataset.preprocessing import FILEPATH_BUDGET_PROCESSED

df = pd.read_csv(FILEPATH_BUDGET_PROCESSED)
df_filtered = df.copy()
colorscale = px.colors.diverging.RdYlBu

st.header("🗺️ EuroNomad Navigator")
st.markdown("Your EU City Cost & Budget Guide!", help="""        
This app uses data from Numbeo, a crowdsourced global database of reported consumer prices. 
The data is processed to estimate monthly budgets based on various lifestyle choices.

**Important Considerations:**
- The displayed figures are estimates and can vary based on individual spending habits.
- The data is based on user-submitted information, which may not always be fully comprehensive or up-to-date.
- Exchange rates are based on the latest available data and may fluctuate.

For more detailed information about the data and methodology, please refer to the Numbeo website.
""")

with st.sidebar:
    st.markdown("""
    Welcome to the **EuroNomad Navigator**!
    
    This app is designed to help you explore and compare the **cost of living** across various cities in Europe, 
    making it easier for you to plan your next move or travel destination.

    Use the interactive map and charts below to visualize and compare key metrics such as **average monthly savings, rent costs, and overall expenses**. 
    You can filter the data by country and adjust the ranges to focus on what matters most to you.

    Whether you're considering relocating, planning a long-term stay, or just curious about different living costs, the **EuroNomad Navigator** provides valuable insights to guide your decisions.
    """)

segmented_dim_options = {
    "Saving Rate": "Monthly Savings over Income",
    "Rent vs Income": "Montlhy Rent over Income",
    "Salary": "Monthly Salary",
    "Expenses": "Total Monthly Expenses",
    "Savings": "Monthly Savings",
}

with st.expander(label="Filters", icon=":material/filter_alt:", expanded=True):

    col1, empty, col2 = st.columns([0.49, 0.02, 0.49])
    col3, empty, col4 = st.columns([0.49, 0.02, 0.49])

    with col1:
        segmented_aggr = st.segmented_control(label="Choose one option", options=["City", "Country"], default="City")
        if not segmented_aggr:
            st.markdown(":red[Please, select an option to continue.]")
            st.stop()
    
    with col3:
        multiselect_filter = st.multiselect("Filter by Country", list(df.sort_values("Country")["Country"].unique()), placeholder="Optional")
        if multiselect_filter:
            df_filtered = df_filtered[df_filtered["Country"].isin(multiselect_filter)]
        else:
            df_filtered = df.copy() 

    with col2:
        segmented_dim = st.pills(label="What do you want to analyze?", options=segmented_dim_options.keys(), default=list(segmented_dim_options.keys())[0], help="""
- **Saving Rate**: Shows the percentage of monthly income that remains after expenses.
- **Rent vs Income**: Displays the percentage of monthly income spent on rent.
- **Salary**: Presents the average monthly net salary after taxes.
- **Expenses**: Shows the total average monthly expenses.
- **Savings**: Indicates the average monthly savings in euros.
"""
            )
        if not segmented_dim:
            st.markdown(":red[Please, select an option to continue.]")
            st.stop()
        segmented_dim_value = segmented_dim_options[segmented_dim]

    with col4:
        slider_range_default= [df_filtered[segmented_dim_value].min(), df_filtered[segmented_dim_value].max() + 1E-6]
        if segmented_dim in ["Saving Rate", "Rent vs Income"]:
            slider_range = st.slider("Range [%]", min_value=slider_range_default[0], max_value=slider_range_default[1], value=(slider_range_default[0], slider_range_default[1]), step=1.0)
        else:
            slider_range = st.slider("Range [€]", min_value=slider_range_default[0], max_value=slider_range_default[1], value=(slider_range_default[0], slider_range_default[1]), step=1.0)
            
df_filtered = df_filtered[df_filtered[segmented_dim_value].between(slider_range[0], slider_range[1])]

# group by like below but keep all columns
if segmented_aggr == "City":
    df_filtered = df_filtered.groupby(segmented_aggr).agg({
        "City": "first",
        "Country": "first",
        "Latitude": "first",
        "Longitude": "first",
        segmented_dim_value: "mean",
    }).reset_index(drop=True)
    
else:
    df_filtered = df_filtered.groupby(segmented_aggr).agg({
        "Country": "first",
        segmented_dim_value: "mean",
    }).reset_index(drop=True)

df_filtered = df_filtered.sort_values(segmented_dim_value, ascending=False).reset_index(drop=True).rename(index=lambda x: x + 1)
df_filtered[segmented_dim_value] = df_filtered[segmented_dim_value].round(2)
col1, col2 = st.columns([0.6, 0.4], gap="medium")

with col1:
    st.markdown(f"**{segmented_dim} by {segmented_aggr} - Map View**", help="Click on the map elements to see detailed information about each city or country.")
    if segmented_aggr == "City":
        fig_map = px.scatter_geo(
            df_filtered,
            lat="Latitude",
            lon="Longitude",
            color=segmented_dim_value,
            color_continuous_scale=colorscale,
            center={
                "lat":52,
                "lon":12
            },
            projection="kavrayskiy7",
            height=500,
            custom_data=df_filtered[["Country", "City", segmented_dim_value]],
        )   
        
        if not df_filtered.empty:
            mid_lat = (df_filtered["Latitude"].max() + df_filtered["Latitude"].min()) / 2
            mid_lon = (df_filtered["Longitude"].max() + df_filtered["Longitude"].min()) / 2
            max_lat_diff_filtered = df_filtered["Latitude"].max() - df_filtered["Latitude"].min()
            max_lat_diff = df["Latitude"].max() - df["Latitude"].min()
            lat_ratio = max_lat_diff_filtered / max_lat_diff

            fig_map.update_geos(
                center={
                    "lat": mid_lat,
                    "lon": mid_lon
                },
                projection_scale=max(4, round(25 - 21 * lat_ratio))
            )
        
        if segmented_dim in ["Saving Rate", "Rent vs Income"]:
            fig_map.update_traces(
                hovertemplate=(
                    "%{customdata[1]}, %{customdata[0]}<br>" +
                    "<b>%{customdata[2]}%</b>"
                ),
                
            )
        else:
            fig_map.update_traces(
                hovertemplate=(
                    "%{customdata[1]}, %{customdata[0]}<br>" +
                    "<b>%{customdata[2]} €</b>"
                ),
            )
    
    else:
        fig_map = px.choropleth(
            df_filtered,
            locations="Country",
            locationmode="country names",
            color=segmented_dim_value,
            color_continuous_scale=colorscale,
            center={
                "lat":52,
                "lon":12
            },
            projection="kavrayskiy7",
            height=600,
            title=f"{segmented_dim} by {segmented_aggr} - Map View",
        )
        
        fig_map.update_geos(
            projection_scale=4
        )
        
        if segmented_dim in ["Saving Rate", "Rent vs Income"]:
            fig_map.update_traces(
                hovertemplate=(
                    "%{customdata[0]}<br>" +
                    f"<b>%{{z:.2f}}%</b>"
                ),
                customdata=df_filtered[["Country"]],
            )
        else:
            fig_map.update_traces(
                hovertemplate=(
                    "%{customdata[0]}<br>" +
                    f"<b>%{{z:.2f}}%</b>"
                ),
                customdata=df_filtered[["Country"]],
            )
        
    fig_hist = px.histogram(
        df_filtered,
        x=segmented_dim_value,
        nbins=20,
        marginal="box",
        histfunc="avg",
        title=f"{segmented_dim} by {segmented_aggr} - Distribution"
    )
    
    fig_map.update_geos(        
        bgcolor="rgba(0,0,0,0)",
        showland=True, landcolor="LightGrey",
        showcoastlines=True, coastlinecolor="Grey",
        showsubunits=False, subunitcolor="Black",
        showocean=True, oceancolor="LightBlue",
        showframe=False, framecolor="Black",
        showcountries=True, countrycolor="Grey",
    )

    fig_map.update_layout(
        coloraxis_colorbar=dict(
            orientation="h",
            xanchor="center",
            y=-0.2,
            len=1,
            title=segmented_dim
        )
    )
    
    fig_hist.update_layout(
        xaxis_title=segmented_dim,
        yaxis_title=f"Number of {segmented_aggr}",
    )
    
    st.plotly_chart(fig_map)
    # st.plotly_chart(fig_hist)

with col2:
    
    with st.container(height=540, border=False):
        st.markdown(f"**{segmented_dim} by {segmented_aggr} - Ranking View**", help="Explore the ranking of cities or countries based on the selected metric. Hover over the bars to see the exact values."
        )
        
        df_filtered_bar = df_filtered.sort_values(segmented_dim_value, ascending=True)
        
        # create different y depending on segmented aggr
        if segmented_aggr == "City":
            fig_bar_y = [f"{i} - {city}, {country}" for i, city, country in zip(df_filtered_bar.index, df_filtered_bar["City"], df_filtered_bar["Country"])]
        else:
            fig_bar_y = [f"{i} - {country}" for i, country in zip(df_filtered_bar.index, df_filtered_bar["Country"])]
        
        fig_bar = px.bar(
        df_filtered_bar,
        x=segmented_dim_value,
        y=fig_bar_y,
        orientation="h",
        color=segmented_dim_value,
        color_continuous_scale=colorscale,
        text_auto=True
        )
            
        fig_bar.update_layout(
            yaxis=dict(
                tickmode="linear",
                tick0=0,
                dtick=1
            ),  
            height=max(300, len(df_filtered[segmented_dim_value].unique()) * 50),
            xaxis_title="",
            yaxis_title="",
            dragmode=False,
        )
        
        if segmented_dim in ["Saving Rate", "Rent vs Income"]:
            fig_bar.update_xaxes(ticksuffix="%")
        else:
            fig_bar.update_xaxes(ticksuffix="€")
        
        fig_bar.update_traces(
            hovertemplate=None,
            hoverinfo='skip'
        )
        
        
        config = {
        'scrollZoom': False,
        'dragmode': False,
        'displayModeBar': False
        }
        
        fig_bar.update_coloraxes(showscale=False)
        fig_bar.update_xaxes(side="top")
        
        st.plotly_chart(fig_bar, config=config)
    
st.markdown("**Detailed Data**")
if segmented_aggr == "City":
    df_filtered = df_filtered.drop(columns=["Latitude", "Longitude"])
st.dataframe(df_filtered)
