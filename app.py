import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    padding: 1rem 2rem;
}

/* Metric Card */
[data-testid="stMetric"] {
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}

/* Force black text */
[data-testid="stMetric"] * {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="weather_db"
)

df = pd.read_sql("SELECT * FROM weather_data", conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# ---------------- TITLE ----------------
st.title("🌦️ Weather Dashboard")

# ---------------- SIDEBAR ----------------
city = st.sidebar.selectbox("Select City", df['city'].unique())
filtered_df = df[df['city'] == city]

latest = filtered_df.sort_values("timestamp", ascending=False).iloc[0]

# ---------------- KPI ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Temperature (°C)", f"{latest['temperature']:.1f}")
col2.metric("Feels Like", f"{latest['feels_like']:.1f}")
col3.metric("Humidity (%)", f"{latest['humidity']}")
col4.metric("Wind Speed", f"{latest['wind_speed']} m/s")

st.caption(f"Condition: {latest['condition_desc']}")

# ---------------- TEMPERATURE GRAPH ----------------
st.subheader("Temperature Trend")

fig, ax = plt.subplots(figsize=(3,1.5))
ax.plot(filtered_df['timestamp'], filtered_df['temperature'], marker='o')

ax.set_xlabel("Time")
ax.set_ylabel("Temp (°C)")
ax.set_title("Temperature Over Time")
ax.tick_params(axis='x', rotation=45)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.pyplot(fig, use_container_width=False)

# ---------------- HUMIDITY GRAPH ----------------
st.subheader("Humidity Trend")

fig, ax = plt.subplots(figsize=(3,1.5))
ax.plot(filtered_df['timestamp'], filtered_df['humidity'], marker='o')

ax.set_xlabel("Time")
ax.set_ylabel("Humidity (%)")
ax.set_title("Humidity Over Time")
ax.tick_params(axis='x', rotation=45)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.pyplot(fig, use_container_width=False)

# ---------------- TABLE ----------------
st.subheader("Recent Data")
st.dataframe(filtered_df.tail(5), use_container_width=True)

# ---------------- CITY COMPARISON ----------------
st.subheader("City Comparison")

latest_all = df.sort_values('timestamp').groupby('city').tail(1)

fig, ax = plt.subplots(figsize=(3,1.5))
ax.bar(latest_all['city'], latest_all['temperature'])

ax.set_xlabel("City")
ax.set_ylabel("Temp (°C)")
ax.set_title("City Temperature Comparison")
ax.tick_params(axis='x', rotation=30)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.pyplot(fig, use_container_width=False)

# ---------------- CLOSE DB ----------------
conn.close()
