import requests
import pandas as pd

# Standardizes currency to USD values so that we can better compare results
def format_currency(dataset):
  url = "https://api.exchangerate-api.com/v4/latest/USD"

  # Requests data from API
  response = requests.get(url)
  data = response.json()
  
  def convert_currency(row):
    rate = data["rates"][row["Unit Code"]]
    return row["Value"] / rate

  for index, row in dataset.iterrows():
    dataset.at[index,"Unit Code"] = "USD"
    dataset.at[index,"Value"] = convert_currency(row)
  return dataset


# Pandas dataframes
wage = pd.read_csv("wage.csv", delimiter = ",")
happiness = pd.read_csv("happiness.csv", delimiter = ",")

#pass the wage data to be converted to USD
wage_usd = format_currency(wage)

#merge the wage and happiness data into one dataframe
wage_and_happiness = wage.merge(happiness)

#group the data by country
wage_and_happiness_by_country = wage_and_happiness.groupby("Country")

