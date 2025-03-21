from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def setup_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def search_and_get_reviews(search_name):
    driver = setup_chrome()
    wait = WebDriverWait(driver, 30)
    
    try:
        # Navigate to Google Maps
        maps_url = "https://www.google.com/maps"
        driver.get(maps_url)
        
        # Search for the name in the Google Maps search box
        print(f"在Google Maps上搜尋{search_name}")
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
        search_box.clear()
        search_box.send_keys(search_name)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the search results to load
        time.sleep(5)
       
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []
    
    return driver

# Define a function to get restaurant information: name, rating, and review count
def get_restaurant_info(wait):
    """
    Get basic information: name, rating, and review count
    """
    try:
        # Get name
        name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_title)))
        store_name = name_element.text
        print(f"店家名稱: {store_name}")
        
        # Get rating
        rating_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.ceNzKf')))
        rating = rating_element.get_attribute('aria-label').split()[0]
        print(f"評分: {rating}")
        
        # Get review count
        review_count_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[aria-label$="則評論"]')))
        review_count_text = review_count_element.text.strip('()')
        review_count = int(review_count_text.replace(',', ''))
        print(f"目前評論數: {review_count}")
        
        return store_name, float(rating), review_count
    except Exception as e:
        print(f"獲取店家資訊時發生錯誤: {str(e)}")
        return None, None, None
    
# Define a function to get restaurant reviews
def get_restaurant_reviews(driver, desired_reviews):
    # driver = setup_chrome()
    # driver.get(url)
    wait = WebDriverWait(driver, 20)
    reviews_data = []
    
    try:
        # Get restaurant info
        store_name, actual_rating, actual_review_count = get_restaurant_info(wait)
        
        # Click reviews tab
        try:
            reviews_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-tab-index="1"]')))
            reviews_tab.click()
            time.sleep(2)
            print("成功點擊評論區")
        except Exception as e:
            print(f"找不到評論區，嘗試其他方法...: {str(e)}")
        
        # Calculate maximum reviews to fetch
        max_reviews = min(desired_reviews, actual_review_count)
        print(f"\n開始載入評論 (目標: {max_reviews} 則)")
        
        # Scroll to load reviews
        last_review_count = 0
        same_count_iterations = 0
        
        while True:
            try:
                # Scroll reviews section
                scrollable_div = driver.find_element(By.CSS_SELECTOR, scroll_container)
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(2)
                
                # Count current reviews
                current_reviews = driver.find_elements(By.CSS_SELECTOR, reviews_area)
                current_count = len(current_reviews)
                print(f"已載入 {current_count} 則評論...", end='\r')
            
                if current_count >= max_reviews:
                    print(f"\n已達到目標數量: {current_count} 則")
                    break
                
                if current_count == last_review_count:
                    same_count_iterations += 1
                    if same_count_iterations >= 5:
                        print(f"\n評論已全部載入，共 {current_count} 則")
                        break
                else:
                    same_count_iterations = 0
                    
                last_review_count = current_count
                
            except Exception as e:
                print(f"\n捲動時發生錯誤: {str(e)}")
                break
        
        # Collect review content with ratings
        try:
            review_elements = driver.find_elements(By.CSS_SELECTOR, each_review_area)
            for element in review_elements[:max_reviews]:
                try:
                    # Try to expand full review
                    try:
                        more_button = element.find_element(By.CSS_SELECTOR, button_for_full_text)
                        driver.execute_script("arguments[0].click();", more_button)
                        time.sleep(0.5)
                    except:
                        pass
                    
                    # Get review text
                    review_text = element.find_element(By.CSS_SELECTOR, each_review).text
                    
                    # Get review rating
                    try:
                        stars_element = element.find_element(By.CSS_SELECTOR, rating_stars)
                        stars_text = stars_element.get_attribute('aria-label')
                        review_rating = int(stars_text[0])  # Extract the first character as the rating
                    except Exception as e:
                        print(f"擷取評分時發生錯誤: {str(e)}")
                        review_rating = None
                    
                    if review_text:
                        reviews_data.append({
                            'text': review_text,
                            'review_rating': review_rating
                        })
                except Exception as e:
                    print(f"擷取評論時發生錯誤: {str(e)}")
                    continue
                    
            print(f"\n成功收集 {len(reviews_data)} 則評論")
            
        except Exception as e:
            print(f"收集評論內容時發生錯誤: {str(e)}")
            
    finally:
        driver.quit()
    
    return reviews_data, store_name, actual_rating, actual_review_count

# Define a function to save reviews to a Pandas DataFrame
def save_reviews_to_dataframe(reviews_data, store_name, actual_rating, actual_review_count):
    """
    Save reviews, restaurant name, rating, and review count to a Pandas DataFrame
    """
    df = pd.DataFrame({
        'Restaurant Name': [store_name] * len(reviews_data),
        'Overall Rating': [actual_rating] * len(reviews_data),
        'Review Count': [actual_review_count] * len(reviews_data),
        'Review': [review['text'] for review in reviews_data],
        'Review Rating': [review['review_rating'] for review in reviews_data]
    })
    return df

# html arguments
target_title = 'h1.DUwDvf' # 搜尋目標的名稱
scroll_container = 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf' # 點擊評論tab後的下面整塊div (滾動頁面用)
reviews_area = 'div.jJc9Ad' # 計算每塊評論
each_review_area = 'div.jJc9Ad' # 每則評論區塊 (含評論者資訊等)
button_for_full_text = 'button.w8nwRe.kyuRq' # 「全文」按鈕
each_review = 'span.wiI7pd' # 每則評論 (只有評論文字)
rating_stars = 'span.kvMYJc' # 評論者的評分 (星星圖案)

def main(location, number):
    search_name = location
    desired_reviews = int(number)
    driver = search_and_get_reviews(search_name)
    reviews_data, store_name, actual_rating, actual_review_count = get_restaurant_reviews(driver, desired_reviews)
    
    if reviews_data:
        print("\n建立 DataFrame...")
        df_reviews = save_reviews_to_dataframe(reviews_data, store_name, actual_rating, actual_review_count)
        
        print("\nDataFrame 前 5 筆資料:")
        print(df_reviews.head())
        
        print("\n評分統計:")
        print(df_reviews['Review Rating'].value_counts().sort_index())
        
        # 返回 df_reviews 和其他變數
        return reviews_data, search_name, desired_reviews
    else:
        print("沒有收集到評論")
        return None, search_name, desired_reviews

if __name__ == "__main__":
    reviews_data, search_name, desired_reviews = main()