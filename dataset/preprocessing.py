import logging
import pandas as pd
from geopy.geocoders import Nominatim

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
pd.options.plotting.backend = "plotly"

FILEPATH_PRICES_RAW = "dataset/prices_raw.csv"
FILEPATH_PRICES_PROCESSED = "dataset/prices_processed.csv"
FILEPATH_BUDGET_PROCESSED = "dataset/budget_processed.csv"

EU_COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
    "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
    "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden"
]
# Column	Description
# city	Name of the city
# country	Name of the country
# x1	Meal, Inexpensive Restaurant (USD)
# x2	Meal for 2 People, Mid-range Restaurant, Three-course (USD)
# x3	McMeal at McDonalds (or Equivalent Combo Meal) (USD)
# x4	Domestic Beer (0.5 liter draught, in restaurants) (USD)
# x5	Imported Beer (0.33 liter bottle, in restaurants) (USD)
# x6	Cappuccino (regular, in restaurants) (USD)
# x7	Coke/Pepsi (0.33 liter bottle, in restaurants) (USD)
# x8	Water (0.33 liter bottle, in restaurants) (USD)
# x9	Milk (regular), (1 liter) (USD)
# x10	Loaf of Fresh White Bread (500g) (USD)
# x11	Rice (white), (1kg) (USD)
# x12	Eggs (regular) (12) (USD)
# x13	Local Cheese (1kg) (USD)
# x14	Chicken Fillets (1kg) (USD)
# x15	Beef Round (1kg) (or Equivalent Back Leg Red Meat) (USD)
# x16	Apples (1kg) (USD)
# x17	Banana (1kg) (USD)
# x18	Oranges (1kg) (USD)
# x19	Tomato (1kg) (USD)
# x20	Potato (1kg) (USD)
# x21	Onion (1kg) (USD)
# x22	Lettuce (1 head) (USD)
# x23	Water (1.5 liter bottle, at the market) (USD)
# x24	Bottle of Wine (Mid-Range, at the market) (USD)
# x25	Domestic Beer (0.5 liter bottle, at the market) (USD)
# x26	Imported Beer (0.33 liter bottle, at the market) (USD)
# x27	Cigarettes 20 Pack (Marlboro) (USD)
# x28	One-way Ticket (Local Transport) (USD)
# x29	Monthly Pass (Regular Price) (USD)
# x30	Taxi Start (Normal Tariff) (USD)
# x31	Taxi 1km (Normal Tariff) (USD)
# x32	Taxi 1hour Waiting (Normal Tariff) (USD)
# x33	Gasoline (1 liter) (USD)
# x34	Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car) (USD)
# x35	Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car) (USD)
# x36	Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment (USD)
# x37	1 min. of Prepaid Mobile Tariff Local (No Discounts or Plans) (USD)
# x38	Internet (60 Mbps or More, Unlimited Data, Cable/ADSL) (USD)
# x39	Fitness Club, Monthly Fee for 1 Adult (USD)
# x40	Tennis Court Rent (1 Hour on Weekend) (USD)
# x41	Cinema, International Release, 1 Seat (USD)
# x42	Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child (USD)
# x43	International Primary School, Yearly for 1 Child (USD)
# x44	1 Pair of Jeans (Levis 501 Or Similar) (USD)
# x45	1 Summer Dress in a Chain Store (Zara, H&M, …) (USD)
# x46	1 Pair of Nike Running Shoes (Mid-Range) (USD)
# x47	1 Pair of Men Leather Business Shoes (USD)
# x48	Apartment (1 bedroom) in City Centre (USD)
# x49	Apartment (1 bedroom) Outside of Centre (USD)
# x50	Apartment (3 bedrooms) in City Centre (USD)
# x51	Apartment (3 bedrooms) Outside of Centre (USD)
# x52	Price per Square Meter to Buy Apartment in City Centre (USD)
# x53	Price per Square Meter to Buy Apartment Outside of Centre (USD)
# x54	Average Monthly Net Salary (After Tax) (USD)
# x55	Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate
# data_quality	0 if Numbeo considers that more contributors are needed to increase data quality, else 1
# create a dictionary to rename the columns as seen above, withouut (USD)

