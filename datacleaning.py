import openai

def collectwords(sample_products):

    
    # Set up the API key
    openai.api_key = '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'

    # Define the prompt
    product_names = "\n".join([(product['name']+product['price']) for product in sample_products])
    prompt_text = f"Based on the following product names, identify words that might indicate the product is not a standalone product or that it's bundled with something else, if it's bundled with components it might originally come with e.g cpu + cpu fan, that's okay:\n{product_names}\n\nExclusion words:"

    # Make the API call
    response = openai.Completion.create(
        engine="curie",  # or "davinci" based on your choice
        prompt=prompt_text,
        max_tokens=1500
    )

    # Extract and print the identified exclusion words
    return response.choices[0].text.strip()



def clean_products(products, inclusion_list, exclusion_list):

    """
    Clean the product list based on inclusion and exclusion keywords with associated priorities.
    
    Parameters:
    - products: List of product dictionaries.
    - inclusion_list: List of tuples with keywords and priorities for product inclusion.
    - exclusion_list: List of tuples with keywords and priorities for product exclusion.
    
    Returns:
    - Cleaned list of products.
    """
    cleaned_products = []
    
    for product in products:
        name = product['name'].lower()
        
        # Initial priority values
        inclusion_priority = 0
        exclusion_priority = 0
        
        for keyword, priority in inclusion_list:
            if keyword.lower() in name and priority > inclusion_priority:
                inclusion_priority = priority
        
        for keyword, priority in exclusion_list:
            if keyword.lower() in name and priority > exclusion_priority:
                exclusion_priority = priority
        
        # Compare priorities and decide to include or exclude the product
        if inclusion_priority >= exclusion_priority:
            cleaned_products.append(product)
    
    return cleaned_products

def filter_products_based_on_condition(products, accepted_conditions):
    """
    Filters the products based on the accepted conditions.
    
    Parameters:
    - products (list): List of product dictionaries.
    - accepted_conditions (list): List of accepted product conditions.
    
    Returns:
    - List of filtered product dictionaries.
    """
    
    return [product for product in products if product['condition'] in accepted_conditions]