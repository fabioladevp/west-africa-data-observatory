from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.load.database import engine


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "worldbank_clean.csv"
)


# --------------------------------------------------
# Load CSV
# --------------------------------------------------

def read_worldbank_data():

    df = pd.read_csv(DATA_FILE)

    print(
        f"Loaded {len(df)} rows from CSV"
    )

    return df


# --------------------------------------------------
# Load dimensions
# --------------------------------------------------

def load_countries(connection, df):

    countries = (
        df[
            ["country_code", "country"]
        ]
        .drop_duplicates()
    )

    query = text(
        """
        INSERT INTO dim_country (
            country_code,
            country_name
        )
        VALUES (
            :country_code,
            :country_name
        )
        ON DUPLICATE KEY UPDATE
            country_name = VALUES(country_name);
        """
    )

    for _, row in countries.iterrows():

        connection.execute(
            query,
            {
                "country_code":
                    row["country_code"],

                "country_name":
                    row["country"]
            }
        )

    print(
        f"Countries loaded: {len(countries)}"
    )


def load_indicators(connection, df):

    indicators = (
        df[
            ["indicator_code", "indicator"]
        ]
        .drop_duplicates()
    )

    query = text(
        """
        INSERT INTO dim_indicator (
            indicator_code,
            indicator_name
        )
        VALUES (
            :indicator_code,
            :indicator_name
        )
        ON DUPLICATE KEY UPDATE
            indicator_name = VALUES(indicator_name);
        """
    )

    for _, row in indicators.iterrows():

        connection.execute(
            query,
            {
                "indicator_code":
                    row["indicator_code"],

                "indicator_name":
                    row["indicator"]
            }
        )

    print(
        f"Indicators loaded: {len(indicators)}"
    )


def load_years(connection, df):

    years = sorted(
        df["year"].dropna().unique()
    )

    query = text(
        """
        INSERT INTO dim_year (
            year
        )
        VALUES (
            :year
        )
        ON DUPLICATE KEY UPDATE
            year = VALUES(year);
        """
    )

    for year in years:

        connection.execute(
            query,
            {
                "year": int(year)
            }
        )

    print(
        f"Years loaded: {len(years)}"
    )


# --------------------------------------------------
# Load fact table
# --------------------------------------------------

def load_facts(connection, df):

    query = text(
        """
        INSERT INTO fact_indicator_value (
            country_id,
            indicator_id,
            year_id,
            value
        )

        SELECT
            c.country_id,
            i.indicator_id,
            y.year_id,
            :value

        FROM dim_country c
        JOIN dim_indicator i
            ON i.indicator_code = :indicator_code

        JOIN dim_year y
            ON y.year = :year

        WHERE
            c.country_code = :country_code

        ON DUPLICATE KEY UPDATE
            value = VALUES(value);
        """
    )

    count = 0

    for _, row in df.iterrows():

        value = (
            None
            if pd.isna(row["value"])
            else float(row["value"])
        )

        connection.execute(
            query,
            {
                "country_code":
                    row["country_code"],

                "indicator_code":
                    row["indicator_code"],

                "year":
                    int(row["year"]),

                "value":
                    value
            }
        )

        count += 1

    print(
        f"Facts loaded: {count}"
    )


# --------------------------------------------------
# Main ETL load
# --------------------------------------------------

def load_database():

    df = read_worldbank_data()

    print("\n-----------------------------")
    print("DATABASE LOAD")
    print("-----------------------------")

    with engine.begin() as connection:

        load_countries(
            connection,
            df
        )

        load_indicators(
            connection,
            df
        )

        load_years(
            connection,
            df
        )

        load_facts(
            connection,
            df
        )

    print()
    print("-----------------------------")
    print("LOAD COMPLETE")
    print("-----------------------------")


if __name__ == "__main__":
    load_database()