import streamlit as st
from pymongo import MongoClient

# MongoDB connection setup
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)

# Database references
db1 = client['Database1']
db2 = client['Database2']

# Collections
collection1 = db1['Collection1']
collection2 = db2['Collection2']

# Streamlit app
st.title("Communicate with Two MongoDB Databases")

# Tabs for Insert and Search functionality
tab1, tab2 = st.tabs(["Insert Data", "Search Data"])

# Insert Data Tab
with tab1:
    st.header("Insert Data into Databases")

    # Streamlit form for inserting data
    with st.form("insert_form"):
        database_choice = st.radio("Select Database:", ("Database1", "Database2"))
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        city = st.text_input("City")
        submit_button = st.form_submit_button("Insert")

        if submit_button:
            if name and city:
                data = {"name": name, "age": age, "city": city}
                if database_choice == "Database1":
                    collection1.insert_one(data)
                    st.success(f"Data inserted into Database1: {data}")
                else:
                    collection2.insert_one(data)
                    st.success(f"Data inserted into Database2: {data}")
            else:
                st.error("Please fill all fields.")

# Search Data Tab
with tab2:
    st.header("Search Data Across Databases")

    # Input search criteria
    search_name = st.text_input("Search by Name")
    search_button = st.button("Search")

    if search_button:
        if search_name:
            # Search in Database1
            results_db1 = list(collection1.find({"name": {"$regex": search_name, "$options": "i"}}))
            # Search in Database2
            results_db2 = list(collection2.find({"name": {"$regex": search_name, "$options": "i"}}))

            # Display results
            if results_db1 or results_db2:
                st.subheader("Results from Database1")
                if results_db1:
                    for result in results_db1:
                        st.write(f"Name: {result['name']}\n Age: {result['age']}\n City: {result['city']}")
                else:
                    st.write("No results found in Database1.")

                st.subheader("Results from Database2")
                if results_db2:
                    for result in results_db2:
                        st.write(f"Name: {result['name']}\n Age: {result['age']}\n City: {result['city']}")
                else:
                    st.write("No results found in Database2.")
            else:
                st.warning("No results found in either database.")
        else:
            st.error("Please enter a name to search.")
