# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        ## Remove whitespaces from every field, except description
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        ## Standardize strings by using lowercase
        lowecase_keys = ['category', 'product_type']
        for lk in lowecase_keys:
            value = adapter.get(lk)
            adapter[lk] = value.lower()

        ## Converting price values to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for pk in price_keys:
            value = adapter.get(pk)
            value = value.replace('£', '')
            adapter[pk] = float(value)

        ## Extract just a number from availability field
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        ## Convert number of reviews into integer
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        ## Convert stars value into int
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5


        return item
