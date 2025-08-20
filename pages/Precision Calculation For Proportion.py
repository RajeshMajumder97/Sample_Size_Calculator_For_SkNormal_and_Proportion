import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm
from scipy.special import erf

st.set_page_config(page_title="Precision Calculation For Proportion",
                   page_icon="🧊")

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


# Streamlit App
st.title("Precision of the estimate of Proportion")

# Function
def Precision(p=0.5,n=100,Conf=0.95,relative='Absolute Precision'):
    if relative=='Relative to the Proportion':
        z = norm.ppf(1 - (1 - Conf) / 2)
        d_rel = z * ((p * (1 - p)) / (n*p**2)) ** 0.5
        return(round(d_rel,2))
    else:
        z = norm.ppf(1 - (1 - Conf) / 2)
        d = z * ((p * (1 - p)) / n) ** 0.5  
        return(round(d,2))

p = st.sidebar.number_input("Proportion (%)",value=50.0,min_value=0.0,max_value=100.0)
d = st.sidebar.number_input("Length of the sample",min_value=3.0, value=100.0)
Conf= st.sidebar.number_input("Confidence Level (%)",min_value=0.0, value=95.0,max_value=100.0)
ads= st.sidebar.radio("Choose Precision Option",options=['Absolute Precision','Relative to the Proportion'])
go= st.button("Calculate Precision")

if go:
    PP= Precision(p=(p*0.01),n=100,Conf=(Conf*0.01),relative=ads)
    col1,col2=st.columns(2)
    col1.metric("Calculated Precision (%)",value=round(PP*100,2))

st.markdown("---")  # Adds a horizontal line for separation

st.subheader("📌 Formula for calculation of Precision")

st.latex(r"""
d = Z_{1-\alpha/2} \times \sqrt{\frac{p(1 - p)}{n}}
""")

st.subheader("📌 Description of Parameters")

st.markdown("""
- **\( Z_{1-alpha/2} \)**: Critical value for the confidence level (e.g., 1.96 for 95% confidence).
- **\( d \)**: Absolute precision (margin of error).
- **\( p \)**: Expected proportion.
- **\( n \)**: Sample size.
""")

st.subheader("📌 References")

st.markdown("""
1. **Naing, N. N. (2003).** Determination of Sample Size.The Malaysian Journal of Medical Sciences: MJMS,10(2), 84-86. Available at: [https://pubmed.ncbi.nlm.nih.gov/23386802/](https://pubmed.ncbi.nlm.nih.gov/23386802/)
""")

st.markdown("---")
st.markdown("**Developed by [Rajesh Majumder]**")
st.markdown("**Email:** rajeshnbp9051@gmail.com")
st.markdown("**Website:** [https://rajeshmajumderblog.netlify.app/](https://rajeshmajumderblog.netlify.app/)")

