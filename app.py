from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.load.database import engine


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="West Africa Data Observatory",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.html(
    """
<style>

:root {
    --navy: #0B1F33;
    --navy-light: #183A59;
    --text: #101828;
    --muted: #667085;
    --border: #E2E8F0;
    --background: #F7F9FC;
    --surface: #FFFFFF;
}


/* ---------------------------------------------------------
   GLOBAL
--------------------------------------------------------- */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
}

.stApp {
    background-color: var(--background);
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}


/* ---------------------------------------------------------
   REMOVE STREAMLIT UI ELEMENTS
--------------------------------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0;
}

[data-testid="stDecoration"] {
    display: none;
}


/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.observatory-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 40px;

    padding-bottom: 20px;
    margin-bottom: 24px;

    border-bottom: 1px solid var(--border);
}

.observatory-brand {
    color: #38526B;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;

    margin-bottom: 7px;
}

.observatory-title {
    margin: 0;

    color: var(--navy);

    font-size: 34px;
    line-height: 1.1;

    font-weight: 650;
    letter-spacing: -0.035em;
}

.observatory-subtitle {
    max-width: 750px;

    margin-top: 10px;

    color: var(--muted);

    font-size: 14px;
    line-height: 1.6;
}

.header-meta {
    flex-shrink: 0;

    text-align: right;

    color: #64748B;

    font-size: 11px;
    line-height: 1.8;

    letter-spacing: 0.08em;
}


/* ---------------------------------------------------------
   SECTION HEADERS
--------------------------------------------------------- */

.section-header {
    margin-top: 4px;
    margin-bottom: 12px;
}

.section-kicker {
    color: #64748B;

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 0.16em;

    text-transform: uppercase;

    margin-bottom: 5px;
}

.section-title {
    color: var(--text);

    font-size: 23px;
    font-weight: 650;

    letter-spacing: -0.025em;

    margin: 0;
}

.section-description {
    color: var(--muted);

    font-size: 13px;

    margin-top: 5px;
}


/* ---------------------------------------------------------
   MAP INFORMATION BAR
--------------------------------------------------------- */

.information-bar {
    background-color: var(--surface);

    border: 1px solid var(--border);
    border-radius: 7px;

    padding: 12px 16px;

    color: #475467;

    font-size: 12px;
    line-height: 1.6;
}

.information-bar strong {
    color: var(--navy);
}


/* ---------------------------------------------------------
   KPI METRICS
--------------------------------------------------------- */

div[data-testid="stMetric"] {
    background-color: var(--surface);

    border: 1px solid var(--border);
    border-radius: 8px;

    padding: 17px 18px;

    min-height: 115px;

    box-shadow: none;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);

    font-size: 11px;
    font-weight: 500;
}

div[data-testid="stMetricValue"] {
    color: var(--navy);

    font-size: 24px;
    font-weight: 650;

    letter-spacing: -0.02em;
}

div[data-testid="stMetricDelta"] {
    font-size: 11px;
}


/* ---------------------------------------------------------
   SELECTBOX
--------------------------------------------------------- */

div[data-baseweb="select"] > div {
    background-color: var(--surface);

    border-color: #D0D5DD;

    border-radius: 6px;

    min-height: 42px;
}


/* ---------------------------------------------------------
   TABS
--------------------------------------------------------- */

button[data-baseweb="tab"] {
    color: #475467;

    font-size: 13px;
    font-weight: 600;
}


/* ---------------------------------------------------------
   DATAFRAME
--------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);

    border-radius: 8px;

    overflow: hidden;
}


/* ---------------------------------------------------------
   FOOTER
--------------------------------------------------------- */

.observatory-footer {
    margin-top: 40px;

    border-top: 1px solid var(--border);

    padding-top: 16px;

    display: flex;
    justify-content: space-between;

    color: #667085;

    font-size: 11px;
}


/* ---------------------------------------------------------
   RESPONSIVE
--------------------------------------------------------- */

@media (max-width: 900px) {

    .observatory-header {
        align-items: flex-start;
        flex-direction: column;
        gap: 15px;
    }

    .header-meta {
        text-align: left;
    }

    .observatory-title {
        font-size: 29px;
    }
}

</style>
"""
)


