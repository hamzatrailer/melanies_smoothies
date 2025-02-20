

# Import python packages
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col 


# Write directly to the app
st.title("Customize your smoothie !")
st.write(
    """Choose the fruits you want in your smoothie !"""
)
name_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie is', name_order)

cnx = st.connection("snowflake")
session = cnx.session
if isinstance(session, Session):
    st.success("✅ Connexion à Snowflake réussie!")
else:
    st.error("connexion non établie")
    
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:'
                                 , my_dataframe, max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()
    if st.button('Submit order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered', icon="✅")

