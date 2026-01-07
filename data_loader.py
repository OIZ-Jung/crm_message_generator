import pandas as pd

def str_to_list(value, sep=","):
    if value is None:
        return []
    value = str(value).strip()
    if value == "":
        return []
    return [v.strip() for v in value.split(sep) if v.strip()]


def load_persona_csv(path: str, name: str) -> dict[str, any]:
    for enc in ["utf-8", "cp949", "euc-kr"]:
        try:
            df = pd.read_csv(path, encoding=enc)

            row = df[df["이름"] == name].iloc[0]

            custumer_persona = {
                "name":row['이름'],
                "age":row['나이'],
                "skin_type":str_to_list(row['피부타입']),
                "skin_issues":str_to_list(row['피부고민']),
                "lifestyle":(row['라이프스타일']),
                "preference":(row['취향']),
                "purchase_pattern":(row['소비패턴']),
                "prefered_brands":str_to_list(row['관심브랜드'])    
            }

            return custumer_persona
        except UnicodeDecodeError:
            continue
    raise ValueError("CSV 인코딩 불가")

import json

def load_persona_signals(path="persona_signals.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_xlsx(path:str):
    return pd.read_excel(path)


def load_csv(path: str):
    for enc in ["utf-8", "cp949", "euc-kr"]:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 인코딩을 읽을 수 없습니다.")

# def load_pdf_text(path):
#     reader = PdfReader(path)
#     return "\n".join(page.extract_text() for page in reader.pages)

# def load_pdf_text(path: str) -> str:
#     reader = PdfReader(path)
#     text = []

#     for page in reader.pages:
#         text.append(page.extract_text())

#     return "\n".join(text)


# def load_single_persona_beauty(path: str, name: str) -> str:
#     for enc in ["utf-8", "cp949", "euc-kr"]:
#         try:
#             df = pd.read_csv(path, encoding=enc)

#             row = df[df["이름"] == name].iloc[0]

#             persona_text = f"""
#         이름: {row['이름']}
#         나이: {row['나이']}세
#         피부 타입: {row['피부타입']}
#         피부 고민: {row['피부고민']}
#         관심 브랜드: {row['관심브랜드']}
#         """

#             return persona_text
#         except UnicodeDecodeError:
#             continue
#     raise ValueError("CSV 인코딩 불가")


# def load_single_persona(path: str, name: str) -> str:
#     for enc in ["utf-8", "cp949", "euc-kr"]:
#         try:
#             df = pd.read_csv(path, encoding=enc)

#             row = df[df["이름"] == name].iloc[0]

#             persona_text = f"""
#         이름: {row['이름']}
#         나이: {row['나이']}세
#         피부 타입: {row['피부타입']}
#         피부 고민: {row['피부고민']}
#         라이프스타일: {row['라이프스타일']}
#         소비 패턴: {row['소비패턴']}
#         관심 브랜드: {row['관심브랜드']}
#         취향: {row['취향']}
#         """

#             return persona_text
#         except UnicodeDecodeError:
#             continue
#     raise ValueError("CSV 인코딩 불가")