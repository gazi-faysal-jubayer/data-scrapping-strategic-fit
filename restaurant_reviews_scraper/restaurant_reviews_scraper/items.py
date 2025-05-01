import scrapy

class RestaurantReviewItem(scrapy.Item):
    author = scrapy.Field()
    rating = scrapy.Field()
    text = scrapy.Field()