import streamlit as st
import plotly.express as px
import pandas as pd
from collections import Counter
from utils.state_management import check_data_availability

def plot_review_topics(df):
    """
    繪製評論主題分布（排除 '其他' 類別）。
    """
    label_counts = df["label"].value_counts().reset_index()
    label_counts.columns = ["評論主題", "討論聲量"]

    # 排除「其他」
    label_counts = label_counts[label_counts["評論主題"] != "其他"]

    # 按評論數升序排列
    label_counts = label_counts.sort_values(by="討論聲量", ascending=True)

    # 繪製圖表
    fig = px.bar(
        label_counts,
        x="討論聲量",
        y="評論主題",
        orientation="h",
        text="討論聲量",
        color="討論聲量",
        color_continuous_scale="Burg"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        plot_bgcolor="white",
        font=dict(size=14),
        width=600,
        height=400,
        margin=dict(t=50, b=50, l=50, r=30),
        showlegend=False,
        dragmode=False
    )

    st.subheader("評論主題分布")
    st.plotly_chart(fig, use_container_width=False, 
                        config={"scrollZoom": False, "displayModeBar": False,
                                "doubleClick": False, "showTips": False})


def display_sentiment_analysis(df):
    """
    顯示評論的情感分析，並用互動詞頻圖取代文字雲。
    """
    label_counts = df["label"].value_counts()

    for topic in label_counts.index:
        if topic == "其他":
            continue
        
        st.markdown(f"#### 📌 **{topic} 的討論**") 
        with st.expander(" ", expanded=True):
            col1, col2 = st.columns([1, 1.2])

            with col1:
                pos_reviews = df[
                    (df["label"] == topic)
                    & (df["rating"].isin([4, 5]))
                    & (df["sentiment_score"] > 0.6)
                ]
                neg_reviews = df[
                    (df["label"] == topic)
                    & (df["rating"].isin([1, 2, 3]))
                    & (df["sentiment_score"] < 0.4)
                ]

                st.markdown(
                    "<span style='color: #28a745; font-size: 18px; font-weight: bold;'>✅ 正面評論</span>",
                    unsafe_allow_html=True
                )
                if not pos_reviews.empty:
                    for s in pos_reviews["sentence"].drop_duplicates().sample(
                        min(3, len(pos_reviews)), replace=True
                    ):
                        st.write(f"- {s}")
                else:
                    st.write("目前沒有符合的留言。")
                st.write("")

                st.markdown(
                    "<span style='color: #dc3545; font-size: 18px; font-weight: bold;'>❌ 負面評論</span>",
                    unsafe_allow_html=True
                )
                if not neg_reviews.empty:
                    sample_size = min(3, len(neg_reviews))  
                    for s in neg_reviews["sentence"].drop_duplicates().sample(
                        sample_size, replace=True
                    ):
                        st.write(f"- {s}")
                else:
                    st.write("目前沒有符合的留言。")

            with col2:
                words = " ".join(df[df["label"] == topic]["word"].dropna())

                if words.strip():
                    # 計算詞頻
                    word_counts = Counter(words.split())
                    common_words = word_counts.most_common(10)  # 取前 10 個詞

                    # 轉換為 DataFrame
                    word_df = pd.DataFrame(common_words, columns=["詞語", "次數"])

                    # 用 Plotly 繪製互動式條狀圖
                    fig = px.bar(
                        word_df,
                        x="次數",
                        y="詞語",
                        orientation="h",
                        title=f"「{topic}」的關鍵詞頻率",
                        text="次數",
                        color="次數",
                        color_continuous_scale="blues"
                    )

                    fig.update_traces(textposition="outside")
                    fig.update_layout(yaxis=dict(categoryorder="total ascending"), dragmode=False)

                    st.plotly_chart(fig, use_container_width=True, 
                                        config={"scrollZoom": False, "displayModeBar": False,
                                                "doubleClick": False, "showTips": False})

                else:
                    st.write("目前沒有足夠的詞語來生成詞頻圖。")


def show_topic_analysis():
    """
    顯示主題分析頁面
    """
    st.subheader("📝 主題與情感分析")
    
    # 檢查是否有可用資料
    df_reviews, df = check_data_availability(need_processed_data=True)
    
    if df is not None:
        st.markdown(f"##### 🍴 {df_reviews.iloc[0]['Restaurant Name']} 🥂")
        plot_review_topics(df)
        st.markdown("---")
        display_sentiment_analysis(df)
    else:
        st.warning("⚠️ 尚未取得評論資料，請先前往「評論輸入」頁面進行分析。")
        
        # 加入一個按鈕，讓用戶可以直接跳轉到輸入頁面
        # if st.button("前往評論輸入頁面"):
        #     st.session_state.current_page = "評論輸入"
        #     st.rerun()