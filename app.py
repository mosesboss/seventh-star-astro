import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------------------------------
# 1. إعداد الصفحة والعنوان
# ----------------------------------------------------
st.set_page_config(page_title="GDP Dashboard", page_icon="🌎", layout="wide")

st.title("🌎 GDP dashboard")
st.markdown("""
Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. 
As you'll notice, the data only goes to 2022 right now, and datapoints for certain years are often missing. 
But it's otherwise a great (and did I mention free?) source of data.
""")

# ----------------------------------------------------
# 2. تحميل البيانات (بيانات افتراضية للتجربة)
# ----------------------------------------------------
@st.cache_data
def get_gdp_data():
    # روابط أو بيانات البنك الدولي
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(url)
    df.rename(columns={"Country Code": "Country Code", "Year": "Year", "Value": "GDP"}, inplace=True)
    return df

try:
    df_gdp = get_gdp_data()
except Exception:
    st.error("تعذر تحميل البيانات المباشرة، يرجى التأكد من الاتصال بالإنترنت.")
    st.stop()

# ----------------------------------------------------
# 3. عناصر التحكم بالمدخلات (السنوات والدول)
# ----------------------------------------------------
min_year = int(df_gdp['Year'].min())
max_year = int(df_gdp['Year'].max())

st.subheader("Which years are you interested in?")
from_year, to_year = st.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(1960, 2022),
    label_visibility="collapsed"
)

all_countries = sorted(df_gdp['Country Code'].unique())
default_countries = ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"]

st.subheader("Which countries would you like to view?")
selected_countries = st.multiselect(
    "Select Countries",
    options=all_countries,
    default=[c for c in default_countries if c in all_countries],
    label_visibility="collapsed"
)

# تصفية البيانات بناءً على مدخلات المستخدم
filtered_df = df_gdp[
    (df_gdp['Country Code'].isin(selected_countries)) &
    (df_gdp['Year'] >= from_year) &
    (df_gdp['Year'] <= to_year)
]

# ----------------------------------------------------
# 4. رسم البياني للتغير عبر الزمن (GDP over time)
# ----------------------------------------------------
st.markdown("---")
st.subheader("GDP over time")

if not filtered_df.empty:
    chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('GDP:Q', title='GDP ($)'),
        color='Country Code:N',
        tooltip=['Country Code', 'Year', 'GDP']
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)

# ----------------------------------------------------
# 5. عرض مؤشرات الأداء (Metrics) لعام 2022
# ----------------------------------------------------
st.markdown("---")
st.subheader(f"GDP in {to_year}")

df_latest = filtered_df[filtered_df['Year'] == to_year]

if not df_latest.empty:
    cols = st.columns(3)
    for idx, row in enumerate(df_latest.iterrows()):
        country = row[1]['Country Code']
        gdp_val = row[1]['GDP']
        gdp_in_billions = f"{gdp_val / 1e9:,.0f}B"
        
        with cols[idx % 3]:
            st.metric(label=f"{country} GDP", value=gdp_in_billions)
else:
    st.info(f"لا توجد بيانات متوفرة لعام {to_year} للدول المحددة.")
