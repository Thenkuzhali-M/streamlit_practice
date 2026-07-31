# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app
st.title(f"Customize Smoothie order form: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on your smoothie will be:", name_on_order)

# option = st.selectbox(
#     "what is your favourite friuit?",
#     ("Banana", "Strawberry", "Peaches"),
# )

# st.write("Your favourite fruit is:", option)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

ingredients_list =st.multiselect('choose upto 5 ingredients:',my_dataframe, max_selections=5) 
if ingredients_list:    
    
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string= '' 
    
    for fruits_choosen in ingredients_list:
      ingredients_string+= fruits_choosen+' '
      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      st.subheader(fruits_choosen + 'Nutrition_information')
      
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+fruits_choosen)  
      sf_df =  st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
   
   

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('submit Order')

    if time_to_insert:
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
# st.text(smoothiefroot_response.json())
sf_df =  st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
