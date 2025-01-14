import streamlit as st
# -----------------------------------------------------------------------------------------------------
# Streamlit Page Configuration
st.set_page_config(
    page_title="Select Option",
    initial_sidebar_state="auto",
    menu_items={
        "About": "This is an **extremely** cool web app!"
    }
)

st.title("Welcome to my **amazing** web-page Dr Cline! :smiley:")

st.write("Here you can find information for (nearly) all restaurants and takeaways in London. Simply click 'View Establishments' and scroll down! :point_left:")
st.write("You can also add and remove existing establishments if you wish; as well as editing existing establishment data. :spock-hand:")
st.write("Feel free to have a look at my dashboard which has some data visualisations based on some key findings:thumbsup:")


