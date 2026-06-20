import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="World Cup Matches Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("WorldCupMatches (1).csv")

df = load_data()

# Clean and prepare data
df['Attendance'] = pd.to_numeric(df['Attendance'], errors='coerce')
df['Home Team Goals'] = pd.to_numeric(df['Home Team Goals'], errors='coerce')
df['Away Team Goals'] = pd.to_numeric(df['Away Team Goals'], errors='coerce')
df['Total Goals'] = df['Home Team Goals'] + df['Away Team Goals']
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Drop rows with NaN in essential columns for analysis if needed
df.dropna(subset=['Stage', 'City', 'Attendance', 'Total Goals', 'Year'], inplace=True)

st.title("World Cup Matches Dashboard")
st.write("A dashboard displaying data from World Cup Matches.")

st.sidebar.header("Filters")

# Update filters to use columns from the World Cup dataset
selected_stages = st.sidebar.multiselect(
    "Select Stage",
    options=sorted(df["Stage"].unique()),
    default=sorted(df["Stage"].unique())
)

selected_cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

min_attendance = st.sidebar.slider(
    "Minimum Attendance",
    min_value=int(df["Attendance"].min()),
    max_value=int(df["Attendance"].max()),
    value=int(df["Attendance"].min())
)

# Filtering logic updated
filtered_df = df[
    (df["Stage"].isin(selected_stages)) &
    (df["City"].isin(selected_cities)) &
    (df["Attendance"] >= min_attendance)
]

total_matches = len(filtered_df)
average_total_goals = round(filtered_df["Total Goals"].mean(), 2) if total_matches else 0
average_attendance = round(filtered_df["Attendance"].mean(), 2) if total_matches else 0
max_attendance = round(filtered_df["Attendance"].max(), 2) if total_matches else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", total_matches)
col2.metric("Average Total Goals", average_total_goals)
col3.metric("Average Attendance", average_attendance)
col4.metric("Max Attendance", max_attendance)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Average Total Goals by Stage")
    stage_goals = filtered_df.groupby("Stage")["Total Goals"].mean().sort_values()
    st.bar_chart(stage_goals)

with right:
    st.subheader("Matches by Year")
    matches_by_year = filtered_df.groupby("Year").size().rename("Number of Matches").sort_index()
    st.bar_chart(matches_by_year)

st.subheader("Match Records")
st.dataframe(
    filtered_df.sort_values("Year", ascending=False),
    width='stretch',
    hide_index=True
)

st.subheader("Simple Insight")
if total_matches:
    best_stage = filtered_df.groupby("Stage")["Total Goals"].mean().idxmax()
    st.success(f"Stage with highest average total goals: {best_stage}")
else:
    st.warning("No records match the selected filters.")
