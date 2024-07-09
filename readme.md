# eBay Product Scanner

This repository contains a Python-based tool for analyzing and visualizing eBay product data, with a focus on CPUs. The tool fetches product information, tags products, and provides insights through data analysis and visualization.

## Features

- Scrape product data from eBay auction results
- Tag products based on their names using customizable tag files, this eliminates bad examples
- Filter products based on tags
- Visualize price distribution of products
- Compare products with CPU benchmark data

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - numpy
  - matplotlib
  - scipy
  - forex-python
  - lxml

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ebay-product-analyzer.git
cd ebay-product-analyzer
```

2. Install the required packages: 

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key in the `datacleaning.py` file:
```python
openai.api_key = 'your-api-key-here'
```
# Usage 

## Run the main script:
python main.py

- Enter a search string when prompted e.g Ryzen 7 3700x or RTX 2070
- Choose whether to load saved products or fetch new data.
- The script will automatically check for an existing tag file, create one if it doesn't exist, and tag the products accordingly.
- Choose whether to filter out products based on tags.
- View the product information and statistics in the console output.
- A price distribution plot will be displayed.

# File Structure

- main.py: The main script that orchestrates the entire process.
- product_manager.py: Handles product data fetching, parsing, and management.
- datacleaning.py: Manages product tagging and tag file operations.
- plotter.py: Contains functions for data visualization.
- tools.py: Utility functions for web scraping and data handling.

# Customization

- Modify the tag file generation process in datacleaning.py to customize product categorization.
- Adjust the plotting parameters in plotter.py to change the visualization style.

# Contributing
Feel free to submit a Pull Request. This is an old project but I still find it useful for checking prices. 
