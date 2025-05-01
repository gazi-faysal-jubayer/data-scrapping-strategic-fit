import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scroll_reviews(driver):
    for _ in range(20):
        driver.execute_script('''const scrollable = document.querySelector('div[aria-label="Reviews"] div'); if (scrollable) scrollable.scrollBy(0, 500);''')
        time.sleep(1)

def extract_reviews(driver):
    reviews = []
    review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
    
    for elem in review_elements:
        try:
            author = elem.find_element(By.CLASS_NAME, 'd4r55').text
            rating = elem.find_element(By.CSS_SELECTOR, 'span.KkqgAe span').get_attribute("aria-label")
            text = elem.find_element(By.CLASS_NAME, 'wiI7pd').text
            reviews.append({'author': author, 'rating': rating, 'text': text})
        except Exception as e:
            print(f"Error extracting review: {str(e)}")
            continue
    return reviews