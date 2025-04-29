import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('dataset/data_proc.csv')
df_filtered = df.copy()

st.header("Cost of Living Map 🗺️")

col1, col2 = st.columns([0.5, 0.5], gap="large")

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

with col1:
    segmented_dim = st.pills(label="What do you want to analyze?", options=segmented_dim_options.keys(), default=list(segmented_dim_options.keys())[0])
    segmented_dim_value = segmented_dim_options[segmented_dim]

with col2:
    slider_range_default= [df_filtered[segmented_dim_value].min(), df_filtered[segmented_dim_value].max()]
    slider_range = st.slider("Range", min_value=slider_range_default[0], max_value=slider_range_default[1], value=(slider_range_default[0], slider_range_default[1]), step=1.0)

col3, col4 = st.columns([0.5, 0.5], gap="large")

with col3:
    segmented_aggr = st.segmented_control(label="Choose one option", options=segmented_aggr_options.keys(), default=list(segmented_aggr_options.keys())[0])
    segmented_aggr_value = segmented_aggr_options[segmented_aggr]

with col4:
    multiselect_filter = st.multiselect("Filter by Country", list(df.sort_values("country")["country"].unique()), placeholder="Optional")
    if multiselect_filter:
        df_filtered = df_filtered[df_filtered["country"].isin(multiselect_filter)]
    else:
        df_filtered = df.copy() 

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

# Tabs for average monthly savings
tab1, tab2 = st.tabs([":material/map: Map", ":material/sort: Rank"])

with tab1:
    
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
            projection="natural earth"
        )
        
    fig_hist = px.histogram(
        df_filtered,
        x=segmented_dim_value,
        title='Distribution of Monthly Savings',
        nbins=20,
        marginal='box',
        histfunc="avg",
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
    fig_map.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    
    st.plotly_chart(fig_map)
    st.plotly_chart(fig_hist)

with tab2:

    fig_bar = px.bar(
        df_filtered,
        x=segmented_dim_value,
        y=segmented_aggr_value,
        orientation="h",
        # title='Average Monthly Savings by Country',
        color=segmented_dim_value,
        color_continuous_scale='tempo',
    )
        
    fig_bar.update_layout(
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        height=max(300, len(df_filtered[segmented_dim_value].unique()) * 30),
    )
    
    # hide the colorscale legent and put the x axis on top
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_xaxes(side="top")
    

    st.plotly_chart(fig_bar)
    
st.write("### Tabular Data")
st.write(df_filtered[[segmented_aggr_value, segmented_dim_value]].reindex(index=df_filtered.index[::-1]))
