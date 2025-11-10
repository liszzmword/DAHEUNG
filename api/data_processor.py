import pandas as pd
import numpy as np
from datetime import datetime
import re

class DataProcessor:
    def __init__(self):
        self.sales_data = None
        self.company_data = None
        self.load_data()

    def load_data(self):
        """데이터 로드 및 전처리"""
        # CSV 파일 로드
        self.sales_data = pd.read_csv('SALES DATA.csv', encoding='utf-8-sig')

        # Excel 파일 로드
        self.company_data = pd.read_excel('Details of the company.xlsx')

        # 데이터 전처리
        self._preprocess_sales_data()
        self._preprocess_company_data()

    def _clean_number(self, value):
        """숫자 형식 정리 (쉼표 제거)"""
        if pd.isna(value):
            return 0
        if isinstance(value, str):
            # 쉼표 제거 및 공백 제거
            value = value.replace(',', '').strip()
            try:
                return float(value)
            except:
                return 0
        return float(value)

    def _clean_percentage(self, value):
        """퍼센트 형식 정리"""
        if pd.isna(value):
            return 0.0
        if isinstance(value, str):
            value = value.replace('%', '').strip()
            try:
                return float(value)
            except:
                return 0.0
        return float(value)

    def _preprocess_sales_data(self):
        """판매 데이터 전처리"""
        # 컬럼명 정리
        self.sales_data.columns = self.sales_data.columns.str.strip()

        # 날짜 형식 변환
        self.sales_data['매출일'] = pd.to_datetime(self.sales_data['매출일'])

        # 숫자 컬럼 정리
        numeric_columns = ['수량', '매입단가(3%)', '판매단가', '공급가액', '부가세', '합계']
        for col in numeric_columns:
            self.sales_data[col] = self.sales_data[col].apply(self._clean_number)

        # 마진율 정리
        self.sales_data['마진율'] = self.sales_data['마진율'].apply(self._clean_percentage)

        # 연도, 월, 분기 추가
        self.sales_data['연도'] = self.sales_data['매출일'].dt.year
        self.sales_data['월'] = self.sales_data['매출일'].dt.month
        self.sales_data['분기'] = self.sales_data['매출일'].dt.quarter

        # 거래처명 정리
        self.sales_data['거래처'] = self.sales_data['거래처'].str.strip()

    def _preprocess_company_data(self):
        """기업 데이터 전처리"""
        # 컬럼명 정리
        self.company_data.columns = self.company_data.columns.str.strip()

        # 거래처명 정리
        self.company_data['거래처'] = self.company_data['거래처'].str.strip()

    def get_product_sales_analysis(self, product_code):
        """특정 제품의 판매 분석"""
        # 제품명에서 제품 코드 추출 (예: 9322-14)
        product_sales = self.sales_data[
            self.sales_data['제품명'].str.contains(product_code, na=False, case=False)
        ]

        if len(product_sales) == 0:
            return None

        # 판매량 분석
        total_quantity = product_sales['수량'].sum()
        total_revenue = product_sales['합계'].sum()
        avg_margin = product_sales['마진율'].mean()

        # 월별 판매 추이
        monthly_sales = product_sales.groupby(['연도', '월']).agg({
            '수량': 'sum',
            '합계': 'sum'
        }).reset_index()

        # 구매 기업 리스트
        customer_list = product_sales.groupby('거래처').agg({
            '수량': 'sum',
            '합계': 'sum',
            '매출일': 'count'
        }).reset_index()
        customer_list.columns = ['거래처', '총구매수량', '총구매금액', '구매횟수']
        customer_list = customer_list.sort_values('총구매금액', ascending=False)

        return {
            'product_code': product_code,
            'total_quantity': int(total_quantity),
            'total_revenue': int(total_revenue),
            'avg_margin': round(avg_margin, 2),
            'monthly_sales': monthly_sales.to_dict('records'),
            'customers': customer_list.to_dict('records'),
            'transaction_count': len(product_sales)
        }

    def get_customer_characteristics(self, customer_names):
        """구매 기업들의 특징 분석"""
        if isinstance(customer_names, str):
            customer_names = [customer_names]

        # 기업 정보 가져오기
        customer_info = self.company_data[
            self.company_data['거래처'].isin(customer_names)
        ].copy()

        if len(customer_info) == 0:
            return None

        # 통계 분석
        characteristics = {
            'total_customers': len(customer_info),
            'industry_distribution': customer_info['업종'].value_counts().to_dict(),
            'avg_employee_count': int(customer_info['직원수'].mean()) if '직원수' in customer_info.columns else 0,
            'location_distribution': customer_info['시도'].value_counts().to_dict(),
            'customer_grade_distribution': customer_info['고객등급'].value_counts().to_dict(),
            'avg_growth_rate': round(customer_info['연평균성장률'].mean(), 2) if '연평균성장률' in customer_info.columns else 0,
            'details': customer_info[['거래처', '업종', '세부 업종', '직원수', '고객등급', '시도']].to_dict('records')
        }

        return characteristics

    def get_customer_trend_analysis(self, months=6):
        """최근 N개월 고객 구매 트렌드 분석"""
        # 최근 날짜 기준
        latest_date = self.sales_data['매출일'].max()
        cutoff_date = latest_date - pd.DateOffset(months=months)

        # 전체 기간 데이터
        all_data = self.sales_data.copy()

        # 최근 N개월 데이터
        recent_data = self.sales_data[self.sales_data['매출일'] >= cutoff_date]

        # 고객별 매출 집계
        customer_total = all_data.groupby('거래처').agg({
            '합계': 'sum',
            '매출일': ['min', 'max', 'count']
        }).reset_index()
        customer_total.columns = ['거래처', '총매출', '첫구매일', '최근구매일', '구매횟수']

        # 날짜를 문자열로 변환 (JSON 직렬화 오류 방지)
        customer_total['첫구매일'] = customer_total['첫구매일'].dt.strftime('%Y-%m-%d')
        customer_total['최근구매일'] = customer_total['최근구매일'].dt.strftime('%Y-%m-%d')

        customer_recent = recent_data.groupby('거래처')['합계'].sum().reset_index()
        customer_recent.columns = ['거래처', f'최근{months}개월매출']

        # 이전 N개월 데이터
        previous_cutoff = cutoff_date - pd.DateOffset(months=months)
        previous_data = self.sales_data[
            (self.sales_data['매출일'] >= previous_cutoff) &
            (self.sales_data['매출일'] < cutoff_date)
        ]
        customer_previous = previous_data.groupby('거래처')['합계'].sum().reset_index()
        customer_previous.columns = ['거래처', f'이전{months}개월매출']

        # 데이터 병합
        analysis = customer_total.merge(customer_recent, on='거래처', how='left')
        analysis = analysis.merge(customer_previous, on='거래처', how='left')
        analysis = analysis.fillna(0)

        # 증감율 계산
        analysis['증감율'] = ((analysis[f'최근{months}개월매출'] - analysis[f'이전{months}개월매출']) /
                           (analysis[f'이전{months}개월매출'] + 1) * 100)

        # 구매량 증가 고객
        increasing_customers = analysis[analysis['증감율'] > 10].sort_values('증감율', ascending=False).head(20)

        # 구매량 감소 고객
        decreasing_customers = analysis[analysis['증감율'] < -10].sort_values('증감율').head(20)

        # 휴면 고객 (최근 N개월 구매 없음)
        inactive_customers = analysis[analysis[f'최근{months}개월매출'] == 0].sort_values('총매출', ascending=False).head(20)

        return {
            'increasing_customers': increasing_customers.to_dict('records'),
            'decreasing_customers': decreasing_customers.to_dict('records'),
            'inactive_customers': inactive_customers.to_dict('records'),
            'summary': {
                'total_customers': len(customer_total),
                'active_customers': len(analysis[analysis[f'최근{months}개월매출'] > 0]),
                'increasing_count': len(analysis[analysis['증감율'] > 10]),
                'decreasing_count': len(analysis[analysis['증감율'] < -10])
            }
        }

    def get_marketing_recommendations(self):
        """마케팅 대상 추천"""
        # 최근 6개월 트렌드 분석
        trend = self.get_customer_trend_analysis(6)

        recommendations = []

        # 1. 구매량 감소 고객 - 재활성화 필요
        for customer in trend['decreasing_customers'][:5]:
            company_info = self.company_data[self.company_data['거래처'] == customer['거래처']]
            recommendations.append({
                'customer': customer['거래처'],
                'reason': '구매량 감소',
                'metric': f"감소율: {customer['증감율']:.1f}%",
                'action': '재활성화 마케팅',
                'priority': 'High',
                'total_revenue': customer['총매출']
            })

        # 2. 휴면 고객 중 과거 매출이 높았던 고객
        for customer in trend['inactive_customers'][:5]:
            recommendations.append({
                'customer': customer['거래처'],
                'reason': '휴면 고객 (과거 우수 고객)',
                'metric': f"과거 총매출: {customer['총매출']:,.0f}원",
                'action': '복귀 유도 프로모션',
                'priority': 'High',
                'total_revenue': customer['총매출']
            })

        # 3. 구매량 증가 고객 - 더 많은 제품 제안
        for customer in trend['increasing_customers'][:3]:
            recommendations.append({
                'customer': customer['거래처'],
                'reason': '구매량 지속 증가',
                'metric': f"증가율: {customer['증감율']:.1f}%",
                'action': '추가 제품 교차 판매',
                'priority': 'Medium',
                'total_revenue': customer['총매출']
            })

        return recommendations

    def get_sales_summary(self):
        """전체 판매 요약"""
        total_revenue = self.sales_data['합계'].sum()
        total_transactions = len(self.sales_data)
        unique_customers = self.sales_data['거래처'].nunique()
        avg_transaction = total_revenue / total_transactions

        # 최근 1년 매출
        latest_date = self.sales_data['매출일'].max()
        one_year_ago = latest_date - pd.DateOffset(years=1)
        recent_revenue = self.sales_data[self.sales_data['매출일'] >= one_year_ago]['합계'].sum()

        return {
            'total_revenue': int(total_revenue),
            'total_transactions': total_transactions,
            'unique_customers': unique_customers,
            'avg_transaction': int(avg_transaction),
            'recent_year_revenue': int(recent_revenue),
            'latest_date': latest_date.strftime('%Y-%m-%d')
        }

    def search_products(self, keyword):
        """제품 검색"""
        products = self.sales_data[
            self.sales_data['제품명'].str.contains(keyword, na=False, case=False)
        ]['제품명'].unique().tolist()
        return products[:20]  # 상위 20개만

    def search_customers(self, keyword):
        """고객 검색"""
        customers = self.sales_data[
            self.sales_data['거래처'].str.contains(keyword, na=False, case=False)
        ]['거래처'].unique().tolist()
        return customers[:20]  # 상위 20개만
