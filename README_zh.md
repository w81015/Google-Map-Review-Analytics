[English version 英文版](README.md)

# Google Map 餐廳評論分析系統

📈 一個以 Streamlit 打造的網頁應用，幫助使用者分析 Google Map 餐廳評論的情緒與主題。

---

## 🔧 功能介紹

本系統提供以下功能頁面：

- **首頁**：功能說明與導覽入口
- **評論輸入**：上傳餐廳評論資料以進行分析
- **評論摘要**：顯示評論的總體趨勢與統計摘要
- **評分分析**：展示評論的星等分布與細節
- **關鍵詞分析**：找出熱門關鍵詞與關聯評論
- **主題分析**：透過主題建模技術提取評論主題內容

---

## 🖥️ 技術架構

### 📦 前端

- **Streamlit**：快速構建互動式網頁應用
- **streamlit-option-menu**：美觀的選單導航介面

### 🧪 後端

- **資料抓取**（`utils/get_reviews.py`）：
  - 使用 Selenium 自動化爬取 Google Maps 上指定餐廳的評論
  - 自動點擊、滾動載入所有可見評論
  - 擷取評論文字與星等評分，並儲存為 pandas DataFrame

- **資料處理與分析**（`utils/process_reviews.py`）：
  - 使用 jieba 斷詞與 TextRank 萃取關鍵詞
  - 使用 Snownlp 進行情感分析
  - 根據定義好的關鍵詞分類評論句子（如：食物、服務、環境…）
  - 將每條評論展開為多句進行細緻分析

---

## 🗂️ 專案結構

```
📁 your_project/
│
├── app.py                     # 主介面與頁面控制
├── page/                      # 分頁模組
│   ├── input_page.py
│   ├── summary_page.py
│   ├── rating_analysis.py
│   ├── keyword_analysis.py
│   └── topic_analysis.py
│
├── utils/                     # 功能模組
│   ├── get_reviews.py         # 爬蟲模組，負責抓取評論
│   └── process_reviews.py     # 處理模組，負責分析評論
│
├── userdict.txt               # 使用者自定義斷詞字典
├── stopwords.txt              # 停用詞列表
```

---

## ▶️ 使用方式

### 安裝套件

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install streamlit streamlit-option-menu selenium webdriver-manager snownlp jieba pandas
```

### 執行 Streamlit 應用

```bash
streamlit run app.py
```

---

## 📌 注意事項

- 執行爬蟲需具備 Chrome 瀏覽器與相容版本的 ChromeDriver（`webdriver-manager` 自動安裝）。
- 分類規則定義於 `process_reviews.py`，可依需要擴充或調整分類關鍵詞。
- 預設情感分析使用 Snownlp，如需更準確可改用 BERT 或繁體語料訓練模型。

---

## 🙋‍♂️ 開發者資訊

- 開發者：Jared Lin
- Github：[https://github.com/w81015](https://github.com/w81015)

---

此系統旨在協助餐飲業者、資料分析師或研究者，快速理解評論趨勢與潛在議題。
