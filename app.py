import pandas as pd
import streamlit as st
from pipeline import ask

st.set_page_config(page_title="Ask Your Data", page_icon="📊")


def draw_chart(df):
    if len(df.columns) != 2 or len(df) < 2 or not pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
        return
    x, y = df.columns
    if any(word in str(x).lower() for word in ("date", "month", "year", "quarter")):
        st.line_chart(df, x=x, y=y)
    else:
        st.bar_chart(df, x=x, y=y)


st.title("Ask Your Data")
st.caption("Ask questions about Northwind Traders in plain English. Read-only: nothing can be changed.")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])
        if "data" in msg:
            draw_chart(msg["data"])
            st.dataframe(msg["data"])
            with st.expander("SQL used"):
                st.code(msg["sql"], language="sql")

question = st.chat_input("Ask a question about the business")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Working on it..."):
            result = ask(question)
        st.write(result["text"])
        if "data" in result:
            draw_chart(result["data"])
            st.dataframe(result["data"])
            with st.expander("SQL used"):
                st.code(result["sql"], language="sql")
            st.download_button("Download CSV", result["data"].to_csv(index=False),
                               "result.csv", "text/csv")
    st.session_state.history.append({"role": "user", "text": question})
    st.session_state.history.append({"role": "assistant", **result})