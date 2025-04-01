import streamlit as st
from streamlit_option_menu import option_menu

# 設定頁面配置
st.set_page_config(
    page_title="Google Map 餐廳評論分析",
    page_icon="📈",
    layout="wide"
)

# 初始化session_state變數
if 'df_reviews' not in st.session_state:
    st.session_state.df_reviews = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "首頁"

# 頁面標題
st.title("📈 Google Map 餐廳評論分析")

# 使用選單進行頁面導航
selected = option_menu(
    menu_title=None,
    options=["首頁", "評論輸入", "評論摘要", "評分分析", "關鍵詞分析", "主題分析"],
    icons=["house", "search", "clipboard-data", "star", "tags", "chat-square-text"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#007BFF"},
    }
)

# 更新當前頁面到session_state
st.session_state.current_page = selected

# 頁面導航
if selected == "首頁":
    st.write("## 歡迎使用 Google Map 餐廳評論分析系統")
    st.write("""
    本系統可以幫助您分析 Google Map 上餐廳的評論，提供以下功能：
    
    - 評論摘要：整體評分和近期評價趨勢
    - 評分分析：評分分布和各星級評論範例
    - 關鍵詞分析：熱門關鍵詞和相關評論
    - 主題分析：評論主題分布和情感分析
    
    請點擊上方的「評論輸入」開始分析！
    """)
    
elif selected == "評論輸入":
    # 導入評論輸入頁面
    from input_page import show_input_page
    show_input_page()
    
elif selected == "評論摘要":
    # 導入評論摘要頁面
    from summary_page import show_summary_page
    show_summary_page()
    
elif selected == "評分分析":
    # 導入評分分析頁面
    from rating_analysis import show_rating_analysis
    show_rating_analysis()
    
elif selected == "關鍵詞分析":
    # 導入關鍵詞分析頁面
    from keyword_analysis import show_keyword_analysis
    show_keyword_analysis()
    
elif selected == "主題分析":
    # 導入主題分析頁面
    from topic_analysis import show_topic_analysis
    show_topic_analysis()

# 頁腳
st.markdown("---")
st.markdown("### 關於系統")
st.markdown("Google Map 餐廳評論分析系統 by Jared Lin")
url = "https://github.com/w81015"
st.markdown("Github: [link](%s)" % url)