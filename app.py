import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from process_reviews import main_process  # 引入函數

def connect():
    st.title("Google Map餐廳評論分析")
    st.write("請輸入店家名稱和欲分析的評論數，我們將進行分析並返回結果。")

    # 使用者輸入
    location = st.text_input("輸入店家名稱", placeholder="例如：小木屋鬆餅(台大店)")
    number = st.number_input("輸入欲分析的評論數", min_value=1, step=1)

    # 按鈕觸發分析
    if st.button("開始分析"):
        if location and number:
            with st.spinner("取得資料並分析中，請稍候..."):
                # 執行 b.py 的函數並捕獲結果
                df = main_process(location, number)
                if df is None or df.empty:
                    st.error("無法獲取資料，請確認輸入店家名稱是否正確。")
                    return None                
                # 顯示 DataFrame
                st.success("分析完成！以下為結果：")
                return df
        else:
            st.error("請完整輸入店家名稱和數字！")
            return None        


def analysis(df):
    if df is not None:
        # Section 2: Average Stars and Sum of Reviews
        col1, col2 = st.columns(2)
        with col1:
            avg_stars = df["rating"].mean()
            total_reviews = len(df)
            st.subheader("平均得分")
            st.metric("Average Stars", round(avg_stars, 2))
            st.subheader("總評論數")
            st.metric("Total Reviews", total_reviews)

        with col2:
            st.subheader("評分分布")
            
            # 1. 取得評分數據並排序
            star_counts = df["rating"].value_counts().sort_index()

            # 2. 使用 Plotly 繪製條形圖
            fig_bar = go.Figure(
                data=[go.Bar(
                    x=star_counts.index,
                    y=star_counts.values,
                    marker=dict(color="skyblue")
                )]
            )

            # 3. 設定圖表標題與軸標籤
            fig_bar.update_layout(
                xaxis_title="評分",
                yaxis_title="數量",
                # title="評分分布",
                plot_bgcolor="white",  # 設定背景為白色
                font=dict(size=14, color="black"),
                width=400,  # 設定圖表寬度
                height=400  # 設定圖表高度
            )

            # 4. 顯示圖表
            st.plotly_chart(fig_bar)

        st.markdown("---")

        # Section 4: Topic, Positive/Negative Keywords, and Sentiment Pie Chart

        # 計算每個主題的評論數量
        label_counts = df["label"].value_counts()

        st.subheader("評論主題分布")
        # 排序評論數量，從大到小
        sorted_labels = label_counts.reset_index()
        sorted_labels.columns = ["評論主題", "評論數"]
        sorted_labels = sorted_labels.sort_values(by="評論數", ascending=True)  # 按評論數排序

        # 繪製條形圖
        fig_bar = px.bar(
            sorted_labels,
            x="評論數",
            y="評論主題",
            orientation="h",
            text="評論數",
            color="評論數",
            color_continuous_scale="Blues",
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(xaxis_title="評論數", yaxis_title="評論主題", showlegend=False)

        # 顯示圖表
        st.plotly_chart(fig_bar)


        st.subheader(f"評論主題{label_counts.index[0]}的情感分布")
        sentiments_topic = df[df["label"] == label_counts.index[0]]["sentiment"].value_counts()
        sentiments_df = sentiments_topic.reset_index()
        sentiments_df.columns = ["情感", "數量"]

        fig_pie = px.pie(
            sentiments_df,
            names="情感",
            values="數量",
            title=f"主題{label_counts.index[0]}的情感分布",
            color="情感",
            color_discrete_map={"正面": "#66b3ff", "負面": "#ff9999", "中性": "#99ff99"},
        )
        st.plotly_chart(fig_pie)


        col5, col6 = st.columns(2)

        with col5:
            st.subheader(f"{label_counts.index[0]}正面評論")
            positive_sentences = df[df["sentiment"] == "正面"]["sentence"].sample(n=3, replace=True).tolist()
            for s in positive_sentences:
                st.write(f"- {s}")

        with col6:
            st.subheader(f"{label_counts.index[0]}負面評論")
            negative_sentences = df[df["sentiment"] == "負面"]["sentence"].sample(n=3, replace=True).tolist()
            for s in negative_sentences:
                st.write(f"- {s}")

        col7, col8 = st.columns(2)

        with col7:
            st.subheader(f"{label_counts.index[0]}正面關鍵詞")
            # 篩選出正面情緒並符合 topic_name 的數據
            positive_data = df[(df["sentiment"] == "正面") & (df["label"] == label_counts.index[0])]
            # 根據 'index' 合併相同的行，保持每個 'index' 只保留一條資料
            original_data_p = positive_data.groupby('index').first().reset_index()
            # 拆分 'keyword' 欄位中的關鍵詞並將其展開為一個列表
            all_keywords = original_data_p['keyword'].str.split(',').explode().str.strip()
            # 計算最常見的五個關鍵詞
            keyword_counts = all_keywords.value_counts().head(10)
            # 顯示最常見的五個關鍵詞
            st.write(", ".join(keyword_counts.index.tolist()))

        with col8:
            st.subheader(f"{label_counts.index[0]}負面關鍵詞")
            # 篩選出正面情緒並符合 topic_name 的數據
            negative_data = df[(df["sentiment"] == "負面") & (df["label"] == label_counts.index[0])]
            # 根據 'index' 合併相同的行，保持每個 'index' 只保留一條資料
            original_data_n = negative_data.groupby('index').first().reset_index()
            # 拆分 'keyword' 欄位中的關鍵詞並將其展開為一個列表
            all_keywords = original_data_n['keyword'].str.split(',').explode().str.strip()
            # 計算最常見的五個關鍵詞
            keyword_counts = all_keywords.value_counts().head(10)
            # 顯示最常見的五個關鍵詞
            st.write(", ".join(keyword_counts.index.tolist()))

        st.markdown("---")

        # Section 3: Random 5-Star Reviews
        # 篩選 5 星與 4 星評論，並隨機取樣
    # 先檢查每個評價星數的子集是否有資料，然後進行抽樣
        five_star_reviews = df[df["rating"] == 5]["text"]
        if not five_star_reviews.empty:
            five_star_review = five_star_reviews.sample(n=1, replace=True).iloc[0]
        else:
            five_star_review = None  # 或其他處理方式

        four_star_reviews = df[df["rating"] == 4]["text"]
        if not four_star_reviews.empty:
            four_star_review = four_star_reviews.sample(n=1, replace=True).iloc[0]
        else:
            four_star_review = None  # 或其他處理方式

        three_star_reviews = df[df["rating"] == 3]["text"]
        if not three_star_reviews.empty:
            three_star_review = three_star_reviews.sample(n=1, replace=True).iloc[0]
        else:
            three_star_review = None  # 或其他處理方式

        two_star_reviews = df[df["rating"] == 2]["text"]
        if not two_star_reviews.empty:
            two_star_review = two_star_reviews.sample(n=1, replace=True).iloc[0]
        else:
            two_star_review = None  # 或其他處理方式

        one_star_reviews = df[df["rating"] == 1]["text"]
        if not one_star_reviews.empty:
            one_star_review = one_star_reviews.sample(n=1, replace=True).iloc[0]
        else:
            one_star_review = None  # 或其他處理方式


        # 構造直接用於顯示的列表
        review_data = [
            {"Google評分": 5, "評論": five_star_review},
            {"Google評分": 4, "評論": four_star_review},
            {"Google評分": 3, "評論": three_star_review},
            {"Google評分": 2, "評論": two_star_review},
            {"Google評分": 1, "評論": one_star_review},
        ]

        review_df = pd.DataFrame(review_data)

        # 使用 st.dataframe 並隱藏索引
        st.subheader("隨機生成各星評論")
        st.markdown(review_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)


def main():
    df = connect()
    analysis(df)

if __name__ == "__main__":
    main()
