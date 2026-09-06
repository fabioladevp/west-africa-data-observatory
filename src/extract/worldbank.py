import requests
import pandas as pd
from pathlib import Path


COUNTRIES = {
    "TGO": "Togo",
    "GHA": "Ghana",
    "BEN": "Benin",
    "CIV": "Cote d'Ivoire"
}


INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP",
    "NY.GDP.PCAP.CD": "GDP per capita",
    "SP.POP.TOTL": "Population",
    "NV.AGR.TOTL.ZS": "Agriculture value added (% GDP)",
    "FP.CPI.TOTL.ZG": "Inflation"
}


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

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if len(data) < 2 or data[1] is None:
        return pd.DataFrame()

    records = []

    for observation in data[1]:
        records.append(
            {
                "country": observation["country"]["value"],
                "country_code": country_code,
                "indicator": INDICATORS[indicator_code],
                "indicator_code": indicator_code,
                "year": int(observation["date"]),
                "value": observation["value"]
            }
        )

    return pd.DataFrame(records)


def fetch_all_data():

    all_dataframes = []

    for country_code, country_name in COUNTRIES.items():

        print(f"\nFetching data for {country_name}...")

        for indicator_code, indicator_name in INDICATORS.items():

            print(f"  -> {indicator_name}")

            df = fetch_world_bank_indicator(
                country_code=country_code,
                indicator_code=indicator_code
            )

            all_dataframes.append(df)

    final_dataframe = pd.concat(
        all_dataframes,
        ignore_index=True
    )

    return final_dataframe


if __name__ == "__main__":

    df = fetch_all_data()

    output_directory = Path("data/raw")
    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "worldbank_indicators.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\n-----------------------------")
    print("EXTRACTION COMPLETE")
    print("-----------------------------")

    print(f"Rows: {len(df)}")

    print(
        f"Countries: "
        f"{df['country'].nunique()}"
    )

    print(
        f"Indicators: "
        f"{df['indicator'].nunique()}"
    )

    print(
        f"Years: "
        f"{df['year'].min()} - "
        f"{df['year'].max()}"
    )

    print(
        f"\nSaved to: {output_file}"
    )