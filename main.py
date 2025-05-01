import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

driver = uc.Chrome(version_main=135)

def scroll_reviews(driver):
    """Scroll the reviews panel to load more reviews."""
    for _ in range(20):  # Adjust for how many you want
        driver.execute_script('''
            const scrollable = document.querySelector('div[aria-label="Reviews"] div');
            if (scrollable) scrollable.scrollBy(0, 500);
        ''')
        time.sleep(1)

def get_reviews(driver):
    reviews = []
    review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
    print(f"Found {len(review_elements)} review elements")
    
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

def scrape_restaurant_reviews(restaurant_name):
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get("https://www.google.com/maps")
        print("Loading Google Maps...")

        # Wait for search box to be present and interactable
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchboxinput")))
        search_box.send_keys(restaurant_name)
        search_box.send_keys(Keys.ENTER)
        print(f"Searching for: {restaurant_name}")

        # Wait for search results
        try:
            # Wait for results to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.hfpxzc')))
            
            # Click on first result
            results = driver.find_elements(By.CSS_SELECTOR, '.hfpxzc')
            if results:
                results[0].click()
                print("Clicked on first result")
                time.sleep(3)  # Let the place details load

                # Try multiple ways to find and click the reviews section
                try:
                    # Look for elements that might open reviews
                    possible_review_buttons = [
                        # Look for elements containing review information
                        "//button[contains(@aria-label, 'review')]",
                        "//button[contains(@jsaction, 'review')]",
                        "//span[contains(text(), 'review')]/ancestor::button",
                        "//div[contains(@aria-label, 'review') and @role='button']"
                    ]
                    
                    review_clicked = False
                    for selector in possible_review_buttons:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements:
                                print(f"Found review button with selector: {selector}")
                                elements[0].click()
                                review_clicked = True
                                time.sleep(3)
                                break
                        except Exception:
                            continue
                    
                    if not review_clicked:
                        print("Could not find reviews button - trying secondary approach")
                        # Try clicking on the reviews count/section
                        reviews_section = driver.find_elements(By.XPATH, 
                            "//div[contains(@aria-label, 'star')]//following::div[contains(., 'review') and not(contains(., '@'))]")
                        if reviews_section:
                            reviews_section[0].click()
                            review_clicked = True
                            time.sleep(3)
                    
                    if review_clicked:
                        print("Starting to scroll reviews...")
                        scroll_reviews(driver)
                        reviews = get_reviews(driver)
                        print(f"Total reviews collected: {len(reviews)}")
                        for r in reviews:
                            print(r)
                    else:
                        print("Could not locate any reviews section")
                        
                except Exception as e:
                    print(f"Error accessing reviews: {str(e)}")
            else:
                print("No search results found.")
                
        except TimeoutException:
            print("Timed out waiting for search results")
    
    finally:
        print("Closing browser")
        driver.quit()

if __name__ == "__main__":
    # Example usage
    scrape_restaurant_reviews("McDonald's Toronto")
