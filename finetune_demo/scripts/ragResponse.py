import re
from fuzzywuzzy import fuzz,process

from haierItems import *
import random

import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from init_model import *
from utils import *

def search(query_transformers, k=5):
    query_embedding_transformers = model_transformers.encode([query_transformers])
    distances, indices = index_transformers.search(query_embedding_transformers, k)
    results_transformers = df_transformers.iloc[indices[0]].to_dict('records')
    return results_transformers

def extract_model_price_pairs_as_list(text):
    # Regular expression pattern to match prices (e.g., Rs. 10,500)
    price_pattern = r'Rs\.?\s?[\d,]+'

    # Extract product names or model numbers
    product_or_models = extract_product_name_or_model(text)

    # Find all prices in the text
    prices = re.findall(price_pattern, text)

    # Create a flat list to store models and prices
    model_price_list = []
    for i, product_or_model in enumerate(product_or_models):
        price = prices[i] if i < len(prices) else "Price unavailable"
        model_price_list.append(product_or_model)
        model_price_list.append(price)

    return model_price_list

def verify_and_replace_model_as_list(model_price_list, inventory):
    updated_model_price_list = []
    # Iterate over model_price_list (in pairs of model and price)
    for i in range(0, len(model_price_list), 2):
        model = model_price_list[i]
        price = model_price_list[i + 1]

        # First: Exact match for the model in the inventory
        exact_matches = [item for item in inventory if model == item['Product Info']]

        if exact_matches:
            updated_model_price_list.append(model)
            updated_model_price_list.append(f"Rs. {exact_matches[0]['Price(Rs)']:,}")
        else:
            # Fuzzy match if no exact match
            partial_matches = [item for item in inventory if fuzz.partial_ratio(model, item['Product Info']) > 80]

            if partial_matches:
                matched_item = partial_matches[0]
                updated_model_price_list.append(matched_item['Product Info'])
                updated_model_price_list.append(f"Rs. {matched_item['Price(Rs)']:,}")
            else:
                # Fallback to vector search if no match is found
                search_results = search(model, k=1)
                if search_results:
                    matched_item = search_results[0]
                    updated_model_price_list.append(matched_item['Product Info'])
                    updated_model_price_list.append(f"Rs. {matched_item['Price(Rs)']:,}")
                else:
                    updated_model_price_list.append(model)
                    updated_model_price_list.append("Price unavailable")

    return updated_model_price_list

def extract_product_name_or_model(text):
    # Broaden regex to handle more variations of product names and models
    # result of this pattern in successful_scripts_GLM3\bot_build_october\hillucinationCheckMechanism\regex_attempts\oct18_automation_oct.txt
    ## flaws: HSU HRI models ignored
    # product_pattern = r'(Haier\s[\w\s\-\/]+(?:\([A-Za-z0-9\-\/]+\))?)'
    product_pattern = r'\b(HSU.*?(?:priced|[A-Za-z]+-?[0-9]*\))|Haier.*?(?:priced|[A-Za-z]+-?[0-9]*\))|HRF.*?(?:priced|[A-Za-z]+-?[0-9]*\)))'

    
    model_pattern = r'[A-Z0-9\-\/]{6,}'

    product_matches = re.findall(product_pattern, text)
    logging.info(f"product_matches: {product_matches}")
    
    if product_matches:
        logging.info("===========ragResponse.py >> extract_product_name_or_model===========")
        for product_name in product_matches:
            product_name = product_name.replace(" priced", "")
            logging.info(f"product_name: {product_name}")
        logging.info("===========ragResponse.py >> extract_product_name_or_model===========")
    
        return product_matches


    model_matches = re.findall(model_pattern, text)
    
    if model_matches:
        return [model.strip("()") for model in model_matches]

    return []

def replace_old_with_new(text, old_info, new_info):
    """
    Replace the old names and prices in the text with the new ones.
    """
    for i in range(0, len(old_info), 2):  # Step through old_info in pairs of name and price
        old_model = old_info[i]
        old_price = old_info[i + 1]
        new_model = new_info[i]
        new_price = new_info[i + 1]

        # Replace both model name and price in the text
        text = text.replace(old_model, new_model)
        text = text.replace(old_price, new_price)

    return text

