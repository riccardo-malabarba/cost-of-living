import pandas as pd
import streamlit as st
import plotly.express as px

eu_data = pd.read_csv('dataset/data_raw.csv')

st.header("Choose Your Country")
page_context = "a comparison of monthly budgets between different cities of a country"

col1, col2, col3, col4 = st.columns(4)
    
with col1:
    # Single-select for household type
    household_type = st.selectbox("Household Type", ["Single", "Couple", "Family"])

with col2:
    # Single-select for lifestyle
    lifestyle = st.selectbox("Lifestyle", ["Frugal", "Moderate", "Luxurious"])

with col3:
    # Single-select for monthly net salary
    custom_salary = st.number_input("Monthly Net Salary", min_value=0.0, value=None, placeholder="Optional")

# Single-select for country and reference country
country = st.selectbox("Select Country", list(eu_data['country'].unique()))
reference_country = st.selectbox("Select Reference Country for Comparison", list(eu_data['country'].unique()))

st.subheader("Monthly Budget Comparison")
fig = px.sunburst(eu_data,
                    path=['country', 'macro_category', 'category'],
                    values='value_column',  # Replace with actual value column
                    title='Monthly Budget Distribution',
                    color_continuous_scale='RdBu')
st.plotly_chart(fig)

# Generate summary and fun fact based on the filtered data
filtered_data = eu_data[eu_data['country'] == country]
st.sidebar.write("### Summary")
st.sidebar.write(generate_summary(filtered_data.to_string()))

st.sidebar.write("### Fun Fact")
if st.sidebar.button("Generate New Fun Fact"):
    st.sidebar.write(generate_fun_fact(filtered_data.to_string(), page_context))

# Price Distribution Page
elif page == "Price Distribution":
st.header("Price Distribution")

# Single-select for country and reference country
country = st.selectbox("Select Country", list(eu_data['country'].unique()))
reference_country = st.selectbox("Select Reference Country for Comparison", list(eu_data['country'].unique()))

# Single-select for macro-category and category
macro_category = st.selectbox("Select Macro-Category", ["Food and Non-Alcoholic Beverages", "Alcoholic Beverages and Tobacco", "Clothing and Footwear", "Housing", "Transportation", "Utilities and Internet", "Sports and Leisure", "Education", "Health", "Restaurants and Hotels", "Miscellaneous Goods and Services"])
category = st.selectbox("Select Category", list(eu_data.columns[2:-3]))  # Adjust based on actual columns

st.subheader("Ridgeline Plot of Average Prices per Macro-Categories")

fig = px.density_contour(eu_data,
                            x='value_column',  # Replace with actual value column
                            y='macro_category',
                            color='country',
                            title='Ridgeline Plot of Average Prices per Macro-Categories',
                            color_continuous_scale='Viridis')

# Generate summary and fun fact based on the filtered data
filtered_data = eu_data[eu_data['country'] == country]
st.sidebar.write("### Summary")
st.sidebar.write(generate_summary(filtered_data.to_string()))

st.sidebar.write("### Fun Fact")
if st.sidebar.button("Generate New Fun Fact"):
    st.sidebar.write(generate_fun_fact(filtered_data.to_string()))

# Price Correlation Page
elif page == "Price Correlation":
st.header("Price Correlation")

# Single-select for macro-category and category
macro_category_1 = st.selectbox("Select Macro-Category 1", ["Food and Non-Alcoholic Beverages", "Alcoholic Beverages and Tobacco", "Clothing and Footwear", "Housing", "Transportation", "Utilities and Internet", "Sports and Leisure", "Education", "Health", "Restaurants and Hotels", "Miscellaneous Goods and Services"])
category_1 = st.selectbox("Select Category 1", list(eu_data.columns[2:-3]))  # Adjust based on actual columns

macro_category_2 = st.selectbox("Select Macro-Category 2", ["Food and Non-Alcoholic Beverages", "Alcoholic Beverages and Tobacco", "Clothing and Footwear", "Housing", "Transportation", "Utilities and Internet", "Sports and Leisure", "Education", "Health", "Restaurants and Hotels", "Miscellaneous Goods and Services"])
category_2 = st.selectbox("Select Category 2", list(eu_data.columns[2:-3]))  # Adjust based on actual columns

st.subheader("Scatter Plot of Category 2 vs Category 1")
fig = px.scatter(eu_data,
                    x=category_1,
                    y=category_2,
                    color='country',
                    title=f'Scatter Plot of {category_2} vs {category_1}',
                    trendline='ols')

st.sidebar.write("### Summary")
st.sidebar.write(generate_summary(eu_data.to_string()))

st.sidebar.write("### Fun Fact")
if st.sidebar.button("Generate New Fun Fact"):
    st.sidebar.write(generate_fun_fact(eu_data.to_string()))
