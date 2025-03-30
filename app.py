import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from process_reviews import main_process  # 引入函數


def connect():
    """
    顯示標題、輸入欄位及分析按鈕，並在按下按鈕後進行評論抓取及分析。
    """
    st.title("📈 Google Map 餐廳評論分析")
    st.write("請輸入**店家名稱**與**評論數量**，系統將爬取評論並進行分析。")

    # 使用卡片式區塊包裝輸入欄位
    with st.container():
        st.subheader("1️⃣ 請輸入店家名稱🍽️")
        col1, col2 = st.columns([0.05, 0.95])
        with col2:
            location = st.text_input(
                "* 請確保名稱與 Google Map 上的完全一致",
                placeholder="例如：小木屋鬆餅(台大店)"
            )

        st.subheader("2️⃣ 請選擇評論數量📝")
        col1, col2 = st.columns([0.05, 0.95])
        with col2:
            number = st.radio(
                "* 評論數量越多，爬取時間會越久",
                [5, 10, 20, 30, 40, 50],
                horizontal=True,
                index=0
            )

    # 分隔線
    st.markdown("---")

    # 按鈕觸發分析
    if st.button("🚀 開始分析", help="按下後若無反應，請刷新頁面後再試一次"):
        if location and number:
            with st.spinner("⏳ 抓取評論需 1-3 分鐘（免費版請見諒🙇‍♂️），請稍候..."):
                # 執行分析函數
                df_reviews, df = main_process(location, number)

                # 結果處理
                if df is None or df.empty:
                    st.error("❌ 無法獲取資料，請確認輸入店家名稱是否正確。")
                    return None, None
                st.success("✅ 分析完成！以下為結果：")

                # 將抓取到的結果儲存到 session_state
                st.session_state.df_reviews = df_reviews
                st.session_state.df = df
                return df_reviews, df
        else:
            if not location:
                st.warning("⚠️ **請輸入店家名稱！**")
                return None, None
            if not number:
                st.warning("⚠️ **請選擇評論數量！**")
                return None, None

    # 若尚未按「開始分析」，但 session_state 中已有資料，直接回傳
    if 'df_reviews' in st.session_state and 'df' in st.session_state:
        return st.session_state.df_reviews, st.session_state.df

    return None, None


def display_summary(df_reviews):
    """
    顯示評論摘要，含店家名稱、評分、留言數及打卡提示。
    """
    st.header(f"🍴{df_reviews.iloc[0]['Restaurant Name']} 🥂")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Google Map 評分", df_reviews.iloc[0]["Overall Rating"])
        st.metric("抓取留言平均得分", round(df_reviews["Review Rating"].mean(), 1))

    with col2:
        st.metric("Google Map 總留言數", df_reviews.iloc[0]["Review Count"])
        st.metric("已抓取留言數", len(df_reviews))

    avg_rating = round(df_reviews["Review Rating"].mean(), 1)
    overall_rating = df_reviews.iloc[0]["Overall Rating"]
    comparison = "較高" if avg_rating > overall_rating else "較低" if avg_rating < overall_rating else None
    interpretation = (
        "顯示近期評價可能趨向正面，店家服務或品質可能有所提升。" if avg_rating > overall_rating else
        "顯示近期評價可能趨向負面，店家服務或品質可能有所下降。" if avg_rating < overall_rating else
        "顯示近期評價與過去評價相當，店家評價穩定。"
    )

    if comparison:
        st.write(
            f"分析結果顯示：在已抓取的 {len(df_reviews)} 條留言中，平均得分為 {avg_rating}，"
            f"比 Google Map 上顯示的整體評分{overall_rating} {comparison}。{interpretation}"
        )
    else:
        st.write(
            f"分析結果顯示：在已抓取的 {len(df_reviews)} 條留言中，平均得分為 {avg_rating}，"
            f"與 Google Map 上顯示的整體評分相同。{interpretation}"
        )

    # 檢查每條 Review 是否包含「打卡」或「送」
    df_reviews['contains_checkwords'] = df_reviews['Review'].apply(
        lambda review: '打卡' in review or '送' in review
    )

    # 計算出現「打卡」或「送」的評論數量
    checkwords_count = df_reviews['contains_checkwords'].sum()

    # 只要有3則或以上出現「打卡」或「送」，顯示提示
    if checkwords_count >= 3:
        st.write("留言中出現打卡或送等，店家可能提供優惠以提升評分。")

    st.markdown("---")


def plot_rating_distribution(df_reviews):
    """
    繪製留言評分分布圖。
    """
    st.subheader("📊 留言評分分布")
    st.write(f"此為抓取的 {len(df_reviews)} 則留言分布，而非 Google Map 上所有留言。")

    star_counts = df_reviews["Review Rating"].value_counts().sort_index()
    all_ratings = range(1, 6)
    complete_star_counts = pd.Series(
        [star_counts.get(rating, 0) for rating in all_ratings],
        index=all_ratings
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=complete_star_counts.index,
                y=complete_star_counts.values,
                marker=dict(color="skyblue")
            )
        ]
    )

    fig.update_layout(
        xaxis_title="評分",
        yaxis_title="留言數量",
        plot_bgcolor="white",
        font=dict(size=14),
        width=600,
        height=400,
        margin=dict(t=30, b=50, l=50, r=30),
        showlegend=False,
        xaxis=dict(tickmode='array', tickvals=list(all_ratings))
    )

    st.plotly_chart(fig, use_container_width=False, config={"scrollZoom": False, "displayModeBar": False})
    st.markdown("---")
    return star_counts


