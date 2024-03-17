import scrapy
from hotel_scrapper.items import HotelItem
# from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin






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
    
    # Selenium
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.debug = False
        self.dialog_removed = False
   
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, cb_kwargs={'url': self.start_urls[0]})

    def parse(self, response, url):
        print('🚀 ==================================================================inside parse===============')
        print("🚀 ~ response:", url)
        if url is None:
            return None
    # ############################################## GOOD CODE ##############################################
        # self.driver.get(self.start_urls[0])
        # print('==================================================================Passing started===============')
        # print(f'response: {response}')
        
        # print("🚀 ~ finding next button===========>:")
        
        # self.driver.implicitly_wait(30)
        # dismiss_button = self.driver.find_element(by=By.XPATH, value='//button[@aria-label="Dismiss sign in information."]')
        # if dismiss_button:
        #     dismiss_button.click()
    # ############################################## GOOD CODE END ##############################################
        
     
      
       
    # FINDING PROPERTY CARD using selenium
    # ############################################## GOOD CODE ##############################################
        # print("🚀 ~ finding property_card===========>:")
        # property_card = self.driver.find_elements(by=By.XPATH, value='//div[@data-testid="property-card"]')
        # print(f'🚀 ~ property_card: {property_card}')
        # print(f'🚀 ~ property_card.count: {property_card.count}')
        # print(f'🚀 ~ property_card. length: {len(property_card)}')
        
        # for idx in range(len(property_card)):
        #     print("🚀 ~ new property===========>:")
        #     try:
                
        #         current_property = property_card.pop()
        #         if current_property:
        #             print(f'🚀 ~ current_property: {current_property.text}')
        #     except Exception as e:
        #         print(f'🚀 ~ error: {e}')
    # ############################################## GOOD CODE END ##############################################

        print('🚀 ==================================================================before looping recursive===============')
        try:
    
            print("🚀 ~ finding next button===========>:")
            self.driver.get(url)
            self.driver.implicitly_wait(15)
            if not self.dialog_removed:
                try:
                    dismiss_button = self.driver.find_element(by=By.XPATH, value='//button[@aria-label="Dismiss sign in information."]')
                    if dismiss_button:
                        dismiss_button.click()
                        self.dialog_removed = True
                except NoSuchElementException as e:
                    print("🚀 ~ dismiss_button not found")
                    pass
            
            try:
                next_button = self.driver.find_element(by=By.XPATH, value='//button[@aria-label="Next page"]')
            except NoSuchElementException as e:
                print("🚀 ~ next_button not found")
                next_button = None
                pass
            
            if next_button is None:
                print('🚀 ~ next_button is None')
                url = None
                try:
                    load_more_button = self.driver.find_element(By.XPATH, "//span[contains(., 'Load more results')]")
                    init_int = 10
                    while load_more_button:
                        print('🚀 ~ load_more_button is found')
                        scroll_origin = ScrollOrigin.from_viewport(10, init_int)
                        delta_init = 2000 + init_int
                        init_int = delta_init
                        ActionChains(self.driver).scroll_from_origin(scroll_origin, 0, delta_init).perform()
                        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(load_more_button)).click()
                        if self.debug:
                            load_more_button = None
                except NoSuchElementException as e:
                    print(f"🚀 ~ load_more_button not found{e}")
                yield self.parse_new_hotel()
                # url = self.driver.current_url
                # yield scrapy.Request(url, self.parse_hotel, dont_filter = True)
                
            else:
                print('🚀 ~ next_button is not None')
                print("🚀 ~ current url before calling parse:", url)
                if self.debug:
                    url = None
                if next_button.is_enabled():
                    print('🚀 ~ next_button is enabled')
                    print("🚀 ~ current url after calling parse:", url)
                    next_button.click()
                    self.driver.implicitly_wait(2)
                    url = self.driver.current_url
                    self.parse(response, url)
                    # yield scrapy.Request(url, self.parse_hotel, dont_filter = True)
                else:
                    url = None
                # self.parse(response, url)
                 
        except:
            print(
                '==================================================================failed or end===============')
            url = None
            self.driver.close()

    def parse_new_hotel(self):
        # self.driver.implicitly_wait(2)
        property_cards = self.driver.find_elements(by=By.XPATH, value='//div[@data-testid="property-card"]')
        print("🚀 ~ finding property_card===========>:")
        print(f'🚀 ~ property_card: {property_cards}')
        print(f'🚀 ~ property_card.count: {property_cards.count}')
        print(f'🚀 ~ property_card. length: {len(property_cards)}')
        # h = []
        for idx in range(len(property_cards)):
            print("🚀 ~ new property===========>:")
            try:
                
                current_property = property_cards.pop()
                if current_property:
                    print(f'🚀 ~ current_property: {current_property.text}')
                    # print(f'🚀 ~ current_property element: {current_property}')
                    # print(f"🚀 ~ current_property innerHTML: {current_property.get_attribute('innerHTML')}")
                    details = current_property.text
                    
                    title = current_property.find_element(by=By.XPATH, value='.//div[@data-testid="title"]')
                    title = title.text
                    try:
                        address = current_property.find_element(by=By.XPATH, value='.//span[@data-testid="address"]')
                        address = address.text
                    except NoSuchElementException:
                        print(f'🚀 ~ error: {e}')
                        address = "none"
                    price = current_property.find_element(by=By.XPATH, value='.//div[@data-testid="availability-rate-information"]')
                    price = price.text
                    
                    try:
                        squars = current_property.find_element(by=By.XPATH, value='.//div[@data-testid="rating-squares"]/..') #./div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/span/div
                    except NoSuchElementException as e:
                        squars = None
                        print(f'🚀 ~ error: {e}')
                    try:
                        star = current_property.find_element(by=By.XPATH, value='.//div[@data-testid="rating-stars"]/..') #./div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/span/div
                    except NoSuchElementException as e:
                        star = None
                        print(f'🚀 ~ error: {e}')
                    
                    recom_units = current_property.find_element(by=By.XPATH, value='.//h4')
                    recom_units = recom_units.text
                    guest_rating = current_property.find_element(by=By.XPATH, value='.//div[@data-testid="review-score"]')
                    guest_rating = guest_rating.text

            
                    hotel = HotelItem()

                    hotel['name'] = title
                    if star:
                        star = star.get_attribute('aria-label')
                    elif squars:
                       star = squars.get_attribute('aria-label') 
                       
                    hotel['star'] = star
                    hotel['d_price'] = price
                    hotel['room_type'] = recom_units
                    hotel['original_price'] = address
                    hotel['guest_rating'] = guest_rating
                    hotel['details'] = details
                    yield hotel
                    # h.append(hotel)
                    
            except NoSuchElementException as e:
                print(f'🚀 ~ error: {e}')
                pass
        print('🚀 ==================================================================before looping recursive===============')
        # return h
