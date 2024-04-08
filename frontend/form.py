import streamlit as st


def form(id=None, title_ph="", content_ph=""):
    form_title = ""
    if id is not None:
        form_title = "Make New Article"
    else:
        form_title = "Edit Article"

    my_form = st.form(form_title)
    title = my_form.text_input("Title", value=title_ph, placeholder=title_ph)
    content = my_form.text_area("Content", value=content_ph, placeholder=content_ph)
    
