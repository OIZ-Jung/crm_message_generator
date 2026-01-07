from sentence_transformers import SentenceTransformer

import numpy as np
from dotenv import load_dotenv
load_dotenv()

def get_model():
    return SentenceTransformer("jhgan/ko-sroberta-multitask")

model = get_model()
def embed_texts(texts):
    return model.encode(texts)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_precomputed_products(_products):
    product_attrs = ['skin_type', 'benefits', 'brand', 'price_info', 'description']
    for p in _products:
        for attr in product_attrs:
            text = str(p['product_dict'].get(attr, ""))
            p[f'{attr}_embedding'] = embed_texts(text)
    return _products

def recommend_products(products, user_persona, top_k=3):
    # 속성 정의
    
    lifestyle_text = " ".join(user_persona.get("lifestyle", "").get("decision_drivers", [])) + "".join(user_persona.get("lifestyle", "").get("reacts_to", []))
    preference_text = " ".join(user_persona.get("preference", []))
    purchase_text = " ".join(user_persona.get("purchase_pattern", []))
    user_skin_type = " ".join(user_persona.get("skin_type", []))
    user_skin_issues = " ".join(user_persona.get("skin_issues", []))
    user_prefered_brands = " ".join(user_persona.get("prefered_brands", []))

    user_embeddings = {
        'lifestyle': embed_texts(lifestyle_text),
        'preference': embed_texts(preference_text),
        'purchase_pattern': embed_texts(purchase_text),
        'skin_type': embed_texts(user_skin_type),
        'skin_issues': embed_texts(user_skin_issues),
        'prefered_brands': embed_texts(user_prefered_brands)
    }
    
    weights = {
        'lifestyle': 0.1,
        'preference': 0.1,
        'purchase_pattern': 0.1,
        'skin_type': 0.05,
        'skin_issues': 0.15,
        'prefered_brands': 0.15,
        'discount_rate': 0.05
    }

    def compute_score(product):
        score = 0.0
        score += cosine_similarity(user_embeddings["skin_type"], product['skin_type_embedding']) * weights['skin_type']
        score += cosine_similarity(user_embeddings["prefered_brands"], product['brand_embedding']) * weights['prefered_brands']
        score += cosine_similarity(user_embeddings["skin_issues"], product['benefits_embedding']) * weights['skin_issues']
        score += cosine_similarity(user_embeddings["lifestyle"], product['description_embedding']) * weights['lifestyle']
        score += cosine_similarity(user_embeddings["preference"], product['description_embedding']) * weights['preference']
        score += cosine_similarity(user_embeddings["purchase_pattern"], product['description_embedding']) * weights['purchase_pattern']
        score += product['product_dict']['discount_rate'] * weights['discount_rate']
        return score
    
    for p in products:
        p['similarity_score'] = compute_score(p)

    ranked_products = sorted(products, key=lambda x: x['similarity_score'], reverse=True)
    return ranked_products[:top_k]


