import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col  

# Initialize Streamlit app
st.title("Customize your smoothie !")
st.write("Choose the fruits you want in your smoothie!")

# Get user input
name_order = st.text_input('Name on Smoothie')

# Create a Snowflake session explicitly
cnx = st.connection("snowflake")  
session = Session.builder.configs(cnx.credentials).create()

# Ensure session is valid before querying
if session:
    try:
        # Fetch data from Snowflake table
        my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name')).to_pandas()

        # Display ingredient selection
        ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe['FRUIT_NAME'], max_selections=5)

        if ingredients_list:
            ingredients_string = ', '.join(ingredients_list)  

            my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_order}')
            """

            st.write(my_insert_stmt)

            if st.button('Submit order'):
                session.sql(my_insert_stmt).collect()
                st.success('Your Smoothie is ordered', icon="✅")

    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

else:
    st.error("Failed to create Snowflake session")
