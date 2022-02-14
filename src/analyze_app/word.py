import datetime
from typing import List, Optional

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


# TODO make it work with ids
@st.cache(ttl=600)
def get_words(
    user_id: Optional[int], chat_id: Optional[int], from_: datetime.datetime, till: datetime.datetime
) -> pd.DataFrame:
    # include last day
    till = till + datetime.timedelta(days=1)
    with connection.cursor() as cursor:
        sql = """
        select wd.id         as id,
               wd.text       as text,
               wd.created_at as created_at,
               st.text       as source_text
        from word wd
            left join word_source_text wst on wd.id = wst.word_id
            left join source_text st on st.id = wst.source_text_id
        where wd.created_at >= %s and wd.created_at < %s;
        """
        cursor.execute(sql, [from_, till])
        data = cursor.fetchall()
        df = pd.DataFrame.from_records(data, columns=["id", "text", "created_at", "source_text"])
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

    word_df = get_words(user_id, chat_id, from_date, till_date)

    st.pyplot(make_word_cloud(word_df["text"].tolist()))

    word = st.selectbox("Слово", options=sorted(word_df["text"].drop_duplicates()))
    for text in word_df[word_df["text"] == word]["source_text"]:
        st.write(text)
        st.write("\n")


if __name__ == "__main__":
    main()
