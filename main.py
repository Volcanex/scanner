import tools
import product_manager
import plotter 
import datacleaning

def old_main():
    string = input("CPU: ")
    products = product_manager.new_search(string)
                                       
    print('PRODUCT LENGTH: '+str(len(products)))

    names = product_manager.display_product_info(products, True)
    print(names)

    plotter.plot_distribution(products, string)


def load_or_fetch_products(search_string):
    """Load products from saved files or fetch new data."""

    def flatten_list_of_lists(list_of_lists):
        """Flatten a list of lists into a single list."""
        return [item for sublist in list_of_lists for item in sublist]
    
    choice = input("Do you want to load saved products? (y/n): ")
    if choice.lower() == 'y':
        product_dicts = product_manager.load_products(search_string)
        print("RETURNED PRODUCT DICTS NUMBERING: "+str(len(product_dicts)))
        return flatten_list_of_lists(product_dicts)
    else:
        return product_manager.new_search(search_string)

def tag_products(products, tag_file):
    """Tag products based on the tag file."""
    if not all(isinstance(product, dict) for product in products):
        raise ValueError("Products should be a list of dictionaries.")
    
    for product in products:
        if 'name' not in product:
            raise ValueError(f"Product does not have a 'name' key: {product}")

        # Ensure the 'tags' key exists and is a list
        if 'tags' not in product:
            product['tags'] = []

        # Convert product name to lowercase for case-insensitive comparison
        product_name_lower = product['name'].lower()

        for tag, keywords in tag_file.items():
            for keyword in keywords:
                if keyword.lower() in product_name_lower:
                    # Avoid duplicate tags
                    if tag not in product['tags']:
                        product['tags'].append(tag)
    return products


def filter_products_by_tags(products):
    """Filter out products based on user input for tags."""
    for tag in set(tag for product in products for tag in product['tags']):
        choice = input(f"Do you want to remove products with the tag '{tag}'? (y/n): ")
        if choice.lower() == 'y':
            initial_count = len(products)
            products = [product for product in products if tag not in product['tags']]
            removed_count = initial_count - len(products)
            
    return products

def main():
    search_string = input("Enter search string (e.g., CPU): ")

    # Load or fetch products
    products = load_or_fetch_products(search_string)
    print('PRODUCT LENGTH: '+str(len(products)))
    
    # Check if a tag file exists
    print("CHECKING TAG FILE")
    tag_file = datacleaning.load_tag_file(search_string)

    print(type(tag_file))

    if not tag_file:
        print("FOUND NONE")
        # If not, generate one using OpenAI

        print("GENERATING NAMES")
        names = product_manager.display_product_info(products, False)

        print("CREATING TAG FILE")

        updated_tags = datacleaning.update_and_save_tags(names, search_string)
        print("SAVING TAG FILE")
        datacleaning.save_tag_file(search_string, updated_tags)

        tag_file = updated_tags

    else:
        print("FOUND")
    
    # Tag the products
    print("TAGGING")
    
    products = tag_products(products, tag_file)
    
    print("SAVING TAGGED")
    product_manager.save_products(products, search_string)

    # Ask user if they want to filter products based on tags
    choice = input("Do you want to filter out products based on tags? (y/n): ")
    if choice.lower() == 'y':
        products = filter_products_by_tags(products)
    
    
    # Display product info and statistics
    names = product_manager.display_product_info(products, True)

    # Visualize product distribution
    plotter.plot_distribution(products, search_string)

main()
