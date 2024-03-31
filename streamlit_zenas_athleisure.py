# Import python packages
import streamlit as st
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")
st.write(
    "Pick a sweatsuit color or style"
)

#name_on_order = st.text_input('Name on smoothie', '')
#st.write('The name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("zenas_athleisure_db.products.catalog_for_website").sort(col('color_or_style'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    #st.write('You selected:', ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
        
    st.write('string is', ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
#        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="âœ…")
        st.success('Your Smoothie is ordered, ' + name_on_order + '!')

