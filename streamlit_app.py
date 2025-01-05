# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smooothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
#st.write('The name on your Smoothie will be:', name_on_order)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width = True)
#st.stop()
#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function.
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.write(my_dataframe)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    , my_dataframe
    , max_selections = 5
    )
#st.write(ingredients_list)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].ILOC[0]
        st.write('The search value for ',fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width = True)
        
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
     values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        


#editable_df = st.data_editor(my_dataframe)

