# File: app/routes.py
from flask import Blueprint, render_template, request, jsonify
from app.models.worksheet_manager import WorksheetManager

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if not data or not all(k in data for k in ['content_type', 'topic', 'levels', 'exercise_types']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        worksheet_manager = WorksheetManager()
        result = worksheet_manager.generate_worksheet(
            content_type=data['content_type'],
            topic=data['topic'],
            selected_levels=data['levels'],
            exercise_types=data['exercise_types']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500