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

v_selected_color = st.multiselect(
    'Pick a sweatsuit color or style'
    , my_dataframe
    , max_selections = 1
)

if v_selected_color:
    #st.write('You selected:', ingredients_list)
    #st.text(ingredients_list)

    #ingredients_string = ''

    #for fruit_chosen in ingredients_list:
        #ingredients_string += fruit_chosen + ' '

    v_price = pd_df.loc[pd_df['COLOR_OR_STYLE'] == v_selected_color, 'PRICE'].iloc[0]
    v_image_URL = pd_df.loc[pd_df['COLOR_OR_STYLE'] == v_selected_color, 'DIRECT_URL'].iloc[0]
    v_sizes = pd_df.loc[pd_df['COLOR_OR_STYLE'] == v_selected_color, 'SIZE_LIST'].iloc[0]
    v_upsell = pd_df.loc[pd_df['COLOR_OR_STYLE'] == v_selected_color, 'UPSELL_PRODUCT_DESC'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        #st.subheader(fruit_chosen + ' Nutrition Information')
        #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        #fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)

    st.write(v_image_URL)

    st.write('Price:  ', v_price)
    st.write('Sizes available:  ', v_sizes)
    st.write(v_upsell)

