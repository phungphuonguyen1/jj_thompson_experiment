from openai import Image
from def_file import *

import streamlit as st
from langchain.llms import OpenAI
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Config function
st.set_page_config(page_title='JJ_Thompson',page_icon="🤘")

# hide main menu and footer
hide_menu_style= """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style,unsafe_allow_html=True)

#styling

st.markdown("""
<style>
    [data-testid=stSidebar][aria-expanded="true"]{
        background-color: #ee9322;
        border-radius: 20px;
    }
</style>
""",unsafe_allow_html=True)

with st.sidebar:
    st.write("""
        <style>
            .st-eb {
                background-color: #EE9322; /* Background color */
                border-radius: 10px; /* Border radius */
            }

            .st-ec .st-ed { /* Thumb of the slider */
                background-color: #FF0000; /* Thumb color */
            }
        </style>
    """, unsafe_allow_html=True)
    title = '<p style="font-family: Courier;text-align: center;font-weight: bolder; color: Darkblue; font-size: 30px;">Input parameters</p>'
    st.markdown(title, unsafe_allow_html=True)
        
        # Use HTML to create a div with background color, opacity, and rounded border
    info_box = """
    <div style="background-color: #BCD5ED;text-align: center; padding: 10px;border-radius:10px">
        <p>Please enter inputs for the calculation.</p>
    </div>
    """
    st.markdown(info_box, unsafe_allow_html=True)

st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: lightblue;
        color: black; # Adjust this for expander header color
        border-radius: 20px;
        text-align:center;
    }
    .streamlit-expanderContent {
        background-color: white;
        color: black; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)


# function take input from user in sidebar
def user_input_features():
    Voltage=st.sidebar.slider('Voltage: ',0.0,5.0, 0.4)
    Distance=st.sidebar.slider('Distance: ',0.01,0.1, 0.05,step=0.01)
    B_field=st.sidebar.slider('B_field: ',0.0001,0.01,step=0.0001)
    X1=st.sidebar.slider('x1: ',0.1,1.0,0.2,step=0.01)
    X2=st.sidebar.slider('x2: ',0.1,1.0,0.2,step=0.01)
    features=[float(Voltage),float(Distance),float(X1),float(X2),float(B_field)]
    return features

# Main area
title_main='<h1 style="text-align:center; font-weight: bolder;color: #EE9322;text-shadow: 3px 1px blue;">DISTRIBUTION OF NANOPARTICLES IN A POLYMER MATRIX PREDICTION</h1>'
header1_main='<h2 style="text-align:center; font-weight: bolder;">Problem Description</h2>'
st.markdown(title_main,unsafe_allow_html=True)
st.markdown(header1_main,unsafe_allow_html=True)
st.markdown("""Thí nghiệm của JJ. Thompson là thí nghiệm đầu tiên giúp tìm ra tỷ số e/m đã đóng góp quan trọng trong việc hiểu về cấu trúc
         của nguyên tử và phát triển lý thuyết về hạt điện (electron).
          """)
#image=Image.open("polymer_nanoparticle.jpg")
#st.image(image,caption="nanoparticle in a polymer matrix, distribution diagram of nanoparticle")
#st.image("https://editor.analyticsvidhya.com/uploads/210362021-07-18%20(2).png",caption="artificial neural network")
st.write("    In this problem, we have 6 inputs including: amplitude of interaction between polymer-nanoparticle, nanoparticle-nanoparticle, diameter of nanoparticle, phi, chain length of polymer and distance range")
st.write("    While output is function g(r)- distribution of nanoparticle.")
st.write("For more information, please read this article:  [nanoNET: machine learning platform for predicting nanoparticles distribution in a polymer matrix](https://pubs.rsc.org/en/content/articlelanding/2023/sm/d3sm00567d/unauth)")

# input explaination:
ls1="""<ul>
        <li>Interaction polymer-nanoparticle: amplitube</li>
        <li>Interaction nanoparticle-nanoparticle: amplitube</li>
        <li>Diameter of nanoparticle: size of nanoparticle (sperical, in nanometer)</li>
        <li>Phi: represented by mass of nanoparticle per total volume</li>
        <li>Length of polymer chain: in nanometer</li>
        <li>Distance: range should be small (less than length of polymer chain)</li>
    </ul>"""


with st.expander("Input explaination"):
    st.markdown(ls1,unsafe_allow_html=True)

input = user_input_features()

if st.sidebar.button("Mô phỏng"):
    #ax.style.use('dark_background')
    df=path_function(input[0],input[1],input[2],input[3],input[4])
    #path
    st.write(df)
    fig,ax=plt.subplots()
    ax.plot(df['x'],df['y'],"r")
    E_field=input[0]/input[1]

    vx= E_field/input[4]
    ELECTRON_CHARGE= 1.6e-19
    ELECTRON_MASS = 9.1e-31
    # Calculate other factors
    ratio =ELECTRON_CHARGE/ELECTRON_MASS
    D=input[1]
    x1=input[2]
    x2=input[3]
    B_field=input[4]
    t1_final=x1/vx
    t2_final=x2/vx
    #note
    ax.text(-0.1,(input[1]/2)*1.3,'E={} V/m,$x_1$={}m,\n$x_2$={}m,$v_0={}m/s$'.format(E_field,x1,x2,vx),fontsize = 12, bbox = dict(facecolor = 'lightblue', alpha = 0.5))
    ax.set_title("Simulation")
    ax.axis("off")

    #facilities
    ax.hlines(y=D/2, xmin=0, xmax=x1, linewidth=4, color='black')
    ax.hlines(y=-D/2, xmin=0, xmax=x1, linewidth=4, color='black')

    ax.vlines(x=x1+x2, ymin=-D/2, ymax=1.5*(y1_inside(vx,ratio,E_field,B_field,t1_final)+y2_outside(ratio,t2_final,x1,B_field,t1_final,E_field)), linewidth=3, color='black')
    ax.hlines(y=0, xmin=0, xmax=x1+x2, linestyles='dotted',color='black')

    #distance note
    # x1
    ax.plot((0,x1),(-1.3*D/2,-1.3*D/2), 'gray',) # arrow line
    ax.plot((0,0),(-1.3*D/2,-1.3*D/2), 'gray', marker='<',) # lower arrowhead
    ax.plot((x1,x1),(-1.3*D/2,-1.3*D/2), 'gray', marker='>',) # upper arrowhead
    ax.text(x1/2.5,-1.5*D/2,"x1={}".format(x1))

    #x2
    ax.plot((x1,x2+x1),(-1.3*D/2,-1.3*D/2), 'gray',) # arrow line
    ax.plot((x1,x1),(-1.3*D/2,-1.3*D/2), 'gray', marker='<',) # lower arrowhead
    ax.plot((x2+x1,x2+x1),(-1.3*D/2,-1.3*D/2), 'gray', marker='>',) # upper arrowhead
    ax.text(x1+x2/2.5,-1.5*D/2,"x2={}".format(x2))

    #D
    ax.plot((-0.1,-0.1),(-D/2,D/2), 'gray',) # arrow line
    ax.plot((-0.1,-0.1),(-D/2,-D/2), 'gray', marker='v',) # lower arrowhead
    ax.plot((-0.1,-0.1),(D/2,D/2), 'gray', marker='^',) # upper arrowhead
    ax.text(-0.15,-D/10,"D={}".format(D),rotation=90)

    # Display the plot in Streamlit
    st.pyplot(fig)
    
