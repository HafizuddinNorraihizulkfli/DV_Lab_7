import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Titanic Dashboard", layout="wide")

st.title("🚢 Titanic Survival Analysis Dashboard")
st.markdown("Analyze the survival rates and demographics of passengers.")

# --- 1. Load Dataset (Directly from URL to avoid local file issues) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# --- 2. Sidebar Filters ---
st.sidebar.header("Filter Options")

# Filter by Class
pclass_filter = st.sidebar.multiselect(
    "Select Passenger Class:",
    options=df["Pclass"].unique(),
    default=df["Pclass"].unique()
)

# Filter by Gender
sex_filter = st.sidebar.selectbox(
    "Select Gender:",
    options=["All", "male", "female"]
)

# Apply Filters
filtered_df = df[df["Pclass"].isin(pclass_filter)]
if sex_filter != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == sex_filter]

# --- 3. Data Summary Section ---
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

total_passengers = len(filtered_df)
avg_fare = filtered_df["Fare"].mean()
survival_rate = (filtered_df["Survived"].mean() * 100)

col1.metric("Total Passengers", total_passengers)
col2.metric("Average Fare", f"${avg_fare:.2f}")
col3.metric("Survival Rate", f"{survival_rate:.1f}%")

st.markdown("---")

# --- 4. Visualizations ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Age Distribution")
    # Viz 1: Histogram
    fig_hist = px.histogram(
        filtered_df, 
        x="Age", 
        nbins=20, 
        title="Passenger Age Distribution",
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.subheader("Survival by Class")
    # Viz 2: Bar Chart
    survival_counts = filtered_df.groupby(['Pclass', 'Survived']).size().reset_index(name='Count')
    survival_counts['Survived'] = survival_counts['Survived'].map({0: 'No', 1: 'Yes'})
    
    fig_bar = px.bar(
        survival_counts, 
        x="Pclass", 
        y="Count", 
        color="Survived", 
        barmode="group",
        title="Survivors vs Non-Survivors by Class"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Raw Data View ---
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
