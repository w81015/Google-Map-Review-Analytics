import streamlit as st
from state_management import check_data_availability

def display_summary(df_reviews):
    """
    顯示評論摘要，含店家名稱、評分、留言數及打卡提示。
    """

    # Metrics Section
    st.markdown("#### 🌟 評分總覽")
    st.columns([0.5, 0.5])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Google Map 所有留言評分", df_reviews.iloc[0]["Overall Rating"])
        st.metric("抓取留言平均得分", round(df_reviews["Review Rating"].mean(), 1))

    with col2:
        st.metric("Google Map 所有留言數", df_reviews.iloc[0]["Review Count"])
        st.metric("抓取留言數", len(df_reviews))

    # Review Analysis
    avg_rating = round(df_reviews["Review Rating"].mean(), 1)
    overall_rating = df_reviews.iloc[0]["Overall Rating"]
    comparison = "較高" if avg_rating > overall_rating else "較低" if avg_rating < overall_rating else "相當"

    interpretation = {
        "較高": "顯示近期評價可能趨向正面，店家服務或品質可能有所提升。",
        "較低": "顯示近期評價可能趨向負面，店家服務或品質可能有所下降。",
        "相當": "顯示近期評價與過去評價相當，店家評價穩定。"
    }[comparison]

    st.markdown("#### 📊 留言分析")
    st.write(
        f"在已抓取的 **{len(df_reviews)}** 條留言中，平均得分為 **{avg_rating}**，"
        f"比 Google Map 上的整體評分 **{overall_rating}** {comparison}。"
    )
    st.success(interpretation)

    # Checking for promotional keywords
    df_reviews['contains_checkwords'] = df_reviews['Review'].apply(
        lambda review: any(kw in review for kw in ["打卡", "送"])
    )
    checkwords_count = df_reviews['contains_checkwords'].sum()

    # Display promotional message if necessary
    st.markdown("### 🔍 打卡活動偵測")
    if checkwords_count >= 3:
        st.warning("📌 留言中多次出現「打卡」或「送」等詞彙，店家可能提供優惠以提升評分。")
    else:
        st.info("📌 留言中沒有明顯的打卡活動痕跡。")


def show_summary_page():
    """
    顯示評論摘要頁面
    """

    st.subheader("📊 評論摘要")
    
    # 檢查是否有可用資料
    df_reviews = check_data_availability()

    if df_reviews is not None:
        st.markdown(f"##### 🍴 {df_reviews.iloc[0]['Restaurant Name']} 🥂")
        display_summary(df_reviews)
    else:
        st.warning("⚠️ 尚未取得評論資料，請先前往「評論輸入」頁面進行分析。")
        
        # 加入一個按鈕，讓用戶可以直接跳轉到輸入頁面
        if st.button("前往評論輸入頁面"):
            st.session_state.current_page = "評論輸入"
            st.rerun()