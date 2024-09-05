import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="spms"
    )
    mycursor = mydb.cursor()
    st.write("Database connection successful.")
except mysql.connector.Error as err:
    st.write(f"Error: {err}")
    st.stop()

# Streamlit app
st.title("Smart Parking Management System Dashboard")

# Query to fetch data
def fetch_data(query):
    try:
        mycursor.execute(query)
        return mycursor.fetchall()
    except mysql.connector.Error as err:
        st.write(f"Error: {err}")
        return []

# Fetch entries data
st.subheader("Current Entries")
entries_query = "SELECT * FROM in_time;"
entries_data = fetch_data(entries_query)
if entries_data:
    entries_df = pd.DataFrame(entries_data, columns=["In Time", "Car Number"])
    st.write(entries_df)
else:
    st.write("No data available.")

# Fetch billing data
st.subheader("Billing Records")
billing_query = """
SELECT car_number, 
       in_time, 
       out_time,
       duration,
       price
FROM records;
"""
billing_data = fetch_data(billing_query)
if billing_data:
    billing_df = pd.DataFrame(billing_data, columns=["Car Number", "In Time", "Out Time", "Duration (minutes)", "Price (rupees)"])
    st.write(billing_df)
else:
    st.write("No billing records available.")

# Option to download data
st.subheader("Download Data")
if st.button('Download Current Entries'):
    if not entries_df.empty:
        entries_csv = entries_df.to_csv(index=False)
        st.download_button(label="Download CSV", data=entries_csv, file_name="entries_data.csv")
    else:
        st.write("No data to download.")

if st.button('Download Billing Records'):
    if not billing_df.empty:
        billing_csv = billing_df.to_csv(index=False)
        st.download_button(label="Download CSV", data=billing_csv, file_name="billing_records.csv")
    else:
        st.write("No data to download.")
