import streamlit as st
from agent import run_agent
from state import get_todo

st.title("Smart TODO")
if "messages" not in st.session_state:
    st.session_state.messages = []

left_col, right_col = st.columns(2)  

with left_col:
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

with right_col:
    todo = get_todo()
    if todo:
        for i, task in enumerate(todo, 1):
            check_col, text_col = st.columns([1, 5])  
            with check_col:
                checked = st.checkbox("", value=task["done"], key=f"task_{i}")
                task["done"] = checked
            with text_col:
                st.markdown(f"~~{task['task']}~~" if task["done"] else task["task"])