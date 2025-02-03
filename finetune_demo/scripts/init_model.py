import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from haierItems import *
import random
from utils import *

# def initialize_search():
#     # Inventory data setup


#     # Create a DataFrame from the inventory
#     df_transformers = pd.DataFrame(haier_items)

#     # Combine relevant fields to form searchable text for each item
#     df_transformers['combined'] = df_transformers.apply(lambda row: f"{row['Product Info']} {row['Categories']} {row['Variation']}", axis=1)

#     texts_transformers = df_transformers['combined'].tolist()
#     logging.info("^^^^^^^^^^^^ init_model_py > def initialize_search(): ^^^^^^^^^^^^")
#     logging.info("texts_transformers[0]: "+ str(texts_transformers[0]))
#     logging.info("^^^^^^^^^^^^ init_model_py > def initialize_search(): ^^^^^^^^^^^^")
#     # Initialize sentence transformer model and encode the combined texts
#     model_transformers = SentenceTransformer('all-MiniLM-L6-v2')
#     embeddings_transformers = model_transformers.encode(texts_transformers)

#     # Setup FAISS index for similarity search
#     dimension_transformers = embeddings_transformers.shape[1]
#     index_transformers = faiss.IndexFlatL2(dimension_transformers)
#     index_transformers.add(np.array(embeddings_transformers))

#     return df_transformers, model_transformers, index_transformers

def initialize_search():
    # Inventory data setup
    df_transformers = pd.DataFrame(haier_items)

    # Combine relevant fields to form searchable text for each item
    df_transformers['combined'] = df_transformers.apply(
        lambda row: f"{row['Product Info']} {row['Categories']} {row['Variation']}", axis=1
    )

    texts_transformers = df_transformers['combined'].tolist()
    
    # Initialize sentence transformer model and encode the combined texts
    model_transformers = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings_transformers = model_transformers.encode(texts_transformers)

    # Setup FAISS index for similarity search
    dimension_transformers = embeddings_transformers.shape[1]
    index_transformers = faiss.IndexFlatL2(dimension_transformers)
    index_transformers.add(np.array(embeddings_transformers))

    return df_transformers, model_transformers, index_transformers
# Initialize search components
df_transformers, model_transformers, index_transformers = initialize_search()
