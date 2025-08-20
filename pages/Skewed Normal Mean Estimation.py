import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm
from scipy.special import erf

st.set_page_config(page_title="Skewed Normal Mean Estimation",
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


def psn(x, delta):
    """ CDF of the skew-normal distribution """
    return 0.5 * (1 + erf(x / np.sqrt(2)))

def nsampleSN(cv=0.45, prec=0.05, conf=0.95, nmin=25, nmax=1000, nby=5, nf=15,designeffect=1,dropOut=0):
    f = prec / cv
    g = min(0.99, 2 * cv)  # Gamma
    
    d1 = 0.5 * np.pi * g ** (2 / 3)
    d2 = g * (2 / 3) + (0.5 * (4 - np.pi)) * (2 / 3)
    delta = np.sqrt(d1 / d2)
    
    # Ensure valid range for sqrt
    denominator = np.sqrt(max(1 - delta ** 2, 1e-10))
    lambda_ = delta / denominator
    
    f_hat = None
    N = nmax
    nset = np.arange(nmin, nmax + 1, nby)
    
    for n in nset:
        delta_star = lambda_ / np.sqrt(1 + n * lambda_ ** 2)
        
        f_grid = np.linspace(0, f, nf)
        ff = np.array(np.meshgrid(-f_grid, f_grid)).T.reshape(-1, 2)[1:, :]
        
        for i in range(len(ff)):
            L = np.sqrt(n) * (ff[i, 0] * np.sqrt(1 - 2 * delta_star ** 2 / np.pi) + delta_star * np.sqrt(2 / np.pi))
            U = np.sqrt(n) * (ff[i, 1] * np.sqrt(1 - 2 * delta_star ** 2 / np.pi) + delta_star * np.sqrt(2 / np.pi))
            
            if psn(U, delta_star) - psn(L, delta_star) >= conf:
                f_hat = ff[i, :]
                break
        
        if f_hat is not None:
            N = n
            break
    
    return (abs(round((N/(1-dropOut))*designeffect)))

# Streamlit App
st.title("Sample Size Calculation for Skew Normal Distribution: Mean Estimation")

cv = st.sidebar.number_input("Coefficient of Variation (%)",max_value=100.0,value=5.00,min_value=1.00)
prec = st.sidebar.number_input("Precision (%)",value=10.00,min_value=0.00,max_value=100.00)
#conf = st.sidebar.number_input("Confidence Level", max_value=0.99,value=0.95,help= "values in decimal")
#nmax = st.sidebar.number_input("Maximum Sample Size", value=5000)
#nmin = st.sidebar.number_input("Minumum Sample Size", value=25,min_value=25)
drpt= st.sidebar.number_input("Drop-Out (%)",value=0.0,min_value=0.0,max_value=100.00) 
x= st.sidebar.radio("Choose Method for Design Effect:",options=['Given','Calculate'])

if(x== "Given"):
    designEffect= st.sidebar.number_input("Design Effect", value=1.0,min_value=1.0,max_value=2.0,help= "values in integer. Minimum is 1")
    go= st.button("Calculate Sample Size")
else:
    m= st.sidebar.number_input("Number of cluster",min_value=2)
    ICC= st.sidebar.number_input("ICC",min_value=0.0)
    designEffect= 1+(m-1)*ICC
    col1,col2,col3=st.columns(3)
    col1.metric("Cluster Size (m)",value=m)
    col2.metric("Intra Class Correlation (ICC)",value=ICC)
    col3.metric("Design Effect",value= round(designEffect,2))
    go= st.button("Calculate Sample Size")


if go:
    confidenceIntervals= [0.8,0.9,0.95,0.97,0.99,0.999,0.9999]
    out=[]
    for conf in confidenceIntervals:
        sample_size= nsampleSN(cv=(cv/100), prec=(prec/100), conf=conf, nmax=3000,nmin=25,designeffect=designEffect,dropOut=(drpt/100))
        out.append(sample_size)
    df= pd.DataFrame({
        "Confidence Levels (%)": [cl *100 for cl in confidenceIntervals],
        "Sample Size": out
    })
    dds= nsampleSN(cv=(cv/100), prec=(prec/100), conf=0.95, nmax=3000,nmin=25,designeffect=designEffect,dropOut=(drpt/100))
    st.write(f"Asuming that with **{(cv)}%** coefficient of variation in a skewed normal distribution,the study would require a sample size of:")
    st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <div style="
            font-size: 36px;
            font-weight: bold;
            background-color: #48D1CC;
            padding: 10px;
            border-radius: 10px;
            text-align: center;">
            {dds}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write(f"for estimating mean with **{(prec)}%** precision and **95%** confidence interval,where the design effect is **{round(designEffect,1)}** with **{(drpt)}%** drop-out from the sample.")
    st.subheader("List of Sample Sizes at different Confidence Levels")
    st.dataframe(df)
    


st.markdown("---")  # Adds a horizontal line for separation

st.subheader("📌 Formula for Sample Size Calculation")

st.markdown("""
Click on the link to see the theory:[Click on the link](https://drive.google.com/file/d/1e2mCYEzSsg79o6538dExkW8AAuoSQkkf/view?usp=sharing))
""")

st.markdown("""
    <div style="
        background-color: #48D1CC;
        padding: 10px;
        border-left: 5px solid orange;
        border-radius: 5px;
        font-size: 18px;">
        <b>Note:</b> The design effect option is only applicable when doing cluster random sampling, other wise the default is 1 and it is recommended to be done in consultation with a statistician.   
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("**Developed by [Rajesh Majumder]**")
st.markdown("**Email:** rajeshnbp9051@gmail.com")
st.markdown("**Website:** [https://rajeshmajumderblog.netlify.app/](https://rajeshmajumderblog.netlify.app/)")
