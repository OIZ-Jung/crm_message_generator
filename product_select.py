# def product_select_1(df, 속성명, 찾을거):
#     # mask = df[속성명].apply(lambda x: x in 찾을거)
#     row = df[df[속성명] == 찾을거]
#     list = []
#     for i in range(len(row)):
#         설명 = f"""
# 제품명:{row["제품"].iloc[i]}
# 원가:{row["원가"].iloc[i]}
# 판매가:{row["판매가"].iloc[i]}
# 할인율:{row["할인률"].iloc[i]}
# 제품타입:{row["제품 타입"].iloc[i]}
# 기능:{row["기능(특징)"].iloc[i]}
# 핵심성분:{row["핵심성분"].iloc[i]}
# 추천나이:{row["나이(대)"].iloc[i]}
# 설명:{row["설명"].iloc[i]}
#         """
#         list.append(설명)
    
#     result = "\n".join(list)
#     return result

# def product_select_all_chunk(df):
#     # mask = df[속성명].apply(lambda x: x in 찾을거)
#     row = df
#     chunk = []
#     for i in range(len(row)):
#         설명 = f"""
# 나이:{row["나이(대)"].iloc[i]}
# 설명:{row["설명"].iloc[i]}
#         """
#         chunk.append(설명)
    
#     return chunk

# def 제품_인덱스_나와라_얍(row, i, list):
#     설명 = f"""
#     제품명:{row["제품"].iloc[i]}
#     원가:{row["원가"].iloc[i]}
#     판매가:{row["판매가"].iloc[i]}
#     할인율:{row["할인률"].iloc[i]}
#     제품타입:{row["제품 타입"].iloc[i]}
#     기능:{row["기능(특징)"].iloc[i]}
#     핵심성분:{row["핵심성분"].iloc[i]}
#     추천나이:{row["나이(대)"].iloc[i]}
#     설명:{row["설명"].iloc[i]}
#         """
#     list.append(설명)

def product_dict(df):
    df['product_dict'] = df.apply(lambda row: {
    "name": row['제품'],
    "brand": row['브랜드'],
    "skin_type": row['피부타입'],
    "benefits": row['기능(특징)'],
    "price_info": f"{row['판매가']}원, 할인 {row['할인률']*100}%",
    "key_ingredients": row['핵심성분'],
    "description": row['설명'],
    "discount_rate":row['할인률']
}, axis=1)
    return df[['product_dict']].to_dict(orient='records')



