from google.cloud import datastore
import requests
import os

header = {'axesso-api-key': '6486680f-b86c-4409-864e-83865516896d'}


# axesso api for http://api-prd.axesso.de/amz/amazon-search-by-keyword-asin
def keyword_lookup(key_word):
    payload = {'keyword': key_word, 'domainCode': 'com', 'sortBy': 'relevanceblender', 'page': 1}

    axesso_response = \
        requests.get("http://api-prd.axesso.de/amz/amazon-search-by-keyword-asin",
                     params=payload,
                     headers=header,
                     )
    # parse response from axesso keyword lookup
    json_response = axesso_response.json()
    found_products = json_response['foundProducts']

    return found_products;


# axesso api for http://api-prd.axesso.de/amz/amazon-lookup-product to look up product details
def lookup_product(product_asin):
    url = "https://www.amazon.com/dp/" + str(product_asin)
    payload = {'url': url}
    axesso_response = requests.get("http://api-prd.axesso.de/amz/amazon-lookup-product",
                                   params=payload,
                                   headers=header,
                                   )
    # just return entire response in json format
    return axesso_response.json()


if __name__ == '__main__':
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "464c9eaf0361c12a3db0fff53c6c0399d8a6f270"
    #datastore_client = datastore.Client()

    found_product_asins = keyword_lookup("coffee machine")
    count = 0
    products_size = len(found_product_asins)
    for product_asin in found_product_asins:
        count += 1

        #print("Treating " + count + "/" + str(products_size) + "...\n")
        product = lookup_product(product_asin)
        #key = datastore_client.key('yo')
        #entity = datastore.Entity(key=key)

        url = "https://www.amazon.com/dp/" + str(product_asin)
        product_dict = {
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
            'reviews': product['reviews'],
            'salePrice': product['salePrice'],
            'shippingPrice': product['shippingPrice'],
            'sizeSelection': product['sizeSelection'],
            'soldBy': product['soldBy'],
            'warehouseAvailability': product['warehouseAvailability']
        }

        print(product_dict)
        break
        #entity.update()
        #datastore_client.put(entity)

    print("Inserted all data. Yay!")
