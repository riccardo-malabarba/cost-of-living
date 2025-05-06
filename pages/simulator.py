import pandas as pd
import streamlit as st
import plotly.express as px

from dataset.preprocessing import FILEPATH_PRICES_PROCESSED, BUDGET_DEFAULT, calculate_budget_df

df = pd.read_csv(FILEPATH_PRICES_PROCESSED)

st.header("🗺️ EuroNomad Navigator")
st.write("Your EU City Cost & Budget Guide!")

df_1 = calculate_budget_df(df, BUDGET_DEFAULT)
df_2 = calculate_budget_df(df, BUDGET_DEFAULT)

# create a modal dialog to input all the info with the same structure of BUDGET DEFAULT
budget = {}

@st.dialog("Budget Configuration", width="large")
def configure_budget():
        
    with st.container():
                
        st.write("Income")
        
        col1, col2, col3 = st.columns([0.2, 0.2, 0.2], gap="medium")
        
        with col1:
            budget["Salary"] = st.selectbox("Salary", ("Average", "Custom"), index=0, key="selectbox_salary")
        
        with col2:
            if st.session_state.get("selectbox_salary") == "Custom":
                st.session_state.salary_disabled = False
            else:
                st.session_state.salary_disabled = True
            budget["Salary Custom"] = st.number_input("Custom Salary", min_value=0, value=0, step=100, disabled=st.session_state.salary_disabled)

        with col3:
            budget["Other Income"] = st.number_input("Other Income", min_value=0, value=0, step=100)
    
    with st.container():
        
        st.divider()
        
        st.write("Expenses")
        
        col1, col2, col3 = st.columns([0.2, 0.2, 0.2], gap="medium")
        
        with col1:
            budget["Meals Out (Cheap)"] = st.number_input("Meals Out (Cheap)", min_value=0, value=4, step=1)
            budget["Clothes Shopping"] = st.selectbox("Clothes Shopping", ("Low", "Medium", "High"), index=0)
            budget["Social Beers"] = st.number_input("Social Beers (monthly)", min_value=0, value=10, step=1)
            budget["Rent"] = st.selectbox("Rent", ("Suburbs", "Center", "Custom"), index=0, key="selectbox_rent")

        with col2:
            budget["Meals Out (Expensive)"] = st.number_input("Meals Out (Expensive)", min_value=0, value=2, step=1)
            budget["Transport"] = st.selectbox("Transport", ("Public", "Private", "Taxi"), index=0)
            budget["Cinemas"] = st.number_input("Cinemas (monthly)", min_value=0, value=2, step=1)
            if st.session_state.get("selectbox_rent") == "Custom":
                st.session_state.rent_disabled = False
            else:
                st.session_state.rent_disabled = True
            budget["Rent Custom"] = st.number_input("Custom Rent", min_value=0, value=0, step=50, disabled=st.session_state.rent_disabled)

        with col3:
            budget["Grocery Shopping"] = st.number_input("Grocery Shopping (monthly))", min_value=1, value=4, step=1)
            budget["Fitness Club"] = True if st.selectbox("Fitness Club", ("Yes", "No"), index=0) == "Yes" else False
            budget["Padel Matches"] = st.number_input("Padel Matches (monthly)", min_value=0, value=2, step=1)
            budget["Other Expenses"] = st.number_input("Other Expenses", min_value=0, value=0, step=100)
    
    col1, col2, col3, col4 = st.columns([0.1,0.2,0.2,0.1])
    
    with col2:
        if st.button("Save", type="primary", icon=":material/save:", use_container_width=True):
            df_1 = calculate_budget_df(df, budget)
            df_2 = calculate_budget_df(df, budget)
            st.rerun()
    
    with col3:
        if st.button("Exit", type="secondary", icon=":material/cancel:", use_container_width=True):
            st.rerun()

if st.button("Configure your monthly budget", type="primary", icon=":material/edit_square:"):
    configure_budget()

col1, col2 = st.columns([0.5, 0.5], gap="large")

with col1:
    selectbox_country_1 = st.selectbox("Select Country A", list(df.sort_values("Country")["Country"].unique()), index=None, placeholder="Select Country")
    
    if selectbox_country_1:
        df_1 = df_1[df_1["Country"]==selectbox_country_1]
    
    selectbox_city_1 = st.selectbox("Select City A", list(df_1.sort_values("City")["City"].unique()), index=None, placeholder="Select City")

    if selectbox_city_1:
        df_1 = df_1[df_1["City"]==selectbox_city_1]
    
    
