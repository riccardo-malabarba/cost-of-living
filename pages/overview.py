import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('dataset/data_proc.csv')
df_filtered = df.copy()

st.header("EuroNomad Navigator 🗺️")
st.write("Your EU City Cost & Budget Guide!")

segmented_dim_options = {
    "Saving Rate": "SavingToSalaryRatio",
    "Rent to Salary": "RentToSalaryRatio",
    "Salary": "AverageMonthlyNetSalary",
    "Expenses": "TotalMonthlyBudget",
    "Savings": "MonthlySavings",
}

segmented_aggr_options = {
    "Cities": "city",
    "Countries": "country"
}

with st.expander(label="Filters", icon=":material/filter_alt:"):

    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        segmented_aggr = st.segmented_control(label="Choose one option", options=segmented_aggr_options.keys(), default=list(segmented_aggr_options.keys())[0])
        segmented_aggr_value = segmented_aggr_options[segmented_aggr]

        segmented_dim = st.pills(label="What do you want to analyze?", options=segmented_dim_options.keys(), default=list(segmented_dim_options.keys())[0])
        segmented_dim_value = segmented_dim_options[segmented_dim]

        multiselect_filter = st.multiselect("Filter by Country", list(df.sort_values("country")["country"].unique()), placeholder="Optional")
        if multiselect_filter:
            df_filtered = df_filtered[df_filtered["country"].isin(multiselect_filter)]
        else:
            df_filtered = df.copy() 
            
        slider_range_default= [df_filtered[segmented_dim_value].min(), df_filtered[segmented_dim_value].max()]
        slider_range = st.slider("Range", min_value=slider_range_default[0], max_value=slider_range_default[1], value=(slider_range_default[0], slider_range_default[1]), step=1.0)


df_filtered = df_filtered[df_filtered[segmented_dim_value].between(slider_range[0], slider_range[1])]
# group by like below but keep all columns
if segmented_aggr == "Cities":
    df_filtered = df_filtered.groupby(segmented_aggr_value).agg({
        segmented_dim_value: 'mean',
        'latitude': 'first',
        'longitude': 'first',
        'country': 'first',
        'city': 'first',
    }).reset_index(drop=True)
else:
    df_filtered = df_filtered.groupby(segmented_aggr_value).agg({
        segmented_dim_value: 'mean',
        'country': 'first',
    }).reset_index(drop=True)

df_filtered = df_filtered.sort_values(segmented_dim_value)

col1, col2 = st.columns([0.6, 0.4], gap="medium")

with col1:
    
    if segmented_aggr == "Cities":
        fig_map = px.scatter_geo(
            df_filtered,
            lat="latitude",
            lon="longitude",
            color=segmented_dim_value,
            hover_name='city',
            hover_data=[segmented_dim_value],
            color_continuous_scale="tempo",
            center={
                "lat":52,
                "lon":12
            },
            projection="kavrayskiy7",
            height=600,
            title=f"{segmented_dim} by {segmented_aggr} - Map View"
        )
    
    else:
        fig_map = px.choropleth(
            df_filtered,
            locations="country",
            locationmode="country names",
            color=segmented_dim_value,
            color_continuous_scale="tempo",
            center={
                "lat":52,
                "lon":12
            },
            projection="kavrayskiy7",
            height=600,
            title=f"{segmented_dim} by {segmented_aggr} - Map View"
        )
        
    fig_hist = px.histogram(
        df_filtered,
        x=segmented_dim_value,
        nbins=20,
        marginal='box',
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
        projection_scale=4,
    )

    fig_map.update_layout(
        coloraxis_colorbar=dict(
            orientation="h",
            xanchor="center",
            y=-0.2,
            len=1
        )
    )
    
    fig_hist.update_layout(
        xaxis_title=segmented_dim,
        yaxis_title=f"Number of {segmented_aggr}",
    )
    
    st.plotly_chart(fig_map)
    st.plotly_chart(fig_hist)

with col2:
    
    with st.container(height=1050):

        fig_bar = px.bar(
        df_filtered,
        x=segmented_dim_value,
        y=segmented_aggr_value,
        orientation="h",
        color=segmented_dim_value,
        color_continuous_scale='tempo',
        title=f"Ranking by {segmented_aggr}"
        )
            
        fig_bar.update_layout(
            yaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1
            ),  
            height=max(300, len(df_filtered[segmented_dim_value].unique()) * 30),
            xaxis_title=segmented_dim,
            yaxis_title=segmented_aggr,
        )
        
        fig_bar.update_coloraxes(showscale=False)
        fig_bar.update_xaxes(side="top")
        
        st.plotly_chart(fig_bar)
    
# Similar to tabular data above, display a cool table with df_filtered and all segmented dim available, ordered by segmented_dim_value from highest to lowest, reindexed from 1 (highest) to n (lowest)

st.write("### Detailed Data")
st.dataframe(df_filtered.sort_values(segmented_dim_value, ascending=False).reset_index(drop=True).rename(index=lambda x: x + 1))
