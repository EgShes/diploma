import datetime
from typing import Any, Iterable, Optional, Tuple

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st

from src.config import DbConfig

connection = None


@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(DbConfig.get_db_url())


def form_sql(
    employee_id: Optional[int], chat_id: Optional[int], from_: datetime.datetime, till: datetime.datetime
) -> Tuple[str, Iterable[Any]]:
    conditions, params = [], []
    sql = """
        select
            se.id as id,
            se.type as type,
            st.employee_id as employee_id,
            st.chat_id as chat_id,
            se.created_at as created_at,
            st.text as source_text
        from sentiment se
            left join source_text st on st.id = se.source_text_id
            left join employee em on st.employee_id = em.id
            left join chat ch on st.chat_id = ch.id"""
    conditions.append("se.created_at >= %s"), params.append(from_)
    conditions.append("se.created_at < %s"), params.append(till)
    if employee_id is not None:
        conditions.append("em.id = %s"), params.append(employee_id)
    if chat_id is not None:
        conditions.append("ch.id = %s"), params.append(chat_id)
    sql += "\nwhere " + " and ".join(conditions) + ";"
    return sql, params


@st.cache(ttl=600)
def get_sentiments(
    employee_id: Optional[int], chat_id: Optional[int], from_: datetime.datetime, till: datetime.datetime
) -> pd.DataFrame:
    # include last day
    till = till + datetime.timedelta(days=1)
    with connection.cursor() as cursor:
        sql, params = form_sql(employee_id, chat_id, from_, till)
        cursor.execute(sql, params)
        data = cursor.fetchall()
        df = pd.DataFrame.from_records(
            data, columns=["id", "type", "employee_id", "chat_id", "created_at", "source_text"]
        )
        return df


def main(
    employee_id: Optional[int], chat_id: Optional[int], from_date: datetime.datetime, till_date: datetime.datetime
):

    global connection
    connection = init_connection()

    sentiment_df = get_sentiments(employee_id, chat_id, from_date, till_date)

    st.dataframe(sentiment_df)

    plot_df = sentiment_df.groupby("type").size().reset_index().rename(columns={0: "amount"})
    fig = px.bar(plot_df, x="type", y="amount", title="Распределение тональности")
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
