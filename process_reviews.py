import jieba
import jieba.analyse
import re
import pandas as pd
from snownlp import SnowNLP
from get_reviews import main

# 加載使用者自定義資源，包括字典和停用詞
def load_user_resources():
    jieba.load_userdict('userdict.txt')
    stopwords = set()
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stopwords.add(line.strip())
    return stopwords


# 提取文本中的關鍵詞
def extract_keywords(text, max_keywords=5, threshold=0.1):
    keywords_with_weights = jieba.analyse.textrank(text, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    # 根據權重篩選並限制關鍵詞數量
    filtered_keywords = [kw for kw, weight in keywords_with_weights if weight >= threshold][:max_keywords]
    return ', '.join(filtered_keywords)


# 將文本分割成句子
def split_sentences(text):
    sentences = re.split(r'[。！!？?；;：，\n\s]+', text)  # 以句子為單位分割文本
    return [s.strip() for s in sentences if s.strip()]  # 去除空白句子


# 將句子分詞，並過濾停用詞
def tokenize_sentence(sentence, stopwords):
    words = jieba.cut(sentence)
    return ' '.join([word for word in words if word not in stopwords])  # 返回分詞結果


# 根據分詞結果為句子分配分類標籤
def classify_sentence(sentence, word_list, category_keywords):
    for category, keywords in category_keywords.items():
        if any(keyword in word_list for keyword in keywords):
            return category  # Return the first matched category
    return "其他"  # Return "其他" if no labels match


# 將文本分割、分詞並進行分類
def split_tokenize_and_classify(text, stopwords, category_keywords):
    sentences = split_sentences(text)
    results = []
    for s in sentences:
        words = tokenize_sentence(s, stopwords)
        label = classify_sentence(s, words, category_keywords)
        results.append({'sentence': s, 'word': words, 'label': label})
    return results


# 將每條原始資料的句子展開為多行
def expand_sentences_in_dataframe(df, stopwords, category_keywords):
    expanded_rows = []

    for _, row in df.iterrows():
        sentences_info = split_tokenize_and_classify(row['text'], stopwords, category_keywords)  # 分割文本並分類
        for info in sentences_info:
            expanded_rows.append({
                'text': row['text'],
                'rating': row['review_rating'],
                'sentence': info['sentence'],
                'word': info['word'],
                'label': info['label'],
                'keyword': row['keyword'],
                'index': row['index']
            })
    
    return pd.DataFrame(expanded_rows)  # 返回展開後的DataFrame


# 進行情感分析，返回情感分數
def sentiment_analysis(sentence):
    s = SnowNLP(sentence)
    return s.sentiments  # 返回情感分數，範圍為0~1


# 主程式
def main_process(location, number):
    stopwords = load_user_resources()

    # 呼叫爬蟲程式
    df_reviews, reviews_data, search_name, desired_reviews = main(location, number)
    df = pd.DataFrame(reviews_data)
    df['index'] = range(1, len(df)+1)

    # 提取關鍵詞
    df['keyword'] = df['text'].apply(lambda x: extract_keywords(x, max_keywords=5))

    # 分類關鍵詞
    category_keywords = {
        "食物": ["爆漿", "拿鐵", "熱騰騰", "融化", "薯條", "美乃滋", "醬", "冰", "蜂蜜", "抹茶", "巧克力", "餡料", "內餡", "餡", "爆漿", "肉", "雞", "雞肉", "豬", "豬肉", "牛", "牛肉", "蔬菜", "飲料", "美食", "調味", "點心", "早餐", "午餐", "中餐", "下午茶", "晚餐", "宵飮", "消夜", "用料", "小氣", "大方", "香", "軟", "脆", "品質", "口味", "嚼勁", "冷", "酥", "材料", "套餐", "東西", "食物", "鬆餅", "華夫餅", "食材", "餐點", "好吃", "難吃", "吃", "喝", "油", "鹹", "甜", "苦", "辣", "酸", "味道", "份量", "飽", "味口", "甜點", "湯", "麵", "飯", "炸物", "烤肉", "燒烤", "料理", "小吃", "健康", "營養", "新鮮", "美味", "口感", "濃", "清淡", "微辣", "重口味", "淡", "鮮", "醇厚", "濃郁"],
        "服務": ["作業", "流程", "加強", "訓練", "傻眼", "人手不足", "語氣", "邏輯", "規定", "抱歉", "道歉", "工讀生", "臉", "欠", "櫃檯", "點餐", "吼", "服務", "態度", "笑", "臭", "糟糕", "店員", "貼心", "友善", "員工", "店家", "兇", "忙", "專業", "親切", "耐心", "效率", "反應", "收銀", "推薦", "滿意", "不滿意", "失望", "慢", "不專業", "差", "熱情", "不耐煩"],
        "時間": ["上菜", "出單", "出餐", "一早", "人潮", "等待", "時間", "分鐘", "等", "慢", "久", "快", "排", "排隊", "一下", "速度"],
        "價格": ["折扣", "打折", "漲", "漲價", "價格", "偏高", "貴", "cp值", "CP值", "划算", "便宜", "$", "新台幣", "台幣", "實惠", "錢", "性價比", "不划算", "折扣", "優惠", "套餐", "過高", "不值", "低價", "高價"],
        "環境": ["整潔", "氛圍", "清幽", "溫馨", "髒", "乾淨", "吵", "安靜", "蟑螂", "老鼠", "蚊子", "蟲", "蒼蠅", "衛生", "悠閒", "亂", "擠", "舒適", "氣氛", "清潔", "噪音", "空氣", "冷氣", "光線", "佈置", "擁擠", "空間", "座位", "陰暗", "清新", "宜人", "涼爽", "美觀", "裝潢", "餐具", "廁所", "清理", "消毒", "垃圾", "異味", "手部消毒"]
    }

    # 使用展開函數進行處理
    expanded_df = expand_sentences_in_dataframe(df, stopwords, category_keywords)

    # 在DataFrame中應用情感分析，添加情感標籤（正面/負面）
    expanded_df['sentiment_score'] = expanded_df['sentence'].apply(sentiment_analysis)
    expanded_df['sentiment'] = expanded_df['sentiment_score'].apply(lambda x: '正面' if x > 0.5 else '負面')
    return df_reviews, expanded_df


if __name__ == "__main__":
    main_process()