import streamlit as st
from agent import run_agent
from state import todo

st.title("Smart TODO")
if "messages" not in st.session_state:
        st.session_state.messages = []
#Add ability to display messages in the chat history just markdown all messages in the session state

col1, col2 = st.columns(2)
with col1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What do you want to do?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        response = run_agent(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
        st.rerun()
with col2:
    if todo:
        for i, task in enumerate(todo, 1):
            col1, col2 = st.columns([1, 5])
            with col1:
                checked = st.checkbox("",value=task["done"], key=f"tasks_{i}")
                task['done'] = checked
            with col2:
                st.markdown(f"~~{task['task']}~~" if task["done"] else task["task"])