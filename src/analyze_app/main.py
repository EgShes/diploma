import streamlit as st

from src.analyze_app.ner import main as ner_main
from src.analyze_app.sentiment import main as sentiment_main
from src.analyze_app.word import main as word_main


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

    st.sidebar.markdown("## Параметры")
    search_type = st.sidebar.selectbox("Область поиска", ["Везде", "Беседа", "Пользователь", "Беседа + Пользователь"])
    user_id = st.sidebar.number_input(
        "id пользователя", min_value=1, step=1, disabled=search_type not in ["Пользователь", "Беседа + Пользователь"]
    )
    chat_id = st.sidebar.number_input(
        "id беседы", min_value=1, step=1, disabled=search_type not in ["Беседа", "Беседа + Пользователь"]
    )

    employee_id = user_id if search_type in ["Пользователь", "Беседа + Пользователь"] else None
    chat_id = chat_id if search_type in ["Беседа", "Беседа + Пользователь"] else None

    st.sidebar.markdown("Даты поиска")
    from_date = st.sidebar.date_input("С")
    till_date = st.sidebar.date_input("По")

    if till_date < from_date:
        st.error("Дата начала поиска не может быть больше даты окончания")
        return

    if service == "Тональность":
        sentiment_main(employee_id, chat_id, from_date, till_date)
    elif service == "Слова":
        word_main(employee_id, chat_id, from_date, till_date)
    elif service == "Сущности":
        ner_main(employee_id, chat_id, from_date, till_date)


if __name__ == "__main__":
    main()
