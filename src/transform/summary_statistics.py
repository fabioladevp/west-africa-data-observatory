import pandas as pd


df = pd.read_csv(
    "data/processed/worldbank_analytics.csv"
)


latest_year = df["year"].max()

latest_data = df[
    df["year"] == latest_year
].copy()


print("\n==============================")
print("WEST AFRICA DATA OBSERVATORY")
print("==============================")

print(f"\nLatest year in dataset: {latest_year}")


print("\n--- GDP ---")

gdp_ranking = latest_data[
    ["country", "gdp_usd"]
].sort_values(
    "gdp_usd",
    ascending=False
)

print(gdp_ranking.to_string(index=False))


print("\n--- GDP PER CAPITA ---")

gdp_pc_ranking = latest_data[
    ["country", "gdp_per_capita_usd"]
].sort_values(
    "gdp_per_capita_usd",
    ascending=False
)

print(gdp_pc_ranking.to_string(index=False))


print("\n--- POPULATION ---")

population_ranking = latest_data[
    ["country", "population"]
].sort_values(
    "population",
    ascending=False
)

print(population_ranking.to_string(index=False))


print("\n--- AGRICULTURE (% GDP) ---")

agriculture_ranking = latest_data[
    ["country", "agriculture_pct_gdp"]
].sort_values(
    "agriculture_pct_gdp",
    ascending=False
)

print(agriculture_ranking.to_string(index=False))