def query_RAG_check(query):    # Process each bot response
    
    text = query
    # Extract model-price pairs into a list
    old_info = extract_model_price_pairs_as_list(text)
    # print("Extracted Old Info List:", old_info)
    # Verify and replace models using the inventory, producing the new list
    new_info = verify_and_replace_model_as_list(old_info, haier_items)
    # print("Verified New Info List:", new_info)

    # Replace the old models and prices with the verified ones in the original text
    updated_text = replace_old_with_new(text, old_info, new_info)

    # print("Updated Text:\n", updated_text)
    # print("=" * 30)
    return updated_text






























def verify_and_replace_model_as_list_with_link(model_price_list, inventory):
    updated_model_price_list = []
    # Iterate over model_price_list (in pairs of model and price)
    for i in range(0, len(model_price_list), 2):
        model = model_price_list[i]
        price = model_price_list[i + 1]

        # First: Exact match for the model in the inventory
        exact_matches = [item for item in inventory if model == item['Product Info']]

        if exact_matches:
            matched_item = exact_matches[0]
            updated_model_price_list.append(f"{matched_item['link']} #{matched_item['Product Info']}#")
            updated_model_price_list.append(price)
        else:
            # Fuzzy match if no exact match
            partial_matches = [item for item in inventory if fuzz.partial_ratio(model, item['Product Info']) > 80]

            if partial_matches:
                matched_item = partial_matches[0]
                updated_model_price_list.append(f"{matched_item['link']} #{matched_item['Product Info']}#")
                updated_model_price_list.append(price)
            else:
                # Fallback to vector search if no match is found
                search_results = search(model, k=1)
                if search_results:
                    matched_item = search_results[0]
                    updated_model_price_list.append(f"{matched_item['link']} #{matched_item['Product Info']}#")
                    updated_model_price_list.append(price)
                else:
                    updated_model_price_list.append(model)
                    updated_model_price_list.append("Price unavailable")

    return updated_model_price_list
from haierItemsModelLinks import haier_model_links
def query_RAG_check_with_link(query):    # Process each bot response

    # Normalize strings: Remove extra whitespace and make lowercase
    def normalize(text):
        return re.sub(r'\s+', ' ', text.strip()).lower()
    
    # Function to perform fuzzy matching with dynamic thresholds
    def find_closest_match(query, haier_items, thresholds):
        product_names = [item["product_info"] for item in haier_items]
        for threshold in thresholds:
            best_match, score = process.extractOne(query, product_names, scorer=fuzz.token_sort_ratio)
            if score >= threshold:
                return (best_match, score)  # Return the first match above the threshold
        return (None, 0)  # No match found

    # Store replaced matches to ensure no redundant replacements
    already_replaced = set()
    
    # Normalize query for matching
    normalized_query = normalize(query)
    
    # Exact matching first
    for item in haier_model_links:
        product_name = normalize(item["product_info"])
        link = item["link"]
    
        if product_name in normalized_query and product_name not in already_replaced:
            # Replace product name with its corresponding link
            pattern = re.escape(item["product_info"].strip())
            query = re.sub(pattern, f"The {link} #{item['product_info'].strip()}#", query, flags=re.IGNORECASE)
            already_replaced.add(product_name)
    
    # Check if any link was added, if not, perform fuzzy matching
    if not any(item["link"] in query for item in haier_model_links):
        # Define thresholds: Start from 95, go down to 70
        thresholds = [95, 90, 85, 80, 75, 70]
        closest_match, score = find_closest_match(query, haier_model_links, thresholds)
        
        if closest_match:
            # Get the corresponding link for the closest match
            link = next(i["link"] for i in haier_items if i["product_info"] == closest_match)
            pattern = re.escape(closest_match.strip())
            query = re.sub(pattern, f"The {link} #{closest_match}#", query, flags=re.IGNORECASE)

    updated_text=query
    return updated_text
