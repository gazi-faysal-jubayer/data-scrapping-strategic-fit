import scrapy
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from restaurant_reviews_scraper.utils.selenium_utils import initialize_driver, scroll_reviews, extract_reviews
import time

class GoogleMapsSpider(scrapy.Spider):
    name = "google_maps_spider"
    allowed_domains = ["google.com"]
    
    def __init__(self, restaurant_name=None, *args, **kwargs):
        super(GoogleMapsSpider, self).__init__(*args, **kwargs)
        self.restaurant_name = restaurant_name or "McDonald's Toronto"
        self.start_urls = ["https://www.google.com/maps"]

    def start_requests(self):
        # We need to return a Request object for Scrapy to work
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # This is a placeholder - we'll use Selenium directly
        driver = initialize_driver()
        try:
            driver.get(self.start_urls[0])
            time.sleep(2)

            search_box = driver.find_element(By.ID, "searchboxinput")
            search_box.send_keys(self.restaurant_name)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)

            self.parse_search_results(driver)
        except Exception as e:
            self.logger.error(f"Error in parse: {str(e)}")
        finally:
            driver.quit()

    def parse_search_results(self, driver):
        try:
            results = driver.find_elements(By.CSS_SELECTOR, '.hfpxzc')
            if results:
                results[0].click()
                time.sleep(3)
                self.parse_reviews(driver)
            else:
                self.logger.info("No search results found.")
        except Exception as e:
            self.logger.error(f"Error accessing search results: {str(e)}")

    def parse_reviews(self, driver):
        try:
            # Try to find and click on reviews
            possible_review_buttons = [
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
                        self.logger.info(f"Found review button with selector: {selector}")
                        elements[0].click()
                        review_clicked = True
                        time.sleep(3)
                        break
                except Exception:
                    continue
            
            if not review_clicked:
                self.logger.info("Trying secondary approach for reviews")
                reviews_section = driver.find_elements(By.XPATH, 
                    "//div[contains(@aria-label, 'star')]//following::div[contains(., 'review') and not(contains(., '@'))]")
                if reviews_section:
                    reviews_section[0].click()
                    review_clicked = True
                    time.sleep(3)
            
            if review_clicked:
                self.logger.info("Scrolling reviews...")
                scroll_reviews(driver)
                
                review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
                for elem in review_elements:
                    try:
                        author = elem.find_element(By.CLASS_NAME, 'd4r55').text
                        rating = elem.find_element(By.CSS_SELECTOR, 'span.KkqgAe span').get_attribute("aria-label")
                        text = elem.find_element(By.CLASS_NAME, 'wiI7pd').text
                        yield {
                            'author': author,
                            'rating': rating,
                            'text': text
                        }
                    except Exception as e:
                        self.logger.error(f"Error extracting review: {str(e)}")
            else:
                self.logger.error("Could not locate reviews section")
                
        except Exception as e:
            self.logger.error(f"Error accessing reviews: {str(e)}")