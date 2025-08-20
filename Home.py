import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="Home",
                   page_icon="🧊")

st.title("Sample Size Calculator For Skewed Normal Mean And Proportion Estimation",)

st.markdown(
    """
    <style>
    button[data-testid="stBaseButton-header"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("The complete version of the sample size calculator is here:  [https://studysizer.streamlit.app/](https://studysizer.streamlit.app/)")

#hide_st_style="""<style>
##MainMenu
#{visiblility:hidden;
#}
#footer
#{visibility: hidden;
#}
#header
#{visibility: hidden;
#}
#</style>"""
#st.markdown(hide_st_style,unsafe_allow_html=True)

image = Image.open('image.png')

st.image(image)

