import streamlit as st
import requests
import login

token = login.cookies["jwt-token"]
headers = {"Authorization": f'Bearer {token}'}

def make_and_edit_req(title, content, id=None):
    if id is not None:
        print(f'title:{title}, content:{content}')
        edit_req = requests.put(f"http://127.0.0.1:8000/posts/{id}", headers=headers, json={"title": title, "content": content})
        if edit_req.status_code == 200: #201 created
            st.success('The article successfully edited')
        else:
            st.error(f"error status code {edit_req.status_code}")
    else:
        print(f'title:{title}, content:{content}')
        submit_new_req = requests.post("http://127.0.0.1:8000/posts", headers=headers, json={"title": title, "content": content})
        if submit_new_req.status_code == 201:
            st.success('Successfully created the article')
        else:
            st.error(f"error status code {submit_new_req.status_code}")




def my_articles():
        
    st.write("Create an Article")
    form = st.form("Create/Edit")
    title = form.text_input("Title", key='input_title')
    content = form.text_area("Content", key='input_content')
        
    submitted = form.form_submit_button('Submit')
    if submitted:
        make_and_edit_req(title, content)
        
    st.write(f'title : {title}')
    st.write(f'content : {content}')
    

    articles = None

    article_resp = requests.get("http://127.0.0.1:8000/posts/my_article", headers=headers)
    
    # Check if the response status code is OK (200)
    if article_resp.status_code == 401:
        st.warning("Login to see your article")
    elif article_resp.status_code == 404:
        st.warning('You do not have any article....make your first article!!', icon="⚠️")
        return

    try:
        # Attempt to parse the response as JSON
        articles = article_resp.json()
    except ValueError as e:
        # If parsing as JSON fails, handle the error
        st.error("Failed to parse response as JSON.")
        st.error(f"Error: {e}")
        return

    # Check if articles is a list
    if isinstance(articles, list):
        # Iterate over the articles and display their details
        for article_item in articles:
            with st.container(border=True):
                
                st.write(f"## {article_item['title']}")
                st.write(article_item['content'])
                st.write(f"Published by: {article_item['owner']['email']}")
                st.write(f"Created at: {article_item['created_at']}")
                st.write("---")  # Add a separator between articles

    
                # Create two columns within the container
                left_column, right_column = st.columns(2)

                # Button in the left column
                with left_column:
                    # if st.button("Edit", key=f"edit_button_{article_item['id']}"):
                    #     article_content(article_item['title'], article_item['content'], article_item['id'])
                    pass

                st.write("Edit an Article")
                # Create form for editing article
                with st.form(f"Edit_{article_item['id']}"):
                    # Create separate variables for title and content
                    title_key = f"title_{article_item['id']}"
                    content_key = f"content_{article_item['id']}"
                    
                    # Get user input for title and content
                    title = st.text_input("Title", value=article_item['title'], key=title_key)
                    content = st.text_area("Content", value=article_item['content'], key=content_key)
                    
                    # Submit button
                    submitted = st.form_submit_button('Submit')
                    
                    # Process form submission
                    if submitted:
                        make_and_edit_req(title, content, article_item['id'])

                    
                # Button in the right column
                with right_column:
                    if st.button("Delete", key=f"delete_button_{article_item['id']}"):
                        del_req = requests.delete(f"http://127.0.0.1:8000/posts/{article_item['id']}", headers=headers)
                        if del_req.status_code == 204: 
                            st.success('The article succesfully delete the article')
                        else:
                            st.error(f"error status code {del_req.status_code}")
