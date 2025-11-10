import pandas as pd
import json

class DataVisualizer:
    """데이터 시각화 클래스 - 클라이언트 사이드 렌더링용 데이터 반환"""

    @staticmethod
    def create_line_chart(data, title, x_field, y_field):
        """라인 차트 데이터 생성"""
        df = pd.DataFrame(data)

        chart_data = {
            "type": "line",
            "title": title,
            "data": {
                "x": df[x_field].tolist(),
                "y": df[y_field].tolist(),
                "x_label": x_field,
                "y_label": y_field
            }
        }

        return json.dumps(chart_data)

    @staticmethod
    def create_bar_chart(data, title, x_field, y_field, limit=10):
        """막대 차트 데이터 생성"""
        df = pd.DataFrame(data).head(limit)

        chart_data = {
            "type": "bar",
            "title": title,
            "data": {
                "x": df[x_field].tolist(),
                "y": df[y_field].tolist(),
                "x_label": x_field,
                "y_label": y_field
            }
        }

        return json.dumps(chart_data)

    @staticmethod
    def create_table(data, title, columns=None):
        """테이블 데이터 생성"""
        df = pd.DataFrame(data)

        if columns:
            df = df[columns]

        table_data = {
            "type": "table",
            "title": title,
            "data": {
                "columns": df.columns.tolist(),
                "rows": df.values.tolist()
            }
        }

        return json.dumps(table_data)

    @staticmethod
    def create_monthly_sales_chart(monthly_data, product_code):
        """월별 판매 추이 차트"""
        return DataVisualizer.create_line_chart(
            monthly_data,
            f'{product_code} 월별 판매 추이',
            '판매월',
            '판매금액'
        )

    @staticmethod
    def create_customer_ranking_chart(customer_data, value_field, limit=15):
        """고객 순위 차트"""
        return DataVisualizer.create_bar_chart(
            customer_data,
            f'TOP {limit} 고객',
            '고객명',
            value_field,
            limit
        )

    @staticmethod
    def create_trend_comparison_chart(increasing_data, decreasing_data):
        """트렌드 비교 차트"""
        df_inc = pd.DataFrame(increasing_data).head(10)
        df_dec = pd.DataFrame(decreasing_data).head(10)

        chart_data = {
            "type": "comparison",
            "title": "구매 트렌드 비교",
            "data": {
                "increasing": {
                    "labels": df_inc['고객명'].tolist(),
                    "values": df_inc['증감률'].tolist()
                },
                "decreasing": {
                    "labels": df_dec['고객명'].tolist(),
                    "values": df_dec['증감률'].tolist()
                }
            }
        }

        return json.dumps(chart_data)

    @staticmethod
    def create_visualization_from_suggestion(suggestion, analysis_data):
        """AI 제안에서 시각화 생성"""
        viz_type = suggestion.get('type', 'table')

        if viz_type == 'line':
            return DataVisualizer.create_line_chart(
                analysis_data,
                suggestion['title'],
                suggestion.get('x_field', 'x'),
                suggestion.get('y_field', 'y')
            )
        elif viz_type == 'bar':
            return DataVisualizer.create_bar_chart(
                analysis_data,
                suggestion['title'],
                suggestion.get('x_field', 'x'),
                suggestion.get('y_field', 'y'),
                suggestion.get('limit', 10)
            )
        elif viz_type == 'table':
            return DataVisualizer.create_table(
                analysis_data,
                suggestion['title'],
                suggestion.get('columns')
            )
        else:
            return DataVisualizer.create_table(
                analysis_data,
                suggestion['title']
            )
