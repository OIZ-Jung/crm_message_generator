# test_prompt.py

from prompt import PROMPT_TEMPLATE
from gemini_client import generate_text, generate_text_stream
from data_loader import load_csv, load_xlsx,load_persona_csv, load_persona_signals
from embedder import recommend_products, get_precomputed_products
from product_select import product_dict
from load import extract_persona_context
import streamlit as st
import time

@st.cache_data
def load_all_data():
    start_time = time.time()
    load_csv_brand_tone = load_csv("data/Brand_tone_guide.csv")
    load_product = load_xlsx("data/product.xlsx")
    load_persona = load_csv("data/고객_페르소나.csv")
    _product = product_dict(load_product)
    persona_signals = load_persona_signals("data/persona_signals.json")
    embedded_product = get_precomputed_products(_product)
    end_time = time.time()
    print(f"데이터 로드 및 임베딩 소요 시간: {end_time - start_time:.2f}초")
    return load_csv_brand_tone, load_product ,load_persona, embedded_product, persona_signals

load_csv_brand_tone, load_product ,load_persona, embedded_product, persona_signals = load_all_data()

import re
import json
def recommend_pro(selected_name):
    load_single_persona_data = load_persona_csv("data/고객_페르소나.csv", selected_name)
    persona_context = extract_persona_context(persona_signals, load_single_persona_data)
    recommend_products_list = recommend_products(products=embedded_product, user_persona=persona_context, top_k=3)
    product_top3 = [p['product_dict'] for p in recommend_products_list[:3]]

    return persona_context, product_top3


def test_prompt(product_top3, persona_context):
    start_time_1 = time.time()
    prompt_product = f"사용자에게 가장 적합한 제품을 추천해주세요. 후보: {product_top3}\
    \n사용자 페르소나: {json.dumps(persona_context, ensure_ascii=False,default=str)}\n\
    \n가장 적합한 제품의 이름이랑 브랜드를 반드시 JSON 형식으로만 출력해주세요(name, brand). 다른 건 출력하지 마세요.\
    \n예시: {{\"name\": \"제품이름 ml\", \"brand\": \"브랜드이름\"}}"
    end_time_1 = time.time()
    print(f"프롬프트 생성 소요 시간: {end_time_1 - start_time_1:.2f}초")
    start_time = time.time()
    response = generate_text(prompt_product)
    selected_product_response = response.strip()
    selected_product = {
        "name": "0",
        "brand": "0"
    }
    end_time = time.time()
    print(response)
    print(f"제품 선택 소요 시간: {end_time - start_time:.2f}초")

# 1️⃣ 중괄호 {} 안의 내용만 뽑기
    start_time_2 = time.time()
    match = re.search(r'\{.*\}', selected_product_response)  # { 로 시작해서 } 로 끝나는 문자열 찾기
    if match:
        json_str = match.group()  # 실제 JSON 문자열
        selected_product = json.loads(json_str)
    else:
        print("JSON 패턴을 찾지 못했습니다.")

    product_top1 = [p for p in product_top3 if p["name"] == selected_product["name"]][0]

    brands_rows = load_csv_brand_tone[load_csv_brand_tone['Brand'] == selected_product["brand"]]
    
    prompt = PROMPT_TEMPLATE.format(
        brand_data=brands_rows,
        customer_data=persona_context,
        target_info=product_top1,
    )
    end_time_2 = time.time()
    print(f"제품 정보 매칭 소요 시간: {end_time_2 - start_time_2:.2f}초")
    return prompt

def generate_marketing_message(prompt):    
    return generate_text_stream(prompt)

if __name__ == "__main__":
    left_empty, mid_column, right_empty = st.columns([1, 2, 1])
    custumer_name = load_persona['이름'].tolist()
    with mid_column:
        st.set_page_config(page_title="Test Prompt", layout="wide")
        st.title("제품 추천 메시지 생성기")
        selected_name = st.selectbox("이름을 선택하세요", custumer_name)
    st.subheader("메시지를 생성하려면 아래 버튼을 클릭하세요.")
    gen_button = st.button("메시지 생성하기")
    result_area = st.container()
    if gen_button:
        with result_area:
            start_time = time.time()
            result_area.empty()
            with st.spinner('사용자 성향 분석 및 제품 선정 중...'):
                persona_context, product_top3 = recommend_pro(selected_name)
                prompt = test_prompt(product_top3, persona_context)
            with st.spinner('메시지 생성 중...'):
                message_generator = generate_marketing_message(prompt)
                full_message = st.write_stream(message_generator)
            end_time = time.time()
            st.success(f'메시지 생성 완료! (소요 시간: {end_time - start_time:.2f}초)')
            with st.expander("프롬프트 보기"):
                st.code(prompt)