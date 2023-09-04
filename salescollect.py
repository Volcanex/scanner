import requests
from bs4 import BeautifulSoup
import os
import tools
import numpy as np
from forex_python.converter import CurrencyRates

def sales(search_string):
    # Insert the search string into the URL
    url = f"http://www.watchcount.com/completed.php?bkw={search_string.replace(' ', '+')}&bcat=0&bcts=&sfsb=Show+Me%21&csbin=all&cssrt=ts&bfw=1&bslr=&bnp=&bxp=150.00#serp"
    savename = 'Sales search'
    response = tools.grab(url, savename, name=search_string)
    soup = BeautifulSoup(response, 'html.parser')

    return soup

def parse_watchcount_html(soup):
    # Find all product rows based on the comment markers
    product_rows = soup.find_all('tr', itemscope="", itemtype="http://schema.org/Product")
    
    products = []
    for row in product_rows:
        product = {}
        
        # Extract product name and URL
        name_elem = row.find('span', itemprop="name")
        if name_elem and name_elem.a:
            product['name'] = name_elem.text.strip()
            product['url'] = name_elem.a['href']
        
        # Extract product ID
        id_elem = row.find('span', title="Product ID")
        if id_elem:
            product['id'] = id_elem.text.strip()
        
        # Extract end time
        end_time_elem = row.find('span', class_="bhserp-dim2")
        if end_time_elem:
            product['end_time'] = end_time_elem.text.strip()
        
        # Extract price
        price_elem = row.find('span', itemprop="price")
        if price_elem:
            product['price'] = price_elem.text.strip()
        
        # Extract seller name and URL
        seller_elem = row.find('span', title="Seller")
        if seller_elem and seller_elem.a:
            product['seller_name'] = seller_elem.text.strip()
            product['seller_url'] = seller_elem.a['href']
        
        # Extract item condition
        condition_elem = row.find('span', title="Item condition")
        if condition_elem:
            product['condition'] = condition_elem.text.strip()
        
        # Extract product image URL
        image_elem = row.find('img', itemprop="image")
        if image_elem:
            product['image_url'] = image_elem['src']
        
        products.append(product)
    
    return products


def display_product_info(products):
    """Print detailed information on specific products based on statistical criteria."""
    
    c = CurrencyRates()

    USD_TO_GBP_CONVERSION_RATE = c.get_rate('USD', 'GBP')
    # Extract prices and compute statistics
    prices_in_usd = [float(product['price'].replace('$', '').replace('(USD)', '').replace('\xa0', ' ').strip()) for product in products]
    prices_in_gbp = [price * USD_TO_GBP_CONVERSION_RATE for price in prices_in_usd]
    mean_price = np.mean(prices_in_gbp)
    std_dev_price = np.std(prices_in_gbp)
    
    # Identify products based on criteria
    median_product = products[np.argsort(prices_in_gbp)[len(prices_in_gbp) // 2]]
    most_expensive_product = products[np.argmax(prices_in_gbp)]
    least_expensive_product = products[np.argmin(prices_in_gbp)]
    
    # Products nearest to one standard deviation above and below the mean
    product_near_std_above = min(products, key=lambda x: abs((float(x['price'].replace('$', '').replace('(USD)', '').replace('\xa0', ' ').strip()) * USD_TO_GBP_CONVERSION_RATE) - (mean_price + std_dev_price)))
    product_near_std_below = min(products, key=lambda x: abs((float(x['price'].replace('$', '').replace('(USD)', '').replace('\xa0', ' ').strip()) * USD_TO_GBP_CONVERSION_RATE) - (mean_price - std_dev_price)))
    
    # Helper function to display a product's details
    def print_product_details(product):
        print(f"Name: {product['name']}")
        converted_price = float(product['price'].replace('$', '').replace('(USD)', '').replace('\xa0', ' ').strip()) * USD_TO_GBP_CONVERSION_RATE
        print(f"Price: £{converted_price:.2f}")
        print(f"Condition: {product['condition']}")
        # Convert end time to hours or days
        end_time = float(product['end_time'])
        if end_time < 24:
            print(f"End Time: {end_time:.2f} hours")
        else:
            print(f"End Time: {end_time / 24:.2f} days")
        print("----------------------")
    
    print("\nMedian Priced Product:")
    print_product_details(median_product)
    
    print("\nMost Expensive Product:")
    print_product_details(most_expensive_product)
    
    print("\nLeast Expensive Product:")
    print_product_details(least_expensive_product)
        
    print("\nProduct Near +1 Std Dev from Mean:")
    print_product_details(product_near_std_above)
        
    print("\nProduct Near -1 Std Dev from Mean:")
    print_product_details(product_near_std_below)
    
    print("\nAll Products:")
    for product in products:
        print_product_details(product)


def main(search_key):
    soup = sales(search_key)
    products = parse_watchcount_html(soup)

    print('Collected? Products length = '+str(len(products)))
    return products