# ============================================================
# DATABASE
# ============================================================

@st.cache_data
def load_data():

    query = """
    SELECT
        c.country_name AS country,
        c.country_code,
        i.indicator_name AS indicator,
        i.indicator_code,
        y.year,
        f.value

    FROM fact_indicator_value f

    JOIN dim_country c
        ON f.country_id = c.country_id

    JOIN dim_indicator i
        ON f.indicator_id = i.indicator_id

    JOIN dim_year y
        ON f.year_id = y.year_id

    ORDER BY
        c.country_name,
        i.indicator_name,
        y.year;
    """

    return pd.read_sql(
        query,
        engine
    )


df = load_data()


# ============================================================
# COUNTRY CONFIGURATION
# ============================================================

COUNTRY_INFO = {

    "Togo": {
        "iso3": "TGO",
        "capital": "Lomé",
        "lat": 6.1256,
        "lon": 1.2254
    },

    "Ghana": {
        "iso3": "GHA",
        "capital": "Accra",
        "lat": 5.6037,
        "lon": -0.1870
    },

    "Benin": {
        "iso3": "BEN",
        "capital": "Porto-Novo",
        "lat": 6.4969,
        "lon": 2.6289
    },

    "Cote d'Ivoire": {
        "iso3": "CIV",
        "capital": "Yamoussoukro",
        "lat": 6.8276,
        "lon": -5.2893
    }
}


