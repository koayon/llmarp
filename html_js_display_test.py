import circuitsvis as cv
import streamlit as st

hello_html = cv.examples.hello("Kola").show_code()
st.title("Testing circuitsvis")
st.write(hello_html, unsafe_allow_html=True)
st.write("")

basic_html = "<div> <h1> Hello </h1> </div>"
st.write(basic_html, unsafe_allow_html=True)
hello_w_end_div = hello_html + " </div>"
st.write(hello_w_end_div, unsafe_allow_html=True)

st.components.v1.html(hello_html)
