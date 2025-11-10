# B2B AI 데이터 분석 에이전트

Gemini 2.5 Pro를 활용한 B2B 영업 데이터 분석 및 인사이트 제공 AI 에이전트

## 주요 기능

### 1. 대화형 데이터 분석
- 자연어 질문으로 데이터 분석 요청
- AI가 데이터를 분석하고 비즈니스 인사이트 제공
- 실시간 대화 기반 상호작용

### 2. 제품 분석
- 특정 제품의 판매량, 매출, 마진율 분석
- 월별 판매 추이 시각화
- 주요 구매 기업 파악
- 구매 기업들의 특성 분석 (업종, 규모, 위치 등)

### 3. 고객 트렌드 분석
- 구매량 증가 고객 파악
- 구매량 감소 고객 파악
- 휴면 고객 식별
- 고객별 구매 패턴 분석

### 4. 마케팅 타겟 추천
- 데이터 기반 마케팅 대상 고객 추천
- 우선순위별 고객 분류
- 고객별 맞춤 마케팅 전략 제안

### 5. 인터랙티브 시각화
- Plotly 기반 동적 차트 생성
- 라인 차트, 바 차트, 파이 차트 등 다양한 시각화
- 반응형 차트로 상세 데이터 확인

## 시스템 구조

```
B2B_AI_AGENT/
├── data_processor.py      # 데이터 처리 및 분석 모듈
├── ai_agent.py           # Gemini AI 에이전트 모듈
├── visualizer.py         # 데이터 시각화 모듈
├── app.py               # Flask 백엔드 API
├── static/
│   └── index.html       # 웹 프론트엔드
├── SALES DATA.csv       # 판매 데이터
├── Details of the company.xlsx  # 기업 정보
└── README.md
```

## 설치 및 실행

### 1. 필요한 패키지 설치

```bash
pip install openpyxl pandas flask flask-cors google-generativeai matplotlib seaborn plotly python-dotenv
```

### 2. 서버 실행

```bash
python app.py
```

### 3. 웹 브라우저에서 접속

```
http://localhost:5000
```

## API 엔드포인트

### 채팅 API
```
POST /api/chat
Body: {"message": "질문 내용"}
```

### 대화 초기화
```
POST /api/reset
```

### 제품 검색
```
GET /api/search/products?keyword=검색어
```

### 고객 검색
```
GET /api/search/customers?keyword=검색어
```

### 제품 분석
```
GET /api/analytics/product/<제품코드>
```

### 트렌드 분석
```
GET /api/analytics/trends?months=6
```

### 마케팅 추천
```
GET /api/analytics/marketing
```

### 전체 요약
```
GET /api/summary
```

## 사용 예시

### 1. 제품 분석 질문
```
9322-14 제품의 판매량에 대해 알려주고 해당 제품을 구매한 기업들의 특징을 알려줘
```

**AI 응답:**
- 제품 판매량, 매출, 마진율 통계
- 월별 판매 추이 그래프
- 주요 구매 고객 목록
- 구매 기업들의 업종 분포, 지역 분포, 평균 직원 수 등

### 2. 트렌드 분석 질문
```
최근 구매량이 줄어든 고객을 알려줘
```

**AI 응답:**
- 구매량 감소율 TOP 고객 목록
- 각 고객의 과거 매출 정보
- 감소 추이 시각화
- 재활성화 전략 제안

### 3. 마케팅 전략 질문
```
지금 어떤 고객한테 마케팅을 해야될까?
```

**AI 응답:**
- 우선순위별 마케팅 타겟 고객
- 각 고객별 추천 전략
- 예상 효과 및 근거

### 4. 복합 질문
```
최근 6개월 동안 구매량이 늘어난 고객들은 어떤 업종이 많아?
```

**AI 응답:**
- 구매 증가 고객 목록
- 업종별 분포 분석
- 파이 차트로 시각화
- 비즈니스 인사이트 제공

## 데이터 구조

### SALES DATA.csv (판매 데이터)
- 번호, 매출일, 거래처, 담당사원
- 제품명, 규격, 제품군
- 수량, 매입단가, 판매단가
- 공급가액, 부가세, 합계, 마진율

### Details of the company.xlsx (기업 정보)
- 거래처, 사업자등록번호
- 총 매출, 해당 제품군 매출 합계
- 고객등급, 연평균성장률
- 최초거래연도, 최신거래연도
- 업종, 세부 업종, 직원수
- 시도, 시군구, 주소, 상태, SNS유무

## 기술 스택

- **AI Model**: Google Gemini 2.5 Pro
- **Backend**: Python, Flask, Flask-CORS
- **Data Processing**: Pandas, NumPy, OpenPyXL
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Frontend**: HTML, CSS, JavaScript

## 주요 특징

1. **자연어 처리**: 일상 언어로 질문 가능
2. **지능형 분석**: AI가 질문을 이해하고 적절한 데이터 분석 수행
3. **실시간 시각화**: 분석 결과를 즉시 차트로 표현
4. **비즈니스 인사이트**: 단순 데이터 제공이 아닌 실행 가능한 전략 제안
5. **대화 기반**: 이전 대화 맥락을 이해하고 연속된 질문 처리

## 환경 변수

`app.py`에서 직접 API 키를 설정하거나, 환경 변수로 관리할 수 있습니다:

```python
API_KEY = "YOUR_GEMINI_API_KEY"
```

## 보안 주의사항

- API 키는 절대 공개 저장소에 업로드하지 마세요
- 프로덕션 환경에서는 환경 변수나 비밀 관리 서비스 사용
- 필요시 `.env` 파일을 사용하여 API 키 관리

## 문제 해결

### 인코딩 오류
데이터 파일이 UTF-8로 인코딩되어 있는지 확인하세요.

### 패키지 설치 오류
Python 3.8 이상 버전을 사용하세요.

### API 오류
Gemini API 키가 올바른지, 할당량이 남아있는지 확인하세요.

## 향후 개선 사항

- [ ] 다국어 지원
- [ ] 사용자 인증 및 권한 관리
- [ ] 데이터 업로드 기능
- [ ] Excel/PDF 리포트 생성
- [ ] 대시보드 템플릿
- [ ] 이메일 알림 기능
- [ ] 예측 분석 기능

## 라이선스

MIT License

## 개발자

AI Agent developed with Gemini 2.5 Pro

## 문의

이슈나 질문이 있으시면 GitHub Issues를 이용해주세요.