def manage_reviews(df_reviews, star_counts):
    st.subheader("⭐ 觀看各星評論")
    
    # 初始化 review_samples
    if "review_samples" not in st.session_state:
        st.session_state.review_samples = {}
        for rating in range(5, 0, -1):
            reviews = df_reviews[df_reviews["Review Rating"] == rating]["Review"]
            st.session_state.review_samples[rating] = (
                reviews.sample(n=1, replace=True).iloc[0] if not reviews.empty else "無評論"
            )
    
    # 初始化展開狀態
    if "expanded_rating" not in st.session_state:
        st.session_state.expanded_rating = None
    
    for rating in range(5, 0, -1):
        stars = "⭐" * rating
        review_count = star_counts.get(rating, 0)
        
        # 根據儲存的狀態決定是否預設展開
        with st.expander(f"{stars} ({rating} 星評論) - 共 {review_count} 則", expanded=st.session_state.expanded_rating == rating):
            st.write(st.session_state.review_samples[rating])
            
            if st.button(
                f"🔄 重新選取 1 則 {rating} 星評論",
                key=f"btn_{rating}"
            ):
                reviews = df_reviews[df_reviews["Review Rating"] == rating]["Review"]
                st.session_state.review_samples[rating] = (
                    reviews.sample(n=1, replace=False).iloc[0] if not reviews.empty else "無評論"
                )
                
                # 設定當前展開的 expander
                st.session_state.expanded_rating = rating
                st.rerun()

    st.markdown("---")


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
            height=400,
            margin=dict(t=30, b=50, l=50, r=30),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=False, config={"scrollZoom": False, "displayModeBar": False})
        return df_top_words

    return None


def display_sentences_with_top_words(df, df_top_words):
    """
    顯示包含前三大熱門關鍵詞的句子。
    """
    if df_top_words is None or df_top_words.empty:
        st.warning("沒有熱門關鍵詞可供篩選句子。")
        return

    top_words = df_top_words["熱門關鍵詞"].head(3).tolist()  # 取前三個熱門詞
    selected_sentences = {}

    for word in top_words:
        matched_sentences = df[df["sentence"].str.contains(word, na=False, case=False)]["sentence"].unique()
        if len(matched_sentences) > 4:
            selected_sentences[word] = random.sample(
                list(matched_sentences),
                min(3, len(matched_sentences))
            )

    st.markdown("###### 前3大熱門關鍵詞的討論內容：")
    st.write("未顯示代表留言數太少無法分析。")

    for word, sentences in selected_sentences.items():
        with st.container():
            st.markdown(f"<h5 style='color:#007BFF;'>🔹 {word}</h5>", unsafe_allow_html=True)
            for sentence in sentences:
                st.markdown(f"  👉 {sentence}")

    st.markdown("---")


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
        margin=dict(t=30, b=50, l=50, r=30),
        showlegend=False
    )

    st.subheader("評論主題分布")
    st.plotly_chart(fig, use_container_width=False, config={"scrollZoom": False, "displayModeBar": False})


def display_sentiment_analysis(df):
    """
    顯示評論的情感分析。
    """
    label_counts = df["label"].value_counts()

    for topic in label_counts.index:
        if topic == "其他":
            continue

        with st.expander(f"##### 「{topic}」的討論", expanded=True):
            col1, col2 = st.columns([1, 1.2])

            with col1:
                pos_reviews = df[
                    (df["label"] == topic)
                    & (df["rating"].isin([4, 5]))
                    & (df["sentiment_score"] > 0.8)
                ]
                neg_reviews = df[
                    (df["label"] == topic)
                    & (df["rating"].isin([1, 2]))
                    & (df["sentiment_score"] < 0.3)
                ]

                st.markdown(
                    "<span style='color: #28a745; font-size: 18px; font-weight: bold;'>✅ 正面評論</span>",
                    unsafe_allow_html=True
                )
                if not pos_reviews.empty:
                    for s in pos_reviews["sentence"].drop_duplicates().sample(
                        min(3, len(pos_reviews)), replace=False
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
                    for s in neg_reviews["sentence"].drop_duplicates().sample(
                        min(3, len(neg_reviews)), replace=False
                    ):
                        st.write(f"- {s}")
                else:
                    st.write("目前沒有符合的留言。")

            with col2:
                words = " ".join(df[df["label"] == topic]["word"].dropna())

                if words.strip():
                    wordcloud = WordCloud(
                        font_path="msjh.ttc",
                        width=400,
                        height=300,
                        background_color="white"
                    ).generate(words)

                    fig_wordcloud, ax_wordcloud = plt.subplots(figsize=(4, 3))
                    ax_wordcloud.imshow(wordcloud, interpolation="bilinear")
                    ax_wordcloud.axis("off")
                    st.pyplot(fig_wordcloud)
                else:
                    st.write("目前沒有足夠的詞語來生成文字雲。")


def main():
    """
    主程式入口：只在需要時執行抓取，否則直接顯示先前保存的資料，確保重新選取評論時不產生多餘延遲。
    """
    # 若 session_state 中尚無資料，才執行 connect() 進行爬取或輸入
    if "df_reviews" not in st.session_state or "df" not in st.session_state:
        df_reviews, df = connect()
        # 若用戶已成功抓取/分析，將結果放到 session_state
        if df_reviews is not None and df is not None:
            st.session_state.df_reviews = df_reviews
            st.session_state.df = df

    # 取得資料
    df_reviews = st.session_state.get("df_reviews", None)
    df = st.session_state.get("df", None)

    # 已完成抓取後，依序顯示各項圖表與評論
    if df_reviews is not None and df is not None:
        display_summary(df_reviews)
        star_counts = plot_rating_distribution(df_reviews)
        manage_reviews(df_reviews, star_counts)
        df_top_words = plot_top_keywords(df)
        display_sentences_with_top_words(df, df_top_words)
        plot_review_topics(df)
        display_sentiment_analysis(df)


if __name__ == "__main__":
    main()