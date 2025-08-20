import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm
from scipy.special import erf

st.set_page_config(page_title="Skewed Normal Precision Calculation",
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
st.title("Precision of the estimate of Mean under skew Normal Distribution")


## Functuion
def estimate_precision(x_bar, s, n, confidence=0.95):
    # Step 2: Coefficient of Variation and skewness
    CV = s / x_bar
    gamma_E = 2 * CV
    gamma = min(0.99, gamma_E)
    # Step 3: delta
    delta =np.sqrt(((np.pi / 2) * gamma**(2/3)) / (gamma**(2/3) + ((4 - np.pi) / 2)**(2/3)))
    # Step 4: omega
    omega = s / np.sqrt(1 - (2 * delta**2) / np.pi)
    # Step 5: SE of mean
    se_mean = (omega * np.sqrt(1 - (2 * delta**2) / np.pi)) / np.sqrt(n)
    # Step 6: Precision
    z = norm.ppf(1 - (1 - confidence) / 2)
    precision = z * (se_mean / x_bar)
    return {
        'precision': precision,
        'standard_error': se_mean,
        'CV': CV
    }

X_Bar = st.sidebar.number_input("Mean",value=100,)
S = st.sidebar.number_input("Standard Deviation",min_value=0.0, value=10.0)
N= st.sidebar.number_input("Length of the sample",min_value=3.0, value=50.0)
Conf= st.sidebar.number_input("Confidence Level (%)",min_value=0.0, value=95.0,max_value=100.0)
go= st.button("Calculate Precision")

if go:
    PP= estimate_precision(x_bar=X_Bar,s=S,n=N,confidence=(Conf*0.01))
    col1,col2,col3=st.columns(3)
    col1.metric("Calculated Precision (%)",value=round(PP['precision']*100,2))
    col2.metric("Coefficient of variation (%)",value=round(PP['CV']*100,2))
    col3.metric("Estimated SE of Mean",value=round(PP['standard_error'],2))
    
st.markdown("---")  # Adds a horizontal line for separation

st.subheader("📌 Formula for calculation of Precision")

st.markdown("""
Click on the link to see the theory:[Click on the link](https://drive.google.com/file/d/1YsOqV_N4rnoZ3hyVcjxuMdofgcO1sTiT/view?usp=sharing))
""")

st.markdown("---")
st.markdown("**Developed by [Rajesh Majumder]**")
st.markdown("**Email:** rajeshnbp9051@gmail.com")
st.markdown("**Website:** [https://rajeshmajumderblog.netlify.app/](https://rajeshmajumderblog.netlify.app/)")
