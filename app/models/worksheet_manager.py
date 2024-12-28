# File: app/models/worksheet_manager.py
from typing import List, Dict
from .content_section import ContentSection
from .content_generator import ContentGenerator

class WorksheetManager:
    def __init__(self):
        self.levels = ['A1', 'A2', 'B1', 'B2']
        self.generator = ContentGenerator()
        self.sections = {level: ContentSection(level=level) for level in self.levels}

    def generate_worksheet(self, content_type: str, topic: str, selected_levels: List[str],
                         exercise_types: List[str]) -> Dict:
        """
        Generate a complete worksheet including content and exercises for selected levels.
        """
        if not selected_levels:
            raise ValueError("No levels selected")
        
        if not exercise_types:
            raise ValueError("No exercise types selected")
        
        if content_type not in self.generator.base_prompts:
            raise ValueError(f"Invalid content type: {content_type}")
        
        worksheet = {}
        
        for level in selected_levels:
            if level not in self.levels:
                raise ValueError(f"Invalid level: {level}")
            
            # Generate main content
            content = self.generator.generate_content(content_type, topic, level)
            
            # Generate exercises based on the content
            exercises = self.generator.generate_exercises(content, level, exercise_types)
            
            # Update section data
            self.sections[level].content = content
            self.sections[level].exercises = exercises
            
            # Add to worksheet
            worksheet[level] = {
                'content': content,
                'exercises': exercises
            }
        
        return worksheet