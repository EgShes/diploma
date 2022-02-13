import streamlit as st

from src.analyze_app.ner import main as ner_main
from src.analyze_app.sentiment import main as sentiment_main


def main():
    st.set_page_config(page_title="Аналитика", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

    st.sidebar.markdown("## Учетные данные")
    login = st.sidebar.text_input("Логин")
    password = st.sidebar.text_input("Пароль", type="password")
    # TODO replace with actual check
    successful_auth = login == "admin" and password == "admin"
    if not successful_auth:
        st.error("Wrong credentials")
        return

    service = st.sidebar.selectbox("Вид анализа", options=["Тональность", "Слова", "Сущности"])
    if service == "Тональность":
        sentiment_main()
    elif service == "Слова":
        return
    elif service == "Сущности":
        ner_main()


if __name__ == "__main__":
    main()