NEW_COLUMN_NAMES = {
    "x1": "Meal_InexpensiveRestaurant",
    "x2": "Meal_MidRangeRestaurant",
    "x3": "McMeal_McDonalds",
    "x4": "DomesticBeer_Restaurant",
    "x5": "ImportedBeer_Restaurant",
    "x6": "Cappuccino_Restaurant",
    "x7": "CokePepsi_Restaurant",
    "x8": "Water_Restaurant",
    "x9": "Milk",
    "x10": "LoafOfBread",
    "x11": "Rice",
    "x12": "Eggs",
    "x13": "LocalCheese",
    "x14": "ChickenFillets",
    "x15": "BeefRound",
    "x16": "Apples",
    "x17": "Banana",
    "x18": "Oranges",
    "x19": "Tomato",
    "x20": "Potato",
    "x21": "Onion",
    "x22": "Lettuce",
    "x23": "Water_Market",
    "x24": "Wine_MidRange",
    "x25": "DomesticBeer_Market",
    "x26": "ImportedBeer_Market",
    "x27": "Cigarettes",
    "x28": "OneWayTicket_LocalTransport",
    "x29": "MonthlyPass_RegularPrice",
    "x30": "TaxiStart",
    "x31": "Taxi1km",
    "x32": "Taxi1hourWaiting",
    "x33": "Gasoline",
    "x34": "VolkswagenGolf",
    "x35": "ToyotaCorolla",
    "x36": "Utilities_Monthly",
    "x37": "MobileTariff_Local",
    "x38": "Internet",
    "x39": "FitnessClub_Monthly",
    "x40": "TennisCourtRent",
    "x41": "Cinema_InternationalRelease",
    "x42": "Preschool_Monthly",
    "x43": "InternationalPrimarySchool_Yearly",
    "x44": "Jeans",
    "x45": "SummerDress",
    "x46": "NikeRunningShoes",
    "x47": "MenLeatherShoes",
    "x48": "Apartment1Bedroom_CityCentre",
    "x49": "Apartment1Bedroom_OutsideCentre",
    "x50": "Apartment3Bedrooms_CityCentre",
    "x51": "Apartment3Bedrooms_OutsideCentre",
    "x52": "PricePerSquareMeter_CityCentre",
    "x53": "PricePerSquareMeter_OutsideCentre",
    "x54": "AverageMonthlyNetSalary",
    "x55": "MortgageInterestRate"
}
USD_TO_EUR_RATE = 1.0824
BUDGET_DEFAULT = {
    "Salary": "Average", # ("Average", "Custom")
    "Salary Custom": 0,
    "Other Income": 0,
    "Meals Out (Cheap)": 4,
    "Meals Out (Expensive)": 2,
    "Grocery Shopping": 4,
    "Clothes Shopping": "Low", # ("Low", "Medium", "High")
    "Transport": "Public", # ("Public", "Private", Taxi)
    "Social Beers": 10,
    "Fitness Club": True,
    "Cinemas": 2,
    "Padel Matches": 2,
    "Rent": "Suburbs", # ("Suburbs", "Center", "Custom")
    "Rent Custom": 0,
    "Other Expenses": 0,
}

def estimate_monthly_budget(row, budget_default=BUDGET_DEFAULT):
    salary = budget_default["Salary Custom"] if budget_default["Salary"] == "Custom" else row["AverageMonthlyNetSalary"]
    other_income =  budget_default["Other Income"]
    total_income =  salary + other_income
    
    meals_out = budget_default["Meals Out (Cheap)"] * row["Meal_InexpensiveRestaurant"] + \
        budget_default["Meals Out (Expensive)"] * row["Meal_MidRangeRestaurant"] / 2
    groceries = budget_default["Grocery Shopping"] * (
        row["Milk"] + row["LoafOfBread"] + row["Rice"] + row["Eggs"] + row["LocalCheese"] +
        row["ChickenFillets"] + row["BeefRound"] + row["Apples"] + row["Banana"] + row["Oranges"] +
        row["Tomato"] + row["Potato"] + row["Onion"] + row["Lettuce"] + row["Water_Market"] + row["Wine_MidRange"]
    )
    
    social = budget_default["Social Beers"] * (row["DomesticBeer_Market"] + row["ImportedBeer_Market"]) / 2
    
    if budget_default["Transport"] == "Public":
        transportation = row["MonthlyPass_RegularPrice"]
    elif budget_default["Transport"] == "Private":
        transportation = row["Gasoline"] * 40
    else:
        transportation = row["TaxiStart"] * 20 + row["Taxi1km"] * 100
        
    household = row["Utilities_Monthly"]
    internet = row["Internet"] 
    leisure = budget_default["Cinemas"] * row["Cinema_InternationalRelease"] + budget_default["Social Beers"] * (row["DomesticBeer_Restaurant"] + row["ImportedBeer_Restaurant"]) / 2
    sports = (budget_default["Fitness Club"] * row["FitnessClub_Monthly"] if budget_default["Fitness Club"] else 0) + budget_default["Padel Matches"] * row["TennisCourtRent"]
    
    if budget_default["Clothes Shopping"] == "Low":
        clothing = (row["Jeans"] + row["SummerDress"] + row["NikeRunningShoes"] + row["MenLeatherShoes"]) / 12
    elif budget_default["Clothes Shopping"] == "Medium":
        clothing = (row["Jeans"] + row["SummerDress"] + row["NikeRunningShoes"] + row["MenLeatherShoes"]) / 6
    else:
        clothing = (row["Jeans"] + row["SummerDress"] + row["NikeRunningShoes"] + row["MenLeatherShoes"]) / 3
        
    # rent
    if budget_default["Rent"] == "Suburbs":
        rent = row["Apartment1Bedroom_OutsideCentre"]
    elif budget_default["Rent"] == "Center":
        rent = row["Apartment1Bedroom_CityCentre"]
    else:
        rent = budget_default["Rent Custom"]
    
    other_expenses = budget_default["Other Expenses"]
    
    total_expenses = meals_out + groceries + clothing + social + transportation + household + internet + leisure + sports + rent + other_expenses
    total_income = (budget_default["Salary Custom"] if budget_default["Salary"] == "Custom" else row["AverageMonthlyNetSalary"]) + budget_default["Other Income"]
    
    monthly_savings = total_income - total_expenses
    
    if monthly_savings < 0:
        monthly_savings = 0
    
    savings_to_income_ratio = (monthly_savings / total_income) * 100 if total_income != 0 else 0
    expenses_to_income_ratio = (total_expenses / total_income) * 100 if total_income != 0 else 0
    rent_to_income_ratio = (rent / total_income) * 100 if total_income != 0 else 0
        
    return {
        "Monthly Salary": salary,
        "Other Monthly Income": other_income,
        "Total Monthly Income": total_income,
        "Meals Out": meals_out,
        "Groceries": groceries,
        "Clothing": clothing,
        "Transportation": transportation,
        "Household": household,
        "Internet": internet,
        "Leisure": leisure,
        "Sports": sports,
        "Rent": rent,
        "Other Monthly Expenses": other_expenses,
        "Total Monthly Expenses": total_expenses,
        "Monthly Savings": monthly_savings,
        "Monthly Savings over Income": savings_to_income_ratio,
        "Montly Expenses over Income":  expenses_to_income_ratio,
        "Montlhy Rent over Income": rent_to_income_ratio
    }

