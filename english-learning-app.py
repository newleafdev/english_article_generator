from flask import Flask, render_template, request, jsonify
from dataclasses import dataclass
from typing import List, Dict
import json

app = Flask(__name__)

@dataclass
class ContentSection:
    level: str
    content: str = ""
    exercises: List[Dict] = None

    def __post_init__(self):
        if self.exercises is None:
            self.exercises = []

class ContentGenerator:
    def __init__(self):
        self.base_prompts = {
            'article': "Write an article about {topic} suitable for {level} English learners.",
            'story': "Write a story about {topic} suitable for {level} English learners.",
            'news': "Write a news report about {topic} suitable for {level} English learners."
        }
        
        self.exercise_prompts = {
            'vocabulary': "Generate vocabulary exercises for {level} level based on this text: {content}",
            'grammar': "Generate grammar exercises for {level} level based on this text: {content}",
            'comprehension': "Generate comprehension questions for {level} level based on this text: {content}",
            'writing': "Generate writing exercises for {level} level based on this text: {content}"
        }

    def generate_content(self, content_type: str, topic: str, level: str) -> str:
        # This is where you'd integrate your local LLM
        # For now, returning placeholder text
        prompt = self.base_prompts[content_type].format(topic=topic, level=level)
        return f"Generated {content_type} for {level} about {topic}"

    def generate_exercises(self, content: str, level: str, exercise_types: List[str]) -> List[Dict]:
        exercises = []
        for ex_type in exercise_types:
            prompt = self.exercise_prompts[ex_type].format(level=level, content=content)
            # Here you'd use your local LLM to generate exercises
            exercises.append({
                'type': ex_type,
                'content': f"Generated {ex_type} exercise for {level}"
            })
        return exercises

class WorksheetManager:
    def __init__(self):
        self.levels = ['A1', 'A2', 'B1', 'B2']
        self.generator = ContentGenerator()
        self.sections = {level: ContentSection(level=level) for level in self.levels}

    def generate_worksheet(self, content_type: str, topic: str, selected_levels: List[str],
                         exercise_types: List[str]) -> Dict:
        worksheet = {}
        
        # Generate content for each selected level
        for level in selected_levels:
            content = self.generator.generate_content(content_type, topic, level)
            exercises = self.generator.generate_exercises(content, level, exercise_types)
            
            self.sections[level].content = content
            self.sections[level].exercises = exercises
            
            worksheet[level] = {
                'content': content,
                'exercises': exercises
            }
        
        return worksheet

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    worksheet_manager = WorksheetManager()
    
    result = worksheet_manager.generate_worksheet(
        content_type=data['content_type'],
        topic=data['topic'],
        selected_levels=data['levels'],
        exercise_types=data['exercise_types']
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
