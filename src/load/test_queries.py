import pandas as pd

from database import engine


query = """
SELECT
    c.country_name,
    y.year,
    i.indicator_name,
    f.value

FROM fact_indicator_value f

JOIN dim_country c
    ON f.country_id = c.country_id

JOIN dim_indicator i
    ON f.indicator_id = i.indicator_id

JOIN dim_year y
    ON f.year_id = y.year_id

WHERE
    c.country_code = 'TGO'

AND
    i.indicator_code = 'NY.GDP.MKTP.CD'

ORDER BY
    y.year DESC

LIMIT 10;
"""


df = pd.read_sql(
    query,
    engine
)


print("\n-----------------------------")
print("DATABASE QUERY TEST")
print("-----------------------------")

print(df.to_string(index=False))