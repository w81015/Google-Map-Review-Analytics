import streamlit as st

def check_data_availability(need_processed_data=False):
    """
    檢查是否有可用的資料，並引導用戶到輸入頁面(如果需要)
    
    Args:
        need_processed_data (bool): 若為True，則同時需要df_reviews和df；若為False，則只需要df_reviews
        
    Returns:
        若need_processed_data為False，返回df_reviews或None
        若need_processed_data為True，返回(df_reviews, df)或(None, None)
    """
    if 'df_reviews' not in st.session_state or st.session_state.df_reviews is None:
        if need_processed_data:
            return None, None
        else:
            return None
            
    if need_processed_data:
        if 'df' not in st.session_state or st.session_state.df is None:
            return None, None
        return st.session_state.df_reviews, st.session_state.df
    else:
        return st.session_state.df_reviews