INDICATOR_OPTIONS = {

    "GDP":
        "NY.GDP.MKTP.CD",

    "GDP per capita":
        "NY.GDP.PCAP.CD",

    "Population":
        "SP.POP.TOTL",

    "Inflation":
        "FP.CPI.TOTL.ZG",

    "Agriculture share of GDP":
        "NV.AGR.TOTL.ZS"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def latest_indicator_value(
    dataframe,
    country,
    indicator_code
):

    data = dataframe[
        (
            dataframe["country"] == country
        )
        &
        (
            dataframe["indicator_code"] == indicator_code
        )
        &
        (
            dataframe["value"].notna()
        )
    ].sort_values(
        "year",
        ascending=False
    )

    if data.empty:
        return None, None

    row = data.iloc[0]

    return (
        float(row["value"]),
        int(row["year"])
    )


def previous_indicator_value(
    dataframe,
    country,
    indicator_code
):

    data = dataframe[
        (
            dataframe["country"] == country
        )
        &
        (
            dataframe["indicator_code"] == indicator_code
        )
        &
        (
            dataframe["value"].notna()
        )
    ].sort_values(
        "year",
        ascending=False
    )

    if len(data) < 2:
        return None, None

    row = data.iloc[1]

    return (
        float(row["value"]),
        int(row["year"])
    )


def percentage_delta(
    latest,
    previous
):

    if (
        latest is None
        or previous is None
        or previous == 0
    ):
        return None

    return (
        (latest - previous)
        / previous
    ) * 100


def format_gdp(value):

    if value is None:
        return "N/A"

    return (
        f"${value / 1_000_000_000:,.2f} bn"
    )


def format_population(value):

    if value is None:
        return "N/A"

    return (
        f"{value / 1_000_000:,.2f} M"
    )


def format_currency(value):

    if value is None:
        return "N/A"

    return f"${value:,.0f}"


def format_percentage(value):

    if value is None:
        return "N/A"

    return f"{value:,.2f}%"


def format_year(value):

    if value is None:
        return "N/A"

    return str(int(value))


# ============================================================
# HEADER
# ============================================================

current_year = datetime.now().year


st.html(
    f"""
<div class="observatory-header">

    <div>

        <div class="observatory-brand">
            West Africa Data Observatory
        </div>

        <h1 class="observatory-title">
            Economic & Development Intelligence
        </h1>

        <div class="observatory-subtitle">
            Regional economic intelligence platform providing
            structured access to macroeconomic and development
            indicators across selected West African economies.
        </div>

    </div>

    <div class="header-meta">
        WORLD BANK DATA<br>
        2000 — {current_year}<br>
        REGIONAL OBSERVATORY
    </div>

</div>
"""
)


# ============================================================
# BUILD MAP DATA
# ============================================================

map_records = []


for country, info in COUNTRY_INFO.items():

    gdp, gdp_year = latest_indicator_value(
        df,
        country,
        "NY.GDP.MKTP.CD"
    )

    gdp_pc, gdp_pc_year = latest_indicator_value(
        df,
        country,
        "NY.GDP.PCAP.CD"
    )

    population, population_year = latest_indicator_value(
        df,
        country,
        "SP.POP.TOTL"
    )

    inflation, inflation_year = latest_indicator_value(
        df,
        country,
        "FP.CPI.TOTL.ZG"
    )

    agriculture, agriculture_year = latest_indicator_value(
        df,
        country,
        "NV.AGR.TOTL.ZS"
    )

    map_records.append(
        {
            "country":
                country,

            "iso3":
                info["iso3"],

            "capital":
                info["capital"],

            "lat":
                info["lat"],

            "lon":
                info["lon"],

            "gdp":
                gdp,

            "gdp_year":
                format_year(gdp_year),

            "gdp_pc":
                gdp_pc,

            "gdp_pc_year":
                format_year(gdp_pc_year),

            "population":
                population,

            "population_year":
                format_year(population_year),

            "inflation":
                inflation,

            "inflation_year":
                format_year(inflation_year),

            "agriculture":
                agriculture,

            "agriculture_year":
                format_year(agriculture_year)
        }
    )


map_df = pd.DataFrame(
    map_records
)


# ============================================================
# REGIONAL MAP HEADER
# ============================================================

st.html(
    """
<div class="section-header">

    <div class="section-kicker">
        Regional overview
    </div>

    <div class="section-title">
        West Africa
    </div>

    <div class="section-description">
        Move over an information point to inspect the latest
        available indicators for each economy.
    </div>

</div>
"""
)


# ============================================================
# MAP
# ============================================================

map_figure = go.Figure()


# ------------------------------------------------------------
# Highlight countries
# ------------------------------------------------------------

map_figure.add_trace(

    go.Choropleth(

        locations=map_df["iso3"],

        z=[1] * len(map_df),

        locationmode="ISO-3",

        colorscale=[
            [0, "#CFD9E3"],
            [1, "#CFD9E3"]
        ],

        showscale=False,

        marker_line_color="#FFFFFF",

        marker_line_width=1.3,

        hoverinfo="skip"
    )
)


# ------------------------------------------------------------
# Prepare hover data
# ------------------------------------------------------------

custom_data = []


for _, row in map_df.iterrows():

    custom_data.append(
        [
            row["capital"],

            format_gdp(
                row["gdp"]
            ),

            row["gdp_year"],

            format_currency(
                row["gdp_pc"]
            ),

            row["gdp_pc_year"],

            format_population(
                row["population"]
            ),

            row["population_year"],

            format_percentage(
                row["inflation"]
            ),

            row["inflation_year"],

            format_percentage(
                row["agriculture"]
            ),

            row["agriculture_year"]
        ]
    )


# ------------------------------------------------------------
# Information points
# ------------------------------------------------------------

map_figure.add_trace(

    go.Scattergeo(

        lon=map_df["lon"],

        lat=map_df["lat"],

        text=map_df["country"],

        customdata=custom_data,

        mode="markers+text",

        textposition="top center",

        textfont=dict(
            size=11,
            color="#172033"
        ),

        marker=dict(
            size=10,

            color="#0B1F33",

            line=dict(
                width=2,
                color="#FFFFFF"
            )
        ),

        hovertemplate=(
            "<b>%{text}</b>"
            "<br>"
            "%{customdata[0]}"
            "<br><br>"
            "<b>GDP</b> %{customdata[1]}"
            " · %{customdata[2]}"
            "<br>"
            "<b>GDP per capita</b> %{customdata[3]}"
            " · %{customdata[4]}"
            "<br>"
            "<b>Population</b> %{customdata[5]}"
            " · %{customdata[6]}"
            "<br>"
            "<b>Inflation</b> %{customdata[7]}"
            " · %{customdata[8]}"
            "<br>"
            "<b>Agriculture / GDP</b> %{customdata[9]}"
            " · %{customdata[10]}"
            "<extra></extra>"
        )
    )
)


# ------------------------------------------------------------
# Geography
# ------------------------------------------------------------

map_figure.update_geos(

    scope="africa",

    projection_type="natural earth",

    showframe=False,

    showcoastlines=True,

    coastlinecolor="#BCC6D1",

    coastlinewidth=0.8,

    showcountries=True,

    countrycolor="#C4CDD7",

    countrywidth=0.7,

    showland=True,

    landcolor="#EDF1F5",

    showocean=True,

    oceancolor="#F8FAFC",

    showlakes=True,

    lakecolor="#F8FAFC",

    lataxis_range=[
        3,
        16
    ],

    lonaxis_range=[
        -18,
        5
    ],

    bgcolor="#F7F9FC"
)


map_figure.update_layout(

    height=475,

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    ),

    paper_bgcolor="#F7F9FC",

    plot_bgcolor="#F7F9FC",

    showlegend=False,

    hoverlabel=dict(
        bgcolor="#0B1F33",
        bordercolor="#0B1F33",
        font_color="#FFFFFF",
        font_size=12
    )
)


