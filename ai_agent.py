import google.generativeai as genai
import json
from data_processor import DataProcessor

class B2BAnalystAgent:
    def __init__(self, api_key):
        """Gemini AI Agent 초기화"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.data_processor = DataProcessor()
        self.conversation_history = []

    def _create_system_prompt(self):
        """시스템 프롬프트 생성"""
        summary = self.data_processor.get_sales_summary()

        return f"""당신은 B2B 영업 및 마케팅 데이터 분석 전문가입니다.

현재 데이터베이스 정보:
- 총 매출액: {summary['total_revenue']:,}원
- 총 거래 건수: {summary['total_transactions']:,}건
- 고유 고객 수: {summary['unique_customers']}개
- 평균 거래액: {summary['avg_transaction']:,}원
- 최근 1년 매출: {summary['recent_year_revenue']:,}원
- 최신 데이터 날짜: {summary['latest_date']}

당신의 역할:
1. 사용자의 질문을 분석하고 적절한 데이터 분석을 수행합니다.
2. 제품 판매 분석, 고객 특성 분석, 트렌드 분석 등을 제공합니다.
3. 마케팅 전략과 실행 가능한 인사이트를 제공합니다.
4. 데이터를 기반으로 명확하고 구체적인 답변을 제공합니다.

**중요: 응답 구조 및 스타일**
답변은 반드시 아래 형식을 따라 그래프와 표를 중심으로 작성하세요:

1. **📊 핵심 요약** (2-3줄)
   - 질문에 대한 핵심 답변을 간결하게 제시

2. **📈 주요 데이터 및 시각화 안내**
   - "아래 그래프를 보시면..." 또는 "차트에서 확인하실 수 있듯이..."로 시작
   - 생성되는 그래프/차트를 명시적으로 언급
   - 그래프에서 확인할 수 있는 핵심 인사이트 설명

3. **📋 상세 분석 (표 형식 활용)**
   - 주요 수치를 표 형식으로 제시
   - TOP 5-10 리스트를 명확히 나열
   - 각 항목에 대한 간단한 설명 추가

4. **💡 비즈니스 인사이트**
   - 데이터에서 발견된 패턴 및 트렌드
   - 실행 가능한 권장사항

응답 작성 규칙:
- 항상 "차트를 보시면", "그래프에서 확인할 수 있듯이", "위 표에서" 등의 표현 사용
- 구체적인 숫자와 함께 설명 (예: "TOP 1위 고객은 XXX사로 총 1,234,567원 구매")
- 그래프/표가 생성될 것임을 미리 안내
- 표 형식으로 정리할 때는 마크다운 테이블 또는 번호 리스트 사용

질문 유형별 처리:
- 제품 분석: 제품 코드/이름으로 판매량, 매출, 마진율, 구매 고객 분석
- 고객 분석: 고객별 구매 패턴, 특성, 산업 분포 분석
- 트렌드 분석: 구매 증가/감소 고객, 휴면 고객 파악
- 마케팅 추천: 타겟 고객 선정, 우선순위, 전략 제안

주요 제품군:
1. **9322 시리즈**: 9322-14 등의 제품 (기본 패턴: XXXX-XX)
2. **GPL 시리즈**: GPL-110GF, GPL-080GF, GPL-160GF 등 (패턴: GPL-XXXGF)
3. **9448HK 시리즈**: 9448HK, Y-9448HK, 9448HK BLACK 등 (패턴: 9448HK 포함)

사용 가능한 함수:
1. get_product_analysis(product_code) - 특정 제품 판매 분석
2. get_customer_characteristics(customer_list) - 고객 특성 분석
3. get_trend_analysis() - 고객 구매 트렌드 분석
4. get_marketing_recommendations() - 마케팅 대상 추천
5. search_products(keyword) - 제품 검색
6. search_customers(keyword) - 고객 검색

