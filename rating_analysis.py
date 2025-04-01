import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from state_management import check_data_availability

def plot_rating_distribution(df_reviews):
    """
    繪製留言評分分布圖。
    """
    st.subheader("📊 留言評分分布")
    st.write(f"（此為抓取的 {len(df_reviews)} 則留言評分，而非 Google Map 上所有留言評分）")

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
        margin=dict(t=40, b=50, l=50, r=30),
        showlegend=False,
        xaxis=dict(tickmode='array', tickvals=list(all_ratings))
    )

    st.plotly_chart(fig, use_container_width=False, config={"scrollZoom": False, "displayModeBar": False})
    return star_counts


def manage_reviews(df_reviews, star_counts):
    """
    管理和顯示各星級評論
    """
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


def show_rating_analysis():
    """
    顯示評分分析頁面
    """
    st.subheader("⭐ 評分分析")
    
    # 檢查是否有可用資料
    df_reviews = check_data_availability()

    
    if df_reviews is not None:
        st.markdown(f"##### 🍴 {df_reviews.iloc[0]['Restaurant Name']} 🥂")
        star_counts = plot_rating_distribution(df_reviews)
        st.markdown("---")
        manage_reviews(df_reviews, star_counts)
    else:
        st.warning("⚠️ 尚未取得評論資料，請先前往「評論輸入」頁面進行分析。")
        
        # 加入一個按鈕，讓用戶可以直接跳轉到輸入頁面
        if st.button("前往評論輸入頁面"):
            st.session_state.current_page = "評論輸入"
            st.rerun()