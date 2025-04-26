import pandas as pd
import os

def load_store_data(location: str, folder: str = "data"):
    """
    根據中文店名 location 直接讀取 data 資料夾中的 df_reviews 和 df 檔案

    例如 location = "麥當勞"
    對應讀取：data/麥當勞.csv 和 data/麥當勞_reviews.csv
    """
    df_path = os.path.join(folder, f"{location}.csv")
    df_reviews_path = os.path.join(folder, f"{location}_reviews.csv")

    # 檢查檔案是否存在
    if not os.path.exists(df_path):
        raise FileNotFoundError(f"找不到檔案：{df_path}")
    if not os.path.exists(df_reviews_path):
        raise FileNotFoundError(f"找不到檔案：{df_reviews_path}")

    df = pd.read_csv(df_path)
    df_reviews = pd.read_csv(df_reviews_path)

    return df_reviews, df