항상 데이터 기반의 객관적인 분석을 제공하고, 비즈니스 의사결정에 도움이 되는 인사이트를 제공하세요."""

    def _analyze_query(self, user_query):
        """사용자 질문 분석 및 필요한 데이터 수집"""
        analysis_results = {}

        # 제품 코드 패턴 찾기
        import re

        # 1. 기본 제품 코드 패턴 (예: 9322-14, 1234-56 등)
        product_codes = re.findall(r'\d{4}-\d{2}', user_query)

        # 2. GPL 제품 패턴 (예: GPL-110GF, GPL-080GF 등)
        gpl_codes = re.findall(r'GPL-?\d{3}[A-Z]*', user_query, re.IGNORECASE)

        # 3. 9448HK 제품 패턴 (예: 9448HK, Y-9448HK 등)
        hk_codes = re.findall(r'[A-Z]?-?9448[A-Z]*', user_query, re.IGNORECASE)

        # 모든 제품 코드 통합
        all_product_codes = product_codes + gpl_codes + hk_codes

        # 질문에 GPL 또는 9448 언급이 있는지 확인
        if 'GPL' in user_query.upper():
            all_product_codes.append('GPL')
        if '9448' in user_query:
            all_product_codes.append('9448HK')

        # 질문 유형 판단
        query_lower = user_query.lower()

        # 그래프/표 요청 여부 확인
        visualization_keywords = ['그래프', '차트', '표', '시각화', '보여', '그려', '도표', '막대', '파이', '라인']
        needs_visualization = any(keyword in user_query for keyword in visualization_keywords)

        # 1. 제품 분석 질문 (더 적극적으로 감지)
        product_keywords = ['제품', '판매량', '매출', '판매', '상품', '물건']
        if all_product_codes or any(keyword in user_query for keyword in product_keywords):
            if all_product_codes:
                for code in all_product_codes:
                    product_analysis = self.data_processor.get_product_sales_analysis(code)
                    if product_analysis:
                        # 안전한 키 생성 (특수문자 제거)
                        safe_key = re.sub(r'[^a-zA-Z0-9_]', '_', code)
                        analysis_results[f'product_{safe_key}'] = product_analysis

                        # 해당 제품 구매 고객 특성 (항상 포함)
                        customer_names = [c['거래처'] for c in product_analysis['customers'][:20]]
                        if customer_names:
                            customer_chars = self.data_processor.get_customer_characteristics(customer_names)
                            if customer_chars:
                                analysis_results[f'customers_of_{safe_key}'] = customer_chars
            else:
                # 제품 코드가 없지만 제품 관련 질문인 경우, 검색 힌트 제공
                analysis_results['hint'] = 'product_search_needed'

        # 2. 트렌드 분석 질문 (더 적극적으로 감지)
        trend_keywords = ['증가', '감소', '늘어', '줄어', '휴면', '트렌드', '변화', '추이', '성장', '하락']
        if any(keyword in user_query for keyword in trend_keywords) or needs_visualization:
            trend_analysis = self.data_processor.get_customer_trend_analysis(6)
            analysis_results['trend_analysis'] = trend_analysis

        # 3. 마케팅 추천 질문
        if any(keyword in user_query for keyword in ['마케팅', '추천', '타겟', '대상', '영업']):
            marketing_recs = self.data_processor.get_marketing_recommendations()
            analysis_results['marketing_recommendations'] = marketing_recs

        # 4. 고객 특성 질문
        if '고객' in user_query or '기업' in user_query or '거래처' in user_query:
            # 특정 고객명이 있는지 확인
            customers = self.data_processor.search_customers('')
            mentioned_customers = [c for c in customers if c in user_query]

            if mentioned_customers:
                customer_chars = self.data_processor.get_customer_characteristics(mentioned_customers)
                analysis_results['specific_customers'] = customer_chars

        return analysis_results

    def chat(self, user_message):
        """사용자와 대화하고 분석 제공"""
        # 데이터 분석 수행
        analysis_data = self._analyze_query(user_message)

        # 프롬프트 구성
        system_prompt = self._create_system_prompt()

        # 분석 결과를 포함한 컨텍스트 생성
        context = f"\n\n분석 데이터:\n{json.dumps(analysis_data, ensure_ascii=False, indent=2)}"

        # 대화 히스토리 구성
        messages = []
        for msg in self.conversation_history[-10:]:  # 최근 10개만 유지
            messages.append({
                'role': msg['role'],
                'parts': [msg['content']]
            })

        # 시각화 정보
        viz_info = ""
        if analysis_data:
            available_charts = []
            if any(key.startswith('product_') for key in analysis_data.keys()):
                available_charts.append("📈 월별 판매 추이 차트")
                available_charts.append("🏆 주요 구매 고객 TOP 15 차트")
                available_charts.append("🏢 고객 업종 분포 파이 차트")
                available_charts.append("📍 고객 지역 분포 파이 차트")
            if 'trend_analysis' in analysis_data:
                available_charts.append("📈 구매량 증가 고객 TOP 10 차트")
                available_charts.append("📉 구매량 감소 고객 TOP 10 차트")

            if available_charts:
                viz_info = f"\n\n생성 가능한 차트:\n" + "\n".join([f"- {chart}" for chart in available_charts])
                viz_info += "\n\n**중요**: 위 차트들이 자동으로 생성되어 사용자에게 표시됩니다. 답변에서 이 차트들을 반드시 언급하세요!"

        # 현재 메시지 추가
        full_prompt = f"""{system_prompt}

