import streamlit as st
import requests
import my_articles
from streamlit_option_menu import option_menu

my_article_list = None

def button_click():
    if st.session_state.article_button == "My Article":
        st.session_state.article_button = "Back"
        st.session_state.article_toggle = True
        
    else:
        st.session_state.article_button = "My Article"
        st.session_state.article_toggle = False

def article():
    st.title("Article Page")

    if "article_button" not in st.session_state:
        st.session_state.article_button = "My Article"
    if "article_toggle" not in st.session_state:
        st.session_state.article_toggle = False

    
    if st.button(st.session_state.article_button, on_click=button_click):
        pass


    if st.session_state.article_toggle:
        my_articles.my_articles()
        return
    else:
        pass
    
    
    response = requests.get("http://127.0.0.1:8000/posts")
    articles = response.json()
    
    for article in articles:
        st.write(f"## {article['title']}")
        st.write(article['content'])
        # Add more details if needed (e.g., owner, created_at, etc.)
        st.write(f"Published by: {article['owner']['email']}")
        st.write(f"Created at: {article['created_at']}")
        st.write("---")  # Add a separator between articles

    
