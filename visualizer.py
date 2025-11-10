import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

class DataVisualizer:
    """데이터 시각화 클래스"""

    @staticmethod
    def create_line_chart(data, title, x_field, y_field):
        """라인 차트 생성"""
        df = pd.DataFrame(data)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x_field],
            y=df[y_field],
            mode='lines+markers',
            name=y_field,
            line=dict(color='#4285f4', width=3),
            marker=dict(size=8)
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_field,
            yaxis_title=y_field,
            hovermode='x unified',
            template='plotly_white',
            height=400
        )

        return fig.to_json()

    @staticmethod
    def create_bar_chart(data, title, x_field, y_field, limit=10):
        """막대 차트 생성"""
        df = pd.DataFrame(data).head(limit)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df[x_field],
            y=df[y_field],
            marker_color='#34a853',
            text=df[y_field],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_field,
            yaxis_title=y_field,
            template='plotly_white',
            height=400,
            xaxis={'categoryorder': 'total descending'}
        )

        return fig.to_json()

    @staticmethod
    def create_pie_chart(data, title):
        """파이 차트 생성"""
        if isinstance(data, dict):
            labels = list(data.keys())
            values = list(data.values())
        else:
            df = pd.DataFrame(data)
            labels = df.iloc[:, 0].tolist()
            values = df.iloc[:, 1].tolist()

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3
        )])

        fig.update_layout(
            title=title,
            template='plotly_white',
            height=400
        )

        return fig.to_json()

    @staticmethod
    def create_monthly_sales_chart(monthly_data, product_code):
        """월별 판매 추이 차트"""
        df = pd.DataFrame(monthly_data)

        # 날짜 문자열 생성
        df['날짜'] = df['연도'].astype(str) + '-' + df['월'].astype(str).str.zfill(2)

        fig = go.Figure()

        # 수량 추이
        fig.add_trace(go.Scatter(
            x=df['날짜'],
            y=df['수량'],
            mode='lines+markers',
            name='판매 수량',
            line=dict(color='#4285f4', width=3),
            marker=dict(size=8),
            yaxis='y'
        ))

        # 매출 추이
        fig.add_trace(go.Scatter(
            x=df['날짜'],
            y=df['합계'],
            mode='lines+markers',
            name='판매 금액',
            line=dict(color='#34a853', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))

        fig.update_layout(
            title=f'제품 {product_code} 월별 판매 추이',
            xaxis=dict(title='월'),
            yaxis=dict(title='판매 수량', side='left'),
            yaxis2=dict(title='판매 금액 (원)', overlaying='y', side='right'),
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(x=0.01, y=0.99)
        )

        return fig.to_json()

    @staticmethod
    def create_customer_ranking_chart(customer_data, metric='총구매금액', limit=15):
        """고객 랭킹 차트"""
        df = pd.DataFrame(customer_data).head(limit)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df['거래처'],
            x=df[metric],
            orientation='h',
            marker=dict(
                color=df[metric],
                colorscale='Blues',
                showscale=True
            ),
            text=df[metric],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ))

        fig.update_layout(
            title=f'주요 고객 TOP {limit} ({metric})',
            xaxis_title=metric,
            yaxis_title='거래처',
            template='plotly_white',
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )

        return fig.to_json()

    @staticmethod
    def create_trend_comparison_chart(increasing, decreasing):
        """증가/감소 고객 비교 차트"""
        inc_df = pd.DataFrame(increasing).head(10)
        dec_df = pd.DataFrame(decreasing).head(10)

        fig = go.Figure()

        # 증가 고객
        fig.add_trace(go.Bar(
            name='구매량 증가',
            y=inc_df['거래처'],
            x=inc_df['증감율'],
            orientation='h',
            marker_color='#34a853'
        ))

        # 감소 고객
        fig.add_trace(go.Bar(
            name='구매량 감소',
            y=dec_df['거래처'],
            x=dec_df['증감율'],
            orientation='h',
            marker_color='#ea4335'
        ))

        fig.update_layout(
            title='고객 구매 트렌드 비교 (TOP 10)',
            xaxis_title='증감율 (%)',
            yaxis_title='거래처',
            template='plotly_white',
            height=600,
            barmode='group'
        )

        return fig.to_json()

    @staticmethod
    def create_industry_distribution_chart(industry_data):
        """업종 분포 차트"""
        labels = list(industry_data.keys())
        values = list(industry_data.values())

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(
                colors=px.colors.qualitative.Set3
            )
        )])

        fig.update_layout(
            title='고객 업종 분포',
            template='plotly_white',
            height=450
        )

        return fig.to_json()

    @staticmethod
    def create_growth_rate_distribution(customer_chars):
        """고객 성장률 분포"""
        if not customer_chars or 'details' not in customer_chars:
            return None

        df = pd.DataFrame(customer_chars['details'])

        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df['연평균성장률'] if '연평균성장률' in df.columns else [],
            nbinsx=20,
            marker_color='#4285f4'
        ))

        fig.update_layout(
            title='고객 연평균 성장률 분포',
            xaxis_title='연평균 성장률 (%)',
            yaxis_title='고객 수',
            template='plotly_white',
            height=400
        )

        return fig.to_json()

    @staticmethod
    def create_visualization_from_suggestion(suggestion, analysis_data):
        """제안된 시각화 생성"""
        viz_type = suggestion['type']
        data_key = suggestion.get('data_key')

        if not data_key or data_key not in analysis_data:
            return None

        data = analysis_data[data_key]

        if viz_type == 'line_chart':
            if 'monthly_sales' in data:
                return DataVisualizer.create_monthly_sales_chart(
                    data['monthly_sales'],
                    data.get('product_code', 'Unknown')
                )

        elif viz_type == 'bar_chart':
            if data_key == 'increasing_customers':
                df = pd.DataFrame(data).head(10)
                return DataVisualizer.create_bar_chart(
                    df.to_dict('records'),
                    suggestion['title'],
                    '거래처',
                    '증감율'
                )
            elif data_key == 'decreasing_customers':
                df = pd.DataFrame(data).head(10)
                return DataVisualizer.create_bar_chart(
                    df.to_dict('records'),
                    suggestion['title'],
                    '거래처',
                    '증감율'
                )
            elif 'customers' in data:
                return DataVisualizer.create_customer_ranking_chart(
                    data['customers'],
                    '총구매금액',
                    15  # TOP 15로 증가
                )

        elif viz_type == 'pie_chart':
            field = suggestion.get('field')
            if field and field in data:
                return DataVisualizer.create_pie_chart(
                    data[field],
                    suggestion['title']
                )

        return None
