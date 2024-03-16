# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HotelItem(scrapy.Item):
    name = scrapy.Field()
    star = scrapy.Field()
    # guest_rating = scrapy.Field()
    # reviews = scrapy.Field()
    room_type = scrapy.Field()
    # room_details = scrapy.Field()
    # eminities = scrapy.Field()
    # occupency = scrapy.Field()
    d_price = scrapy.Field()
    original_price = scrapy.Field()
    # price_details = scrapy.Field()
    conditions = scrapy.Field()
    # url = scrapy.Field()
    details = scrapy.Field()


class BookingReviewer(scrapy.Item):
    hotel_name = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    age = scrapy.Field()
    date = scrapy.Field()
    room_type = scrapy.Field()
    guest_type = scrapy.Field()
    trip_type = scrapy.Field()
    length_of_stay = scrapy.Field()
    country = scrapy.Field()
    user_review_count = scrapy.Field()
    #language = scrapy.Field()
    positive_content = scrapy.Field()
    negative_content = scrapy.Field()
    score = scrapy.Field()
    #tags = scrapy.Field()
    posted_via = scrapy.Field()
    hotel_clean = scrapy.Field()
    hotel_comfort = scrapy.Field()
    hotel_location = scrapy.Field()
    hotel_clean = scrapy.Field()
    hotel_staff = scrapy.Field()
    hotel_services = scrapy.Field()
    hotel_value = scrapy.Field()
    hotel_wifi = scrapy.Field()
    #superb = scrapy.Field()
    #good = scrapy.Field()
    #ok = scrapy.Field()
    #poor = scrapy.Field()
    #verypoor = scrapy.Field()