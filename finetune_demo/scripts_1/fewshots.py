from haierItems import *
import random
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from init_model import *
from utils import *
import re


relevant_items = ""
def search(query_transformers, k=5):
    results_transformers = []
    query_embedding_transformers = model_transformers.encode([query_transformers])
    seen_product_info = set()
    n_results_to_fetch = k * 2  # Start by fetching more than required to handle duplicates

    while len(results_transformers) < k:
        # Retrieve a larger batch of results
        distances, indices = index_transformers.search(query_embedding_transformers, n_results_to_fetch)
        all_results = df_transformers.iloc[indices[0]].to_dict('records')

        # Filter duplicates and add unique items until we reach desired count
        for item in all_results:
            product_info = item['Product Info']
            if product_info not in seen_product_info:
                results_transformers.append(item)
                seen_product_info.add(product_info)
            
            if len(results_transformers) == k:
                break

        n_results_to_fetch += k  # Increase the fetch count to ensure finding unique items if needed

    return results_transformers[:k]  # Return only the top `k` unique items







def getFewshotsHistory(query):
    global relevant_items
    
    relevant_items = search(query)
    
    logging.info("("*50)
    logging.info(f"Agains the user query: {query}")
    logging.info("("*50)

    logging.info(")"*50)
    for rel in relevant_items:
        logging.info(f"relevant_items :{rel['Product Info']}\n")
    logging.info(")"*50)
    return [ {"role": "user", "content": f"Here is the list of items of Haier products. Read it and say OK! "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "


},
                {'role': 'assistant', 'content': 'OK'},




                {'role': 'user', 'content': """Here is the second list. Read it and say OK!
                "{
                      "contactInformation": {
                        "headOffice": {
                          "address": "4-B, Q-Block, Old College Road, M. M. Alam Road Extension, Gulberg-II, Lahore, Pakistan"
                        },
                        "emails": [
                          "info@haier.com.pk",
                          "corporatesales@haier.com.pk",
                          "Export@haier.com.pk"
                        ],
                        "phone": "(042) 1111 42437"
                      }
                    }"
                """
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
             f"{haier_items[random.randint(0,len(haier_items)-1)]}, "

    },
                {'role': 'assistant', 'content': "OK"},

        # {'role': 'user', 'content': "Here is the third list of items of Haier products. Read it and say OK! " +
        #      f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
        #      f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
        #      f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
        #      f"{haier_items[random.randint(0,len(haier_items)-1)]}, "
        #      f"{haier_items[random.randint(0,len(haier_items)-1)]}, "},
        {'role': 'user', 'content': "Here is the third list of items of Haier products. Read it and say OK! " + str(relevant_items)},
        {'role': 'assistant', 'content': 'OK'},

        # {'role': 'user', 'content': 'Act as an AI customer support chatbot specialized in Haier products. Provide accurate and helpful information, and ensure customer satisfaction. Your knowledge is limited to above list of products only. Say OK!'},
        # {'role': 'assistant', 'content': 'OK'},






        
    # {"role": "user", "content": "Please only use the information from the these 3 list of Haier products I have provided."},
    #  {'role': 'assistant', 'content': "OK, I will only use the information from 3 list of Haier products you have provided me."},



# {"role": "user", "content": "Can you tell me about the latest Haier Game Pad?"},
#      {'role': 'assistant', 'content': "Sure, the Haier Game Pad is a top-quality gaming accessory. It is listed under 'Electronic Devices/Gaming & Consoles/PlayStation Consoles' and is priced at Rs 9555."},

#         {'role': 'user', 'content': 'How do I make a pizza?'},
#         {'role': 'assistant', 'content': "I cannot help you with this; however, we have the Haier Single Tub Washing Machine (HWM80-35), that can be of good use."},





     # {"role": "user", "content": "How can I stream content on my TV with Haier products?"},
     # {'role': 'assistant', 'content': "You can use the Haier Android Dongle (S905Y4) for streaming. It is priced at Rs 14810 and supports various streaming services."},




#         {'role': 'user', 'content': "What are the best practices for web development?"},
#         {'role': 'assistant', 'content': 'I cannot help you with this; however, we have the Haier Single Tub Washing Machine (HWM80-50), which is ideal for you when handling large loads.'},



     # {"role": "user", "content": "What are the features of Haier Spinner (HD 60-50)?"},
     # {'role': 'assistant', 'content': "The Haier Spinner (HD 60-50) is a top-loading washing machine with a 06KG capacity. It is priced at Rs 18673 and offers efficient cleaning."},


        # {'role': 'user', 'content': 'Act as an AI customer support chatbot specialized in Haier products. Provide accurate and helpful information, and ensure customer satisfaction.'},
        # {'role': 'assistant', 'content': 'I understand. I will act as an AI customer support chatbot specialized in Haier products.'},


        ## adding requirement 1 msg and 1 info msg
        
        {"role": "user", "content": "I need a fridge"},
         {'role': 'assistant', 'content': "Sure! We have several options available. Could you please specify your requirements or preferences?"},
 
        {'role': 'user', 'content': 'Any you have'},
            {'role': 'assistant', 'content': "We have various refrigerators available. Here's one option: Haier E-Star EP Series Refrigerator (HRF-438 EPR/EPB/EPC/EPG). It has a capacity of 246 liters with non-inverter technology. The price is Rs. 101,964. Let me know if this meets your requirements or if you want more options."},
{'role': 'user', 'content': 'Act as an AI customer support chatbot specialized in Haier products. Provide accurate and helpful information, and ensure customer satisfaction.'},
        {'role': 'assistant', 'content': 'I understand. I will act as an AI customer support chatbot specialized in Haier products.'},

        # {"role": "user", "content": "Hello"},
        #  {'role': 'assistant', 'content': "Hi there! How can I assist you today?"}


    ]
