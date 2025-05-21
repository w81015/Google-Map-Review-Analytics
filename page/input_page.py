import streamlit as st
from utils.data_loader import load_store_data

def show_input_page():
    """
    顯示標題、輸入欄位及分析按鈕，並在按下按鈕後進行評論抓取及分析。
    """
    st.subheader("📝 輸入店家資訊")
    st.write("請選擇**店家名稱**，系統將呈現預先爬取的評論與分析成果。")
    st.write("此頁面為免費版，進階版可以直接輸入店家名稱並即時爬取最新Google Map留言。")

    # 使用卡片式區塊包裝輸入欄位
    with st.container():
        st.subheader("1️⃣ 請選擇店家🍽️")
        col1, col2 = st.columns([0.05, 0.95])
        with col2:
            store_list = ["阜杭豆漿", "小木屋鬆餅(台大店)", "Juicy Bun Burger 就是棒 美式餐廳 政大店"]
            location = st.radio(
                "",
                store_list,
                index=0,
                horizontal=True
            )

    st.markdown("---")

    # 按鈕分析
    if st.button("🚀 開始分析", help="按下後若無反應，請刷新頁面後再試一次"):
        if location:
            with st.spinner("⏳"):
                # 根據使用者選擇讀取資料
                df_reviews, df = load_store_data(location)

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
    
    # 如果已有資料，顯示提示
    elif 'df_reviews' in st.session_state and st.session_state.df_reviews is not None:
        st.success(f"✅ 已完成分析：{st.session_state.df_reviews.iloc[0]['Restaurant Name']}")
        st.info("📊 您可以點擊上方選單查看不同分析結果，或輸入新的店家名稱重新分析。")
