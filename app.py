from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ai_agent import B2BAnalystAgent
from visualizer import DataVisualizer
import os
import json

app = Flask(__name__, static_folder='public')
CORS(app)

# Vercel용 정적 파일 경로 설정
if os.path.exists('static'):
    app.static_folder = 'static'
elif os.path.exists('public'):
    app.static_folder = 'public'

# Gemini API Key - 환경 변수에서 가져오기 (Vercel 배포용)
API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyA9_-Nn8LFkh4PJXvwSpy1xrEuVOG8zrUU')

# AI Agent 초기화 (lazy loading)
agent = None

def get_agent():
    """Agent 싱글톤 패턴"""
    global agent
    if agent is None:
        agent = B2BAnalystAgent(API_KEY)
    return agent

@app.route('/')
def index():
    """메인 페이지"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """채팅 API"""
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': '메시지가 필요합니다.'}), 400

        # AI Agent 응답 생성
        result = get_agent().chat(user_message)

        # 시각화 생성
        visualizations = []
        for viz_suggestion in result.get('visualizations', []):
            viz_json = DataVisualizer.create_visualization_from_suggestion(
                viz_suggestion,
                result['analysis_data']
            )
            if viz_json:
                visualizations.append({
                    'title': viz_suggestion['title'],
                    'chart': json.loads(viz_json)
                })

        return jsonify({
            'response': result['response'],
            'visualizations': visualizations,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """대화 히스토리 초기화"""
    try:
        get_agent().reset_conversation()
        return jsonify({
            'message': '대화가 초기화되었습니다.',
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/search/products', methods=['GET'])
def search_products():
    """제품 검색"""
    try:
        keyword = request.args.get('keyword', '')
        products = get_agent().data_processor.search_products(keyword)
        return jsonify({
            'products': products,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/search/customers', methods=['GET'])
def search_customers():
    """고객 검색"""
    try:
        keyword = request.args.get('keyword', '')
        customers = get_agent().data_processor.search_customers(keyword)
        return jsonify({
            'customers': customers,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/analytics/product/<product_code>', methods=['GET'])
def get_product_analytics(product_code):
    """제품 분석 API"""
    try:
        analysis = get_agent().data_processor.get_product_sales_analysis(product_code)

        if not analysis:
            return jsonify({
                'error': '제품을 찾을 수 없습니다.',
                'success': False
            }), 404

        # 시각화 생성
        visualizations = []

        # 월별 판매 추이
        if analysis.get('monthly_sales'):
            monthly_chart = DataVisualizer.create_monthly_sales_chart(
                analysis['monthly_sales'],
                product_code
            )
            visualizations.append({
                'title': '월별 판매 추이',
                'chart': json.loads(monthly_chart)
            })

        # 주요 고객
        if analysis.get('customers'):
            customer_chart = DataVisualizer.create_customer_ranking_chart(
                analysis['customers'],
                '총구매금액',
                15
            )
            visualizations.append({
                'title': '주요 구매 고객',
                'chart': json.loads(customer_chart)
            })

        return jsonify({
            'analysis': analysis,
            'visualizations': visualizations,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/analytics/trends', methods=['GET'])
def get_trends():
    """트렌드 분석 API"""
    try:
        months = request.args.get('months', 6, type=int)
        trends = get_agent().data_processor.get_customer_trend_analysis(months)

        # 시각화 생성
        visualizations = []

        # 트렌드 비교 차트
        if trends.get('increasing_customers') and trends.get('decreasing_customers'):
            trend_chart = DataVisualizer.create_trend_comparison_chart(
                trends['increasing_customers'],
                trends['decreasing_customers']
            )
            visualizations.append({
                'title': '고객 구매 트렌드',
                'chart': json.loads(trend_chart)
            })

        return jsonify({
            'trends': trends,
            'visualizations': visualizations,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/analytics/marketing', methods=['GET'])
def get_marketing_recommendations():
    """마케팅 추천 API"""
    try:
        recommendations = get_agent().data_processor.get_marketing_recommendations()

        return jsonify({
            'recommendations': recommendations,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """전체 요약 정보"""
    try:
        summary = get_agent().data_processor.get_sales_summary()
        return jsonify({
            'summary': summary,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

if __name__ == '__main__':
    # static 폴더 생성
    if not os.path.exists('static'):
        os.makedirs('static')

    print("=" * 50)
    print("B2B AI Agent 서버 시작")
    print("=" * 50)
    print("웹 인터페이스: http://localhost:5000")
    print("API 엔드포인트:")
    print("  - POST /api/chat - AI와 대화")
    print("  - POST /api/reset - 대화 초기화")
    print("  - GET /api/search/products?keyword=xxx - 제품 검색")
    print("  - GET /api/search/customers?keyword=xxx - 고객 검색")
    print("  - GET /api/analytics/product/<code> - 제품 분석")
    print("  - GET /api/analytics/trends?months=6 - 트렌드 분석")
    print("  - GET /api/analytics/marketing - 마케팅 추천")
    print("  - GET /api/summary - 전체 요약")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