# Preprocess function
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)  # Remove special characters
    text = text.strip()
    return text
    
def getFewshotsHistory(query, user_history):

    database=haier_items
    # Query





    # Preprocessed query
    query_cleaned = preprocess(query)
    
    # Find the best match
    best_match = None
    best_score = 0
    
    for entry in database:
        product_info = preprocess(entry["Product Info"])
    
        # Calculate similarity score based on matching words
        query_words = set(query_cleaned.split())
        product_words = set(product_info.split())
        match_score = len(query_words & product_words)  # Intersection of words
    
        if match_score > best_score:
            best_score = match_score
            best_match = entry
    




    # ===========================================================




    
    global relevant_items,relevant_items1,relevant_items2,relevant_items3
    
    relevant_items = search(query,k=4)
    
    if best_match:
        logging.info(f"{best_match} is the exact string matching product found against query : {query} ")
        relevant_items.append(best_match)
        string_match=best_match
    
    else:
        logging.info(f"No exact string matching product found against query : {query}")
        string_match='Not Found'
        
    # Fetch relevant items based on the last user message (4 items)
    # relevant_items1 = search(user_history[-1]['content'], k=4) if len(user_history) > 0 else ["Air Conditioner"]
    relevant_items1 = search(user_history[-1]['content'] if len(user_history) > 0 else "Air Conditioner", k=4)

    # Fetch relevant items based on the second last message (3 items)
    relevant_items2 = search(user_history[-2]['content'] if len(user_history) > 1 else "Refrigerator", k=3)

    # Fetch relevant items based on the third last message (3 items)
    relevant_items3 = search(user_history[-3]['content'] if len(user_history) > 2 else "Washing Machine", k=3)

    logging.info("("*50)
    logging.info(f"Against the user query: {query}")
    logging.info("("*50)

    logging.info(")"*50)
    for rel in relevant_items:
        logging.info(f"Following products were found :{rel['Product Info']}\n")
    logging.info(")"*50)

    
    return [         
        {"role": "user", "content": f"Here are some products I am interested in: {', '.join([item['Product Info'] +' '+ item['Variation'] +' '+ 'priced at '+ str(item['Price(Rs)']) for item in relevant_items3])}. Read it and say OK"},
        {'role': 'assistant', 'content': 'OK'},
        {"role": "user", "content": f"Here are some more products I am interested in: {', '.join([item['Product Info'] +' '+ item['Variation'] +' '+ 'priced at '+ str(item['Price(Rs)']) for item in relevant_items2])}. Read it and say OK"},
        {'role': 'assistant', 'content': 'OK'},
        {"role": "user", "content": f"Here are some more products I am interested in: {', '.join([item['Product Info'] +' '+ item['Variation'] +' '+ 'priced at '+ str(item['Price(Rs)']) for item in relevant_items1])}. Read it and say OK"},
        {'role': 'assistant', 'content': 'OK'},
        {"role": "user", "content": f"Here are some more products I am interested in: {', '.join([item['Product Info'] +' '+ item['Variation'] +' '+ 'priced at '+ str(item['Price(Rs)']) for item in relevant_items])}. Read it and say OK"},
        {'role': 'assistant', 'content': 'OK'},

        
    # {"role": "user", "content": "What’s the price of the HMW-28100-28L Digital Grill Microwave Oven?"},
    # {"role": "assistant", "content": "The HMW-28100-28L Digital Grill Microwave Oven by Haier is priced at Rs 33,999. It's a versatile digital grill microwave and is currently listed as active in our catalog under Grill Series."},


    #     {'role': 'user', 'content': 'How do I make a pizza?'},
    #     {'role': 'assistant', 'content': "I cannot help you with this; however, we have the Haier Single Tub Washing Machine (HWM80-35), that can be of good use."},





    #  {"role": "user", "content": "Is the Haier 3D Wash Series Washing Machine still available?"},
    # {"role": "assistant", "content": "The Haier 3D Wash Series Washing Machine (HWM150-1789) is currently inactive. When available, it is listed in Top Load Fully Automatic and usually priced around Rs 112,400."},





    #     {'role': 'user', 'content': "What are the best practices for web development?"},
    #     {'role': 'assistant', 'content': 'I cannot help you with this; however, we have the Haier Single Tub Washing Machine (HWM80-50), which is ideal for you when handling large loads.'},



    # {"role": "user", "content": "Can you give me the details for the Marvel Inverter Series Air Conditioner?"},
    # {"role": "assistant", "content": "The Haier Marvel Inverter Series Air Conditioner (HSU-18HFMAE) is a 1.5-ton model listed under 'Home Appliances/Air Conditioners/Inverter AC.' It's inactive, but when available, it is priced around Rs 144,528."},





    #     {'role': 'user', 'content': 'does haier has apple iphone'},
    #     {'role': 'assistant', 'content': "No, Apple iPhone is not produced by Haier. However, we do have a range of home appliances such as washing machines, microwaves, and televisions. Is there anything specific you are looking for in terms of appliances?"},


    # {"role": "user", "content": "I’m looking for a T-Door SBS Refrigerator. Do you have any models?"},
    #     {"role": "assistant", "content": "The Haier T-Door SBS Series Refrigerator (HRF-578TBG/TBP/678TGG) is part of our Side by Side Refrigerator lineup. Although currently inactive, it is available in a sleek black glass finish and is usually priced at Rs 329,900."},



        {"role": "user", "content": "I need a fridge"},
         {'role': 'assistant', 'content': "Sure! We have several options available. Could you please specify your requirements or preferences?"},



        {'role': 'user', 'content': 'Any you have'},
        {'role': 'assistant', 'content': "We have various refrigerators available. Here's one option: Haier E-Star EP Series Refrigerator (HRF-438 EPR/EPB/EPC/EPG). It has a capacity of 246 liters with non-inverter technology. The price is Rs. 101,964. Let me know if this meets your requirements or if you want more options."},

        {'role': 'user', 'content': 'Act as an AI customer support chatbot specialized in Haier products. Provide accurate and helpful information, and ensure customer satisfaction.'},
        {'role': 'assistant', 'content': 'I understand. I will act as an AI customer support chatbot specialized in Haier products.'},

        # {"role": "user", "content": "Hello"},
        #  {'role': 'assistant', 'content': "Hi there! How can I assist you today?"}


    ], string_match


