import scrapy
from hotel_scrapper.items import HotelItem
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
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.dialog_removed = False
        self.loop_count = 0
   
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, cb_kwargs={'url': self.start_urls[0]})

    def parse(self, response, url):
        print('🚀 ==================================================================inside parse===============')
        self.loop_count += 1
        print(f'🚀 ~ LOOP COUNT {self.loop_count}')
        print(f"🚀 ~ URL for the Loop{self.loop_count}: {url}" )
 
        print('🚀 ==================================================================before looping recursive===============')
        
            
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
            print("🚀 ~ finding next button===========>:")
            next_button = self.driver.find_element(by=By.XPATH, value='//button[@aria-label="Next page"]')
            print("🚀 ~ finding next button found inside try===========>:")
        except NoSuchElementException as e:
            print("🚀 ~ next_button not found")
            next_button = None
            pass
        
        if next_button is None:
            print('🚀 ~ next_button is None')
            while_count = 0
            load_more_button = True
            init_int = self.driver.execute_script("return document.body.scrollHeight")
            delta_init = init_int
            while load_more_button:
                # Scroll down to bottom
                while_count += 1
                print(f'🚀 ~ while_count: {while_count}')
                self.driver.implicitly_wait(5)
                self.driver.execute_script(f"window.scrollTo(0, {delta_init});")
                print('🚀 ~ searching for loading more')                    
                delta_init +=  init_int
                try:
                    load_more_button = self.driver.find_element(By.XPATH, "//span[contains(., 'Load more results')]")
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(load_more_button)).click()
                except NoSuchElementException as e:
                    load_more_button = False
                    pass
            
            property_cards = self.driver.find_elements(by=By.XPATH, value='//div[@data-testid="property-card"]')
            print("🚀 ~ finding property_card===========>:")
            print(f'🚀 ~ property_card: {property_cards}')
            print(f'🚀 ~ property_card.count: {property_cards.count}')
            print(f'🚀 ~ property_card. length: {len(property_cards)}')
            for idx in range(len(property_cards)):
                print("🚀 ~ new property===========>:")
                print(f"🚀 ~ SINGLE PAGE===========>:with index: {idx}")
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
                    yield 
            
        else:
            print('🚀 ~ next_button Exists')
            print("🚀 ~ current url before calling parse:", url)
            total_count = 0
            while next_button:
                print('🚀 ~ parse_new_hotel')
                property_cards = self.driver.find_elements(by=By.XPATH, value='//div[@data-testid="property-card"]')
                print("🚀 ~ finding property_card===========>:")
                print(f'🚀 ~ property_card: {property_cards}')
                print(f'🚀 ~ property_card.count: {property_cards.count}')
                print(f'🚀 ~ property_card. length: {len(property_cards)}')
                for idx in range(len(property_cards)):
                    total_count += 1
                    print("🚀 ~ new property===========>:")
                    print(f"🚀 ~ MULTI PAGE===========>:with index: {idx}")
                    print(f"🚀 ~ TOTOAL Property COUNT ===========>: {total_count}")
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
                        yield
                try:
                    next_button = self.driver.find_element(by=By.XPATH, value='//button[@aria-label="Next page"]')
                except NoSuchElementException as e:
                    print("🚀 ~ next_button not found")
                    next_button = False
                    pass
                if next_button.is_enabled():
                    print('🚀 ~ next_button is enabled')
                    next_button.click()
                    print("🚀 ~ Button clicked:")
                    self.driver.implicitly_wait(10)
                    print("🚀 ~ Wait done after clicked:")
                    url = self.driver.current_url
                    print("🚀 ~ NEW URL:", url)
                    # NOTE:Below should not be required as we're not relying on url but the next_button
                    # self.driver.get(url) Use this line if the new page is not loading
                    
        
        self.driver.close()
