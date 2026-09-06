import requests
import pandas as pd
from pathlib import Path


def fetch_world_bank_indicator(
    country_code,
    indicator_code,
    start_year=2000,
    end_year=2025
):
    url = (
        f"https://api.worldbank.org/v2/country/"
        f"{country_code}/indicator/{indicator_code}"
    )

    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 1000
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    observations = data[1]

    records = []

    for observation in observations:
        records.append(
            {
                "country": observation["country"]["value"],
                "country_code": country_code,
                "indicator": observation["indicator"]["value"],
                "indicator_code": indicator_code,
                "year": int(observation["date"]),
                "value": observation["value"]
            }
        )

    dataframe = pd.DataFrame(records)

    return dataframe


if __name__ == "__main__":

    df = fetch_world_bank_indicator(
        country_code="TGO",
        indicator_code="NY.GDP.MKTP.CD"
    )

    output_directory = Path("data/raw")
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "togo_gdp.csv"

    df.to_csv(output_file, index=False)

    print(df.head())
    print()
    print(f"Saved {len(df)} rows to {output_file}")