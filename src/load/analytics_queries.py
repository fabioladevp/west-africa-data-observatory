import pandas as pd

from src.load.database import engine


# --------------------------------------------------
# 1. Latest GDP ranking
# --------------------------------------------------

gdp_query = """
SELECT
    c.country_name AS country,
    y.year,
    f.value AS gdp_usd
FROM fact_indicator_value f

JOIN dim_country c
    ON f.country_id = c.country_id

JOIN dim_indicator i
    ON f.indicator_id = i.indicator_id

JOIN dim_year y
    ON f.year_id = y.year_id

WHERE i.indicator_code = 'NY.GDP.MKTP.CD'

AND y.year = (
    SELECT MAX(y2.year)
    FROM fact_indicator_value f2

    JOIN dim_indicator i2
        ON f2.indicator_id = i2.indicator_id

    JOIN dim_year y2
        ON f2.year_id = y2.year_id

    WHERE i2.indicator_code = 'NY.GDP.MKTP.CD'
)

ORDER BY gdp_usd DESC;
"""


# --------------------------------------------------
# 2. Latest GDP per capita ranking
# --------------------------------------------------

gdp_per_capita_query = """
SELECT
    c.country_name AS country,
    y.year,
    f.value AS gdp_per_capita_usd
FROM fact_indicator_value f

JOIN dim_country c
    ON f.country_id = c.country_id

JOIN dim_indicator i
    ON f.indicator_id = i.indicator_id

JOIN dim_year y
    ON f.year_id = y.year_id

WHERE i.indicator_code = 'NY.GDP.PCAP.CD'

AND y.year = (
    SELECT MAX(y2.year)
    FROM fact_indicator_value f2

    JOIN dim_indicator i2
        ON f2.indicator_id = i2.indicator_id

    JOIN dim_year y2
        ON f2.year_id = y2.year_id

    WHERE
        i2.indicator_code = 'NY.GDP.PCAP.CD'
        AND f2.value IS NOT NULL
)

ORDER BY gdp_per_capita_usd DESC;
"""


# --------------------------------------------------
# 3. Agriculture ranking
# --------------------------------------------------

agriculture_query = """
SELECT
    c.country_name AS country,
    y.year,
    f.value AS agriculture_pct_gdp
FROM fact_indicator_value f

JOIN dim_country c
    ON f.country_id = c.country_id

JOIN dim_indicator i
    ON f.indicator_id = i.indicator_id

JOIN dim_year y
    ON f.year_id = y.year_id

WHERE i.indicator_code = 'NV.AGR.TOTL.ZS'

AND y.year = (
    SELECT MAX(y2.year)
    FROM fact_indicator_value f2

    JOIN dim_indicator i2
        ON f2.indicator_id = i2.indicator_id

    JOIN dim_year y2
        ON f2.year_id = y2.year_id

    WHERE
        i2.indicator_code = 'NV.AGR.TOTL.ZS'
        AND f2.value IS NOT NULL
)

ORDER BY agriculture_pct_gdp DESC;
"""


# --------------------------------------------------
# Execute queries
# --------------------------------------------------

print("\n================================")
print("WEST AFRICA DATA OBSERVATORY")
print("SQL ANALYTICS")
print("================================")


gdp_df = pd.read_sql(
    gdp_query,
    engine
)

print("\n--- LATEST GDP RANKING ---")
print(
    gdp_df.to_string(
        index=False
    )
)


gdp_pc_df = pd.read_sql(
    gdp_per_capita_query,
    engine
)

print("\n--- LATEST GDP PER CAPITA RANKING ---")
print(
    gdp_pc_df.to_string(
        index=False
    )
)


agriculture_df = pd.read_sql(
    agriculture_query,
    engine
)

print("\n--- LATEST AGRICULTURE SHARE RANKING ---")
print(
    agriculture_df.to_string(
        index=False
    )
)