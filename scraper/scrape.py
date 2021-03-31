from google.cloud import datastore
import requests
import os
import time

header = {'axesso-api-key': '6486680f-b86c-4409-864e-83865516896d'}


# axesso api for http://api-prd.axesso.de/amz/amazon-search-by-keyword-asin
def keyword_lookup(key_word):
    max_page = 7
    page = 1

    payload = {'keyword': key_word, 'domainCode': 'com', 'sortBy': 'relevanceblender'}
    asins = []

    while page <= max_page:
        payload['page'] = page
        axesso_response = \
            requests.get("http://api-prd.axesso.de/amz/amazon-search-by-keyword-asin",
                         params=payload,
                         headers=header,
                         )
        # parse response from axesso keyword lookup
        json_response = axesso_response.json()
        found_products = json_response['foundProducts']

        # add the found products into one list
        for i in range(len(found_products)):
            asins.append(found_products[i])

        # increment to get next page
        page += 1

    return asins;


# axesso api for http://api-prd.axesso.de/amz/amazon-lookup-product to look up product details
def lookup_product(asin):
    amazon_url = "https://www.amazon.com/dp/" + str(product_asin)
    payload = {'url': amazon_url}
    axesso_response = requests.get("http://api-prd.axesso.de/amz/amazon-lookup-product",
                                   params=payload,
                                   headers=header,
                                   )
    # just return entire response in json format
    return axesso_response.json()


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\mangz\Downloads\justcompare_service_account_key.json"

    print("Looking up keyword... \n")
    found_product_asins = keyword_lookup("coffee machine")
    count = 0
    products_size = len(found_product_asins)

    for product_asin in found_product_asins:
        count += 1

        product = lookup_product(product_asin)

        datastore_client = datastore.Client()
        key = datastore_client.key("AmazonProduct")
        entity = datastore.Entity(key=key, exclude_from_indexes=(
            "acKeywordLink",
            "addon",
            "amazonUrl",
            "answeredQuestions",
            # "asin",
            # "categories",
            # "countReview",
            "currency",
            "dealPrice",
            "features",
            "fulfilledBy",
            "imageUrlList",
            "manufacturer",
            "minimalQuantity",
            "pantry",
            # "price",
            # "priceSaving",
            "priceShippingInformation",
            # "prime",
            "productDescription",
            "productDetails",
            # "productRating",
            "productTitle",
            "retailPrice",
            "salePrice"
            "shippingPrice"
            "sizeSelection",
            "soldBy",
            "warehouseAvailability"
        ))

        '''
        # Handle reviews separately
        print("Inserting reviews indo database... \n")
        for review in product['reviews']:
            review_key = datastore_client.key("Review")
            review_entity = datastore.Entity(key=review_key, exclude_from_indexes=("text", "date", "rating", "title",
                                                                                   "userName", "url"))
            review_entity.update({
                'text': review['text'],
                'date': review['date'],
                'rating': review['rating'],
                'title': review['title'],
                'userName': review['userName'],
                'url': review['url'],
                'asin': product_asin
            })
            datastore_client.put(review_entity)
        '''

        # Then handle the full product items
        url = "https://www.amazon.com/dp/" + str(product_asin)

        entity.update({
            'acKeywordLink': product['acKeywordLink'],
            'addon': product['addon'],
            'amazonUrl': url,
            'answeredQuestions': product['answeredQuestions'],
            'asin': product['asin'],
            'categories': product['categories'],
            'countReview': product['countReview'],
            'currency': product['currency'],
            'dealPrice': product['dealPrice'],
            'features': product['features'],
            'fulfilledBy': product['fulfilledBy'],
            'imageUrlList': product['imageUrlList'],
            'manufacturer': product['manufacturer'],
            'minimalQuantity': product['minimalQuantity'],
            'pantry': product['pantry'],
            'price': product['price'],
            'priceSaving': product['priceSaving'],
            'priceShippingInformation': product['priceShippingInformation'],
            'prime': product['prime'],
            'productDescription': product['productDescription'],
            'productDetails': product['productDetails'],
            'productRating': product['productRating'],
            'productTitle': product['productTitle'],
            'retailPrice': product['retailPrice'],
            'salePrice': product['salePrice'],
            'shippingPrice': product['shippingPrice'],
            'sizeSelection': product['sizeSelection'],
            'soldBy': product['soldBy'],
            'warehouseAvailability': product['warehouseAvailability']
        })
        datastore_client.put(entity)
        print("Inserted " + str(count) + "/" + str(products_size) + "...\n")
        time.sleep(30)  # add 30 second delay.

    print("Inserted all data. Yay!")
