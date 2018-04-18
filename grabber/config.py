REVIEW_PER_PAGE = 50

XPATH_REVIEW_COUNT = '//span[@data-hook="total-review-count"]/text()'
XPATH_REVIEW_SECTION = '//div[@data-hook="review"]'

XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
XPATH_SINGLE_RATING = './td//a//text()'
XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'

XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
XPATH_REVIEW_TEXT = './/span[@data-hook="review-body"]//text()'
XPATH_PURCHASE = './/div[contains(@class, "review-data review-format-strip")]//' \
                 'span[contains(@data-hook, "avp-badge")]//text()'

XPATH_REVIEW_COMMENTS = './/span[@class="a-expander-prompt"]/span[@class="a-size-base"]//text()'
XPATH_AUTHOR_NAME = './/a[contains(@class,"author")]//text()'
XPATH_AUTHOR_LINK = './/a[contains(@class,"author")]'
XPATH_AUTHOR = './/div[@id="customer-profile-bio"]//text()'

XPATH_BADGES_ROW = './/div[contains(@class, "review-data review-format-strip")]//text()'

vine_review = 'Vine Customer Review of Free Product'


class AmazonUrlPatterns:
    PRODUCT_PAGE = 'https://{}/dp/{}'
    REVIEW_PAGE = 'https://{}/product-reviews/{}?reviewerType=all_reviews&sortBy=recent&pageSize={}&pageNumber={}'


USER_AGENT_LIST = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0',
    'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
    'Mozilla/4.0 (compatible; MSIE 6.0b; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Win64; x64; Trident/6.0; .NET4.0E; .NET4.0C)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)',
    'Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)'
    ]