with col2:
    selectbox_country_2 = st.selectbox("", list(df.sort_values("Country")["Country"].unique()), index=None, placeholder="Select Country")
    
    if selectbox_country_2:
        df_2 = df_2[df_2["Country"]==selectbox_country_2]
    
    selectbox_city_2 = st.selectbox("", list(df_2.sort_values("City")["City"].unique()), index=None, placeholder="Select City")
    
    if selectbox_city_2:
        df_2 = df_2[df_2["City"]==selectbox_city_2]
    
        
col1, col2 = st.columns([0.5, 0.5], gap="medium")

if df_1.empty:
    df_1_income = 0
    df_1_expenses = 0
    df_1_savings = 0
else:
    df_1_income = df_1["Total Monthly Income"].mean()
    df_1_expenses = df_1["Total Monthly Expenses"].mean()
    df_1_savings = df_1["Monthly Savings"].mean()

if df_2.empty:
    df_2_income = 0
    df_2_expenses = 0
    df_2_savings = 0
else:
    df_2_income = df_2["Total Monthly Income"].mean()
    df_2_expenses = df_2["Total Monthly Expenses"].mean()
    df_2_savings = df_2["Monthly Savings"].mean()

income_diff = df_1_income - df_2_income
expenses_diff = df_1_expenses - df_2_expenses
savings_diff = df_1_savings - df_2_savings


with col1:
    
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        st.metric(label="Total Monthly Income", value=f"{df_1_income:.0f} €", delta=f"{income_diff:.0f} €")
    with col_b:
        st.metric(label="Total Monthly Expenses", value=f"{df_1_expenses:.0f} €", delta=f"{expenses_diff:.0f} €")
    with col_c:
        st.metric(label="Monthly Savings", value=f"{df_1_savings:.0f} €", delta=f"{savings_diff:.0f} €")
    
    # sunburst chart to show income, and savings with a proper hierarchy to budget items
    if not df_1.empty:
        fig_sunburst_1 = px.sunburst(
            names=["Income", "Expenses", "Savings"] + [
                "Meals Out",
                "Groceries",
                "Clothing",
                "Transportation",
                "Household",
                "Internet",
                "Leisure",
                "Sports",
                "Rent",
                "Other Monthly Expenses"
            ],
            parents=["", "Income", "Income"] + ["Expenses"] * 10,
            values=[
                df_1["Total Monthly Income"].mean(),
                df_1["Total Monthly Expenses"].mean(),
                df_1["Monthly Savings"].mean()
            ] + [
                df_1["Meals Out"].mean(),
                df_1["Groceries"].mean(),
                df_1["Clothing"].mean(),
                df_1["Transportation"].mean(),
                df_1["Household"].mean(),
                df_1["Internet"].mean(),
                df_1["Leisure"].mean(),
                df_1["Sports"].mean(),
                df_1["Rent"].mean(),
                df_1["Other Monthly Expenses"].mean()
            ],
            title=f"Budget in {selectbox_city_1}"
        )
        st.plotly_chart(fig_sunburst_1, key="fig_sunburst_1")
    else:
        st.write("Select a city to see the budget")
        
    fig_sunburst_1.update_traces(
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f} €'
    )
        
    
with col2:
    
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        st.metric(label="Total Monthly Income", value=f"{df_2_income:.0f} €")
    with col_b:
        st.metric(label="Total Monthly Expenses", value=f"{df_2_expenses:.0f} €")
    with col_c:
        st.metric(label="Monthly Savings", value=f"{df_2_savings:.0f} €")
    
    if not df_2.empty:
        fig_pie_2 = px.pie(
            df_2,
            names=[
                "Meals Out",
                "Groceries",
                "Clothing",
                "Transportation",
                "Household",
                "Internet",
                "Leisure",
                "Sports",
                "Rent",
                "Other Monthly Expenses"
            ],
            values=[
                df_2["Meals Out"].mean(),
                df_2["Groceries"].mean(),
                df_2["Clothing"].mean(),
                df_2["Transportation"].mean(),
                df_2["Household"].mean(),
                df_2["Internet"].mean(),
                df_2["Leisure"].mean(),
                df_2["Sports"].mean(),
                df_2["Rent"].mean(),
                df_2["Other Monthly Expenses"].mean()
            ],
            title=f"Expenses in {selectbox_city_2}"
        )
        st.plotly_chart(fig_pie_2, key="fig_pie_2")
    else:
        st.write("Select a city to see the expenses")
