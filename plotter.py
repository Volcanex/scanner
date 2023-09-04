import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 
from forex_python.converter import CurrencyRates

def plot_distribution(products, search_key):
    # Initialize currency converter
    c = CurrencyRates()
    
    USD_TO_GBP_CONVERSION_RATE = 0.79
    
    def clean_price(price_string):
        # Remove currency symbols and other non-numeric characters
        cleaned_price = price_string.replace('$', '').replace('£', '').replace('\xa0', '').replace('(USD)', '').replace('(GBP)', '').strip()
        return float(cleaned_price)

    # Extract prices from the products and convert to GBP
    prices = [clean_price(product['price']) * (USD_TO_GBP_CONVERSION_RATE if '$' in product['price'] else 1) for product in products]

    
    # Calculate statistics
    mean_price = np.mean(prices)
    median_price = np.median(prices)
    std_dev_price = np.std(prices)
    
    # Data for the normal distribution curve
    x = np.linspace(min(prices), max(prices), 1000)
    bin_width = (max(prices) - min(prices)) / 20  # Assuming 20 bins for the histogram
    scaling_factor = len(prices) * bin_width
    y = norm.pdf(x, mean_price, std_dev_price) * scaling_factor

    # Plotting
    plt.figure(figsize=(10,6))
    plt.hist(prices, bins=20, color='skyblue', edgecolor='black', alpha=0.6, label="Histogram")
    plt.plot(x, y, 'r-', label="Normal Distribution")
    plt.axvline(mean_price, color='g', linestyle='dashed', linewidth=1)
    plt.axvline(median_price, color='b', linestyle='dashed', linewidth=1)
    plt.axvline(mean_price + std_dev_price, color='y', linestyle='dotted', linewidth=1, label='+1 Std Dev')
    plt.axvline(mean_price - std_dev_price, color='y', linestyle='dotted', linewidth=1, label='-1 Std Dev')

    min_ylim, max_ylim = plt.ylim()
    plt.text(mean_price+2, max_ylim*0.9, f'Mean: £{mean_price:.2f}', color='g')
    plt.text(median_price-25, max_ylim*0.8, f'Median: £{median_price:.2f}', color='b')

    plt.title(f'Price Distribution of {search_key}(s) in GBP')
    plt.xlabel('Price (£)')
    plt.ylabel('Number of Listings')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()