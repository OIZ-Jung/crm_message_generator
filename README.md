# CRM Message Generator

고객 페르소나 기반 제품 추천 및 마케팅 메시지를 생성하는 **Streamlit 데모 프로젝트**입니다.  
이 프로젝트는 **화장품 CRM 공모전을 염두에 두고 설계**되었지만, 독립적인 학습용 프로젝트입니다.

---

## Features

- 고객 페르소나 분석
- Embedding 기반 Top-3 후보 필터링 + LLM 최적 제품 추천
- 브랜드 톤 가이드 반영 마케팅 메시지 생성
- Streamlit UI를 통한 간단한 인터랙션
- Docker 기반 실행 환경

---

## Dataset

모든 데이터셋은 **데모용으로 직접 제작**한 샘플 데이터입니다.
실제 고객 데이터를 포함하지 않으며 가상 데이터입니다.

- `data/Brand_tone_guide.csv` : 브랜드 톤 가이드
- `data/product.xlsx` : 제품 목록
- `data/고객_페르소나.csv` : 고객 페르소나
- `data/persona_signals.json` : 페르소나 시그널 정보
- `data/라이프스타일_취향_소비패턴목록.pdf` : persona_signals.json 변환 전 원문
- `data/브랜드.csv` : Brand_tone_guide.csv 변환 전 원문

---

## Run Locally (Streamlit)

1. 가상환경 활성화

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

2. 의존성 설치

```bash
   pip install -r requirements.txt
```

3. Steamlit 실행

```bash
   streamlit run test.py --server.port 9000
```

## Run with Docker

```bash
docker build -t crm-app .
docker run -p 9000:9000 --env-file .env crm-app
```

## Demo

![CRM Message Generator](assets/0108.gif)
_메시지 생성 시연_