st.plotly_chart(
    map_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "scrollZoom": False
    }
)


# ============================================================
# MAP EXPLANATION
# ============================================================

st.html(
    """
<div class="information-bar">

    <strong>Coverage.</strong>

    The current observatory includes Togo, Ghana, Benin and
    Côte d'Ivoire. Values displayed on the map correspond to
    the latest available observation for each indicator.
    Publication years may differ between datasets.

</div>
"""
)


# ============================================================
# COUNTRY INTELLIGENCE
# ============================================================

st.html(
    """
<br>

<div class="section-header">

    <div class="section-kicker">
        Country intelligence
    </div>

    <div class="section-title">
        Country profile
    </div>

    <div class="section-description">
        Examine headline indicators and historical economic trends.
    </div>

</div>
"""
)


selected_country = st.selectbox(
    "Country",
    sorted(
        df["country"].unique()
    ),
    label_visibility="collapsed"
)


country_df = df[
    df["country"] == selected_country
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

gdp, gdp_year = latest_indicator_value(
    df,
    selected_country,
    "NY.GDP.MKTP.CD"
)


previous_gdp, previous_gdp_year = (
    previous_indicator_value(
        df,
        selected_country,
        "NY.GDP.MKTP.CD"
    )
)


gdp_delta = percentage_delta(
    gdp,
    previous_gdp
)


gdp_pc, gdp_pc_year = latest_indicator_value(
    df,
    selected_country,
    "NY.GDP.PCAP.CD"
)


population, population_year = latest_indicator_value(
    df,
    selected_country,
    "SP.POP.TOTL"
)


inflation, inflation_year = latest_indicator_value(
    df,
    selected_country,
    "FP.CPI.TOTL.ZG"
)


agriculture, agriculture_year = latest_indicator_value(
    df,
    selected_country,
    "NV.AGR.TOTL.ZS"
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.metric(
        label=f"GDP · {format_year(gdp_year)}",

        value=format_gdp(gdp),

        delta=(
            f"{gdp_delta:+.1f}% vs previous year"
            if gdp_delta is not None
            else None
        )
    )


with k2:

    st.metric(
        label=(
            f"GDP per capita · "
            f"{format_year(gdp_pc_year)}"
        ),

        value=format_currency(
            gdp_pc
        )
    )


with k3:

    st.metric(
        label=(
            f"Population · "
            f"{format_year(population_year)}"
        ),

        value=format_population(
            population
        )
    )


with k4:

    st.metric(
        label=(
            f"Inflation · "
            f"{format_year(inflation_year)}"
        ),

        value=format_percentage(
            inflation
        )
    )


with k5:

    st.metric(
        label=(
            f"Agriculture / GDP · "
            f"{format_year(agriculture_year)}"
        ),

        value=format_percentage(
            agriculture
        )
    )


# ============================================================
# ANALYTICAL AREA
# ============================================================

st.html("<br>")


tab1, tab2, tab3 = st.tabs(
    [
        "Country trends",
        "Regional comparison",
        "Data explorer"
    ]
)


# ============================================================
# TAB 1 — COUNTRY TRENDS
# ============================================================

with tab1:

    selected_indicator_name = st.selectbox(

        "Indicator",

        list(
            INDICATOR_OPTIONS.keys()
        ),

        key="country_indicator"
    )


    selected_code = (
        INDICATOR_OPTIONS[
            selected_indicator_name
        ]
    )


    trend_data = country_df[
        (
            country_df["indicator_code"]
            == selected_code
        )
        &
        (
            country_df["value"].notna()
        )
    ].sort_values(
        "year"
    )


    trend_figure = go.Figure()


    trend_figure.add_trace(

        go.Scatter(

            x=trend_data["year"],

            y=trend_data["value"],

            mode="lines+markers",

            line=dict(
                color="#0B1F33",
                width=2.5
            ),

            marker=dict(
                size=5,
                color="#0B1F33"
            ),

            hovertemplate=(
                "<b>%{x}</b>"
                "<br>%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )


    trend_figure.update_layout(

        height=420,

        title=dict(
            text=(
                f"{selected_indicator_name}"
                f" — {selected_country}"
            ),
            font=dict(
                size=16,
                color="#101828"
            )
        ),

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        margin=dict(
            l=25,
            r=20,
            t=60,
            b=30
        ),

        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            title=None,
            gridcolor="#EAECF0",
            zeroline=False
        ),

        hoverlabel=dict(
            bgcolor="#0B1F33",
            bordercolor="#0B1F33",
            font_color="#FFFFFF"
        ),

        showlegend=False
    )


    st.plotly_chart(
        trend_figure,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# TAB 2 — REGIONAL COMPARISON
# ============================================================

with tab2:

    comparison_indicator = st.selectbox(

        "Indicator",

        list(
            INDICATOR_OPTIONS.keys()
        ),

        key="comparison_indicator"
    )


    comparison_code = (
        INDICATOR_OPTIONS[
            comparison_indicator
        ]
    )


    comparison_data = df[
        (
            df["indicator_code"]
            == comparison_code
        )
        &
        (
            df["value"].notna()
        )
    ].copy()


    comparison_figure = px.line(

        comparison_data,

        x="year",

        y="value",

        color="country"
    )


    comparison_figure.update_traces(
        line=dict(
            width=2.2
        )
    )


    comparison_figure.update_layout(

        height=440,

        title=dict(
            text=(
                f"{comparison_indicator}"
                " — Regional comparison"
            ),
            font=dict(
                size=16,
                color="#101828"
            )
        ),

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        margin=dict(
            l=25,
            r=20,
            t=60,
            b=30
        ),

        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            title=None,
            gridcolor="#EAECF0",
            zeroline=False
        ),

        hoverlabel=dict(
            bgcolor="#0B1F33",
            font_color="#FFFFFF"
        )
    )


    st.plotly_chart(
        comparison_figure,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# TAB 3 — DATA EXPLORER
# ============================================================

with tab3:

    indicator_filter = st.selectbox(

        "Dataset indicator",

        sorted(
            df["indicator"].unique()
        )
    )


    filtered_df = df[
        df["indicator"]
        == indicator_filter
    ].copy()


    filtered_df = filtered_df.sort_values(
        [
            "country",
            "year"
        ],
        ascending=[
            True,
            False
        ]
    )


    st.dataframe(

        filtered_df[
            [
                "country",
                "country_code",
                "year",
                "indicator",
                "value"
            ]
        ],

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
<div class="observatory-footer">

    <span>
        West Africa Data Observatory
    </span>

    <span>
        Primary data source: World Bank
    </span>

</div>
"""
)