import scrapy
from hotel_scrapper.items import HotelItem
# from scrapy.loader import ItemLoader
from selenium import webdriver


from datetime import datetime, timedelta
checinkin = datetime.now() + timedelta(days=14)
checkin = checinkin.strftime('%Y-%m-%d')
checkin_year = checkin[:4]
checkin_month = checkin[5:7]
checkin_day = checkin[8:]
checkout = datetime.now() + timedelta(days=15)
checkout = checkout.strftime('%Y-%m-%d')
checkout_year = checkout[:4]
checkout_month = checkout[5:7]
checkout_day = checkout[8:]

class RatesSpiderSpider(scrapy.Spider):
    name = "rates_spider"
    allowed_domains = ['www.booking.com']

    start_urls = [
        f"https://www.booking.com/searchresults.en-gb.html?ss=Maldives&ssne=Maldives&ssne_untouched=Maldives&label=gen173nr-1FCAEoggI46AdIM1gEaLQBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKcgfKuBsACAdICJDMzMDk1NWE2LTNlMGMtNDU1Ni1iYmE4LTBmNTZhMjY2NmRhNNgCBuACAQ&sid=d8f692159d780d393c7c6e9ed3d571a6&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=129&dest_type=country&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=bf7c5dbc3b110061&ac_meta=GhBiZjdjNWRiYzNiMTEwMDYxIAAoATICZW46CE1hbGRpdmVzQABKAFAA&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0"
        ]
    

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(self.start_urls[0])

        mx_pages = 20
        self.driver.implicitly_wait(15)
        # signin = self.driver.find_element_by_xpath("//a[@aria-label='aria-label']")
        # print("🚀 ~ signin===========>:", signin)
        # next = self.driver.find_element_by_xpath("//button[@aria-label='Next page']")
        # next.click()
        # self.driver.find_element_by_xpath("/html/body/div[3]/div/div/header/nav[1]/div[2]/span[1]/button").click()  
        # input = self.driver.find_element_by_xpath("//input[@placeholder='Where are you going?']")
        # input.send_keys("Maldives")
        # submit = self.driver.find_element_by_xpath('//*[@id="indexsearch"]/div[2]/div/form/div[1]/div[4]/button')
        # submit.click()
      

        # while mx_pages > 0:
        #     mx_pages = mx_pages - 1
        #     try:

        #         print(
        #             '==================================================================inside the loop===============')
        #         # print(response.xpath('//button[@aria-label="Next page"]'))

        #         next = self.driver.find_element_by_xpath(
        #             '//button[@aria-label="Next page"]')
        #         # print(next)
        #         url = self.driver.current_url
        #         # print(url)
        #         yield scrapy.Request(url, callback=self.parse_hotel)
        #         print("page xxxxxx")
        #         next.click()
        #         # self.driver.implicitly_wait(10)
        #     except:
        #         print(
        #             '==================================================================failed or end===============')
        #         break

        self.driver.close()

    def parse_hotel(self, response):
        print('==================================================================Passing started===============')
        print('response')
        # print(response)

        # print(response.xpath('//div[@data-testid="property-card"]').extract())
        # hotel_cards = Response.xpath(
        #     '//div[@data-testid="property-card"]')
        hotel_titles = response.xpath(
            '//div[@data-testid="title"]').xpath('.//text()').extract()
        hotel = []
        location = response.xpath(
            '//span[@data-testid="address"]').xpath('.//text()').extract()

        # some stars are 0
        start_counts = response.xpath(
            '//div[@data-testid="rating-squares"]')
        prices = response.xpath(
            '//div[@data-testid="price-and-discounted-price"]').xpath('.//span/text()').extract()
        # SOme are unavaialable
        # recom_filter = a[not(contains(@id, 'xx'))]
        # recom_units = response.xpath('//div[@data-testid="recommended-units"]').xpath('.//dev/dev/dev[0]/span/text()'
        # .xpath('.//dev/dev/dev[0]/span/text()').extract()
        # recom_units = response.xpath(
        #     '//div[@data-testid="recommended-units"]').xpath('.//div/').get()
        # .xpath('.//dev/dev/dev[0]/span/text()').extract()

        print("=============printing====title===")
        for price, title, address in zip(hotel_titles, prices, location):
            print(title)
            print(price)
            print(address)
            # print(recom_units)
            # print(len(recom_units))
            # print(star)

            hotel = HotelItem()

            hotel['name'] = title
            hotel['star'] = "star"
            hotel['d_price'] = price
            # hotel['room_type'] = recom_units
            hotel['original_price'] = address
            hotel['guest_rating'] = "none"

            yield hotel
