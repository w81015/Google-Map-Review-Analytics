import streamlit as st
import pandas as pd
import plotly.express as px
import random
from collections import Counter
from utils.state_management import check_data_availability

def plot_top_keywords(df):
    """
    繪製熱門關鍵詞長條圖。
    """
    st.subheader("🔥 前 10 大熱門關鍵詞")

    all_words = df["word"].dropna().str.split().explode()
    filtered_words = [word for word in all_words if isinstance(word, str) and len(word) > 1]
    word_counts = Counter(filtered_words)

    top_words = word_counts.most_common(10)
    if top_words:
        df_top_words = pd.DataFrame(top_words, columns=["熱門關鍵詞", "討論聲量"])
        fig = px.bar(
            df_top_words,
            x="熱門關鍵詞",
            y="討論聲量",
            text="討論聲量",
            color="討論聲量",
            color_continuous_scale="Blugrn"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="white",
            font=dict(size=14),
            width=600,
            height=450,
            margin=dict(t=40, b=50, l=50, r=30),
            showlegend=False,
            dragmode=False
        )
        st.plotly_chart(fig, use_container_width=False, 
                        config={"scrollZoom": False, "displayModeBar": False,
                                "doubleClick": False, "showTips": False})
        return df_top_words

    return None


def display_sentences_with_top_words(df, df_top_words):
    """
    顯示包含前幾大熱門關鍵詞的句子。
    """
    if df_top_words is None or df_top_words.empty:
        st.warning("沒有熱門關鍵詞可供篩選句子。")
        return

    top_words = df_top_words["熱門關鍵詞"].head(5).tolist()  # 取前5個熱門詞
    selected_sentences = {}

    for word in top_words:
        matched_sentences = df[df["sentence"].str.contains(word, na=False, case=False)]["sentence"].unique()
        if len(matched_sentences) > 4:
            selected_sentences[word] = random.sample(
                list(matched_sentences),
                min(5, len(matched_sentences))
            )

    st.markdown("###### 熱門關鍵詞的討論內容：")
    st.write("(未顯示代表留言數太少無法分析)")

    for word, sentences in selected_sentences.items():
        with st.container():
            st.markdown(f"<h5 style='color:#007BFF;'>🔹 {word}</h5>", unsafe_allow_html=True)
            for sentence in sentences:
                st.markdown(f"  👉 {sentence}")


def show_keyword_analysis():
    """
    顯示關鍵詞分析頁面
    """
    st.subheader("🔍 關鍵詞分析")
    
    # 檢查是否有可用資料
    df_reviews, df = check_data_availability(need_processed_data=True)
    

    if df is not None:
        st.markdown(f"##### 🍴 {df_reviews.iloc[0]['Restaurant Name']} 🥂")
        df_top_words = plot_top_keywords(df)
        st.markdown("---")
        display_sentences_with_top_words(df, df_top_words)
    else:
        st.warning("⚠️ 尚未取得評論資料，請先前往「評論輸入」頁面進行分析。")
        
        # 加入一個按鈕，讓用戶可以直接跳轉到輸入頁面
        # if st.button("前往評論輸入頁面"):
        #     st.session_state.current_page = "評論輸入"
        #     st.rerun()