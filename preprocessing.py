import pandas as pd

FILEPATH_COST_OF_LIVING = 'dataset/global-cost-of-living.csv'
FILEPATH_EARNINGS = 'dataset/eu_annual_net_salary.csv'
EU_COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
    "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
    "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden"
]

# Load the uploaded CSV files
df_cost_of_living = pd.read_csv(FILEPATH_COST_OF_LIVING)
annual_net_earnings_data = pd.read_csv(FILEPATH_EARNINGS)

# Filter the dataset for European countries
df_cost_of_living = df_cost_of_living[df_cost_of_living['country'].isin(EU_COUNTRIES)]

# Define the new column names with descriptive category names
new_column_names = {
    'x1': 'Meal_InexpensiveRestaurant',
    'x2': 'Meal_MidRangeRestaurant',
    'x3': 'McMeal_McDonalds',
    'x4': 'DomesticBeer_Restaurant',
    'x5': 'ImportedBeer_Restaurant',
    'x6': 'Cappuccino_Restaurant',
    'x7': 'CokePepsi_Restaurant',
    'x8': 'Water_Restaurant',
    'x9': 'Milk',
    'x10': 'LoafOfBread',
    'x11': 'Rice',
    'x12': 'Eggs',
    'x13': 'LocalCheese',
    'x14': 'ChickenFillets',
    'x15': 'BeefRound',
    'x16': 'Apples',
    'x17': 'Banana',
    'x18': 'Oranges',
    'x19': 'Tomato',
    'x20': 'Potato',
    'x21': 'Onion',
    'x22': 'Lettuce',
    'x23': 'Water_Market',
    'x24': 'Wine_MidRange',
    'x25': 'DomesticBeer_Market',
    'x26': 'ImportedBeer_Market',
    'x27': 'Cigarettes',
    'x28': 'OneWayTicket_LocalTransport',
    'x29': 'MonthlyPass_RegularPrice',
    'x30': 'TaxiStart',
    'x31': 'Taxi1km',
    'x32': 'Taxi1hourWaiting',
    'x33': 'Gasoline',
    'x34': 'VolkswagenGolf',
    'x35': 'ToyotaCorolla',
    'x36': 'Utilities_Monthly',
    'x37': 'MobileTariff_Local',
    'x38': 'Internet',
    'x39': 'FitnessClub_Monthly',
    'x40': 'TennisCourtRent',
    'x41': 'Cinema_InternationalRelease',
    'x42': 'Preschool_Monthly',
    'x43': 'InternationalPrimarySchool_Yearly',
    'x44': 'Jeans',
    'x45': 'SummerDress',
    'x46': 'NikeRunningShoes',
    'x47': 'MenLeatherShoes',
    'x48': 'Apartment1Bedroom_CityCentre',
    'x49': 'Apartment1Bedroom_OutsideCentre',
    'x50': 'Apartment3Bedrooms_CityCentre',
    'x51': 'Apartment3Bedrooms_OutsideCentre',
    'x52': 'PricePerSquareMeter_CityCentre',
    'x53': 'PricePerSquareMeter_OutsideCentre',
    'x54': 'AverageMonthlyNetSalary',
    'x55': 'MortgageInterestRate'
}

# Rename the columns
df_cost_of_living.rename(columns=new_column_names, inplace=True)

# Add macro-categories
macro_categories = {
    'Food and Non-Alcoholic Beverages': [
        'Meal_InexpensiveRestaurant', 'Meal_MidRangeRestaurant', 'McMeal_McDonalds',
        'Cappuccino_Restaurant', 'CokePepsi_Restaurant', 'Water_Restaurant',
        'Milk', 'LoafOfBread', 'Rice', 'Eggs', 'LocalCheese', 'ChickenFillets',
        'BeefRound', 'Apples', 'Banana', 'Oranges', 'Tomato', 'Potato', 'Onion',
        'Lettuce', 'Water_Market'
    ],
    'Alcoholic Beverages and Tobacco': [
        'DomesticBeer_Restaurant', 'ImportedBeer_Restaurant', 'DomesticBeer_Market',
        'ImportedBeer_Market', 'Wine_MidRange', 'Cigarettes'
    ],
    'Transportation': [
        'OneWayTicket_LocalTransport', 'MonthlyPass_RegularPrice', 'TaxiStart',
        'Taxi1km', 'Taxi1hourWaiting', 'Gasoline', 'VolkswagenGolf', 'ToyotaCorolla'
    ],
    'Utilities and Internet': [
        'Utilities_Monthly', 'MobileTariff_Local', 'Internet'
    ],
    'Sports and Leisure': [
        'FitnessClub_Monthly', 'TennisCourtRent', 'Cinema_InternationalRelease'
    ],
    'Education': [
        'Preschool_Monthly', 'InternationalPrimarySchool_Yearly'
    ],
    'Clothing and Footwear': [
        'Jeans', 'SummerDress', 'NikeRunningShoes', 'MenLeatherShoes'
    ],
    'Housing': [
        'Apartment1Bedroom_CityCentre', 'Apartment1Bedroom_OutsideCentre',
        'Apartment3Bedrooms_CityCentre', 'Apartment3Bedrooms_OutsideCentre',
        'PricePerSquareMeter_CityCentre', 'PricePerSquareMeter_OutsideCentre'
    ],
    'Salary and Finance': [
        'AverageMonthlyNetSalary', 'MortgageInterestRate'
    ]
}

# Define the conversion rate
usd_to_eur_rate = 1.0824

# Convert prices from USD to EUR
for column in df_cost_of_living.columns[2:]:  # Skip 'city' and 'country' columns
    if df_cost_of_living[column].dtype == float:  # Only convert numeric columns
        df_cost_of_living[column] = df_cost_of_living[column] / usd_to_eur_rate

# Filter the annual net earnings dataset for the year 2024 and EU countries
annual_net_earnings_2024 = annual_net_earnings_data[
    (annual_net_earnings_data['TIME_PERIOD'] == 2024) &
    (annual_net_earnings_data['Geopolitical entity (reporting)'].isin(EU_COUNTRIES))
]

# Simplify the annual net earnings dataset
annual_net_earnings_2024_simplified = annual_net_earnings_2024[['Geopolitical entity (reporting)', 'OBS_VALUE']]
annual_net_earnings_2024_simplified.columns = ['country', 'AnnualNetEarnings']
annual_net_earnings_2024_simplified['MonthlyNetEarnings'] = annual_net_earnings_2024_simplified['AnnualNetEarnings'] / 12

# Merge the datasets on the 'country' column
eu_data = pd.merge(df_cost_of_living, annual_net_earnings_2024_simplified, on='country', how='right')

# Display the first few rows of the dataset with the new column
eu_data.to_csv('dataset/eu_data.csv')