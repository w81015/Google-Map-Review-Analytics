import streamlit as st
from utils.process_reviews import main_process

def show_input_page():
    """
    顯示標題、輸入欄位及分析按鈕，並在按下按鈕後進行評論抓取及分析。
    """
    st.subheader("📝 輸入店家資訊")
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
            with st.spinner("⏳ 抓取評論需 1-3 分鐘（免費版請見諒🙇‍♂️...）\n請耐心等待，並請勿在抓取時切換頁面。"):
                # 執行分析函數
                df_reviews, df = main_process(location, number)

                # 結果處理
                if df is None or df.empty:
                    st.error("❌ 無法獲取資料，請確認輸入店家名稱是否正確。")
                else:
                    st.success("✅ 分析完成！")

                    # 將抓取到的結果儲存到 session_state
                    st.session_state.df_reviews = df_reviews
                    st.session_state.df = df
                    
                    # 顯示導引
                    st.info("📊 請點擊上方選單查看不同分析結果：")
                    st.markdown("""
                    - **評論摘要**：整體評分和近期評價趨勢
                    - **評分分析**：評分分布和各星級評論
                    - **關鍵詞分析**：熱門關鍵詞和相關評論
                    - **主題分析**：評論主題分布和討論內容
                    """)
        else:
            if not location:
                st.warning("⚠️ **請輸入店家名稱！**")
            if not number:
                st.warning("⚠️ **請選擇評論數量！**")
    
    # 如果已有資料，顯示提示
    elif 'df_reviews' in st.session_state and st.session_state.df_reviews is not None:
        st.success(f"✅ 已完成分析：{st.session_state.df_reviews.iloc[0]['Restaurant Name']}")
        st.info("📊 您可以點擊上方選單查看不同分析結果，或輸入新的店家名稱重新分析。")