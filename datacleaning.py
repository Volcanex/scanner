import json
import os
import openai

openai.api_key = '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'

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

def save_tag_file(name, tag_data):
    """
    Save tagging instructions to a file.

    Parameters:
    - name (str): The search_string or identifier for the tag file.
    - tag_data (dict): A dictionary containing tags and their associated keywords.
    """
    
    filename = f"tag_files/{name}.json"
    
    # Ensure "tag_files/" directory exists
    if not os.path.exists("tag_files/"):
        os.makedirs("tag_files/")
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(tag_data, file, ensure_ascii=False, indent=4)


def load_tag_file(name):
    """
    Load tagging instructions from a file.

    Parameters:
    - name (str): The search_string or identifier for the tag file.

    Returns:
    - dict: A dictionary containing tags and their associated keywords.

    tag_data = {
        "Multiple Offerings": ["Bundle", "Joblot"],
        "Vintage": ["Retro", "Antique", "Old"]
    }
    """
    
    filename = f"tag_files/{name}.json"
    
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            tag_data = json.load(file)
            return tag_data
    else:
        # If the file doesn't exist, return none 
        return None

def tag_products(products, tag_data):
    """
    Tag products based on their names and the provided tag data.

    Parameters:
    - products (list): A list of product dictionaries.
    - tag_data (dict): A dictionary containing tags and their associated keywords.

    Returns:
    - list: A list of tagged product dictionaries.
    """
    
    for product in products:
        product_name = product.get('name', '').lower()
        
        for tag, keywords in tag_data.items():
            for keyword in keywords:
                if keyword.lower() in product_name:
                    product['tags'].append(tag)
                    break  # Break after the first keyword match for this tag

    return products

def create_prompt(product_names: str, existing_tag_file: str) -> str:
    """Create a prompt for the LLM based on product names and an existing tag file."""
    prompt = f"""
Product names:

{product_names}

Existing tag file? 

{existing_tag_file}

Please suggest appropriate tags and keywords for these products. Categories may need to be added, and keywords may need to be added to existing tags. Use the existing tag file as a guide and add or update tags as necessary. Please ONLY output the JSON data."""
    return prompt

def get_tags_from_openai(prompt):
    role = f"""We are trying to categorize products listed on eBay based on their names. The goal is to create or update a tag file in JSON format that associates product tags with keywords found in product names. These tags are essential as they help us determine the price of the product. The tags are used for filtering entries into sub-categories. Use common sense. Products vary and you should decide what are the main tags that affect the price. A tag is a yes or no marker, either it exists or it doesn't. The keywords are used by an algorithm to apply tags to the dataset. There may be multiple keywords that show a product needs a tag e.g 'bundle', 'multiple', 'joblot' would all signify a tag of 'multiple products'. Please add tags that signify groupings of items. Please add tags that signal the item is not what we're looking for.  The delimiter is __ The format of the JSON is:

{{
    "Tag Name": ["keyword1", "keyword2", ...],
    ...
}}
"""

    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(model="gpt-4", messages=messages, max_tokens=4000)
    print(response)
    return response.choices[0].message['content']


def parse_llm_output(output: str) -> dict:
    """Extract JSON data from the LLM's verbose output."""
    start_index = output.find('{')
    end_index = output.rfind('}') + 1
    json_data = output[start_index:end_index]
    return json.loads(json_data)

def update_and_save_tags(product_names: str, filename: str):
    """
    Update the tags based on product names and save them to a file.

    Parameters:
    - product_names (str): The string containing product names separated by '__'.
    - filename (str): The name of the file to load and save the tag data.
    """
    
    # 1. Load the existing tag file
    existing_tag_file = load_tag_file(filename)
    if existing_tag_file:
        existing_tag_file_str = json.dumps(existing_tag_file, ensure_ascii=False, indent=4)
    else:
        existing_tag_file_str = "{}"  # Empty JSON if no tag file exists
    
    # 2. Create a prompt using the loaded tag file and the provided product names
    prompt = create_prompt(product_names, existing_tag_file_str)
    
    # 3. Call the OpenAI API to get the updated tags
    llm_output = get_tags_from_openai(prompt)
    
    # 4. Parse the returned data to extract the JSON
    updated_tags = parse_llm_output(llm_output)
    
    # 5. Return updated tags
    return updated_tags
