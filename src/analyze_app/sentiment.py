import datetime
from typing import Optional

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st

from src.config import DbConfig

connection = None


@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(DbConfig.get_db_url())


# TODO make it work with ids
@st.cache(ttl=600)
def get_sentiments(
    user_id: Optional[int], chat_id: Optional[int], from_: datetime.datetime, till: datetime.datetime
) -> pd.DataFrame:
    # include last day
    till = till + datetime.timedelta(days=1)
    with connection.cursor() as cursor:
        sql = "select id, type, created_at from sentiment where created_at >= %s and created_at < %s;"
        cursor.execute(sql, [from_, till])
        data = cursor.fetchall()
        df = pd.DataFrame.from_records(data, columns=["id", "type", "created_at"])
        return df


def main():

    global connection
    connection = init_connection()

    st.sidebar.markdown("## Параметры")
    search_type = st.sidebar.selectbox("Область поиска", ["Везде", "Беседа", "Пользователь"])
    user_id = st.sidebar.number_input("id пользователя", min_value=1, step=1, disabled=search_type != "Пользователь")
    chat_id = st.sidebar.number_input("id беседы", min_value=1, step=1, disabled=search_type != "Беседа")

    user_id = user_id if search_type == "Пользователь" else None
    chat_id = chat_id if search_type == "Беседа" else None

    st.sidebar.markdown("Даты поиска")
    from_date = st.sidebar.date_input("С")
    till_date = st.sidebar.date_input("По")

    if till_date < from_date:
        st.error("Дата начала поиска не может быть больше даты окончания")
        return

    data = get_sentiments(user_id, chat_id, from_date, till_date)
    data = data.groupby("type").size().reset_index()
    data = data.rename(columns={0: "amount"})

    fig = px.bar(data, x="type", y="amount", title="Распределение тональности")
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