def process_df(df: pd.DataFrame):
    
    df = df.dropna()
    df = df[df["country"].isin(EU_COUNTRIES)]
    df = df[df["data_quality"] == 1]
    df = df.rename(columns=NEW_COLUMN_NAMES)

    logging.info(df.describe())

    # Convert prices from USD to EUR
    for column in df.columns: 
        if df[column].dtype == float:
            df[column] = df[column] / USD_TO_EUR_RATE

    # Add Geo Info
    geolocator = Nominatim(user_agent="city_coordinates_app")

    def get_geo_info(suburb, country):
        try:
            # Geocode using suburb and country
            location = geolocator.geocode(f"{suburb}, {country}", exactly_one=True, timeout=10)

            if location:
                # Extract city and country code from the address components
                location_reversed = geolocator.reverse(f"{location.latitude},{location.longitude}", language="en", timeout=10)
                address_components = location_reversed.raw.get("address")
                city = address_components.get("city") or suburb
                country_check = address_components.get("country")
                country_code = address_components.get("country_code")
                if country_check.lower() != country.lower():
                    if country_check == "Czechia" and country == "Czech Republic":
                        pass
                    else:
                        logging.warning(f"Wrong country {country_check} for {suburb}")
                        return None, None, None, None
                logging.info(f"Location found for {suburb}")
                if city != suburb and city:
                    logging.info(f"Updated city: from {suburb} to {city}")
                return city, country_code, location.latitude, location.longitude
            else:
                logging.warning(f"Location not found for {suburb}, {country}")
                return None, None, None, None
        except Exception as e:
            logging.error(f"Error geocoding {suburb}, {country}: {e}")
            return None, None, None, None

    # Apply the function to the DataFrame
    df[["city_aggr", "country_code", "Latitude", "Longitude"]] = df.apply(
        lambda row: pd.Series(get_geo_info(row["city"], row["country"])), axis=1
    )

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    numeric_cols.remove("Latitude")
    numeric_cols.remove("Longitude")

    df_numeric = df.groupby("city_aggr")[numeric_cols].mean().reset_index()
    df_non_numeric = df[df["city"] == df["city_aggr"]][["country", "city", "city_aggr", "Latitude", "Longitude"]]

    merged_df = pd.merge(df_numeric, df_non_numeric, on="city_aggr", how="left")
    merged_df = merged_df.dropna()
    
    merged_df = merged_df.drop(columns=["city"])
    merged_df = merged_df.rename(columns={"country": "Country", "city_aggr": "City"})
    
    columns = ["City", "Country", "Latitude", "Longitude"] + [col for col in merged_df.columns if col not in ["City", "Country", "Latitude", "Longitude"]]
    merged_df = merged_df[columns]
    
    df = merged_df
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].round(2)

    return df

def calculate_budget_df(df: pd.DataFrame, budget_default=BUDGET_DEFAULT):
    
    budget_columns = df.apply(estimate_monthly_budget, budget_default=budget_default, axis=1, result_type="expand")
    df = df[["City", "Country", "Latitude", "Longitude"]]    
    df = pd.concat([df, budget_columns], axis=1)

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].round(2)
            
    return df

if __name__ == "__main__":
    FULL = False
    if FULL:
        df = pd.read_csv(FILEPATH_PRICES_RAW)
        df = process_df(df)
        df.to_csv(FILEPATH_PRICES_PROCESSED, index=False)
    else:
        df = pd.read_csv(FILEPATH_PRICES_PROCESSED)
    df = calculate_budget_df(df)
    df.to_csv(FILEPATH_BUDGET_PROCESSED, index=False)
    logging.info("Done")