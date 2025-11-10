from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
from io import BytesIO

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent import B2BAnalystAgent
from visualizer import DataVisualizer
import json

app = Flask(__name__)
CORS(app)

# Gemini API Key
API_KEY = os.environ.get('GEMINI_API_KEY', 'AQ.Ab8RN6JV3nQZw9pBE9fhmkGDLAl2ncDhvVvGakCaBj06vuUefA')

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
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

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

# Vercel용 핸들러
handler = app