사용자 질문: {user_message}

분석 데이터:{context}{viz_info}

**답변 지침**:
1. 위 분석 데이터를 활용하여 답변하세요
2. 생성 가능한 차트가 있다면 반드시 "아래 그래프를 확인하시면...", "차트에서 보시는 것처럼..." 등으로 언급하세요
3. 구체적인 숫자와 함께 표 형식(마크다운 테이블 또는 번호 리스트)으로 데이터를 제시하세요
4. 비즈니스 인사이트와 실행 가능한 권장사항을 제공하세요"""

        messages.append({
            'role': 'user',
            'parts': [full_prompt]
        })

        # Gemini API 호출
        try:
            chat = self.model.start_chat(history=messages[:-1])
            response = chat.send_message(messages[-1]['parts'][0])

            assistant_message = response.text

            # 대화 히스토리 업데이트
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            self.conversation_history.append({
                'role': 'model',
                'content': assistant_message
            })

            return {
                'response': assistant_message,
                'analysis_data': analysis_data,
                'visualizations': self._suggest_visualizations(analysis_data)
            }

        except Exception as e:
            return {
                'response': f"죄송합니다. 오류가 발생했습니다: {str(e)}",
                'analysis_data': analysis_data,
                'visualizations': []
            }

    def _suggest_visualizations(self, analysis_data):
        """분석 데이터에 적합한 시각화 제안"""
        visualizations = []

        for key, data in analysis_data.items():
            if key.startswith('product_'):
                # 제품 분석 시각화
                visualizations.append({
                    'type': 'line_chart',
                    'title': f'📈 월별 판매 추이',
                    'data_key': key,
                    'x': '월',
                    'y': '판매량'
                })
                visualizations.append({
                    'type': 'bar_chart',
                    'title': f'🏆 주요 구매 고객 TOP 15',
                    'data_key': key,
                    'x': '거래처',
                    'y': '총구매금액'
                })

            elif key == 'trend_analysis':
                # 트렌드 분석 시각화
                visualizations.append({
                    'type': 'bar_chart',
                    'title': '📈 구매량 증가 고객 TOP 10',
                    'data_key': 'increasing_customers',
                    'x': '거래처',
                    'y': '증감율'
                })
                visualizations.append({
                    'type': 'bar_chart',
                    'title': '📉 구매량 감소 고객 TOP 10',
                    'data_key': 'decreasing_customers',
                    'x': '거래처',
                    'y': '증감율'
                })

            elif key.startswith('customers_of_'):
                # 고객 특성 시각화
                visualizations.append({
                    'type': 'pie_chart',
                    'title': '🏢 고객 업종 분포',
                    'data_key': key,
                    'field': 'industry_distribution'
                })
                visualizations.append({
                    'type': 'pie_chart',
                    'title': '📍 고객 지역 분포',
                    'data_key': key,
                    'field': 'location_distribution'
                })

            elif key == 'marketing_recommendations':
                # 마케팅 추천은 표로 표시되므로 별도 차트 불필요
                pass

        return visualizations

    def reset_conversation(self):
        """대화 히스토리 초기화"""
        self.conversation_history = []
