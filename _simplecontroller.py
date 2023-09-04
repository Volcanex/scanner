import tools
import product_manager
import plotter 
import datacleaning

def old_main():
    string = input("CPU: ")
    products = product_manager.new_search(string)
                                       
    print('PRODUCT LENGTH:'+str(len(products)))

    names = product_manager.display_product_info(products, True)
    print(names)

    plotter.plot_distribution(products, string)


def load_or_fetch_products(search_string):
    """Load products from saved files or fetch new data."""
    choice = input("Do you want to load saved products? (y/n): ")
    if choice.lower() == 'y':
        return product_manager.load_products(search_string)
    else:
        return product_manager.new_search(search_string)

def tag_products(products, tag_file):
    """Tag products based on the tag file."""
    for product in products:
        for tag, keywords in tag_file.items():
            for keyword in keywords:
                if keyword in product['name']:
                    product['tags'].append(tag)
    return products

def filter_products_by_tags(products):
    """Filter out products based on user input for tags."""
    for tag in set(tag for product in products for tag in product['tags']):
        choice = input(f"Do you want to remove products with the tag '{tag}'? (y/n): ")
        if choice.lower() == 'y':
            products = [product for product in products if tag not in product['tags']]
    return products

def main():
    search_string = input("Enter search string (e.g., CPU): ")

    # Load or fetch products
    products = load_or_fetch_products(search_string)
    
    # Check if a tag file exists
    tag_file = datacleaning.load_tag_file(search_string)

    if not tag_file:
        # If not, generate one using OpenAI
        names = product_manager.display_product_info(products, True)
        # Dear god

        updated_tags = datacleaning.update_and_save_tags(names, search_string)
        datacleaning.save_tag_file(updated_tags)

        tag_file = updated_tags
    
    # Tag the products
    products = tag_products(products, tag_file)
    
    product_manager.save_products(products, search_string)

    # Ask user if they want to filter products based on tags
    choice = input("Do you want to filter out products based on tags? (y/n): ")
    if choice.lower() == 'y':
        products = filter_products_by_tags(products)
    
    
    # Display product info and statistics
    names = product_manager.display_product_info(products, True)
    print(names)

    # Visualize product distribution
    plotter.plot_distribution(products, search_string)

main()
