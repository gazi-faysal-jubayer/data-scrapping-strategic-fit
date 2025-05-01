# FILE: /restaurant_reviews_scraper/restaurant_reviews_scraper/restaurant_reviews_scraper/settings.py

BOT_NAME = 'restaurant_reviews_scraper'

SPIDER_MODULES = ['restaurant_reviews_scraper.spiders']
NEWSPIDER_MODULE = 'restaurant_reviews_scraper.spiders'

USER_AGENT = 'restaurant_reviews_scraper (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
   'restaurant_reviews_scraper.pipelines.RestaurantReviewPipeline': 300,  # Changed from RestaurantReviewsPipeline
}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# This setting is used to avoid getting blocked by the website
DOWNLOAD_DELAY = 2

# Enable or disable extensions
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Enable or disable the AutoThrottle extension (disabled by default)
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'