# # Old code ======
    def parse_hotel(self, response):
        print('==================================================================Passing started===============')
        print('response')
        # print(response)
        hotel_cards = response.xpath('//div[@data-testid="property-card"]')
        for hotel_card in hotel_cards:
            title = hotel_card.xpath('.//div[@data-testid="title"]/text()').get()
            address = hotel_card.xpath('.//span[@data-testid="address"]/text()').get()
            price = hotel_card.xpath('.//div[@data-testid="availability-rate-information"]/text()').get()
            
            try:
                squars = hotel_card.xpath('.//div[@data-testid="rating-squares"]/..')
            except NoSuchElementException as e:
                squars = None
                print(f'🚀 ~ error: {e}')
            
            try:
                star = hotel_card.xpath('.//div[@data-testid="rating-stars"]/..')
            except NoSuchElementException as e:
                star = None
                print(f'🚀 ~ error: {e}')

            if star:
                star = star.get_attribute('aria-label')
            elif squars:
                star = squars.get_attribute('aria-label')
                
            recom_units = hotel_card.xpath('.//h4/text()').get()
            guest_rating = hotel_card.xpath('.//div[@data-testid="review-score"]/text()').get()
            
            hotel = HotelItem()
            hotel['name'] = title
            hotel['star'] = "star"
            hotel['d_price'] = price
            hotel['room_type'] = recom_units
            hotel['original_price'] = address
            hotel['guest_rating'] = guest_rating

            yield hotel
