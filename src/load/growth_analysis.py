import pandas as pd

from src.load.database import engine


query = """
SELECT
    c.country_name AS country,

    MAX(
        CASE
            WHEN y.year = 2020 THEN f.value
        END
    ) AS gdp_2020,

    MAX(
        CASE
            WHEN y.year = 2024 THEN f.value
        END
    ) AS gdp_2024,

    (
        (
            MAX(
                CASE
                    WHEN y.year = 2024 THEN f.value
                END
            )
            -
            MAX(
                CASE
                    WHEN y.year = 2020 THEN f.value
                END
            )
        )
        /
        MAX(
            CASE
                WHEN y.year = 2020 THEN f.value
            END
        )
    ) * 100 AS growth_pct

FROM fact_indicator_value f

JOIN dim_country c
    ON f.country_id = c.country_id

JOIN dim_indicator i
    ON f.indicator_id = i.indicator_id

JOIN dim_year y
    ON f.year_id = y.year_id

WHERE
    i.indicator_code = 'NY.GDP.MKTP.CD'

AND
    y.year IN (2020, 2024)

GROUP BY
    c.country_id,
    c.country_name

HAVING
    gdp_2020 IS NOT NULL
    AND gdp_2024 IS NOT NULL

ORDER BY
    growth_pct DESC;
"""


df = pd.read_sql(
    query,
    engine
)


# Make the output easier to read

df["gdp_2020_billion"] = (
    df["gdp_2020"] / 1_000_000_000
)

df["gdp_2024_billion"] = (
    df["gdp_2024"] / 1_000_000_000
)


result = df[
    [
        "country",
        "gdp_2020_billion",
        "gdp_2024_billion",
        "growth_pct"
    ]
].copy()


result = result.rename(
    columns={
        "gdp_2020_billion": "GDP 2020 ($bn)",
        "gdp_2024_billion": "GDP 2024 ($bn)",
        "growth_pct": "Growth (%)"
    }
)


result["GDP 2020 ($bn)"] = (
    result["GDP 2020 ($bn)"]
    .round(2)
)

result["GDP 2024 ($bn)"] = (
    result["GDP 2024 ($bn)"]
    .round(2)
)

result["Growth (%)"] = (
    result["Growth (%)"]
    .round(2)
)


print("\n================================")
print("GDP GROWTH ANALYSIS")
print("2020 → 2024")
print("================================")

print(
    result.to_string(
        index=False
    )
)