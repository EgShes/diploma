import datetime
from typing import Any, Iterable, List, Optional, Tuple

import matplotlib
import pandas as pd
import psycopg2
import streamlit as st
from matplotlib import pyplot as plt
from wordcloud import WordCloud

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
            wd.id as id,
            wd.text as text,
            st.employee_id as employee_id,
            st.chat_id as chat_id,
            wd.created_at as created_at,
            st.text as source_text
        from word wd
            left join word_source_text wst on wd.id = wst.word_id
            left join source_text st on st.id = wst.source_text_id
            left join employee em on st.employee_id = em.id
            left join chat ch on st.chat_id = ch.id"""
    conditions.append("wd.created_at >= %s"), params.append(from_)
    conditions.append("wd.created_at < %s"), params.append(till)
    if employee_id is not None:
        conditions.append("em.id = %s"), params.append(employee_id)
    if chat_id is not None:
        conditions.append("ch.id = %s"), params.append(chat_id)
    sql += "\nwhere " + " and ".join(conditions) + ";"
    return sql, params


@st.cache(ttl=600)
def get_words(
    employee_id: Optional[int], chat_id: Optional[int], from_: datetime.datetime, till: datetime.datetime
) -> pd.DataFrame:
    # include last day
    till = till + datetime.timedelta(days=1)
    with connection.cursor() as cursor:
        sql, params = form_sql(employee_id, chat_id, from_, till)
        cursor.execute(sql, params)
        data = cursor.fetchall()
        df = pd.DataFrame.from_records(
            data, columns=["id", "text", "employee_id", "chat_id", "created_at", "source_text"]
        )
        return df


@st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
def make_word_cloud(words: List[str]) -> plt.Figure:
    text = " ".join(words) if words else "Пусто пусто пусто"
    fig = plt.figure()
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Облако слов")
    return fig


def main(
    employee_id: Optional[int], chat_id: Optional[int], from_date: datetime.datetime, till_date: datetime.datetime
):

    global connection
    connection = init_connection()

    word_df = get_words(employee_id, chat_id, from_date, till_date)

    st.pyplot(make_word_cloud(word_df["text"].tolist()))

    word = st.selectbox("Слово", options=sorted(word_df["text"].drop_duplicates()))
    for text in word_df[word_df["text"] == word]["source_text"]:
        st.write(text)
        st.write("\n")


if __name__ == "__main__":
    main()
