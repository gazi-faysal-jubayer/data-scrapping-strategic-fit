# Restaurant Reviews Scraper

This project is a web scraper designed to collect restaurant reviews from Google Maps using Scrapy and Selenium. It automates the process of searching for restaurants and extracting relevant review data, including the author's name, rating, and review text.

## Project Structure

```
restaurant_reviews_scraper/
├── scrapy.cfg               # Scrapy configuration file
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── restaurant_reviews_scraper/
│   ├── __init__.py         # Marks the directory as a Python package
│   ├── items.py            # Defines the data structures for scraped items
│   ├── middlewares.py       # Custom middleware components
│   ├── pipelines.py         # Item pipelines for processing scraped data
│   ├── settings.py          # Configuration settings for the Scrapy project
│   ├── utils/               # Utility functions for the project
│   │   ├── __init__.py      # Marks the utils directory as a Python package
│   │   └── selenium_utils.py # Selenium utility functions
│   └── spiders/             # Contains the spiders for scraping
│       ├── __init__.py      # Marks the spiders directory as a Python package
│       └── google_maps_spider.py # Spider for scraping Google Maps reviews
└── output/                  # Directory for storing output files
    └── .gitkeep             # Keeps the output directory tracked by Git
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd restaurant_reviews_scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the spider and start scraping restaurant reviews, use the following command:

```
scrapy crawl google_maps_spider -a restaurant_name="McDonald's Toronto"
```

Replace `"McDonald's Toronto"` with the name of the restaurant you wish to scrape reviews for.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.